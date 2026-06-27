#!/usr/bin/env python3
"""
Precog Editorial System - Hardened V2
Anti-Algo News Network - Precog Pipeline Controller
"""

import asyncio
import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from precogs.image_verification import ImageVerification
from precogs.precog_tor import PrecogTor
from precogs.precog_breaking import PrecogBreaking
from precogs.precog_anthropic import PrecogAnthropic

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('precogs/precog_pipeline.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class PrecogPipeline:
    """
    Main Precog Pipeline Controller
    Coordinates all Precogs and enforces verification rules
    """
    
    def __init__(self):
        self.image_verifier = ImageVerification()
        self.precogs = {
            'tor': PrecogTor(self.image_verifier),
            'breaking': PrecogBreaking(self.image_verifier),
            'anthropic': PrecogAnthropic(self.image_verifier)
        }
        self.output_dir = Path('data/precog_output')
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Statistics
        self.stats = {
            'total_stories': 0,
            'published_stories': 0,
            'rejected_stories': 0,
            'rejection_reasons': {}
        }
    
    async def start_all_precogs(self):
        """Start all Precogs simultaneously"""
        logger.info("🚀 Starting Precog Pipeline...")
        logger.info("📡 Anti-Algo News Network - Precog Editorial System V2")
        
        # Start all precogs
        tasks = []
        for name, precog in self.precogs.items():
            logger.info(f"🔄 Starting {name.upper()} Precog...")
            tasks.append(precog.run())
        
        # Run all precogs concurrently
        await asyncio.gather(*tasks)
        
        # Generate final report
        self.generate_report()
    
    async def run_single_precog(self, precog_name: str):
        """Run a single Precog"""
        if precog_name not in self.precogs:
            logger.error(f"❌ Unknown Precog: {precog_name}")
            return
        
        logger.info(f"🚀 Starting {precog_name.upper()} Precog...")
        await self.precogs[precog_name].run()
        self.generate_report()
    
    def generate_report(self):
        """Generate final report"""
        logger.info("=" * 60)
        logger.info("📊 PRECOG PIPELINE REPORT")
        logger.info("=" * 60)
        logger.info(f"Total Stories Generated: {self.stats['total_stories']}")
        logger.info(f"✅ Published Stories: {self.stats['published_stories']}")
        logger.info(f"❌ Rejected Stories: {self.stats['rejected_stories']}")
        
        if self.stats['rejection_reasons']:
            logger.info("\n📋 Rejection Reasons:")
            for reason, count in self.stats['rejection_reasons'].items():
                logger.info(f"  • {reason}: {count}")
        
        logger.info("=" * 60)
        logger.info("🎯 Pipeline Complete - A 1272 Hz")
        logger.info("=" * 60)
        
        # Save report to file
        report_path = self.output_dir / f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_path, 'w') as f:
            json.dump(self.stats, f, indent=2)
        
        logger.info(f"📄 Report saved to: {report_path}")


async def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Precog Pipeline Controller')
    parser.add_argument(
        '--precog',
        type=str,
        choices=['tor', 'breaking', 'anthropic', 'all'],
        default='all',
        help='Which Precog to run (default: all)'
    )
    
    args = parser.parse_args()
    
    pipeline = PrecogPipeline()
    
    if args.precog == 'all':
        await pipeline.start_all_precogs()
    else:
        await pipeline.run_single_precog(args.precog)


if __name__ == '__main__':
    asyncio.run(main())