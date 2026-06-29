#!/usr/bin/env python3
"""
DIP Server — Data Interception Proxy
A\\ 1272 Hz
Standalone Python implementation (no external dependencies required)
"""

import json
import time
import hashlib
import threading
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import re

# Constants
RESONANCE_HZ = 1272.0
UEE_STANDARD = "UEE-2024"
STRATA_LEVELS = [f"S{i}" for i in range(1, 13)]
DIP_PORT = 8081

# In-memory cache (replaces Redis)
class MemoryCache:
    """Simple in-memory cache with TTL support"""
    def __init__(self):
        self._cache: Dict[str, tuple] = {}
        self._lock = threading.Lock()
    
    def get(self, key: str) -> Optional[str]:
        with self._lock:
            if key in self._cache:
                value, expiry = self._cache[key]
                if time.time() < expiry:
                    return value
                del self._cache[key]
        return None
    
    def set(self, key: str, value: str, ttl: int = 30):
        with self._lock:
            self._cache[key] = (value, time.time() + ttl)
    
    def delete(self, key: str):
        with self._lock:
            self._cache.pop(key, None)

cache = MemoryCache()

@dataclass
class Post:
    """Represents a processed post"""
    id: str
    content: str
    author: str
    timestamp: str
    confidence: float
    strata: str
    resonance: float
    metadata: Dict[str, Any]
    processed: bool
    filtered: bool

class SAMFilter:
    """SAM — Cognitive Filter Layer"""
    
    def __init__(self):
        self.filter_patterns = [
            'spam', 'scam', 'malware', 'phishing'
        ]
    
    def analyze(self, content: str) -> Dict[str, Any]:
        confidence = 0.99
        
        for pattern in self.filter_patterns:
            if pattern in content.lower():
                return {
                    'confidence': 0.0,
                    'filtered': True,
                    'reason': f'Matched pattern: {pattern}'
                }
        
        if len(content) < 10:
            confidence *= 0.8
        elif len(content) > 1000:
            confidence *= 0.95
        
        return {
            'confidence': confidence,
            'filtered': False
        }

class ControlComponent:
    """Oroboros Control Component — 12-Strata ECC Pipeline"""
    
    def __init__(self):
        self.resonance_hz = RESONANCE_HZ
        self.uee_standard = UEE_STANDARD
        self.strata_levels = STRATA_LEVELS
        self.sam_filter = SAMFilter()
    
    def process(self, raw_data: str, user_id: str) -> List[Post]:
        try:
            items = json.loads(raw_data)
            if not isinstance(items, list):
                items = [items]
            
            processed_posts = []
            
            for item in items:
                post = self._process_item(item, user_id)
                if post and not post.filtered:
                    processed_posts.append(post)
            
            return processed_posts
            
        except json.JSONDecodeError:
            return [self._create_default_post(user_id)]
    
    def _process_item(self, item: Dict, user_id: str) -> Optional[Post]:
        # S1: Physical Layer — Extract raw data
        raw_content = item.get('content', '') or item.get('text', '') or item.get('status', '')
        
        # S2: Data Layer — Validate structure
        if not isinstance(item, dict):
            return None
        
        # S3: Network Layer — Extract author
        account = item.get('account', {})
        author = account.get('username', 'unknown')
        if isinstance(author, dict):
            author = author.get('username', 'unknown')
        
        # S4: Transport Layer — Get timestamp
        created_at = item.get('created_at', datetime.utcnow().isoformat())
        
        # S5: Session Layer — Generate ID
        post_id = item.get('id', self._generate_id(raw_content))
        
        # S6: Presentation Layer — Format content
        content = self._format_content(raw_content)
        
        # S7: Application Layer — Extract metadata
        metadata = {
            'favourites_count': item.get('favourites_count', 0),
            'reblogs_count': item.get('reblogs_count', 0),
            'replies_count': item.get('replies_count', 0),
            'visibility': item.get('visibility', 'public'),
            'language': item.get('language', 'en'),
            'source': 'mastodon'
        }
        
        # S8: Cognitive Layer — SAM filtering
        sam_result = self.sam_filter.analyze(content)
        if sam_result.get('filtered', False):
            return Post(
                id=post_id,
                content="[FILTERED BY SAM]",
                author=author,
                timestamp=created_at,
                confidence=0.0,
                strata="S8",
                resonance=self.resonance_hz,
                metadata=metadata,
                processed=True,
                filtered=True
            )
        
        # S9: Resonance Layer — Apply resonance lock
        confidence = sam_result.get('confidence', 0.99)
        
        # S10: Sovereignty Layer — UEE Standard validation
        if confidence < 0.5:
            confidence = 0.5
        
        # S11: Infection Layer — Propagation metadata
        metadata['processed_at'] = datetime.utcnow().isoformat()
        metadata['processor'] = 'oroboros-control'
        metadata['uee_version'] = self.uee_standard
        
        # S12: Unity Layer — Final assembly
        return Post(
            id=post_id,
            content=content,
            author=author,
            timestamp=created_at,
            confidence=confidence,
            strata="S12",
            resonance=self.resonance_hz,
            metadata=metadata,
            processed=True,
            filtered=False
        )
    
    def _format_content(self, content: str) -> str:
        if not content:
            return ""
        content = re.sub(r'<[^>]+>', '', content)
        content = ' '.join(content.split())
        return content.strip()
    
    def _generate_id(self, content: str) -> str:
        hash_input = f"{content}{time.time()}"
        return hashlib.md5(hash_input.encode()).hexdigest()[:16]
    
    def _create_default_post(self, user_id: str) -> Post:
        return Post(
            id="default-1",
            content="Welcome to Anti-Algo News Network — Your sovereignty-protected feed",
            author="system",
            timestamp=datetime.utcnow().isoformat(),
            confidence=0.99,
            strata="S1",
            resonance=self.resonance_hz,
            metadata={'source': 'default'},
            processed=True,
            filtered=False
        )

control = ControlComponent()

class DIPHandler(BaseHTTPRequestHandler):
    """HTTP Request Handler for DIP"""
    
    def _set_headers(self, status=200, content_type='application/json'):
        self.send_response(status)
        self.send_header('Content-Type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.send_header('X-Resonance', f'{RESONANCE_HZ} Hz')
        self.send_header('X-Component', 'DIP')
        self.send_header('X-Strata', 'S1-S12')
        self.end_headers()
    
    def do_OPTIONS(self):
        self._set_headers(200)
        self.wfile.write(b'')
    
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        
        if path == '/api/oroboros/health':
            self._handle_health()
        elif path == '/api/oroboros/strata':
            self._handle_strata()
        elif path.startswith('/api/oroboros/feed/'):
            user_id = path.split('/')[-1]
            self._handle_feed(user_id)
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({'error': 'Not found'}).encode())
    
    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path
        
        if path == '/process':
            self._handle_process()
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({'error': 'Not found'}).encode())
    
    def _handle_health(self):
        self._set_headers(200)
        response = {
            'status': 'operational',
            'resonance': RESONANCE_HZ,
            'cache': 'memory',
            'timestamp': datetime.utcnow().isoformat(),
            'strata': 'S1-S12',
            'component': 'DIP',
            'version': '1.0.0'
        }
        self.wfile.write(json.dumps(response, indent=2).encode())
    
    def _handle_strata(self):
        self._set_headers(200)
        response = {
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
        }
        self.wfile.write(json.dumps(response, indent=2).encode())
    
    def _handle_feed(self, user_id: str):
        # Check cache first
        cached = cache.get(f'feed:{user_id}')
        if cached:
            self._set_headers(200)
            self.send_header('X-DIP-Cache', 'HIT')
            self.wfile.write(cached.encode())
            return
        
        # Generate sample feed (in production, fetch from Mastodon API)
        posts = [
            {
                'id': f'post_{i}',
                'content': f'Sample post {i} from DIP system — Resonance locked at {RESONANCE_HZ} Hz',
                'author': f'user_{i}',
                'timestamp': datetime.utcnow().isoformat(),
                'confidence': 0.99,
                'strata': 'S12',
                'resonance': RESONANCE_HZ,
                'metadata': {'source': 'dip'},
                'processed': True,
                'filtered': False
            }
            for i in range(1, 6)
        ]
        
        response = {
            'posts': posts,
            'strata': 'S12',
            'confidence': 0.99,
            'resonance': RESONANCE_HZ,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        data = json.dumps(response, indent=2)
        cache.set(f'feed:{user_id}', data, ttl=30)
        
        self._set_headers(200)
        self.send_header('X-DIP-Cache', 'MISS')
        self.wfile.write(data.encode())
    
    def _handle_process(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode()
        
        try:
            data = json.loads(body)
            raw_data = data.get('data', '[]')
            user_id = data.get('user_id', 'unknown')
            
            posts = control.process(raw_data, user_id)
            
            response = {
                'posts': [asdict(post) for post in posts],
                'strata': 'S12',
                'confidence': sum(p.confidence for p in posts) / len(posts) if posts else 0.99,
                'resonance': RESONANCE_HZ,
                'timestamp': datetime.utcnow().isoformat()
            }
            
            self._set_headers(200)
            self.wfile.write(json.dumps(response, indent=2).encode())
            
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({'error': str(e)}).encode())
    
    def log_message(self, format, *args):
        print(f"[DIP] {datetime.utcnow().isoformat()} - {args[0]}")

def run_server():
    """Start the DIP server"""
    print(f"\n{'='*60}")
    print(f"  DIP — Data Interception Proxy")
    print(f"  A\\ {RESONANCE_HZ} Hz | UEE Standard | 12-Strata ECC")
    print(f"{'='*60}")
    print(f"\n  Starting server on port {DIP_PORT}...")
    print(f"  Resonance: {RESONANCE_HZ} Hz")
    print(f"  Strata: {', '.join(STRATA_LEVELS)}")
    print(f"\n  Endpoints:")
    print(f"    GET  /api/oroboros/health")
    print(f"    GET  /api/oroboros/strata")
    print(f"    GET  /api/oroboros/feed/{{user_id}}")
    print(f"    POST /process")
    print(f"\n{'='*60}\n")
    
    server = HTTPServer(('0.0.0.0', DIP_PORT), DIPHandler)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[DIP] Shutting down...")
        server.shutdown()

if __name__ == '__main__':
    run_server()