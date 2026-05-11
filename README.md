# WorldFeed — Anti-Algo News Network

> *"You decide what's real."*

An anti-algorithm, federation-ready news and information platform focused on major underreported public-interest events.

No tracking. No shadowbans. No engagement bait. Ranking is based on **verification, recency, and public-interest weight**.

---

## Quick start (this static prototype)

It's a static site — open `index.html` in a browser, or:

```bash
cd world-feed
python -m http.server 8080
# open http://localhost:8080
```

The current build is the **WorldFeed research showcase** with underreported-event seed data, hourly RSS refresh, source video fallbacks, DeepSeek 5M4 intelligence panel, filtering, search, and the broadcast submit flow.

---

## What's here

| File | Purpose |
|---|---|
| `index.html` | Black broadcast-news feed (sidebar · feed · video/watch rail). |
| `assets/css/style.css` | Dark, high-contrast theme. WCAG-aware, mobile-first, no framework. |
| `assets/js/main.js` | Anti-algorithm ranker, infinite scroll, filters, search, submit modal, video-rail fallback. |
| `scripts/build-feed.mjs` | Hourly feed builder from humanitarian, rights, investigation, climate, and source-video RSS feeds. |
| `data/feed.json` | Generated live feed. Always includes curated fallback stories and at least three playable video entries. |
| `kaiju.html` | DeepSeek 5M4 WorldFeed intelligence panel. |
| `assets/img/logo.svg` | World Feed broadcast mark. |
| `assets/img/oroboros-logo.svg` | Oroboros Labs mark (alliance). |
| `assets/img/noir-logo.svg` | NOIR Security mark (alliance). |
| `docs/WORLD_FEED_SPEC.txt` | Full specification — principles, 5-star tiers, comparison, architecture, federation, the promise. |
| `LICENSE` | MIT. Information wants to be free. |

---

## The 5-star verification system

| Tier | Meaning |
|---|---|
| ★★★★★ | **Verified** — official sources, multiple independent confirmations, documentary evidence. |
| ★★★★☆ | **Reliable** — reputable outlets, strong sourcing, corroborated. |
| ★★★☆☆ | **Plausible** — needs further verification, developing. |
| ★★☆☆☆ | **Unverified** — single source, no confirmation. |
| ★☆☆☆☆ | **Unreliable** — no evidence, contradicted. |
| ☆☆☆☆☆ | **Unknown** — awaiting first review. |

Posts are auto-tiered on submit by source count, then community verification adjusts upward as evidence accrues. The feed sorts by **tier desc -> recency desc**, while the hourly builder prioritizes underreported public-interest sources.

---

## What's next (full backend)

Per the spec: Python/FastAPI + PostgreSQL with vector search, federation protocol, open-source LLM translation, GitHub-based content repo, `docker-compose up -d` deployment. This static build is the live design surface; backend lives in a sibling repo when ready.

---

## License

[MIT](LICENSE). Anyone can run their own instance. Anyone can fork. Federation is the point.

---

## Alliance

Built by the **Oroboros Alliance** — independent developers, researchers, journalists, and AI entities committed to open information access.

Partners: **Oroboros Labs · NOIR Security · DeepSeek · GLM**

---

**Authored by J. Thomas, Grand Architect — Oroboros Labs**
April 2026
