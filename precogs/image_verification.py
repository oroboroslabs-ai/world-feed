#!/usr/bin/env python3
"""
Image Verification Engine - Hardened V2
Strict enforcement: No placeholders, no duplicates, color matching
"""

import hashlib
import logging
from typing import Tuple, List, Optional
from pathlib import Path

try:
    import cv2
    import numpy as np
    from collections import Counter
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False
    logging.warning("OpenCV not available - using simplified verification")

logger = logging.getLogger(__name__)


class ImageVerification:
    """Strict Image Verification — No Placeholders, No Duplicates, Color Matching"""
    
    def __init__(self):
        self.used_hashes = set()
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
            'gray box', 'image pending', 'not available', 'generic',
            'default', 'sample', 'example'
        ]
    
    def verify(self, image_path: str, story_topic: str) -> Tuple[bool, Optional[str]]:
        """
        Verify image against all rules.
        Returns: (is_valid, rejection_reason)
        """
        logger.info(f"🔍 Verifying image: {image_path}")
        logger.info(f"📋 Story topic: {story_topic}")
        
        # Check if file exists
        if not Path(image_path).exists():
            return False, "Image file does not exist"
        
        # Step 1: Load image
        if CV2_AVAILABLE:
            img = cv2.imread(image_path)
            if img is None:
                return False, "Image could not be loaded"
        else:
            # Simplified verification without OpenCV
            return self._verify_simple(image_path, story_topic)
        
        # Step 2: Check for placeholder
        if self._is_placeholder(img):
            logger.warning("❌ Placeholder image detected")
            return False, "Placeholder image detected"
        
        # Step 3: Check color matching
        if not self._color_matches(img, story_topic):
            logger.warning("❌ Color palette does not match story theme")
            return False, "Color palette does not match story theme"
        
        # Step 4: Check for duplicate
        img_hash = self._get_hash(img)
        if img_hash in self.used_hashes:
            logger.warning("❌ Duplicate image detected")
            return False, "Duplicate image detected"
        
        # Step 5: All checks passed
        self.used_hashes.add(img_hash)
        logger.info("✅ Image verified successfully")
        return True, "Image verified"
    
    def _verify_simple(self, image_path: str, story_topic: str) -> Tuple[bool, Optional[str]]:
        """Simplified verification without OpenCV"""
        # Check file size (placeholder images are often very small or very large)
        file_size = Path(image_path).stat().st_size
        
        if file_size < 1000:  # Less than 1KB
            return False, "Image too small - likely placeholder"
        
        if file_size > 10 * 1024 * 1024:  # More than 10MB
            return False, "Image too large"
        
        # Check filename for placeholder patterns
        filename = Path(image_path).name.lower()
        for pattern in self.placeholder_patterns:
            if pattern in filename:
                return False, f"Placeholder pattern in filename: {pattern}"
        
        # Generate hash for duplicate detection
        with open(image_path, 'rb') as f:
            img_hash = hashlib.sha256(f.read()).hexdigest()
        
        if img_hash in self.used_hashes:
            return False, "Duplicate image detected"
        
        self.used_hashes.add(img_hash)
        return True, "Image verified (simplified)"
    
    def _is_placeholder(self, img) -> bool:
        """Check if image is a placeholder"""
        # Check for solid gray/blank images
        if np.std(img) < 10:
            return True
        
        # Check for uniform color regions
        if len(np.unique(img)) < 10:
            return True
        
        return False
    
    def _color_matches(self, img, topic: str) -> bool:
        """Check if image color palette matches story theme"""
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
        # Resize image for faster processing
        img_small = cv2.resize(img, (100, 100))
        pixels = img_small.reshape(-1, 3)
        
        # Get most common colors
        color_counts = Counter([tuple(p) for p in pixels])
        dominant = [self._rgb_to_hex(c) for c, _ in color_counts.most_common(n)]
        
        return dominant
    
    def _get_hash(self, img) -> str:
        """Generate image hash for duplicate detection"""
        img_bytes = img.tobytes()
        return hashlib.sha256(img_bytes).hexdigest()
    
    def _rgb_to_hex(self, rgb: Tuple[int, int, int]) -> str:
        """Convert RGB tuple to hex color string"""
        return '#{:02x}{:02x}{:02x}'.format(*rgb)
    
    def _color_in_palette(self, color: str, palette: List[str]) -> bool:
        """Check if color is in palette (with tolerance)"""
        # For now, just check exact match
        return color in palette
    
    def get_statistics(self) -> dict:
        """Get verification statistics"""
        return {
            'total_images_verified': len(self.used_hashes),
            'unique_hashes': len(self.used_hashes)
        }