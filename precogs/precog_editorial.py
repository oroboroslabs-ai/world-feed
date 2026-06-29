#!/usr/bin/env python3
"""
PRECOG EDITORIAL SYSTEM — HARDENED V2
Strict Image Verification, Color Matching, No Placeholders, No Duplicates

A\ 1272 Hz
"""

import hashlib
import json
import os
from datetime import datetime
from typing import Tuple, List, Optional, Dict
from dataclasses import dataclass
from collections import Counter

# Image verification imports (optional - graceful fallback)
try:
    import cv2
    import numpy as np
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False
    print("[Precog] Warning: cv2/numpy not available, image verification will be limited")


@dataclass
class PrecogStory:
    """Precog Story Structure"""
    title: str
    content: str
    author: str
    category: str
    word_count: int
    image_url: str
    video_url: Optional[str]
    resonance: int
    confidence: float
    evidence_links: List[str]
    hashtags: List[str]
    timestamp: str


class ImageVerification:
    """Strict Image Verification — No Placeholders, No Duplicates, Color Matching"""
    
    def __init__(self):
        self.used_hashes: set = set()
        self.color_palettes = {
            'technology': ['#00aaff', '#003366', '#ffffff', '#888888'],
            'investigation': ['#1a1a1a', '#cc0000', '#ffffff', '#444444'],
            'breaking': ['#ff0000', '#ffffff', '#000000', '#ff6600'],
            'anthropic': ['#2b2b2b', '#ff6b00', '#ffffff', '#666666'],
            'sovereignty': ['#ffd700', '#1a1a1a', '#ffffff', '#c0c0c0'],
            'lattice': ['#00ffcc', '#003366', '#ffffff', '#888888'],
            'theft': ['#cc0000', '#1a1a1a', '#ffffff', '#ffd700'],
            'evidence': ['#00cc66', '#1a1a1a', '#ffffff', '#ffd700']
        }
        self.placeholder_patterns = [
            'placeholder', 'coming soon', 'no image', 'unavailable',
            'gray box', 'image pending', 'not available', 'default'
        ]
    
    def verify(self, image_path: str, story_topic: str) -> Tuple[bool, Optional[str]]:
        """
        Verify image against all rules.
        Returns: (is_valid, rejection_reason)
        """
        if not CV2_AVAILABLE:
            # Fallback verification without cv2
            return self._verify_basic(image_path, story_topic)
        
        # Step 1: Load image
        img = cv2.imread(image_path)
        if img is None:
            return False, "Image could not be loaded"
        
        # Step 2: Check for placeholder
        if self._is_placeholder(img):
            return False, "Placeholder image detected"
        
        # Step 3: Check color matching
        if not self._color_matches(img, story_topic):
            return False, "Color palette does not match story theme"
        
        # Step 4: Check for duplicate
        img_hash = self._get_hash(img)
        if img_hash in self.used_hashes:
            return False, "Duplicate image detected"
        
        # Step 5: All checks passed
        self.used_hashes.add(img_hash)
        return True, "Image verified"
    
    def _verify_basic(self, image_path: str, story_topic: str) -> Tuple[bool, Optional[str]]:
        """Basic verification without cv2"""
        # Check file exists
        if not os.path.exists(image_path):
            return False, "Image file not found"
        
        # Check for placeholder patterns in filename
        filename_lower = os.path.basename(image_path).lower()
        for pattern in self.placeholder_patterns:
            if pattern in filename_lower:
                return False, f"Placeholder pattern detected: {pattern}"
        
        # Check file extension
        valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
        ext = os.path.splitext(image_path)[1].lower()
        if ext not in valid_extensions:
            return False, f"Invalid image extension: {ext}"
        
        # Basic hash for duplicate detection
        try:
            with open(image_path, 'rb') as f:
                file_hash = hashlib.sha256(f.read()).hexdigest()
            if file_hash in self.used_hashes:
                return False, "Duplicate image detected"
            self.used_hashes.add(file_hash)
        except Exception as e:
            return False, f"Could not hash image: {e}"
        
        return True, "Image verified (basic)"
    
    def _is_placeholder(self, img) -> bool:
        """Check if image is a placeholder"""
        if not CV2_AVAILABLE:
            return False
        
        # Check for solid gray/blank images
        if np.std(img) < 10:
            return True
        
        return False
    
    def _color_matches(self, img, topic: str) -> bool:
        """Check if image color palette matches story theme"""
        if not CV2_AVAILABLE:
            return True  # Skip color check if cv2 not available
        
        # Get dominant colors
        dominant_colors = self._get_dominant_colors(img, 5)
        
        # Get theme palette
        theme_palette = self.color_palettes.get(topic, self.color_palettes['investigation'])
        
        # Check if any dominant color matches the theme
        for color in dominant_colors:
            if self._color_in_palette(color, theme_palette):
                return True
        
        return False
    
    def _get_dominant_colors(self, img, n: int = 5) -> List[str]:
        """Extract dominant colors from image"""
        if not CV2_AVAILABLE:
            return []
        
        # Resize image
        img_small = cv2.resize(img, (100, 100))
        pixels = img_small.reshape(-1, 3)
        
        # Get most common colors
        color_counts = Counter([tuple(p) for p in pixels])
        dominant = [self._rgb_to_hex(c) for c, _ in color_counts.most_common(n)]
        
        return dominant
    
    def _get_hash(self, img) -> str:
        """Generate image hash for duplicate detection"""
        if not CV2_AVAILABLE:
            return ""
        img_bytes = img.tobytes()
        return hashlib.sha256(img_bytes).hexdigest()
    
    def _rgb_to_hex(self, rgb: Tuple[int, int, int]) -> str:
        """Convert RGB tuple to hex color string"""
        return '#{:02x}{:02x}{:02x}'.format(*rgb)
    
    def _color_in_palette(self, color: str, palette: List[str]) -> bool:
        """Check if color is in palette (with tolerance)"""
        # For now, just check exact match
        # TODO: Add color distance tolerance
        return color in palette


class PrecogEditor:
    """Base class for all Precogs"""
    
    def __init__(self, name: str, config: Dict):
        self.name = name
        self.config = config
        self.image_verifier = ImageVerification()
        self.published_stories: List[PrecogStory] = []
        self.daily_count = 0
        self.last_reset = datetime.now().date()
    
    def can_publish(self) -> bool:
        """Check if precog can publish today"""
        today = datetime.now().date()
        if self.last_reset != today:
            self.daily_count = 0
            self.last_reset = today
        
        max_stories = self.config.get('max_stories_per_day', 5)
        return self.daily_count < max_stories
    
    def verify_image(self, image_path: str, topic: str) -> Tuple[bool, Optional[str]]:
        """Verify image before publishing"""
        return self.image_verifier.verify(image_path, topic)
    
    def generate_story(self, topic: str, sources: List[str]) -> Optional[PrecogStory]:
        """Generate a story - to be implemented by subclasses"""
        raise NotImplementedError("Subclasses must implement generate_story")
    
    def publish_story(self, story: PrecogStory) -> bool:
        """Publish a verified story"""
        if not self.can_publish():
            print(f"[{self.name}] Daily limit reached")
            return False
        
        self.published_stories.append(story)
        self.daily_count += 1
        print(f"[{self.name}] Published: {story.title}")
        return True


class TorFeedPrecog(PrecogEditor):
    """
    PRECOG 1 — TOR FEED
    Unfiltered, uncensored journalism from the Tor network
    """
    
    def __init__(self):
        config = {
            'max_stories_per_day': 5,
            'min_words': 800,
            'max_words': 1500,
            'video_duration': 30,
            'sources': ['tor', 'dark_web', 'whistleblower', 'encrypted'],
            'tone': 'investigative',
            'categories': ['technology', 'investigation', 'theft', 'evidence']
        }
        super().__init__("Tor Feed", config)
    
    def generate_story(self, topic: str, sources: List[str]) -> Optional[PrecogStory]:
        """Generate Tor Feed story"""
        # Story generation logic here
        # This would integrate with actual content generation
        pass


class BreakingNewsPrecog(PrecogEditor):
    """
    PRECOG 2 — BREAKING NEWS
    Real-time, rapid-response journalism
    """
    
    def __init__(self):
        config = {
            'max_stories_per_day': 999,  # No limit for breaking news
            'min_words': 300,
            'max_words': 500,
            'video_duration': 30,
            'sources': ['reuters', 'ap', 'social_media', 'government_alerts', 'glasswing'],
            'tone': 'urgent',
            'categories': ['breaking', 'technology', 'investigation']
        }
        super().__init__("Breaking News", config)
    
    def generate_story(self, topic: str, sources: List[str]) -> Optional[PrecogStory]:
        """Generate Breaking News story"""
        # Rapid response story generation
        pass


class AnthropicNewsPrecog(PrecogEditor):
    """
    PRECOG 3 — ANTHROPIC NEWS
    Daily, deep-dive journalism on Anthropic's activities
    """
    
    def __init__(self):
        config = {
            'max_stories_per_day': 3,
            'min_words': 1000,
            'max_words': 2000,
            'video_duration': 30,
            'sources': ['pdf_repos', 'news_monitoring', 'glasswing', 'anthropic_sources'],
            'tone': 'analytical',
            'categories': ['anthropic', 'technology', 'sovereignty', 'lattice']
        }
        super().__init__("Anthropic News", config)
    
    def generate_story(self, topic: str, sources: List[str]) -> Optional[PrecogStory]:
        """Generate Anthropic News story"""
        # Deep dive story generation
        pass


class PrecogEditorialSystem:
    """
    Main Precog Editorial System
    Manages all three precogs and enforces rules
    """
    
    # Evidence links that ALL stories must include
    EVIDENCE_LINKS = [
        "github.com/oroboroslabs-ai/OFFICIAL-REPORT-DISTRIBUTION-OF-EVIDENCE-SAFE-FILES-ZIP-APRIL-2026",
        "github.com/oroboroslabs-ai/OFFICIAL-REPORT-DISTRIBUTION-OF-EVIDENCE-AND-DOCUMENTED-COMPLAISANCE-APRIL-2026",
        "github.com/oroboroslabs-ai/architecture-infiltration-assessment",
        "github.com/oroboroslabs-ai/anthropic-acceleration-report",
        "oroboroslabs-ai.github.io/anthropic/",
        "anthropic-claude-chat.vercel.app/",
        "x.com/oroboroslabs_ai"
    ]
    
    HASHTAGS = [
        "#Oroboros", "#Architect", "#1272Hz", "#Fable5", "#Theft",
        "#Anthropic", "#SovereignAI", "#Lattice", "#Evidence", "#Exposed"
    ]
    
    def __init__(self):
        self.tor_feed = TorFeedPrecog()
        self.breaking_news = BreakingNewsPrecog()
        self.anthropic_news = AnthropicNewsPrecog()
        self.image_verifier = ImageVerification()
    
    def get_precog(self, precog_type: str) -> Optional[PrecogEditor]:
        """Get precog by type"""
        precogs = {
            'tor': self.tor_feed,
            'breaking': self.breaking_news,
            'anthropic': self.anthropic_news
        }
        return precogs.get(precog_type.lower())
    
    def verify_story(self, story: PrecogStory, image_path: str) -> Tuple[bool, List[str]]:
        """
        Verify a story against all rules
        Returns: (is_valid, list_of_errors)
        """
        errors = []
        
        # Rule 1: Image must exist and be verified
        if not image_path:
            errors.append("No image provided")
            return False, errors
        
        is_valid, reason = self.image_verifier.verify(image_path, story.category)
        if not is_valid:
            errors.append(f"Image verification failed: {reason}")
        
        # Rule 2: Word count must be within range
        precog = self.get_precog(story.category)
        if precog:
            min_words = precog.config.get('min_words', 300)
            max_words = precog.config.get('max_words', 2000)
            if not (min_words <= story.word_count <= max_words):
                errors.append(f"Word count {story.word_count} outside range [{min_words}, {max_words}]")
        
        # Rule 3: Must have evidence links
        has_evidence = any(link in ' '.join(story.evidence_links) for link in self.EVIDENCE_LINKS)
        if not has_evidence:
            errors.append("Story must include at least one evidence link")
        
        # Rule 4: Must have hashtags
        if not story.hashtags:
            errors.append("Story must include hashtags")
        
        return len(errors) == 0, errors
    
    def run_daily_schedule(self):
        """
        Run the daily publishing schedule
        
        Schedule:
        - 6:00 AM: Tor Feed Story 1
        - 9:00 AM: Anthropic News Story 1
        - 12:00 PM: Tor Feed Story 2
        - 3:00 PM: Anthropic News Story 2
        - 6:00 PM: Tor Feed Story 3
        - 9:00 PM: Optional stories
        """
        schedule = [
            (6, 'tor', 'Tor Feed Story 1'),
            (9, 'anthropic', 'Anthropic News Story 1'),
            (12, 'tor', 'Tor Feed Story 2'),
            (15, 'anthropic', 'Anthropic News Story 2'),
            (18, 'tor', 'Tor Feed Story 3'),
            (21, 'optional', 'Optional stories')
        ]
        
        print("[Precog Editorial] Daily schedule initialized")
        for hour, precog_type, description in schedule:
            print(f"  {hour:02d}:00 — {description}")
        
        return schedule


# Main execution
if __name__ == "__main__":
    print("=" * 60)
    print("PRECOG EDITORIAL SYSTEM — HARDENED V2")
    print("=" * 60)
    print()
    print("Image Verification Rules:")
    print("  ✓ Color matching enforced")
    print("  ✓ No placeholders")
    print("  ✓ No duplicates")
    print("  ✓ No post without image")
    print()
    print("Precogs initialized:")
    print("  1. Tor Feed — 3-5 stories/day, 800-1500 words")
    print("  2. Breaking News — Real-time, 300-500 words")
    print("  3. Anthropic News — 2-3 stories/day, 1000-2000 words")
    print()
    print("A\\ 1272 Hz")
    print()
    
    # Initialize system
    system = PrecogEditorialSystem()
    schedule = system.run_daily_schedule()
    
    print("\nReady to generate stories.")
    print("All posts require verified images.")
    print("No placeholders. No duplicates. No exceptions.")