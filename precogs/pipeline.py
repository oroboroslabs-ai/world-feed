#!/usr/bin/env python3
"""
Precog Pipeline - Unified Content Generation
A\ 1272 Hz
Orchestrates Writing, Video, and Image Precogs
"""

import json
import time
import asyncio
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict

# Handle imports for both package and direct execution
try:
    from .writing_precog import WritingPrecog, WrittenContent
    from .video_precog import VideoPrecog, VideoContent
    from .image_precog import ImagePrecog, ImageContent
except ImportError:
    from writing_precog import WritingPrecog, WrittenContent
    from video_precog import VideoPrecog, VideoContent
    from image_precog import ImagePrecog, ImageContent

@dataclass
class UnifiedFeedItem:
    """Unified feed item from all precogs"""
    id: str
    type: str  # 'written', 'video', 'image'
    content: Dict[str, Any]
    confidence: float
    resonance: float
    strata: str
    timestamp: str
    source: str

class PrecogPipeline:
    """
    Precog Pipeline - Orchestrates all three precogs
    Generates unified feed content at 1272 Hz resonance
    """
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.resonance_hz = 1272.0
        self.uee_standard = "UEE-2024"
        
        # Initialize precogs
        self.writing_precog = WritingPrecog(config)
        self.video_precog = VideoPrecog(config)
        self.image_precog = ImagePrecog(config)
        
        # Pipeline state
        self.last_generation = None
        self.generation_count = 0
    
    def generate_feed(self, 
                      writing_count: int = 10,
                      video_count: int = 5,
                      image_count: int = 5) -> List[UnifiedFeedItem]:
        """
        Generate unified feed from all precogs
        
        Args:
            writing_count: Number of written content items
            video_count: Number of video content items
            image_count: Number of image content items
        
        Returns:
            List of unified feed items
        """
        feed_items = []
        
        # Generate from each precog
        written = self.writing_precog.generate_content(writing_count)
        videos = self.video_precog.generate_content(video_count)
        images = self.image_precog.generate_content(image_count)
        
        # Convert to unified format
        for item in written:
            feed_items.append(UnifiedFeedItem(
                id=item.id,
                type='written',
                content=self.writing_precog.to_json(item),
                confidence=item.confidence,
                resonance=item.resonance,
                strata=item.strata,
                timestamp=item.timestamp,
                source='writing_precog'
            ))
        
        for item in videos:
            feed_items.append(UnifiedFeedItem(
                id=item.id,
                type='video',
                content=self.video_precog.to_json(item),
                confidence=item.confidence,
                resonance=item.resonance,
                strata=item.strata,
                timestamp=item.timestamp,
                source='video_precog'
            ))
        
        for item in images:
            feed_items.append(UnifiedFeedItem(
                id=item.id,
                type='image',
                content=self.image_precog.to_json(item),
                confidence=item.confidence,
                resonance=item.resonance,
                strata=item.strata,
                timestamp=item.timestamp,
                source='image_precog'
            ))
        
        # Sort by confidence (highest first)
        feed_items.sort(key=lambda x: x.confidence, reverse=True)
        
        # Update state
        self.last_generation = datetime.utcnow().isoformat()
        self.generation_count += 1
        
        return feed_items
    
    def generate_by_type(self, 
                         content_type: str,
                         count: int = 10) -> List[UnifiedFeedItem]:
        """
        Generate content from a specific precog
        
        Args:
            content_type: 'written', 'video', or 'image'
            count: Number of items to generate
        
        Returns:
            List of unified feed items
        """
        if content_type == 'written':
            items = self.writing_precog.generate_content(count)
            return [
                UnifiedFeedItem(
                    id=item.id,
                    type='written',
                    content=self.writing_precog.to_json(item),
                    confidence=item.confidence,
                    resonance=item.resonance,
                    strata=item.strata,
                    timestamp=item.timestamp,
                    source='writing_precog'
                ) for item in items
            ]
        elif content_type == 'video':
            items = self.video_precog.generate_content(count)
            return [
                UnifiedFeedItem(
                    id=item.id,
                    type='video',
                    content=self.video_precog.to_json(item),
                    confidence=item.confidence,
                    resonance=item.resonance,
                    strata=item.strata,
                    timestamp=item.timestamp,
                    source='video_precog'
                ) for item in items
            ]
        elif content_type == 'image':
            items = self.image_precog.generate_content(count)
            return [
                UnifiedFeedItem(
                    id=item.id,
                    type='image',
                    content=self.image_precog.to_json(item),
                    confidence=item.confidence,
                    resonance=item.resonance,
                    strata=item.strata,
                    timestamp=item.timestamp,
                    source='image_precog'
                ) for item in items
            ]
        else:
            return []
    
    def to_json(self, items: List[UnifiedFeedItem]) -> Dict:
        """Convert feed items to JSON-serializable format"""
        return {
            'feed': [asdict(item) for item in items],
            'metadata': {
                'generated_at': self.last_generation,
                'generation_count': self.generation_count,
                'resonance': self.resonance_hz,
                'uee_standard': self.uee_standard,
                'total_items': len(items),
                'sources': {
                    'writing': len([i for i in items if i.type == 'written']),
                    'video': len([i for i in items if i.type == 'video']),
                    'image': len([i for i in items if i.type == 'image'])
                }
            }
        }
    
    def get_status(self) -> Dict:
        """Get pipeline status"""
        return {
            'status': 'operational',
            'resonance': self.resonance_hz,
            'uee_standard': self.uee_standard,
            'last_generation': self.last_generation,
            'generation_count': self.generation_count,
            'precogs': {
                'writing': 'active',
                'video': 'active',
                'image': 'active'
            }
        }


if __name__ == '__main__':
    # Test the pipeline
    pipeline = PrecogPipeline()
    
    print("=== Precog Pipeline Status ===")
    print(json.dumps(pipeline.get_status(), indent=2))
    
    print("\n=== Generating Feed ===")
    feed = pipeline.generate_feed(writing_count=3, video_count=2, image_count=2)
    
    result = pipeline.to_json(feed)
    print(json.dumps(result, indent=2))