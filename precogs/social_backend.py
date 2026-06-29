#!/usr/bin/env python3
"""
Social Backend - Mastodon Federation Integration
A\\ 1272 Hz

Connects the DIP feed to Mastodon for:
- User authentication (sign in via Mastodon)
- Post federation (share to Mastodon)
- Social interactions (like, boost, reply)
- Profile sync
"""

import json
import os
import time
import hashlib
import secrets
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import urllib.request
import urllib.error
import urllib.parse
import ssl

# Mastodon instances for federation
MASTODON_INSTANCES = {
    'primary': 'https://mastodon.social',
    'tech': 'https://fosstodon.org',
    'backup': 'https://mastodon.online'
}

# Oroboros account on Mastodon
OROBOROS_ACCOUNT = '@oroboroslabs_ai'

@dataclass
class MastodonAccount:
    """Mastodon account data"""
    username: str
    instance: str
    display_name: str
    avatar_url: str
    followers_count: int
    following_count: int
    statuses_count: int
    bio: str
    verified: bool

@dataclass
class MastodonStatus:
    """Mastodon status/toot data"""
    id: str
    content: str
    created_at: str
    account: Dict
    media_attachments: List[Dict]
    replies_count: int
    reblogs_count: int
    favourites_count: int
    url: str
    visibility: str

class MastodonClient:
    """
    Mastodon API Client
    Handles authentication, posting, and federation
    """
    
    def __init__(self, instance: str = None):
        self.instance = instance or MASTODON_INSTANCES['primary']
        self.client_id = None
        self.client_secret = None
        self.access_token = None
        self.user_account = None
        
        # SSL context for requests
        self.ssl_context = ssl.create_default_context()
        self.ssl_context.check_hostname = True
        self.ssl_context.verify_mode = ssl.CERT_REQUIRED
        
        # Cache
        self._cache = {}
        self._cache_timeout = 300  # 5 minutes
    
    def get_oauth_url(self, redirect_uri: str = 'urn:ietf:wg:oauth:2.0:oob') -> str:
        """
        Get OAuth authorization URL for Mastodon sign in
        Returns URL to redirect user to for authentication
        """
        # Create OAuth app
        app_data = self._create_app(redirect_uri)
        
        if app_data:
            self.client_id = app_data.get('client_id')
            self.client_secret = app_data.get('client_secret')
            
            # Build OAuth URL
            params = {
                'client_id': self.client_id,
                'redirect_uri': redirect_uri,
                'response_type': 'code',
                'scope': 'read write follow push'
            }
            
            oauth_url = f"{self.instance}/oauth/authorize?{urllib.parse.urlencode(params)}"
            return oauth_url
        
        return None
    
    def _create_app(self, redirect_uri: str) -> Optional[Dict]:
        """Create Mastodon OAuth app"""
        url = f"{self.instance}/api/v1/apps"
        
        data = {
            'client_name': 'Oroboros WorldFeed',
            'redirect_uris': redirect_uri,
            'scopes': 'read write follow push',
            'website': 'https://oroboroslabs-ai.github.io/world-feed/'
        }
        
        try:
            req = urllib.request.Request(url, data=urllib.parse.urlencode(data).encode())
            req.add_header('Content-Type', 'application/x-www-form-urlencoded')
            
            with urllib.request.urlopen(req, context=self.ssl_context, timeout=10) as response:
                return json.loads(response.read().decode())
        except Exception as e:
            print(f"[MastodonClient] Error creating app: {e}")
            return None
    
    def get_access_token(self, auth_code: str, redirect_uri: str) -> Optional[str]:
        """
        Exchange authorization code for access token
        """
        url = f"{self.instance}/oauth/token"
        
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'redirect_uri': redirect_uri,
            'grant_type': 'authorization_code',
            'code': auth_code,
            'scope': 'read write follow push'
        }
        
        try:
            req = urllib.request.Request(url, data=urllib.parse.urlencode(data).encode())
            req.add_header('Content-Type', 'application/x-www-form-urlencoded')
            
            with urllib.request.urlopen(req, context=self.ssl_context, timeout=10) as response:
                result = json.loads(response.read().decode())
                self.access_token = result.get('access_token')
                return self.access_token
        except Exception as e:
            print(f"[MastodonClient] Error getting access token: {e}")
            return None
    
    def verify_credentials(self) -> Optional[MastodonAccount]:
        """Verify user credentials and get account info"""
        if not self.access_token:
            return None
        
        url = f"{self.instance}/api/v1/accounts/verify_credentials"
        
        try:
            req = urllib.request.Request(url)
            req.add_header('Authorization', f'Bearer {self.access_token}')
            
            with urllib.request.urlopen(req, context=self.ssl_context, timeout=10) as response:
                data = json.loads(response.read().decode())
                
                self.user_account = MastodonAccount(
                    username=data.get('username', ''),
                    instance=self.instance,
                    display_name=data.get('display_name', ''),
                    avatar_url=data.get('avatar', ''),
                    followers_count=data.get('followers_count', 0),
                    following_count=data.get('following_count', 0),
                    statuses_count=data.get('statuses_count', 0),
                    bio=data.get('note', ''),
                    verified=data.get('verified', False)
                )
                
                return self.user_account
        except Exception as e:
            print(f"[MastodonClient] Error verifying credentials: {e}")
            return None
    
    def post_status(self, 
                     content: str, 
                     visibility: str = 'public',
                     in_reply_to: str = None,
                     media_ids: List[str] = None,
                     sensitive: bool = False,
                     spoiler_text: str = None) -> Optional[MastodonStatus]:
        """
        Post a status (toot) to Mastodon
        """
        if not self.access_token:
            print("[MastodonClient] No access token - cannot post")
            return None
        
        url = f"{self.instance}/api/v1/statuses"
        
        data = {
            'status': content,
            'visibility': visibility
        }
        
        if in_reply_to:
            data['in_reply_to_id'] = in_reply_to
        
        if media_ids:
            data['media_ids'] = media_ids
        
        if sensitive:
            data['sensitive'] = True
        
        if spoiler_text:
            data['spoiler_text'] = spoiler_text
        
        try:
            req = urllib.request.Request(url, data=json.dumps(data).encode())
            req.add_header('Authorization', f'Bearer {self.access_token}')
            req.add_header('Content-Type', 'application/json')
            
            with urllib.request.urlopen(req, context=self.ssl_context, timeout=30) as response:
                result = json.loads(response.read().decode())
                
                return MastodonStatus(
                    id=result.get('id', ''),
                    content=result.get('content', ''),
                    created_at=result.get('created_at', ''),
                    account=result.get('account', {}),
                    media_attachments=result.get('media_attachments', []),
                    replies_count=result.get('replies_count', 0),
                    reblogs_count=result.get('reblogs_count', 0),
                    favourites_count=result.get('favourites_count', 0),
                    url=result.get('url', ''),
                    visibility=result.get('visibility', 'public')
                )
        except Exception as e:
            print(f"[MastodonClient] Error posting status: {e}")
            return None
    
    def get_account_statuses(self, account_id: str = None, limit: int = 20) -> List[MastodonStatus]:
        """
        Get statuses from an account (default: Oroboros account)
        """
        if not account_id:
            # Get Oroboros account ID
            account_id = self._get_oroboros_account_id()
        
        if not account_id:
            return []
        
        cache_key = f"statuses_{account_id}_{limit}"
        if cache_key in self._cache:
            cached = self._cache[cache_key]
            if time.time() - cached['timestamp'] < self._cache_timeout:
                return cached['data']
        
        url = f"{self.instance}/api/v1/accounts/{account_id}/statuses?limit={limit}"
        
        try:
            req = urllib.request.Request(url)
            req.add_header('Content-Type', 'application/json')
            
            with urllib.request.urlopen(req, context=self.ssl_context, timeout=10) as response:
                data = json.loads(response.read().decode())
                
                statuses = []
                for item in data:
                    statuses.append(MastodonStatus(
                        id=item.get('id', ''),
                        content=item.get('content', ''),
                        created_at=item.get('created_at', ''),
                        account=item.get('account', {}),
                        media_attachments=item.get('media_attachments', []),
                        replies_count=item.get('replies_count', 0),
                        reblogs_count=item.get('reblogs_count', 0),
                        favourites_count=item.get('favourites_count', 0),
                        url=item.get('url', ''),
                        visibility=item.get('visibility', 'public')
                    ))
                
                # Cache results
                self._cache[cache_key] = {
                    'timestamp': time.time(),
                    'data': statuses
                }
                
                return statuses
        except Exception as e:
            print(f"[MastodonClient] Error getting statuses: {e}")
            return []
    
    def _get_oroboros_account_id(self) -> Optional[str]:
        """Get Oroboros account ID from Mastodon"""
        url = f"{self.instance}/api/v1/accounts/lookup?acct=oroboroslabs"
        
        try:
            req = urllib.request.Request(url)
            req.add_header('Content-Type', 'application/json')
            
            with urllib.request.urlopen(req, context=self.ssl_context, timeout=10) as response:
                data = json.loads(response.read().decode())
                return data.get('id')
        except Exception as e:
            print(f"[MastodonClient] Error getting account ID: {e}")
            return None
    
    def favourite_status(self, status_id: str) -> bool:
        """Favourite (like) a status"""
        if not self.access_token:
            return False
        
        url = f"{self.instance}/api/v1/statuses/{status_id}/favourite"
        
        try:
            req = urllib.request.Request(url, data=b'', method='POST')
            req.add_header('Authorization', f'Bearer {self.access_token}')
            
            with urllib.request.urlopen(req, context=self.ssl_context, timeout=10) as response:
                return response.status == 200
        except Exception as e:
            print(f"[MastodonClient] Error favouriting: {e}")
            return False
    
    def reblog_status(self, status_id: str) -> bool:
        """Reblog (boost) a status"""
        if not self.access_token:
            return False
        
        url = f"{self.instance}/api/v1/statuses/{status_id}/reblog"
        
        try:
            req = urllib.request.Request(url, data=b'', method='POST')
            req.add_header('Authorization', f'Bearer {self.access_token}')
            
            with urllib.request.urlopen(req, context=self.ssl_context, timeout=10) as response:
                return response.status == 200
        except Exception as e:
            print(f"[MastodonClient] Error reblogging: {e}")
            return False
    
    def get_public_timeline(self, limit: int = 20) -> List[MastodonStatus]:
        """Get public timeline"""
        url = f"{self.instance}/api/v1/timelines/public?limit={limit}"
        
        try:
            req = urllib.request.Request(url)
            req.add_header('Content-Type', 'application/json')
            
            with urllib.request.urlopen(req, context=self.ssl_context, timeout=10) as response:
                data = json.loads(response.read().decode())
                
                statuses = []
                for item in data:
                    statuses.append(MastodonStatus(
                        id=item.get('id', ''),
                        content=item.get('content', ''),
                        created_at=item.get('created_at', ''),
                        account=item.get('account', {}),
                        media_attachments=item.get('media_attachments', []),
                        replies_count=item.get('replies_count', 0),
                        reblogs_count=item.get('reblogs_count', 0),
                        favourites_count=item.get('favourites_count', 0),
                        url=item.get('url', ''),
                        visibility=item.get('visibility', 'public')
                    ))
                
                return statuses
        except Exception as e:
            print(f"[MastodonClient] Error getting public timeline: {e}")
            return []


class SocialBackend:
    """
    Main Social Backend Service
    Integrates Mastodon with the DIP feed
    """
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.mastodon = MastodonClient()
        self.sessions = {}  # Store user sessions
        self.resonance = 1272.0
    
    def get_signin_url(self, instance: str = None) -> Dict[str, str]:
        """
        Get sign in URL for Mastodon
        Returns OAuth URL for user authentication
        """
        if instance:
            self.mastodon = MastodonClient(instance)
        
        oauth_url = self.mastodon.get_oauth_url()
        
        if oauth_url:
            return {
                'status': 'success',
                'oauth_url': oauth_url,
                'instance': self.mastodon.instance,
                'message': 'Redirect user to oauth_url for authentication'
            }
        
        return {
            'status': 'error',
            'message': 'Failed to create OAuth URL'
        }
    
    def complete_signin(self, auth_code: str, redirect_uri: str) -> Dict[str, Any]:
        """
        Complete sign in after user authorizes
        Returns user account info
        """
        access_token = self.mastodon.get_access_token(auth_code, redirect_uri)
        
        if access_token:
            account = self.mastodon.verify_credentials()
            
            if account:
                # Create session
                session_id = secrets.token_hex(32)
                self.sessions[session_id] = {
                    'account': asdict(account),
                    'access_token': access_token,
                    'instance': self.mastodon.instance,
                    'created_at': datetime.now(timezone.utc).isoformat()
                }
                
                return {
                    'status': 'success',
                    'session_id': session_id,
                    'account': asdict(account),
                    'message': f'Welcome, {account.display_name or account.username}!'
                }
        
        return {
            'status': 'error',
            'message': 'Authentication failed'
        }
    
    def signout(self, session_id: str) -> Dict[str, str]:
        """Sign out and invalidate session"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            return {'status': 'success', 'message': 'Signed out successfully'}
        
        return {'status': 'error', 'message': 'Session not found'}
    
    def get_session(self, session_id: str) -> Optional[Dict]:
        """Get session data"""
        return self.sessions.get(session_id)
    
    def post_to_mastodon(self, 
                          session_id: str,
                          content: str,
                          visibility: str = 'public',
                          media_urls: List[str] = None) -> Dict[str, Any]:
        """
        Post content to Mastodon
        """
        session = self.get_session(session_id)
        
        if not session:
            return {'status': 'error', 'message': 'Not authenticated'}
        
        # Set access token
        self.mastodon.access_token = session['access_token']
        
        # Post status
        status = self.mastodon.post_status(
            content=content,
            visibility=visibility
        )
        
        if status:
            return {
                'status': 'success',
                'status_id': status.id,
                'url': status.url,
                'message': 'Posted to Mastodon successfully'
            }
        
        return {'status': 'error', 'message': 'Failed to post to Mastodon'}
    
    def get_oroboros_feed(self, limit: int = 20) -> List[Dict]:
        """
        Get Oroboros account feed from Mastodon
        This is the public feed that appears in DIP
        """
        statuses = self.mastodon.get_account_statuses(limit=limit)
        
        feed = []
        for status in statuses:
            feed.append({
                'id': status.id,
                'type': 'mastodon',
                'content': status.content,
                'created_at': status.created_at,
                'account': status.account,
                'media': status.media_attachments,
                'replies': status.replies_count,
                'reblogs': status.reblogs_count,
                'favourites': status.favourites_count,
                'url': status.url,
                'visibility': status.visibility,
                'source': 'mastodon_federation'
            })
        
        return feed
    
    def get_federated_feed(self, limit: int = 20) -> List[Dict]:
        """Get federated public timeline"""
        statuses = self.mastodon.get_public_timeline(limit=limit)
        
        feed = []
        for status in statuses:
            feed.append({
                'id': status.id,
                'type': 'mastodon',
                'content': status.content,
                'created_at': status.created_at,
                'account': status.account,
                'media': status.media_attachments,
                'replies': status.replies_count,
                'reblogs': status.reblogs_count,
                'favourites': status.favourites_count,
                'url': status.url,
                'visibility': status.visibility,
                'source': 'mastodon_federation'
            })
        
        return feed
    
    def interact(self, 
                  session_id: str,
                  status_id: str,
                  action: str) -> Dict[str, Any]:
        """
        Interact with a status (favourite, reblog)
        """
        session = self.get_session(session_id)
        
        if not session:
            return {'status': 'error', 'message': 'Not authenticated'}
        
        self.mastodon.access_token = session['access_token']
        
        if action == 'favourite':
            success = self.mastodon.favourite_status(status_id)
            return {
                'status': 'success' if success else 'error',
                'message': 'Favourited' if success else 'Failed to favourite'
            }
        
        elif action == 'reblog':
            success = self.mastodon.reblog_status(status_id)
            return {
                'status': 'success' if success else 'error',
                'message': 'Reblogged' if success else 'Failed to reblog'
            }
        
        return {'status': 'error', 'message': 'Unknown action'}


# API endpoints for Flask server
def create_social_endpoints(app, social_backend: SocialBackend):
    """Create Flask API endpoints for social features"""
    from flask import request, jsonify, redirect
    
    @app.route('/api/social/signin', methods=['GET'])
    def social_signin():
        """Get Mastodon sign in URL"""
        instance = request.args.get('instance', MASTODON_INSTANCES['primary'])
        result = social_backend.get_signin_url(instance)
        return jsonify(result)
    
    @app.route('/api/social/callback', methods=['GET'])
    def social_callback():
        """OAuth callback from Mastodon"""
        code = request.args.get('code')
        result = social_backend.complete_signin(code, 'urn:ietf:wg:oauth:2.0:oob')
        return jsonify(result)
    
    @app.route('/api/social/signout', methods=['POST'])
    def social_signout():
        """Sign out"""
        session_id = request.json.get('session_id')
        result = social_backend.signout(session_id)
        return jsonify(result)
    
    @app.route('/api/social/post', methods=['POST'])
    def social_post():
        """Post to Mastodon"""
        data = request.json
        result = social_backend.post_to_mastodon(
            session_id=data.get('session_id'),
            content=data.get('content'),
            visibility=data.get('visibility', 'public'),
            media_urls=data.get('media_urls')
        )
        return jsonify(result)
    
    @app.route('/api/social/feed/oroboros', methods=['GET'])
    def social_feed_oroboros():
        """Get Oroboros Mastodon feed"""
        limit = request.args.get('limit', 20, type=int)
        feed = social_backend.get_oroboros_feed(limit=limit)
        return jsonify(feed)
    
    @app.route('/api/social/feed/federated', methods=['GET'])
    def social_feed_federated():
        """Get federated public timeline"""
        limit = request.args.get('limit', 20, type=int)
        feed = social_backend.get_federated_feed(limit=limit)
        return jsonify(feed)
    
    @app.route('/api/social/interact', methods=['POST'])
    def social_interact():
        """Interact with a status"""
        data = request.json
        result = social_backend.interact(
            session_id=data.get('session_id'),
            status_id=data.get('status_id'),
            action=data.get('action')
        )
        return jsonify(result)


if __name__ == "__main__":
    # Test the social backend
    backend = SocialBackend()
    
    print("[SocialBackend] Testing Mastodon integration...")
    print(f"[SocialBackend] Primary instance: {MASTODON_INSTANCES['primary']}")
    print(f"[SocialBackend] Oroboros account: {OROBOROS_ACCOUNT}")
    
    # Get Oroboros feed
    feed = backend.get_oroboros_feed(limit=5)
    print(f"[SocialBackend] Retrieved {len(feed)} statuses from Oroboros account")
    
    for status in feed:
        print(f"  - {status['id']}: {status['content'][:50]}...")