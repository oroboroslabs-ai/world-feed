#!/usr/bin/env python3
"""
Precog API Integration - Connect Precogs to Anti-Algo Site
Pushes verified stories to the live WorldFeed
"""

import json
import logging
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PrecogAPI:
    """Connect Precogs to Anti-Algo Site"""
    
    def __init__(self):
        self.precog_output_dir = Path('data/precog_output')
        self.site_data_dir = Path('data')
        self.images_dir = Path('assets/img/precog')
        
        # Ensure directories exist
        self.images_dir.mkdir(parents=True, exist_ok=True)
        
        # Load existing site data
        self.site_data = self._load_site_data()
    
    def _load_site_data(self) -> dict:
        """Load existing site data"""
        data_file = self.site_data_dir / 'worldfeed.json'
        
        if data_file.exists():
            with open(data_file, 'r') as f:
                return json.load(f)
        else:
            # Initialize with empty structure
            return {
                'stories': [],
                'last_updated': None
            }
    
    def _save_site_data(self):
        """Save site data"""
        data_file = self.site_data_dir / 'worldfeed.json'
        
        self.site_data['last_updated'] = datetime.now().isoformat()
        
        with open(data_file, 'w') as f:
            json.dump(self.site_data, f, indent=2)
        
        logger.info(f"Site data saved to {data_file}")
    
    def _copy_image_to_site(self, image_path: str) -> str:
        """Copy image to site assets"""
        source_path = Path(image_path)
        
        if not source_path.exists():
            logger.warning(f"Image not found: {image_path}")
            return None
        
        # Generate new filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        dest_filename = f"precog_{timestamp}_{source_path.name}"
        dest_path = self.images_dir / dest_filename
        
        # Copy image
        shutil.copy(source_path, dest_path)
        
        # Return relative path for site
        return f"assets/img/precog/{dest_filename}"
    
    def _convert_precog_to_site_format(self, precog_story: dict) -> dict:
        """Convert Precog story to site format"""
        # Copy image to site
        image_path = self._copy_image_to_site(precog_story['image_path'])
        
        # Determine tier based on precog type
        tier_map = {
            'TOR_FEED': 5,
            'BREAKING_NEWS': 5,
            'ANTHROPIC_NEWS': 4
        }
        
        tier = tier_map.get(precog_story['precog'], 3)
        
        # Determine categories
        cats = ['new', 'verified']
        if precog_story.get('is_breaking'):
            cats.append('breaking')
        if precog_story.get('is_deep_dive'):
            cats.append('docs')
        
        # Convert to site format
        # Generate summary
        body_text = precog_story['body']
        if len(body_text) > 500:
            precog_summary = body_text[:500] + '...'
        else:
            precog_summary = body_text
        
        site_story = {
            'id': precog_story['id'],
            'tier': tier,
            'cats': cats,
            'title': precog_story['title'],
            'body': precog_summary,
            'summary': precog_summary,
            'sources': precog_story['sources'],
            'type': 'story',
            'minutesAgo': 1,  # Fresh story
            'location': 'global',
            'imageUrl': image_path,
            'videoUrl': '',
            'link': '#',
            'hasFullText': True,
            'precog': precog_story['precog'],
            'created_at': precog_story['created_at']
        }
        
        return site_story
    
    def load_precog_stories(self) -> List[dict]:
        """Load all Precog-generated stories"""
        stories = []
        
        # Load from each precog directory
        for precog_type in ['tor', 'breaking', 'anthropic']:
            precog_dir = self.precog_output_dir / precog_type
            
            if not precog_dir.exists():
                continue
            
            for story_file in precog_dir.glob('story_*.json'):
                try:
                    with open(story_file, 'r') as f:
                        story = json.load(f)
                        stories.append(story)
                        logger.info(f"Loaded story: {story['title']}")
                except Exception as e:
                    logger.error(f"Error loading {story_file}: {e}")
        
        return stories
    
    def push_to_site(self):
        """Push Precog stories to the site"""
        logger.info("Connecting Precogs to Anti-Algo Site...")
        
        # Load Precog stories
        precog_stories = self.load_precog_stories()
        
        if not precog_stories:
            logger.warning("No Precog stories found to push")
            return
        
        logger.info(f"Found {len(precog_stories)} Precog stories")
        
        # Convert and add to site data
        new_stories = []
        for precog_story in precog_stories:
            try:
                site_story = self._convert_precog_to_site_format(precog_story)
                new_stories.append(site_story)
                logger.info(f"Converted story: {site_story['title']}")
            except Exception as e:
                logger.error(f"Error converting story: {e}")
        
        # Add new stories to site data (at the beginning)
        self.site_data['stories'] = new_stories + self.site_data['stories']
        
        # Save updated site data
        self._save_site_data()
        
        logger.info(f"Successfully pushed {len(new_stories)} stories to Anti-Algo Site")
        
        # Generate report
        self._generate_push_report(new_stories)
    
    def _generate_push_report(self, stories: List[dict]):
        """Generate push report"""
        report = {
            'push_timestamp': datetime.now().isoformat(),
            'total_stories_pushed': len(stories),
            'stories': [
                {
                    'id': story['id'],
                    'title': story['title'],
                    'precog': story['precog'],
                    'tier': story['tier'],
                    'categories': story['cats']
                }
                for story in stories
            ]
        }
        
        report_file = self.precog_output_dir / f"push_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"Push report saved to {report_file}")


def main():
    """Main entry point"""
    api = PrecogAPI()
    api.push_to_site()
    
    print("\n" + "="*60)
    print("PRECOGS CONNECTED TO ANTI-ALGO SITE")
    print("="*60)
    print("Stories are now live on the WorldFeed")
    print("A 1272 Hz")
    print("="*60)


if __name__ == '__main__':
    main()