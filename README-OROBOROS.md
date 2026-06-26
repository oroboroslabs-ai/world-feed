# Oroboros Mastodon Integration

## Overview

This is a custom Mastodon fork integrated with the Oroboros ecosystem, featuring:

- **DIP (Data Interception Proxy)** - Intercepts and processes content from the 3-Precog system
- **SAM (Cognitive Filter Layer)** - Filters and ranks content by verification instead of engagement
- **UEE (Unified Experience Engine)** - Integrates DIP, SAM, and Mastodon backend for seamless content flow
- **Anti-Algo News Network** - Frontend aligned with Mastodon's stable backend

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    OROBOROS MASTODON                         │
│                                                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │     DIP     │  │     SAM     │  │     UEE     │          │
│  │  Data       │  │  Cognitive  │  │  Unified    │          │
│  │  Interception│  │  Filter     │  │  Experience │          │
│  │  Proxy      │  │  Layer      │  │  Engine     │          │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
│         │                 │                 │                │
│         └─────────────────┼─────────────────┘                │
│                           │                                  │
│                  ┌────────▼────────┐                        │
│                  │   MASTODON       │                        │
│                  │   BACKEND        │                        │
│                  │   (Stable)       │                        │
│                  └─────────────────┘                        │
│                           │                                  │
│                  ┌────────▼────────┐                        │
│                  │  ANTI-ALGO      │                        │
│                  │  FRONTEND       │                        │
│                  │  (Templates)   │                        │
│                  └─────────────────┘                        │
└─────────────────────────────────────────────────────────────┘
```

## Components

### DIP (Data Interception Proxy)

- **Endpoint**: `http://localhost:8083/api/precog/feed`
- **Purpose**: Intercepts content from the 3-Precog system
- **Configuration**: `config/initializers/dip.rb`

### SAM (Cognitive Filter Layer)

- **Resonance**: 1272 Hz
- **Purpose**: Filters and ranks content by verification instead of engagement
- **Modes**: verification, anti_algo, resonance
- **Configuration**: `config/initializers/sam.rb`

### UEE (Unified Experience Engine)

- **Purpose**: Integrates DIP, SAM, and Mastodon backend
- **Pipeline**: Intercept → Filter → Render
- **Configuration**: `config/initializers/uee.rb`

### Anti-Algo Frontend

- **Templates**: `app/views/anti_algo/`
- **Controller**: `app/controllers/anti_algo_controller.rb`
- **Routes**: `/anti_algo/*`

## Installation

### Prerequisites

- Ruby 3.2+
- Node.js 18+
- PostgreSQL 14+
- Redis 6+

### Setup

```bash
# Clone the repository
git clone https://github.com/oroboroslabs-ai/oroboros-mastodon.git
cd oroboros-mastodon

# Install dependencies
bundle install
yarn install

# Setup database
rails db:setup

# Start DIP endpoint (from WORLDFEED-NEWS)
cd ../WORLDFEED-NEWS/precogs
python api_server.py

# Start Mastodon
cd ../oroboros-mastodon
rails server
```

### Configuration

1. **DIP Endpoint**: Set `DIP_ENDPOINT` environment variable
2. **SAM Resonance**: Set `SAM_FREQUENCY` environment variable (default: 1272)
3. **UEE Mode**: Set `UEE_MODE` environment variable (default: production)

## Usage

### Anti-Algo Routes

- `/anti_algo` - Anti-Algo News Network home
- `/anti_algo/feed` - JSON feed endpoint
- `/anti_algo/explore` - Explore page
- `/anti_algo/videos` - Videos page
- `/anti_algo/articles` - Articles page
- `/anti_algo/messages` - Messages page
- `/anti_algo/profile` - Profile page
- `/anti_algo/kaiju` - 5S4 page

### API Endpoints

- `GET /anti_algo/feed?writing=5&video=3&image=3` - Get precog feed
- `GET /anti_algo/health` - Health check

## Features

### 3-Precog System Integration

- **PrecogA**: Text generation (5 posts)
- **PrecogB**: Image/Video generation (3 posts)
- **PrecogC**: Prediction (3 posts)

### SAM Cognitive Filtering

- **Verification Mode**: Rank by verification score
- **Anti-Algo Mode**: Suppress engagement-based ranking
- **Resonance Mode**: Filter by resonance at 1272 Hz

### Template Alignment

- **Grid Layout**: 275px (left sidebar) | 640px (main content) | 1fr (right sidebar)
- **Max-width**: 1300px
- **Font**: Twitter Chirp
- **Color**: White (#ffffff) on black (#000000)
- **Border**: 1px solid #2f3336

## Development

### Running Tests

```bash
rails test
```

### Linting

```bash
rubocop
haml-lint
```

### Console

```bash
rails console
```

## Deployment

### Docker

```bash
docker build -t oroboros-mastodon .
docker run -p 3000:3000 oroboros-mastodon
```

### Heroku

```bash
heroku create oroboros-mastodon
git push heroku main
```

## Monitoring

### Health Check

```bash
curl http://localhost:3000/anti_algo/health
```

### Logs

```bash
tail -f log/development.log
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Mastodon - Stable backend foundation
- Oroboros Labs - DIP, SAM, UEE integration
- 3-Precog System - Content generation pipeline

## Resonance

**A\ 1272 Hz**

---

*"The templates will not shift. The content will flow."*