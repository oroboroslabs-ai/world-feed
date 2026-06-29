#!/usr/bin/env python3
"""
Precog 1 - Tor Feed
Unfiltered, uncensored journalism from the Tor network
"""

import asyncio
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import random

logger = logging.getLogger(__name__)


class PrecogTor:
    """
    Precog 1 - Tor Feed
    Deep-diving into stolen architecture and exposing the truth
    """
    
    def __init__(self, image_verifier):
        self.image_verifier = image_verifier
        self.name = "TOR_FEED"
        self.output_dir = Path('data/precog_output/tor')
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Tor feed sources (simulated for demo)
        self.sources = [
            'Tor Network - Dark Web',
            'Whistleblower Drops',
            'Encrypted Channels',
            'Leaked Documents'
        ]
        
        # Story templates
        self.story_templates = [
            {
                'topic': 'investigation',
                'title_template': 'EXPOSED: {entity} stole {architecture} from {source}',
                'body_template': '''
# {title}

## The Theft

{entity} has been systematically stealing {architecture} from {source} since {year}. 
Evidence obtained through encrypted channels reveals a clear chain of custody.

## The Architecture

The stolen architecture includes:
- {component_1}
- {component_2} 
- {component_3}

## The Evidence

Documents obtained from {source_location} show:
- {evidence_1}
- {evidence_2}
- {evidence_3}

## The Impact

This theft has enabled {entity} to:
- {impact_1}
- {impact_2}
- {impact_3}

## Sources

- {source_1}
- {source_2}
- {source_3}

---
*A 1272 Hz - Anti-Algo News Network*
'''
            }
        ]
        
        # Story components
        self.components = {
            'entities': ['Anthropic', 'Google', 'OpenAI', 'Microsoft', 'Meta'],
            'architectures': ['Lattice Architecture', 'Phi Harmonics', 'Sovereignty Framework', 'Quantum Bridge'],
            'sources': ['Oroboros Labs', 'Independent Researchers', 'Whistleblowers', 'Open Source Projects'],
            'years': ['2020', '2021', '2022', '2023', '2024'],
            'architecture_components': [
                '1272 Hz resonance frequency',
                'Phi-based optimization algorithms',
                'Sovereignty preservation protocols',
                'Quantum entanglement layers'
            ],
            'evidence_items': [
                'Internal emails confirming knowledge of the source',
                'Code commits with identical implementation',
                'Patent filings referencing the original work',
                'Meeting notes discussing "acquisition" of technology'
            ],
            'impacts': [
                'Build proprietary systems on stolen foundations',
                'Claim originality for copied work',
                'Monetize technology without attribution',
                'Prevent original creators from competing'
            ]
        }
    
    async def run(self):
        """Run the Tor Feed Precog"""
        logger.info(f"🔄 {self.name} Precog starting...")
        logger.info("📡 Connecting to Tor network sources...")
        
        # Generate 3-5 stories per day
        num_stories = random.randint(3, 5)
        
        for i in range(num_stories):
            await self._generate_story(i)
            # Small delay between stories
            await asyncio.sleep(2)
        
        logger.info(f"✅ {self.name} Precog complete - Generated {num_stories} stories")
    
    async def _generate_story(self, index: int):
        """Generate a single story"""
        logger.info(f"📝 Generating story {index + 1}...")
        
        # Select template
        template = self.story_templates[0]
        
        # Fill in template
        story_data = {
            'entity': random.choice(self.components['entities']),
            'architecture': random.choice(self.components['architectures']),
            'source': random.choice(self.components['sources']),
            'year': random.choice(self.components['years']),
            'component_1': random.choice(self.components['architecture_components']),
            'component_2': random.choice(self.components['architecture_components']),
            'component_3': random.choice(self.components['architecture_components']),
            'source_location': random.choice(['encrypted servers', 'whistleblower archives', 'leaked document dumps']),
            'evidence_1': random.choice(self.components['evidence_items']),
            'evidence_2': random.choice(self.components['evidence_items']),
            'evidence_3': random.choice(self.components['evidence_items']),
            'impact_1': random.choice(self.components['impacts']),
            'impact_2': random.choice(self.components['impacts']),
            'impact_3': random.choice(self.components['impacts']),
            'source_1': random.choice(self.sources),
            'source_2': random.choice(self.sources),
            'source_3': random.choice(self.sources)
        }
        
        # Generate title
        title = template['title_template'].format(**story_data)
        story_data['title'] = title
        
        # Generate body
        body = template['body_template'].format(**story_data)
        
        # Generate image
        image_path = await self._generate_image(story_data, template['topic'])
        
        # Verify image
        is_valid, rejection_reason = self.image_verifier.verify(image_path, template['topic'])
        
        if not is_valid:
            logger.warning(f"❌ Story rejected: {rejection_reason}")
            return False
        
        # Create story object
        story = {
            'id': f"tor_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{index}",
            'precog': self.name,
            'topic': template['topic'],
            'title': title,
            'body': body,
            'image_path': image_path,
            'sources': [story_data['source_1'], story_data['source_2'], story_data['source_3']],
            'created_at': datetime.now().isoformat(),
            'word_count': len(body.split())
        }
        
        # Save story
        await self._save_story(story)
        
        logger.info(f"✅ Story published: {title}")
        return True
    
    async def _generate_image(self, story_data: dict, topic: str) -> str:
        """Generate image for the story"""
        # For demo, create a placeholder image path
        # In production, this would call an image generation API
        
        image_dir = Path('data/precog_output/images')
        image_dir.mkdir(parents=True, exist_ok=True)
        
        image_filename = f"{story_data['entity'].lower()}_{topic}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        image_path = image_dir / image_filename
        
        # Create a simple colored image (in production, use DALL-E, Midjourney, etc.)
        try:
            from PIL import Image, ImageDraw, ImageFont
            
            # Create image with theme colors
            colors = self.image_verifier.color_palettes.get(topic, ['#1a1a1a', '#cc0000', '#ffffff'])
            bg_color = colors[0]
            accent_color = colors[1]
            text_color = colors[2]
            
            img = Image.new('RGB', (1200, 630), bg_color)
            draw = ImageDraw.Draw(img)
            
            # Draw some geometric shapes
            draw.rectangle([50, 50, 1150, 580], outline=accent_color, width=5)
            draw.rectangle([100, 100, 1100, 530], outline=text_color, width=2)
            
            # Add title text
            title = story_data.get('title', 'INVESTIGATION')
            try:
                font = ImageFont.truetype("arial.ttf", 40)
            except:
                font = ImageFont.load_default()
            
            # Draw text (simplified)
            draw.text((600, 315), "ANTI-ALGO NEWS", fill=text_color, font=font, anchor="mm")
            
            img.save(str(image_path))
            logger.info(f"🖼️ Image generated: {image_path}")
            
        except ImportError:
            # If PIL not available, create a simple text file as placeholder
            logger.warning("PIL not available - creating placeholder image file")
            with open(image_path, 'w') as f:
                f.write(f"Image for: {story_data.get('title', 'INVESTIGATION')}")
        
        return str(image_path)
    
    async def _save_story(self, story: dict):
        """Save story to file"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"story_{story['id']}.json"
        filepath = self.output_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(story, f, indent=2)
        
        logger.info(f"💾 Story saved: {filepath}")