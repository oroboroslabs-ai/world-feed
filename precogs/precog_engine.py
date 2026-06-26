#!/usr/bin/env python3
"""
Precog Engine - Full Site Automation
A\\ 1272 Hz

The 3 Precogs handle all content generation and posting:
- Precog A: Text & Story Writer
- Precog B: Image & Video Generator  
- Precog C: Prediction & Acquisition

All content is automatically published to the site.
"""

import json
import os
import time
from datetime import datetime
from typing import Dict, List, Optional, Any

# Import the precogs
try:
    from writing_precog import WritingPrecog
    from video_precog import VideoPrecog
    from image_precog import ImagePrecog
    from data_sources import DataSources
except ImportError:
    from .writing_precog import WritingPrecog
    from .video_precog import VideoPrecog
    from .image_precog import ImagePrecog
    from .data_sources import DataSources

class PrecogA_TextWriter:
    """Precog A — Text & Story Writer"""
    
    def __init__(self):
        self.writer = WritingPrecog()
        self.name = "Precog A - Text Writer"
        
    def write(self, prediction: Dict = None) -> List[Dict]:
        """Generate text content based on prediction"""
        print(f"[{self.name}] Generating text content...")
        
        # Generate content from all sources
        content = self.writer.generate_content(count=10)
        
        # Convert to postable format
        posts = []
        for item in content:
            posts.append({
                'id': item.id,
                'type': 'written',
                'title': item.title,
                'content': item.content,
                'author': item.author,
                'category': item.category,
                'confidence': item.confidence,
                'resonance': item.resonance,
                'strata': item.strata,
                'timestamp': item.timestamp,
                'source': item.metadata.get('source_type', 'precog_a'),
                'key_points': item.metadata.get('key_points', '')
            })
        
        print(f"[{self.name}] Generated {len(posts)} text posts")
        return posts

class PrecogB_ImageVideo:
    """Precog B — Image & Video Generator"""
    
    def __init__(self):
        self.image_gen = ImagePrecog()
        self.video_gen = VideoPrecog()
        self.name = "Precog B - Image/Video"
        
    def generate_image(self, text_content: Dict) -> Dict:
        """Generate an image for the post"""
        images = self.image_gen.generate_content(count=1)
        if images:
            img = images[0]
            return {
                'id': img.id,
                'type': 'image',
                'title': img.title,
                'description': img.description,
                'image_url': img.image_url,
                'thumbnail_url': img.thumbnail_url,
                'width': img.width,
                'height': img.height,
                'category': img.category,
                'confidence': img.confidence,
                'resonance': img.resonance,
                'strata': img.strata,
                'timestamp': img.timestamp,
                'source': img.metadata.get('source_type', 'precog_b')
            }
        return None
    
    def generate_video(self, text_content: Dict) -> Dict:
        """Generate a video for the post"""
        videos = self.video_gen.generate_content(count=1)
        if videos:
            vid = videos[0]
            return {
                'id': vid.id,
                'type': 'video',
                'title': vid.title,
                'description': vid.description,
                'thumbnail_url': vid.thumbnail_url,
                'video_url': vid.video_url,
                'duration': vid.duration,
                'category': vid.category,
                'confidence': vid.confidence,
                'resonance': vid.resonance,
                'strata': vid.strata,
                'timestamp': vid.timestamp,
                'source': vid.metadata.get('source_type', 'precog_b'),
                'video_validated': vid.metadata.get('video_validated', False)
            }
        return None
    
    def generate_all(self, count: int = 5) -> tuple:
        """Generate both images and videos"""
        print(f"[{self.name}] Generating visual content...")
        
        images = self.image_gen.generate_content(count=count)
        videos = self.video_gen.generate_content(count=count)
        
        image_posts = []
        for img in images:
            image_posts.append({
                'id': img.id,
                'type': 'image',
                'title': img.title,
                'description': img.description,
                'image_url': img.image_url,
                'thumbnail_url': img.thumbnail_url,
                'width': img.width,
                'height': img.height,
                'category': img.category,
                'confidence': img.confidence,
                'resonance': img.resonance,
                'strata': img.strata,
                'timestamp': img.timestamp,
                'source': img.metadata.get('source_type', 'precog_b')
            })
        
        video_posts = []
        for vid in videos:
            video_posts.append({
                'id': vid.id,
                'type': 'video',
                'title': vid.title,
                'description': vid.description,
                'thumbnail_url': vid.thumbnail_url,
                'video_url': vid.video_url,
                'duration': vid.duration,
                'category': vid.category,
                'confidence': vid.confidence,
                'resonance': vid.resonance,
                'strata': vid.strata,
                'timestamp': vid.timestamp,
                'source': vid.metadata.get('source_type', 'precog_b'),
                'video_validated': vid.metadata.get('video_validated', False)
            })
        
        print(f"[{self.name}] Generated {len(image_posts)} images, {len(video_posts)} videos")
        return image_posts, video_posts

class PrecogC_Prediction:
    """Precog C — Prediction & Acquisition"""
    
    def __init__(self):
        self.data_sources = DataSources()
        self.name = "Precog C - Prediction"
        
    def predict(self) -> Dict:
        """5-hour feed prediction"""
        print(f"[{self.name}] Running prediction cycle...")
        
        # Get all source data
        anthropic = self.data_sources.anthropic_reports
        glasswing = self.data_sources.glasswing_data
        x_profile = self.data_sources.x_profile
        breaking = self.data_sources.breaking_news
        
        # Combine and analyze
        prediction = {
            'timestamp': datetime.utcnow().isoformat(),
            'anthropic_count': len(anthropic),
            'glasswing_count': len(glasswing),
            'x_profile_count': len(x_profile),
            'breaking_count': len(breaking),
            'total_sources': len(anthropic) + len(glasswing) + len(x_profile) + len(breaking),
            'recommended_content': {
                'written': min(10, len(anthropic) + len(glasswing)),
                'images': min(10, len(breaking)),
                'videos': min(5, len(glasswing))
            },
            'trending_topics': self._extract_topics(breaking),
            'resonance': 1272.0
        }
        
        print(f"[{self.name}] Prediction complete: {prediction['total_sources']} sources, trending: {prediction['trending_topics'][:3]}")
        return prediction
    
    def _extract_topics(self, news: List) -> List[str]:
        """Extract trending topics from news"""
        topics = []
        for item in news:
            if 'title' in item:
                topics.append(item['title'])
        return topics[:10]

class PostingPipeline:
    """Automated Posting Pipeline"""
    
    def __init__(self, site_path: str = None):
        self.name = "Posting Pipeline"
        self.site_path = site_path or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.dip_html_path = os.path.join(self.site_path, 'dip.html')
        self.data_js_path = os.path.join(self.site_path, 'assets', 'js', 'precog_data.js')
        
    def post(self, text_posts: List, image_posts: List, video_posts: List) -> Dict:
        """Post all content to the site"""
        print(f"[{self.name}] Posting content to site...")
        
        # Combine all posts
        all_posts = []
        
        # Add written posts
        for post in text_posts:
            all_posts.append({
                'id': post['id'],
                'type': 'written',
                'content': post,
                'confidence': post['confidence'],
                'resonance': post['resonance'],
                'strata': post['strata'],
                'timestamp': post['timestamp'],
                'source': post['source']
            })
        
        # Add image posts
        for post in image_posts:
            all_posts.append({
                'id': post['id'],
                'type': 'image',
                'content': post,
                'confidence': post['confidence'],
                'resonance': post['resonance'],
                'strata': post['strata'],
                'timestamp': post['timestamp'],
                'source': post['source']
            })
        
        # Add video posts
        for post in video_posts:
            all_posts.append({
                'id': post['id'],
                'type': 'video',
                'content': post,
                'confidence': post['confidence'],
                'resonance': post['resonance'],
                'strata': post['strata'],
                'timestamp': post['timestamp'],
                'source': post['source']
            })
        
        # Sort by timestamp
        all_posts.sort(key=lambda x: x['timestamp'], reverse=True)
        
        # Update offline data in dip.html
        self._update_offline_data(all_posts)
        
        print(f"[{self.name}] Posted {len(all_posts)} items to site")
        
        return {
            'status': 'complete',
            'total_posts': len(all_posts),
            'written': len(text_posts),
            'images': len(image_posts),
            'videos': len(video_posts),
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def _update_offline_data(self, posts: List):
        """Update the offline data in dip.html"""
        try:
            # Read current dip.html
            with open(self.dip_html_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Generate new offline data
            offline_data = json.dumps(posts, indent=12)
            
            # Find and replace the offline data section
            start_marker = 'function getOfflineFeed() {\n            return ['
            end_marker = '];\n        }'
            
            start_idx = content.find(start_marker)
            end_idx = content.find(end_marker, start_idx)
            
            if start_idx != -1 and end_idx != -1:
                new_content = content[:start_idx + len(start_marker) - 1] + offline_data + content[end_idx:]
                
                # Write back
                with open(self.dip_html_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                print(f"[{self.name}] Updated offline data in dip.html")
        except Exception as e:
            print(f"[{self.name}] Error updating offline data: {e}")

class PrecogEngine:
    """The 3 Precogs — Full Site Automation"""
    
    def __init__(self):
        self.precog_a = PrecogA_TextWriter()
        self.precog_b = PrecogB_ImageVideo()
        self.precog_c = PrecogC_Prediction()
        self.pipeline = PostingPipeline()
        self.resonance = 1272.0
        
    def run_cycle(self) -> Dict:
        """Run the full precog cycle"""
        print(f"\n{'='*60}")
        print(f"[PRECOG ENGINE] Starting cycle at {datetime.utcnow().isoformat()}")
        print(f"[PRECOG ENGINE] Resonance: {self.resonance} Hz")
        print(f"{'='*60}\n")
        
        # 1. Predict what content is needed
        print("[PRECOG ENGINE] Step 1: Running Precog C prediction...")
        prediction = self.precog_c.predict()
        
        # 2. Generate text content
        print("\n[PRECOG ENGINE] Step 2: Running Precog A text generation...")
        text_posts = self.precog_a.write(prediction)
        
        # 3. Generate visuals
        print("\n[PRECOG ENGINE] Step 3: Running Precog B visual generation...")
        image_posts, video_posts = self.precog_b.generate_all(
            count=prediction['recommended_content']['images']
        )
        
        # 4. Post to site
        print("\n[PRECOG ENGINE] Step 4: Posting to site...")
        result = self.pipeline.post(text_posts, image_posts, video_posts)
        
        # Summary
        print(f"\n{'='*60}")
        print(f"[PRECOG ENGINE] Cycle complete!")
        print(f"[PRECOG ENGINE] Total posts: {result['total_posts']}")
        print(f"[PRECOG ENGINE] - Written: {result['written']}")
        print(f"[PRECOG ENGINE] - Images: {result['images']}")
        print(f"[PRECOG ENGINE] - Videos: {result['videos']}")
        print(f"[PRECOG ENGINE] Resonance: {self.resonance} Hz")
        print(f"{'='*60}\n")
        
        return result
    
    def run_continuous(self, interval_minutes: int = 30):
        """Run continuously at specified interval"""
        print(f"[PRECOG ENGINE] Starting continuous mode (every {interval_minutes} minutes)")
        
        while True:
            try:
                self.run_cycle()
                print(f"[PRECOG ENGINE] Sleeping for {interval_minutes} minutes...")
                time.sleep(interval_minutes * 60)
            except KeyboardInterrupt:
                print("\n[PRECOG ENGINE] Stopping continuous mode")
                break
            except Exception as e:
                print(f"[PRECOG ENGINE] Error: {e}")
                time.sleep(60)  # Wait 1 minute before retrying

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Precog Engine - Full Site Automation')
    parser.add_argument('--continuous', '-c', action='store_true', help='Run continuously')
    parser.add_argument('--interval', '-i', type=int, default=30, help='Interval in minutes (default: 30)')
    parser.add_argument('--once', '-o', action='store_true', help='Run once and exit')
    
    args = parser.parse_args()
    
    engine = PrecogEngine()
    
    if args.continuous:
        engine.run_continuous(interval_minutes=args.interval)
    elif args.once:
        engine.run_cycle()
    else:
        # Default: run once
        engine.run_cycle()

if __name__ == '__main__':
    main()