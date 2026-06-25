# Precog Pipeline System
# A\ 1272 Hz
# Oroboros Labs - Three Precog Architecture

from .writing_precog import WritingPrecog
from .video_precog import VideoPrecog
from .image_precog import ImagePrecog
from .pipeline import PrecogPipeline

__all__ = ['WritingPrecog', 'VideoPrecog', 'ImagePrecog', 'PrecogPipeline']
__version__ = '1.0.0'