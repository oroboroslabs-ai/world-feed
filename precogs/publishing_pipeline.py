#!/usr/bin/env python3
"""
Publishing Pipeline - Total Site Automation
A\\ 1272 Hz

The 3 Precogs handle all content generation and publishing:
- Precog A: Text & Story Writer
- Precog B: Image & Video Generator (with Video Diffusion Pipeline)
- Precog C: Prediction & Acquisition

Continuous operation with automated posting.
"""

import json
import os
import time
import schedule
import threading
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from pathlib import Path

# Import the precogs
try:
    from precog_engine import PrecogEngine, PrecogA_TextWriter, PrecogB_ImageVideo, PrecogC_Prediction, PostingPipeline
except ImportError:
    from .precog_engine import PrecogEngine, PrecogA_TextWriter, PrecogB_ImageVideo, PrecogC_Prediction, PostingPipeline

class PublishingPipeline:
    """
    Total Publishing Pipeline
    Handles continuous content generation and posting
    """
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.resonance = 1272.0
        self.strata_levels = ['S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S9', 'S10', 'S11', 'S12']
        
        # Initialize the 3 Precogs
        self.precog_a = PrecogA_TextWriter()  # Text & Story Writer
        self.precog_b = PrecogB_ImageVideo()  # Image & Video Generator
        self.precog_c = PrecogC_Prediction()  # Prediction & Acquisition
        
        # Posting pipeline
        self.poster = PostingPipeline()
        
        # State tracking
        self.cycle_count = 0
        self.last_run = None
        self.total_posts = 0
        self.is_running = False
        
        # Paths
        self.site_path = Path(__file__).parent.parent
        self.dip_html_path = self.site_path / 'dip.html'
        self.admin_html_path = self.site_path / 'admin.html'
        self.data_path = self.site_path / 'assets' / 'data'
        
        # Ensure data directory exists
        self.data_path.mkdir(parents=True, exist_ok=True)
        
        print(f"[PublishingPipeline] Initialized at {self.resonance} Hz")
        print(f"[PublishingPipeline] Site path: {self.site_path}")
    
    def run_cycle(self) -> Dict:
        """
        Run a complete publishing cycle
        The 3 Precogs work together to generate and post content
        """
        self.cycle_count += 1
        self.last_run = datetime.now(timezone.utc)
        
        print(f"\n{'='*70}")
        print(f"[PUBLISHING PIPELINE] Cycle {self.cycle_count}")
        print(f"[PUBLISHING PIPELINE] Time: {self.last_run.isoformat()}")
        print(f"[PUBLISHING PIPELINE] Resonance: {self.resonance} Hz")
        print(f"{'='*70}\n")
        
        # Step 1: Precog C - Prediction & Acquisition
        print("[Step 1/4] Precog C: Running prediction & acquisition...")
        prediction = self.precog_c.predict()
        
        recommended_written = prediction['recommended_content']['written']
        recommended_images = prediction['recommended_content']['images']
        recommended_videos = prediction['recommended_content']['videos']
        
        print(f"  -> Predicted {prediction['total_sources']} sources")
        print(f"  -> Recommended: {recommended_written} written, {recommended_images} images, {recommended_videos} videos")
        print(f"  -> Trending: {prediction['trending_topics'][:3]}")
        
        # Step 2: Precog A - Text & Story Writer
        print(f"\n[Step 2/4] Precog A: Generating {recommended_written} text posts...")
        text_posts = self.precog_a.write(prediction)
        print(f"  -> Generated {len(text_posts)} text posts")
        
        # Step 3: Precog B - Image & Video Generator
        print(f"\n[Step 3/4] Precog B: Generating visuals...")
        print(f"  -> Generating {recommended_images} images...")
        print(f"  -> Generating {recommended_videos} videos...")
        image_posts, video_posts = self.precog_b.generate_all(
            count=max(recommended_images, recommended_videos)
        )
        print(f"  -> Generated {len(image_posts)} images, {len(video_posts)} videos")
        
        # Step 4: Post to site
        print(f"\n[Step 4/4] Posting Pipeline: Publishing to site...")
        result = self.poster.post(text_posts, image_posts, video_posts)
        
        # Update totals
        self.total_posts += result['total_posts']
        
        # Summary
        print(f"\n{'='*70}")
        print(f"[PUBLISHING PIPELINE] Cycle {self.cycle_count} Complete")
        print(f"[PUBLISHING PIPELINE] Total posts this cycle: {result['total_posts']}")
        print(f"[PUBLISHING PIPELINE] Written: {result['written']}, Images: {result['images']}, Videos: {result['videos']}")
        print(f"[PUBLISHING PIPELINE] Total posts all time: {self.total_posts}")
        print(f"[PUBLISHING PIPELINE] Resonance: {self.resonance} Hz")
        print(f"{'='*70}\n")
        
        # Save cycle report
        self._save_cycle_report(result)
        
        return result
    
    def _save_cycle_report(self, result: Dict):
        """Save cycle report for admin dashboard"""
        report = {
            'cycle': self.cycle_count,
            'timestamp': result['timestamp'],
            'total_posts': result['total_posts'],
            'written': result['written'],
            'images': result['images'],
            'videos': result['videos'],
            'total_all_time': self.total_posts,
            'resonance': self.resonance,
            'strata': 'S12',
            'status': 'complete'
        }
        
        report_path = self.data_path / 'last_cycle.json'
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
    
    def start_continuous(self, interval_minutes: int = 30):
        """
        Start continuous publishing
        Runs the cycle every interval_minutes
        """
        print(f"\n[PUBLISHING PIPELINE] Starting continuous operation")
        print(f"[PUBLISHING PIPELINE] Interval: {interval_minutes} minutes")
        print(f"[PUBLISHING PIPELINE] Press Ctrl+C to stop\n")
        
        self.is_running = True
        
        # Run first cycle immediately
        self.run_cycle()
        
        # Schedule subsequent cycles
        schedule.every(interval_minutes).minutes.do(self.run_cycle)
        
        # Keep running
        while self.is_running:
            schedule.run_pending()
            time.sleep(1)
    
    def stop_continuous(self):
        """Stop continuous operation"""
        self.is_running = False
        print(f"\n[PUBLISHING PIPELINE] Stopped continuous operation")
        print(f"[PUBLISHING PIPELINE] Total cycles: {self.cycle_count}")
        print(f"[PUBLISHING PIPELINE] Total posts: {self.total_posts}")
    
    def get_status(self) -> Dict:
        """Get current pipeline status"""
        return {
            'is_running': self.is_running,
            'cycle_count': self.cycle_count,
            'total_posts': self.total_posts,
            'last_run': self.last_run.isoformat() if self.last_run else None,
            'resonance': self.resonance,
            'precogs': {
                'precog_a': 'Text & Story Writer - Active',
                'precog_b': 'Image & Video Generator - Active',
                'precog_c': 'Prediction & Acquisition - Active'
            },
            'strata': 'S1-S12',
            'uee_standard': 'UEE-2024'
        }


class ContinuousPublisher:
    """
    Background publisher that runs continuously
    """
    
    def __init__(self, interval_minutes: int = 30):
        self.interval = interval_minutes
        self.pipeline = PublishingPipeline()
        self.thread = None
        self.stop_event = threading.Event()
    
    def start(self):
        """Start the background publisher"""
        if self.thread and self.thread.is_alive():
            print("[ContinuousPublisher] Already running")
            return
        
        self.stop_event.clear()
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()
        print(f"[ContinuousPublisher] Started (interval: {self.interval} min)")
    
    def stop(self):
        """Stop the background publisher"""
        self.stop_event.set()
        if self.thread:
            self.thread.join(timeout=5)
        print("[ContinuousPublisher] Stopped")
    
    def _run_loop(self):
        """Main loop for continuous publishing"""
        while not self.stop_event.is_set():
            try:
                self.pipeline.run_cycle()
            except Exception as e:
                print(f"[ContinuousPublisher] Error: {e}")
            
            # Wait for interval or stop event
            self.stop_event.wait(self.interval * 60)
    
    def get_status(self) -> Dict:
        """Get publisher status"""
        return self.pipeline.get_status()


# CLI interface
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Oroboros Publishing Pipeline - 3 Precogs')
    parser.add_argument('--once', action='store_true', help='Run one cycle and exit')
    parser.add_argument('--continuous', action='store_true', help='Run continuously')
    parser.add_argument('--interval', type=int, default=30, help='Interval in minutes for continuous mode')
    parser.add_argument('--status', action='store_true', help='Get current status')
    
    args = parser.parse_args()
    
    if args.status:
        pipeline = PublishingPipeline()
        status = pipeline.get_status()
        print(json.dumps(status, indent=2))
    elif args.once:
        pipeline = PublishingPipeline()
        result = pipeline.run_cycle()
        print(json.dumps(result, indent=2))
    elif args.continuous:
        try:
            pipeline = PublishingPipeline()
            pipeline.start_continuous(interval_minutes=args.interval)
        except KeyboardInterrupt:
            pipeline.stop_continuous()
    else:
        # Default: run once
        pipeline = PublishingPipeline()
        result = pipeline.run_cycle()
        print(json.dumps(result, indent=2))
