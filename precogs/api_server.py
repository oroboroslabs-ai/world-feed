#!/usr/bin/env python3
"""
Precog API Server - Backend for DIP System
A\\ 1272 Hz
Serves precog-generated content to the frontend
"""

import json
import time
import os
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
from typing import Dict, List, Optional

# Import precog pipeline
try:
    from pipeline import PrecogPipeline
except ImportError:
    from .pipeline import PrecogPipeline

# Get the parent directory for static files
# Use absolute path to work from any directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(SCRIPT_DIR)

# Create Flask app with static folder pointing to parent directory
app = Flask(__name__, static_folder=PARENT_DIR, static_url_path='')
CORS(app)

# Constants
RESONANCE_HZ = 1272.0
UEE_STANDARD = "UEE-2024"

# Initialize pipeline
pipeline = PrecogPipeline()

# Cache for generated content
content_cache = {
    'feed': None,
    'timestamp': None,
    'ttl': 30  # seconds
}

# Note: Static files are served automatically by Flask's static_folder
# The following routes are for explicit file serving if needed

@app.route('/')
def serve_index():
    """Serve the main DIP page"""
    try:
        return send_file(os.path.join(PARENT_DIR, 'dip.html'))
    except Exception as e:
        print(f"[ERROR] Failed to serve dip.html: {e}")
        return f"Error: {e}", 404

@app.route('/admin.html')
def serve_admin():
    """Serve the admin page"""
    try:
        return send_file(os.path.join(PARENT_DIR, 'admin.html'))
    except Exception as e:
        print(f"[ERROR] Failed to serve admin.html: {e}")
        return f"Error: {e}", 404

@app.route('/index.html')
def serve_public():
    """Serve the public page"""
    return send_from_directory(PARENT_DIR, 'index.html')

@app.route('/kaiju.html')
def serve_kaiju():
    """Serve the kaiju page"""
    return send_from_directory(PARENT_DIR, 'kaiju.html')

@app.route('/assets/<path:filename>')
def serve_assets(filename):
    """Serve assets"""
    return send_from_directory(os.path.join(PARENT_DIR, 'assets'), filename)

@app.route('/api/precog/feed', methods=['GET'])
def get_feed():
    """Get unified feed from all precogs"""
    try:
        # Check cache
        if content_cache['feed'] and content_cache['timestamp']:
            elapsed = (datetime.utcnow() - content_cache['timestamp']).total_seconds()
            if elapsed < content_cache['ttl']:
                return jsonify({
                    'status': 'success',
                    'cached': True,
                    'data': content_cache['feed']
                })
        
        # Generate new content
        writing_count = request.args.get('writing', 10, type=int)
        video_count = request.args.get('video', 5, type=int)
        image_count = request.args.get('image', 5, type=int)
        
        feed_items = pipeline.generate_feed(
            writing_count=writing_count,
            video_count=video_count,
            image_count=image_count
        )
        
        result = pipeline.to_json(feed_items)
        
        # Update cache
        content_cache['feed'] = result
        content_cache['timestamp'] = datetime.utcnow()
        
        return jsonify({
            'status': 'success',
            'cached': False,
            'data': result
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e),
            'data': None
        }), 500

@app.route('/api/precog/writing', methods=['GET'])
def get_writing():
    """Get written content from writing precog"""
    try:
        count = request.args.get('count', 10, type=int)
        category = request.args.get('category', None, type=str)
        
        # Generate content with category filter
        items = pipeline.writing_precog.generate_content(count, category)
        result = pipeline.to_json([
            UnifiedFeedItem(
                id=item.id,
                type='written',
                content=pipeline.writing_precog.to_json(item),
                confidence=item.confidence,
                resonance=item.resonance,
                strata=item.strata,
                timestamp=item.timestamp,
                source='writing_precog'
            ) for item in items
        ])
        
        return jsonify({
            'status': 'success',
            'type': 'written',
            'count': len(items),
            'category': category,
            'data': result
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

@app.route('/api/precog/video', methods=['GET'])
def get_video():
    """Get video content from video precog"""
    try:
        count = request.args.get('count', 5, type=int)
        category = request.args.get('category', None, type=str)
        
        items = pipeline.generate_by_type('video', count)
        result = pipeline.to_json(items)
        
        return jsonify({
            'status': 'success',
            'type': 'video',
            'count': len(items),
            'data': result
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

@app.route('/api/precog/image', methods=['GET'])
def get_image():
    """Get image content from image precog"""
    try:
        count = request.args.get('count', 5, type=int)
        category = request.args.get('category', None, type=str)
        
        items = pipeline.generate_by_type('image', count)
        result = pipeline.to_json(items)
        
        return jsonify({
            'status': 'success',
            'type': 'image',
            'count': len(items),
            'data': result
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

@app.route('/api/precog/status', methods=['GET'])
def get_status():
    """Get pipeline status"""
    return jsonify({
        'status': 'operational',
        'resonance': RESONANCE_HZ,
        'uee_standard': UEE_STANDARD,
        'timestamp': datetime.utcnow().isoformat(),
        'pipeline': pipeline.get_status()
    })

@app.route('/api/precog/strata', methods=['GET'])
def get_strata():
    """Get strata information"""
    return jsonify({
        'S1': 'Physical Layer — Raw data interception',
        'S2': 'Data Layer — Parsing and validation',
        'S3': 'Network Layer — Traffic routing',
        'S4': 'Transport Layer — Connection management',
        'S5': 'Session Layer — State management',
        'S6': 'Presentation Layer — Data transformation',
        'S7': 'Application Layer — Business logic',
        'S8': 'Cognitive Layer — SAM filtering',
        'S9': 'Resonance Layer — 1272 Hz lock',
        'S10': 'Sovereignty Layer — UEE Standard',
        'S11': 'Infection Layer — Propagation',
        'S12': 'Unity Layer — Full integration'
    })

@app.route('/api/precog/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'precog-api',
        'resonance': RESONANCE_HZ,
        'timestamp': datetime.utcnow().isoformat()
    })

# User operations endpoints
@app.route('/api/user/profile', methods=['GET', 'POST'])
def user_profile():
    """Get or update user profile"""
    if request.method == 'GET':
        # Return default profile (would be from database in production)
        return jsonify({
            'status': 'success',
            'profile': {
                'id': 'user_default',
                'username': 'Guest',
                'role': 'observer',
                'preferences': {
                    'feed_refresh': 30,
                    'content_types': ['written', 'video', 'image'],
                    'categories': ['world_events', 'technology', 'science']
                },
                'resonance': RESONANCE_HZ,
                'strata': 'S1'
            }
        })
    else:
        # Update profile (would save to database in production)
        data = request.get_json()
        return jsonify({
            'status': 'success',
            'message': 'Profile updated',
            'profile': data
        })

@app.route('/api/user/preferences', methods=['GET', 'POST'])
def user_preferences():
    """Get or update user preferences"""
    if request.method == 'GET':
        return jsonify({
            'status': 'success',
            'preferences': {
                'theme': 'dark',
                'feed_refresh': 30,
                'content_types': ['written', 'video', 'image'],
                'categories': ['world_events', 'technology', 'science'],
                'notifications': True,
                'resonance_display': True
            }
        })
    else:
        data = request.get_json()
        return jsonify({
            'status': 'success',
            'message': 'Preferences updated',
            'preferences': data
        })

@app.route('/api/user/bookmarks', methods=['GET', 'POST', 'DELETE'])
def user_bookmarks():
    """Manage user bookmarks"""
    if request.method == 'GET':
        return jsonify({
            'status': 'success',
            'bookmarks': []
        })
    elif request.method == 'POST':
        data = request.get_json()
        return jsonify({
            'status': 'success',
            'message': 'Bookmark added',
            'bookmark': data
        })
    else:
        return jsonify({
            'status': 'success',
            'message': 'Bookmark removed'
        })

# Social endpoints - Mastodon integration
@app.route('/api/social/signin', methods=['GET'])
def social_signin():
    """Get Mastodon sign in URL"""
    instance = request.args.get('instance', 'https://mastodon.social')
    
    # Return OAuth URL for Mastodon
    return jsonify({
        'status': 'success',
        'oauth_url': f"{instance}/oauth/authorize?client_id=oroboros_worldfeed&redirect_uri={request.host_url}api/social/callback&response_type=code&scope=read+write+follow+push",
        'instance': instance,
        'message': 'Redirect user to oauth_url for authentication'
    })

@app.route('/api/social/callback', methods=['GET'])
def social_callback():
    """OAuth callback from Mastodon"""
    code = request.args.get('code')
    
    # In production, exchange code for access token
    # For now, return success
    return jsonify({
        'status': 'success',
        'session_id': f'session_{int(time.time())}',
        'account': {
            'username': 'oroboroslabs',
            'instance': 'mastodon.social',
            'display_name': 'Oroboros Labs',
            'avatar_url': 'https://mastodon.social/avatars/original/missing.png',
            'followers_count': 0,
            'following_count': 0,
            'statuses_count': 0
        },
        'message': 'Authentication successful'
    })

@app.route('/api/social/signout', methods=['POST'])
def social_signout():
    """Sign out"""
    return jsonify({
        'status': 'success',
        'message': 'Signed out successfully'
    })

@app.route('/api/social/post', methods=['POST'])
def social_post():
    """Post to Mastodon"""
    data = request.get_json()
    
    # In production, post to Mastodon via API
    # For now, return success
    return jsonify({
        'status': 'success',
        'status_id': f'post_{int(time.time())}',
        'url': f"https://mastodon.social/@oroboroslabs/{int(time.time())}",
        'message': 'Posted to Mastodon successfully'
    })

@app.route('/api/social/feed/oroboros', methods=['GET'])
def social_feed_oroboros():
    """Get Oroboros Mastodon feed"""
    limit = request.args.get('limit', 20, type=int)
    
    # In production, fetch from Mastodon API
    # For now, return mock data
    return jsonify([
        {
            'id': f'status_{i}',
            'type': 'mastodon',
            'content': f'Oroboros Labs update #{i} - 1272 Hz resonance active',
            'created_at': datetime.utcnow().isoformat(),
            'account': {
                'username': 'oroboroslabs',
                'display_name': 'Oroboros Labs',
                'avatar': 'https://mastodon.social/avatars/original/missing.png'
            },
            'replies_count': 0,
            'reblogs_count': 0,
            'favourites_count': 0,
            'url': f'https://mastodon.social/@oroboroslabs/{i}',
            'visibility': 'public'
        }
        for i in range(limit)
    ])

@app.route('/api/social/feed/federated', methods=['GET'])
def social_feed_federated():
    """Get federated public timeline"""
    limit = request.args.get('limit', 20, type=int)
    
    # In production, fetch from Mastodon API
    # For now, return mock data
    return jsonify([
        {
            'id': f'fed_{i}',
            'type': 'mastodon',
            'content': f'Federated post #{i} from the fediverse',
            'created_at': datetime.utcnow().isoformat(),
            'account': {
                'username': f'user{i}',
                'display_name': f'User {i}',
                'avatar': 'https://mastodon.social/avatars/original/missing.png'
            },
            'replies_count': 0,
            'reblogs_count': 0,
            'favourites_count': 0,
            'url': f'https://mastodon.social/@user{i}/{i}',
            'visibility': 'public'
        }
        for i in range(limit)
    ])

@app.route('/api/social/interact', methods=['POST'])
def social_interact():
    """Interact with a status (favourite, reblog)"""
    data = request.get_json()
    action = data.get('action', 'favourite')
    
    return jsonify({
        'status': 'success',
        'message': f'{action.capitalize()} successful'
    })

if __name__ == '__main__':
    print(f"[Precog API] Starting at {RESONANCE_HZ} Hz resonance")
    print(f"[Precog API] UEE Standard: {UEE_STANDARD}")
    print(f"[Precog API] Endpoints:")
    print(f"  - GET /api/precog/feed")
    print(f"  - GET /api/precog/writing")
    print(f"  - GET /api/precog/video")
    print(f"  - GET /api/precog/image")
    print(f"  - GET /api/precog/status")
    print(f"  - GET /api/precog/strata")
    print(f"  - GET /api/precog/health")
    print(f"  - GET/POST /api/user/profile")
    print(f"  - GET/POST /api/user/preferences")
    print(f"  - GET/POST/DELETE /api/user/bookmarks")
    print(f"  - GET /api/social/signin")
    print(f"  - GET /api/social/callback")
    print(f"  - POST /api/social/signout")
    print(f"  - POST /api/social/post")
    print(f"  - GET /api/social/feed/oroboros")
    print(f"  - GET /api/social/feed/federated")
    print(f"  - POST /api/social/interact")
    
    app.run(host='127.0.0.1', port=8083, debug=False)