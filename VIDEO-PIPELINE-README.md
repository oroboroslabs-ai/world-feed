# Oroboros Video Diffusion Pipeline

## Overview

The Video Diffusion Pipeline integrates with `Q:\video-production-pipeline` to generate AI videos for the DIP (Data Interception Proxy) feed.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    PRECOG VIDEO PIPELINE                        │
│                    1272 Hz Resonance                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐    ┌──────────────────┐    ┌──────────────┐ │
│  │ Data Sources │───>│ Video Diffusion  │───>│   DIP Feed   │ │
│  │              │    │    Pipeline      │    │              │ │
│  │ - Anthropic  │    │                  │    │ - Videos     │ │
│  │ - Glasswing  │    │ Q:\video-        │    │ - Thumbnails │ │
│  │ - X Profile  │    │ production-      │    │ - Metadata   │ │
│  │ - Breaking   │    │ pipeline          │    │              │ │
│  │   News       │    │                  │    │              │ │
│  └──────────────┘    │                  │    └──────────────┘ │
│                      │ - SDXL          │                      │
│                      │ - SVD           │                      │
│                      │ - CogVideoX     │                      │
│                      │ - IP-Adapter    │                      │
│                      │ - FILM          │                      │
│                      └──────────────────┘                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Components

### 1. Video Diffusion Pipeline (`video_diffusion_pipeline.py`)

Main integration module that connects to `Q:\video-production-pipeline`:

```python
from precogs.video_diffusion_pipeline import VideoDiffusionPipeline

# Initialize pipeline
pipeline = VideoDiffusionPipeline()

# Generate video from prompt
result = pipeline.generate_video(
    prompt="Breaking: Major AI breakthrough announced",
    source="breaking_news",
    category="breaking_news"
)

# Generate from source data
result = pipeline.generate_from_source(source_data, category="report")
```

### 2. Video Precog (`video_precog.py`)

Updated to use the diffusion pipeline:

```python
from precogs.video_precog import VideoPrecog

# Initialize (automatically connects to diffusion pipeline)
precog = VideoPrecog()

# Generate videos
videos = precog.generate_content(count=5, category='breaking_news')
```

### 3. Video Production Pipeline (`Q:\video-production-pipeline`)

Core diffusion infrastructure:

- **SDXL**: Text-to-image generation (1024x1024, fp16)
- **SVD**: Stable Video Diffusion (image-to-video, 25 frames, 8 fps)
- **CogVideoX**: Direct text-to-video (49 frames, 8 fps)
- **IP-Adapter**: Style-consistent generation
- **FILM**: Keyframe interpolation

## Hardware Requirements

- **GPU**: NVIDIA RTX 5060 Ti 16GB (Blackwell architecture)
- **CUDA**: 12.8+
- **VRAM**: 
  - SDXL: ~6 GB
  - SVD: ~10 GB
  - CogVideoX: ~12 GB

## Video Categories

| Category | Duration | Style | FPS |
|----------|----------|-------|-----|
| breaking_news | 30-60s | documentary | 30 |
| documentary | 2-5min | cinematic | 24 |
| analysis | 1-3min | technical | 30 |
| briefing | 30-90s | professional | 30 |
| feature | 3-10min | narrative | 24 |
| report | 1-2min | news | 30 |
| update | 15-45s | quick | 30 |

## Usage

### Start Video Pipeline

```batch
cd Q:\oroboros-core\WORLDFEED-NEWS
start-video-pipeline.bat
```

### Generate Single Video

```python
from precogs.video_diffusion_pipeline import VideoDiffusionPipeline

pipeline = VideoDiffusionPipeline()
result = pipeline.generate_video(
    prompt="AI breakthrough in quantum computing",
    source="breaking_news",
    category="breaking_news"
)
```

### Batch Generation

```python
prompts = [
    {"prompt": "Climate summit results", "source": "breaking_news", "category": "report"},
    {"prompt": "Tech innovation analysis", "source": "anthropic", "category": "analysis"},
    {"prompt": "Economic forum highlights", "source": "glasswing", "category": "briefing"}
]

results = pipeline.batch_generate(prompts)
```

### Integration with Precog Engine

The video diffusion pipeline is automatically integrated with `precog_engine.py`:

```python
from precogs.precog_engine import PrecogEngine

engine = PrecogEngine()
engine.run_cycle()  # Automatically uses video diffusion pipeline
```

## Output Structure

```
Q:\video-production-pipeline\
├── output/
│   └── {job_id}/
│       ├── video.mp4
│       └── thumbnail.png
├── jobs/
│   └── {job_id}.json
└── cache/
    └── step_*.json
```

## Video Metadata

Each generated video includes:

```json
{
  "id": "2d2d6f59b637",
  "type": "video",
  "title": "Video: Breaking News Title",
  "description": "Video coverage: ...",
  "thumbnail_url": "https://.../thumbnail.png",
  "video_url": "https://.../video.mp4",
  "duration": 479,
  "category": "breaking_news",
  "confidence": 0.97,
  "resonance": 1272.0,
  "strata": "S12",
  "timestamp": "2026-06-26T00:18:17.571213",
  "source": "anthropic_report",
  "video_validated": true,
  "status": "completed"
}
```

## Fallback Mode

When the diffusion pipeline is unavailable (no GPU, missing dependencies), the system automatically falls back to placeholder mode:

- Generates metadata only
- Uses Unsplash thumbnails
- Marks videos as `video_validated: false`
- Shows poster-only in DIP feed

## Configuration

Edit `Q:\video-production-pipeline\pipeline\config.json`:

```json
{
  "pipeline": "Oroboros Video Diffusion Pipeline",
  "version": "3.0.0-optimized",
  "hardware": {
    "gpu": "NVIDIA GeForce RTX 5060 Ti",
    "vram": "16 GB GDDR7"
  },
  "models": {
    "generation": { "sdxl": {...} },
    "video": { "svd": {...}, "cogvideox": {...} }
  }
}
```

## Troubleshooting

### No GPU Detected

```batch
nvidia-smi
# If error, install NVIDIA drivers
```

### CUDA Out of Memory

```python
# Reduce batch size or use fp16
pipeline.config['precision'] = 'fp16'
```

### Import Errors

```batch
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
pip install diffusers transformers accelerate safetensors
```

## Resonance

All videos are generated at **1272 Hz** resonance frequency, aligned with the Oroboros Strata S1-S12 framework.

## UEE Standard

Videos follow **UEE-2024** (Unified Encoding Standard) for metadata and format consistency.

---

**Oroboros Labs** | WorldFeed News | 1272 Hz