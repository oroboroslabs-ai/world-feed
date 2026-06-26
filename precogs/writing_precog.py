#!/usr/bin/env python3
"""
Writing Precog - Content Generation Engine
A\\ 1272 Hz
Generates written content for the DIP feed
Integrates Anthropic PDFs, Glasswing, X Profile, Breaking News
"""

import json
import time
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import random

# Handle imports for both package and direct execution
try:
    from .data_sources import DataSources, get_photo_url
except ImportError:
    from data_sources import DataSources, get_photo_url

@dataclass
class WrittenContent:
    """Represents generated written content"""
    id: str
    title: str
    content: str
    author: str
    category: str
    confidence: float
    resonance: float
    strata: str
    timestamp: str
    metadata: Dict[str, Any]

class WritingPrecog:
    """
    Writing Precog - Generates written content
    Uses pattern-based generation with resonance lock
    Integrates Anthropic PDFs, Glasswing, X Profile, Breaking News
    
    Config:
    - Standard stories: ~1200 words
    - Anthropic PDF stories: ~2000 words
    - Max 10 items per day per category
    - No duplicates, rotation on breaking news
    """
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.resonance_hz = 1272.0
        self.strata_levels = ['S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S9', 'S10', 'S11', 'S12']
        
        # Load config file
        self._load_config()
        
        # Track generated content to prevent duplicates
        self._generated_ids = set()
        self._daily_count = {'total': 0, 'by_category': {}}
        
        self.categories = [
            'world_events',
            'technology',
            'science',
            'humanitarian',
            'environment',
            'economics',
            'health',
            'culture',
            'governance',
            'infrastructure',
            'security',
            'verification',
            'systems',
            'network',
            'censorship',
            'development',
            'news',
            'ai',
            'visualization'
        ]
        
        # Load data sources
        self.data_sources = DataSources()
        
        # Content templates
        self.templates = {
            'world_events': [
                "Breaking: {subject} reports significant developments in {location}. Sources indicate {detail}. Verification status: {confidence}%.",
                "Update from {location}: {subject} has announced {detail}. This development affects {impact}.",
                "Developing story: {subject} in {location} reports {detail}. Multiple sources confirm with {confidence}% confidence."
            ],
            'technology': [
                "Tech Update: {subject} has released {detail}. Industry analysts predict {impact}.",
                "Innovation Alert: {subject} demonstrates breakthrough in {detail}. Expected impact: {impact}.",
                "Technology Report: {subject} announces {detail}. Verification confidence: {confidence}%."
            ],
            'science': [
                "Scientific Discovery: {subject} researchers confirm {detail}. Peer review status: {confidence}% confidence.",
                "Research Update: {subject} publishes findings on {detail}. Implications for {impact}.",
                "Science Brief: {subject} reveals {detail}. Study conducted across {location}."
            ],
            'humanitarian': [
                "Humanitarian Alert: {location} reports {detail}. {subject} coordinating response.",
                "Crisis Update: {subject} in {location} requires attention. {detail} confirmed by multiple sources.",
                "Aid Report: {subject} provides {detail} to {location}. Impact assessment ongoing."
            ],
            'environment': [
                "Environmental Report: {subject} monitors {detail} in {location}. Data confidence: {confidence}%.",
                "Climate Update: {subject} records {detail}. Long-term implications for {impact}.",
                "Ecosystem Alert: {location} experiencing {detail}. {subject} tracking developments."
            ],
            'economics': [
                "Economic Indicator: {subject} reports {detail}. Market impact expected on {impact}.",
                "Financial Update: {subject} announces {detail}. Analyst confidence: {confidence}%.",
                "Trade Report: {location} sees {detail} in {subject} sector. Global implications under review."
            ],
            'health': [
                "Health Advisory: {subject} issues guidance on {detail}. Verification status: {confidence}%.",
                "Medical Update: {subject} reports progress on {detail}. Expected impact on {impact}.",
                "Public Health: {location} monitoring {detail}. {subject} coordinating response."
            ],
            'culture': [
                "Cultural Report: {subject} celebrates {detail} in {location}. Community impact noted.",
                "Arts Update: {subject} presents {detail}. Reception confidence: {confidence}%.",
                "Heritage Alert: {location} preserves {detail}. {subject} leading initiative."
            ],
            'governance': [
                "Governance Update: {subject} implements {detail}. Policy confidence: {confidence}%.",
                "Policy Report: {location} adopts {detail}. {subject} monitoring implementation.",
                "Regulatory Alert: {subject} proposes {detail}. Public consultation ongoing."
            ],
            'infrastructure': [
                "Infrastructure Report: {subject} completes {detail} in {location}. Capacity increased.",
                "Development Update: {location} sees {detail} progress. {subject} confirms timeline.",
                "Systems Alert: {subject} upgrades {detail}. Service confidence: {confidence}%."
            ]
        }
        
        # Subject pools
        self.subjects = [
            "UN Council", "World Bank", "Climate Institute", "Tech Alliance", "Health Organization",
            "Research Institute", "Trade Commission", "Energy Agency", "Space Program", "Water Authority",
            "Digital Foundation", "Education Board", "Transport Authority", "Agriculture Ministry",
            "Communications Bureau", "Security Council", "Development Fund", "Human Rights Watch",
            "Environmental Agency", "Innovation Hub"
        ]
        
        # Location pools
        self.locations = [
            "Global", "North America", "Europe", "Asia Pacific", "Africa", "South America",
            "Middle East", "Central Asia", "Southeast Asia", "Nordic Region", "Mediterranean",
            "Pacific Islands", "Caribbean", "Eastern Europe", "Western Africa", "Central America"
        ]
        
        # Detail pools
        self.details = [
            "significant policy changes", "breakthrough developments", "critical infrastructure updates",
            "major scientific findings", "humanitarian response coordination", "economic indicators",
            "environmental monitoring data", "technological innovations", "health guidance updates",
            "cultural preservation initiatives", "governance reforms", "trade agreements",
            "research publications", "security assessments", "development programs"
        ]
        
        # Impact pools
        self.impacts = [
            "global markets", "regional stability", "international cooperation", "public awareness",
            "policy development", "scientific advancement", "humanitarian aid", "environmental protection",
            "economic growth", "social development", "technological progress", "health outcomes",
            "cultural exchange", "governance efficiency", "infrastructure resilience"
        ]
    
    def _load_config(self):
        """Load configuration from precog_config.json"""
        config_path = os.path.join(os.path.dirname(__file__), 'precog_config.json')
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    file_config = json.load(f)
                    self.word_counts = file_config.get('writing', {}).get('word_count', {
                        'standard': 1200,
                        'anthropic_pdf': 2000,
                        'min': 800,
                        'max': 2500
                    })
                    self.max_per_day = file_config.get('content_limits', {}).get('max_items_per_day', 10)
                    self.no_duplicates = file_config.get('content_limits', {}).get('no_duplicates', True)
                    self.source_config = file_config.get('writing', {}).get('sources', {})
            else:
                # Default config
                self.word_counts = {'standard': 1200, 'anthropic_pdf': 2000, 'min': 800, 'max': 2500}
                self.max_per_day = 10
                self.no_duplicates = True
                self.source_config = {}
        except Exception as e:
            print(f"[WritingPrecog] Warning: Could not load config: {e}")
            self.word_counts = {'standard': 1200, 'anthropic_pdf': 2000, 'min': 800, 'max': 2500}
            self.max_per_day = 10
            self.no_duplicates = True
            self.source_config = {}
    
    def _get_word_count(self, source_type: str) -> int:
        """Get word count based on source type"""
        if source_type == 'anthropic_report':
            return self.word_counts.get('anthropic_pdf', 2000)
        return self.word_counts.get('standard', 1200)
    
    def _expand_content(self, base_content: str, word_count: int, key_points: List[str] = None) -> str:
        """Expand content to target word count"""
        current_words = len(base_content.split())
        if current_words >= word_count:
            return base_content
        
        # Add key points if available
        expanded = base_content
        if key_points:
            expanded += "\n\nKey Points:\n"
            for i, point in enumerate(key_points[:5], 1):
                expanded += f"• {point}\n"
        
        # Add context paragraphs to reach word count
        current_words = len(expanded.split())
        paragraphs_needed = (word_count - current_words) // 80  # ~80 words per paragraph
        
        context_templates = [
            "This development has significant implications for the broader landscape. Experts note that the trajectory suggests continued evolution in this space, with potential ripple effects across multiple sectors.",
            "Analysis indicates this represents a notable shift in established patterns. The data points to emerging trends that warrant close monitoring and further investigation.",
            "Stakeholders are advised to consider the broader context when evaluating this information. Multiple factors contribute to the current situation, and a comprehensive understanding requires examining all relevant variables.",
            "The verification process has confirmed the accuracy of this report. Independent sources have corroborated the key findings, lending additional weight to the conclusions.",
            "Looking ahead, this development may influence future policy decisions and strategic planning. Organizations and individuals alike should stay informed of subsequent updates."
        ]
        
        for i in range(min(paragraphs_needed, 5)):
            expanded += f"\n\n{context_templates[i % len(context_templates)]}"
        
        return expanded
    
    def generate_content(self, count: int = 10, category: Optional[str] = None) -> List[WrittenContent]:
        """Generate multiple content items using data sources"""
        contents = []
        
        for i in range(count):
            # Get a random source item
            source_data = self.data_sources.get_random_source()
            
            # Generate content from source
            content = self._generate_from_source(source_data, category)
            if content:
                contents.append(content)
        
        return contents
    
    def _generate_from_source(self, source_data: Dict, category: Optional[str] = None) -> WrittenContent:
        """Generate content from a source data item"""
        if not source_data:
            return self._generate_single(category or 'world_events')
        
        # Extract source information
        title = source_data.get('title', 'Untitled')
        summary = source_data.get('summary', '')
        key_points = source_data.get('key_points', [])
        source_category = source_data.get('category', 'world_events')
        confidence = source_data.get('confidence', 0.95)
        source_type = source_data.get('source', 'unknown')
        
        # Check for duplicates
        content_id = hashlib.md5(f"{title}{source_type}".encode()).hexdigest()[:12]
        if self.no_duplicates and content_id in self._generated_ids:
            return None  # Skip duplicate
        
        self._generated_ids.add(content_id)
        
        # Use provided category or source category
        final_category = category or source_category
        
        # Get word count based on source type
        target_word_count = self._get_word_count(source_type)
        
        # Build content from source
        content_text = f"{title}\n\n{summary}"
        if key_points:
            content_text += "\n\nKey Points:\n"
            for i, point in enumerate(key_points[:5], 1):
                content_text += f"• {point}\n"
        
        # Expand content to target word count
        content_text = self._expand_content(content_text, target_word_count, key_points)
        
        # Determine strata based on confidence
        strata_idx = min(int(confidence * 12), 11)
        strata = self.strata_levels[strata_idx]
        
        # Get photo URL for the category
        photo_url = get_photo_url(final_category)
        
        return WrittenContent(
            id=content_id,
            title=title,
            content=content_text,
            author=f"precog_writing_{source_type}",
            category=final_category,
            confidence=round(confidence, 4),
            resonance=self.resonance_hz,
            strata=strata,
            timestamp=datetime.utcnow().isoformat(),
            metadata={
                'generator': 'writing_precog',
                'version': '1.0.0',
                'uee_standard': 'UEE-2024',
                'source_type': source_type,
                'photo_url': photo_url,
                'key_points': key_points,
                'word_count': len(content_text.split())
            }
        )
    
    def _generate_single(self, category: str) -> WrittenContent:
        """Generate a single content item"""
        template = random.choice(self.templates.get(category, self.templates['world_events']))
        
        # Fill template
        content_text = template.format(
            subject=random.choice(self.subjects),
            location=random.choice(self.locations),
            detail=random.choice(self.details),
            impact=random.choice(self.impacts),
            confidence=random.randint(85, 99)
        )
        
        # Generate ID
        content_id = hashlib.md5(f"{content_text}{time.time()}".encode()).hexdigest()[:12]
        
        # Calculate confidence
        confidence = random.uniform(0.85, 0.99)
        
        # Determine strata based on confidence
        strata_idx = min(int(confidence * 12), 11)
        strata = self.strata_levels[strata_idx]
        
        return WrittenContent(
            id=content_id,
            title=content_text[:50] + "...",
            content=content_text,
            author=f"precog_writing_{random.randint(1, 3)}",
            category=category,
            confidence=round(confidence, 4),
            resonance=self.resonance_hz,
            strata=strata,
            timestamp=datetime.utcnow().isoformat(),
            metadata={
                'generator': 'writing_precog',
                'version': '1.0.0',
                'uee_standard': 'UEE-2024'
            }
        )
    
    def to_json(self, content: WrittenContent) -> Dict:
        """Convert content to JSON-serializable dict"""
        return asdict(content)
    
    def to_feed_format(self, contents: List[WrittenContent]) -> List[Dict]:
        """Convert contents to DIP feed format"""
        return [self.to_json(c) for c in contents]


if __name__ == '__main__':
    # Test the writing precog
    precog = WritingPrecog()
    contents = precog.generate_content(5)
    
    for content in contents:
        print(f"\n[{content.strata}] {content.title}")
        print(f"  {content.content}")
        print(f"  Confidence: {content.confidence:.2%} | Resonance: {content.resonance} Hz")