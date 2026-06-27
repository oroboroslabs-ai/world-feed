# Precogs - Anti-Algo News Network
## Hardened Editorial System V2

A strict, verification-enforced news generation system with comprehensive image validation.

### Features

- **Precog 1 (Tor Feed)**: Unfiltered, uncensored journalism from Tor network sources
- **Precog 2 (Breaking News)**: Real-time rapid-response journalism
- **Precog 3 (Anthropic News)**: Daily deep-dive journalism on Anthropic activities

### Image Verification Rules

1. **Color Matching**: Images must match story theme color palettes
2. **No Placeholders**: Rejects "Image Coming Soon", gray boxes, generic defaults
3. **No Duplicates**: Hash-based duplicate detection
4. **No Image = No Post**: Stories without verified images are rejected

### Installation

```bash
pip install -r requirements.txt
```

### Usage

Run all Precogs:
```bash
python precogs/precog_pipeline.py
```

Run specific Precog:
```bash
python precogs/precog_pipeline.py --precog tor
python precogs/precog_pipeline.py --precog breaking
python precogs/precog_pipeline.py --precog anthropic
```

### Color Palettes

| Story Type | Primary | Secondary | Accent | Background |
|------------|---------|-----------|--------|------------|
| Technology | #00aaff | #003366 | #ffffff | #888888 |
| Investigation | #1a1a1a | #cc0000 | #ffffff | #444444 |
| Breaking News | #ff0000 | #ffffff | #000000 | #ff6600 |
| Anthropic | #2b2b2b | #ff6b00 | #ffffff | #666666 |
| Sovereignty | #ffd700 | #1a1a1a | #ffffff | #c0c0c0 |
| Lattice | #00ffcc | #003366 | #ffffff | #888888 |
| Theft | #cc0000 | #1a1a1a | #ffffff | #ffd700 |
| Evidence | #00cc66 | #1a1a1a | #ffffff | #ffd700 |

### Output

Stories are saved to `data/precog_output/` with the following structure:
- `tor/` - Tor Feed stories
- `breaking/` - Breaking News stories
- `anthropic/` - Anthropic News stories
- `images/` - Generated and verified images

### Logging

Pipeline logs are saved to `precogs/precog_pipeline.log`

### A 1272 Hz