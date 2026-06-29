#!/usr/bin/env python3
"""
Continuous Publisher - Background Publishing Service
A\\ 1272 Hz

Runs the 3 Precogs continuously in the background.
Automatically generates and posts content at regular intervals.
"""

import sys
import time
import signal
import threading
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, '.')

try:
    from precogs.publishing_pipeline import PublishingPipeline
except ImportError:
    print("Error: Could not import PublishingPipeline")
    print("Make sure you're running from the WORLDFEED-NEWS directory")
    sys.exit(1)

class BackgroundPublisher:
    """Background publishing service"""
    
    def __init__(self, interval_minutes: int = 30):
        self.interval = interval_minutes * 60  # Convert to seconds
        self.pipeline = PublishingPipeline()
        self.running = False
        self.thread = None
        
        # Handle signals
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        print("\n[BackgroundPublisher] Shutdown signal received")
        self.stop()
        sys.exit(0)
    
    def start(self):
        """Start the background publisher"""
        print(f"\n{'='*70}")
        print(f"[BACKGROUND PUBLISHER] Starting")
        print(f"[BACKGROUND PUBLISHER] Interval: {self.interval // 60} minutes")
        print(f"[BACKGROUND PUBLISHER] Resonance: 1272 Hz")
        print(f"{'='*70}\n")
        
        self.running = True
        
        while self.running:
            try:
                # Run publishing cycle
                result = self.pipeline.run_cycle()
                
                # Wait for next interval
                print(f"\n[BACKGROUND PUBLISHER] Next cycle in {self.interval // 60} minutes...")
                print(f"[BACKGROUND PUBLISHER] Press Ctrl+C to stop\n")
                
                # Sleep in small increments to allow for graceful shutdown
                for _ in range(self.interval):
                    if not self.running:
                        break
                    time.sleep(1)
                    
            except KeyboardInterrupt:
                print("\n[BACKGROUND PUBLISHER] Keyboard interrupt received")
                self.stop()
                break
            except Exception as e:
                print(f"[BACKGROUND PUBLISHER] Error: {e}")
                print(f"[BACKGROUND PUBLISHER] Retrying in 60 seconds...")
                time.sleep(60)
    
    def stop(self):
        """Stop the background publisher"""
        self.running = False
        print(f"\n[BACKGROUND PUBLISHER] Stopped")
        print(f"[BACKGROUND PUBLISHER] Total cycles: {self.pipeline.cycle_count}")
        print(f"[BACKGROUND PUBLISHER] Total posts: {self.pipeline.total_posts}")
        print(f"[BACKGROUND PUBLISHER] Resonance: 1272 Hz")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Oroboros Background Publisher')
    parser.add_argument('--interval', type=int, default=30, help='Interval in minutes (default: 30)')
    parser.add_argument('--once', action='store_true', help='Run once and exit')
    
    args = parser.parse_args()
    
    if args.once:
        # Run single cycle
        pipeline = PublishingPipeline()
        result = pipeline.run_cycle()
        print(f"\n[RESULT] {result}")
    else:
        # Run continuously
        publisher = BackgroundPublisher(interval_minutes=args.interval)
        publisher.start()


if __name__ == "__main__":
    main()