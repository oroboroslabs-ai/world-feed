// WorldFeed RSS/video builder. Runs hourly via GitHub Actions.
// Focus: underreported public-interest events, reliable source video, no blank rail.

import { writeFileSync, mkdirSync } from 'node:fs';

const SOURCES = [
  // Primary and humanitarian wires
  { name: 'UN News', url: 'https://news.un.org/feed/subscribe/en/news/all/rss.xml', tier: 5, kind: 'text', primary: true },
  { name: 'WHO', url: 'https://www.who.int/rss-feeds/news-english.xml', tier: 5, kind: 'text', primary: true },
  { name: 'The New Humanitarian', url: 'https://www.thenewhumanitarian.org/rss.xml', tier: 5, kind: 'text' },
  { name: 'OHCHR', url: 'https://www.ohchr.org/en/rss.xml', tier: 5, kind: 'text', primary: true },
  { name: 'Human Rights Watch', url: 'https://www.hrw.org/rss/news', tier: 4, kind: 'text' },
  { name: 'MSF', url: 'https://www.msf.org/rss/all', tier: 4, kind: 'text' },
  { name: 'Bellingcat', url: 'https://www.bellingcat.com/feed/', tier: 4, kind: 'text' },
  { name: 'ICIJ', url: 'https://www.icij.org/feed/', tier: 4, kind: 'text' },
  { name: 'Mongabay', url: 'https://news.mongabay.com/feed/', tier: 4, kind: 'text' },
  { name: 'Inside Climate News', url: 'https://insideclimatenews.org/feed/', tier: 4, kind: 'text' },
  { name: 'Rest of World', url: 'https://restofworld.org/feed/latest/', tier: 4, kind: 'text' },
  { name: 'Al Jazeera', url: 'https://www.aljazeera.com/xml/rss/all.xml', tier: 4, kind: 'text' },
  { name: 'Guardian Global Development', url: 'https://www.theguardian.com/global-development/rss', tier: 4, kind: 'text' },

  // Video backbones. These make the right rail resilient even when text feeds are quiet.
  { name: 'United Nations (video)', url: 'https://www.youtube.com/feeds/videos.xml?channel_id=UC5O114-PQNYkurlTg6hekZw', tier: 5, kind: 'video', primary: true },
  { name: 'Al Jazeera English (video)', url: 'https://www.youtube.com/feeds/videos.xml?channel_id=UCNye-wNBqNL5ZzHSJj3l8Bg', tier: 4, kind: 'video' },
  { name: 'Reuters (video)', url: 'https://www.youtube.com/feeds/videos.xml?channel_id=UChqUTb7kYRX8-EiaN3XFrSQ', tier: 4, kind: 'video' },
  { name: 'DW News (video)', url: 'https://www.youtube.com/feeds/videos.xml?channel_id=UCknLrEdhRCp1aegoMqRaCZg', tier: 4, kind: 'video' },
  { name: 'AP (video)', url: 'https://www.youtube.com/feeds/videos.xml?channel_id=UC52X5wxOL_s5yw0dQk7NtgA', tier: 4, kind: 'video' },
  { name: 'WHO (video)', url: 'https://www.youtube.com/feeds/videos.xml?channel_id=UC07-dOwgza1IguKA86jqxNA', tier: 5, kind: 'video', primary: true }
];

const CURATED_ITEMS = [
  {
    id: 'sudan-health-crisis',
    tier: 5,
    cats: ['new', 'verified', 'developing'],
    title: "Sudan's war enters a fourth year with the world's largest humanitarian crisis still underfunded",
    body: 'WHO reports 34 million people needing aid in Sudan, 21 million lacking health services, repeated attacks on health care, and disease outbreaks across multiple states.',
    summary: 'Sudan remains the largest humanitarian and health crisis in the world.',
    sources: ['WHO', 'IPC', 'UN agencies'],
    type: 'document',
    minutesAgo: 12,
    location: 'Sudan',
    imageUrl: 'https://images.unsplash.com/photo-1521295121783-8a321d551ad2?auto=format&fit=crop&w=1200&q=80',
    videoUrl: '',
    link: 'https://www.who.int/news/item/14-04-2026-after-three-years-of-conflict--sudan-faces-a-deeper-health-crisis',
    hasFullText: false
  },
  {
    id: 'myanmar-2026-needs',
    tier: 5,
    cats: ['verified', 'docs'],
    title: 'Myanmar 2026 humanitarian plan warns 16 million people need life-saving assistance',
    body: 'The UN in Myanmar says conflict, disaster, displacement, and economic collapse continue to compound needs. Humanitarians warn that Myanmar remains dire and under-funded.',
    summary: 'Myanmar needs are rising while funding is narrowing.',
    sources: ['UN Myanmar', 'OCHA', '2026 HNRP'],
    type: 'document',
    minutesAgo: 38,
    location: 'Myanmar',
    imageUrl: 'https://images.unsplash.com/photo-1517148815978-75f6acaaf32c?auto=format&fit=crop&w=1200&q=80',
    videoUrl: '',
    link: 'https://myanmar.un.org/en/306830-conflict-fuels-suffering-myanmar-un-publishes-humanitarian-report-forecasting-most-urgent',
    hasFullText: false
  },
  {
    id: 'haiti-access-crisis',
    tier: 5,
    cats: ['new', 'verified', 'developing'],
    title: 'Haiti access crisis keeps aid, food, health, water, and education under severe pressure',
    body: 'UN reporting says armed groups control large parts of Port-au-Prince, more than 1.4 million people have fled their homes, and six million people need some form of humanitarian assistance in 2026.',
    summary: 'Haiti remains overlooked and badly underfunded.',
    sources: ['UN Geneva', 'OCHA', 'IOM', 'WFP'],
    type: 'story',
    minutesAgo: 55,
    location: 'Haiti',
    imageUrl: 'https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=1200&q=80',
    videoUrl: '',
    link: 'https://www.ungeneva.org/en/news-media/news/2026/02/115602/keeping-hope-alive-younger-generations-haiti-funding-falters',
    hasFullText: false
  },
  {
    id: 'global-food-crises-2026',
    tier: 5,
    cats: ['verified', 'docs'],
    title: 'Global Report on Food Crises 2026: acute hunger remains entrenched across protracted crises',
    body: 'The 2026 GRFC reports severe food insecurity concentrated in protracted crisis contexts, with conflict as the main driver and malnutrition still critical.',
    summary: 'Food-system data belongs on the front page.',
    sources: ['FAO', 'WFP', 'GNAFC', 'FSIN'],
    type: 'document',
    minutesAgo: 72,
    location: 'global',
    imageUrl: 'https://images.unsplash.com/photo-1509099836639-18ba1795216d?auto=format&fit=crop&w=1200&q=80',
    videoUrl: '',
    link: 'https://www.preventionweb.net/publication/documents-and-publications/2026-global-report-food-crises',
    hasFullText: false
  },
  {
    id: 'wfp-global-outlook',
    tier: 5,
    cats: ['verified', 'docs'],
    title: 'WFP 2026 outlook: acute hunger remains double pre-pandemic levels',
    body: 'WFP estimates 318 million people face acute hunger in 2026, with 41 million at Emergency levels or worse. Conflict, climate shocks, and funding shortfalls keep the pressure high.',
    summary: 'Conflict and climate shocks compound hunger.',
    sources: ['World Food Programme'],
    type: 'document',
    minutesAgo: 96,
    location: 'global',
    imageUrl: 'https://images.unsplash.com/photo-1464226184884-fa280b87c399?auto=format&fit=crop&w=1200&q=80',
    videoUrl: '',
    link: 'https://www.wfp.org/publications/wfp-global-outlook',
    hasFullText: false
  }
];

const FALLBACK_VIDEOS = [
  {
    id: 'video-un-car',
    tier: 4,
    cats: ['new', 'video', 'developing'],
    title: 'UN field briefing: Central African Republic remains fragile but hopeful',
    body: 'Reliable video fallback from the United Nations channel.',
    summary: 'UN field briefing source video.',
    sources: ['United Nations video'],
    type: 'video',
    minutesAgo: 90,
    location: 'UN video',
    imageUrl: 'https://img.youtube.com/vi/MleE9I3rjGUo/hqdefault.jpg',
    videoUrl: 'https://www.youtube.com/watch?v=MleE9I3rjGUo',
    link: 'https://www.youtube.com/watch?v=MleE9I3rjGUo',
    hasFullText: false
  },
  {
    id: 'video-un-briefing',
    tier: 4,
    cats: ['video', 'verified'],
    title: 'UN daily briefing tracks Lebanon, health alerts, and overlooked field updates',
    body: 'Daily UN briefings are a reliable backstop for the video pipeline.',
    summary: 'UN daily briefing source video.',
    sources: ['United Nations video'],
    type: 'video',
    minutesAgo: 140,
    location: 'UN briefing',
    imageUrl: 'https://img.youtube.com/vi/B9ui_khfryo/hqdefault.jpg',
    videoUrl: 'https://www.youtube.com/watch?v=B9ui_khfryo',
    link: 'https://www.youtube.com/watch?v=B9ui_khfryo',
    hasFullText: false
  },
  {
    id: 'video-aj-energy',
    tier: 4,
    cats: ['video', 'docs'],
    title: 'Source video: energy dependency and infrastructure risk in the United States',
    body: 'Public-interest source video from Al Jazeera English.',
    summary: 'Infrastructure risk source video.',
    sources: ['Al Jazeera English video'],
    type: 'video',
    minutesAgo: 180,
    location: 'video source',
    imageUrl: 'https://img.youtube.com/vi/fEwr_u_TRAI/hqdefault.jpg',
    videoUrl: 'https://www.youtube.com/watch?v=fEwr_u_TRAI',
    link: 'https://www.youtube.com/watch?v=fEwr_u_TRAI',
    hasFullText: false
  }
];

const UNDERREPORTED_RE = /\b(sudan|myanmar|haiti|congo|drc|yemen|sahel|somalia|ethiopia|afghanistan|mali|burkina|niger|chad|gaza|lebanon|central african republic|car\b|refugee|displacement|displaced|famine|hunger|malnutrition|food insecurity|cholera|measles|outbreak|water|sanitation|humanitarian|aid|relief|rights|war crimes|investigation|corruption|climate|drought|flood|forest|indigenous|migration|supply chain|infrastructure|blackout)\b/i;
const DOCUMENT_RE = /\b(report|study|paper|filing|document|dataset|appeal|outlook|response plan|briefing|investigation)\b/i;
const LOW_VALUE_RE = /\b(celebrity|red carpet|box office|trailer|fashion|gaming|sport|football|soccer|nba|nfl|mlb)\b/i;

async function fetchRSS(src, timeoutMs = 12000) {
  try {
    const ctrl = new AbortController();
    const t = setTimeout(() => ctrl.abort(), timeoutMs);
    const res = await fetch(src.url, {
      signal: ctrl.signal,
      headers: { 'User-Agent': 'WorldFeed-bot/3.0 (+https://oroboroslabs-ai.github.io/world-feed/)' }
    });
    clearTimeout(t);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const xml = await res.text();
    return parseRSS(xml, src);
  } catch (e) {
    console.error(`[skip] ${src.name}: ${e.message}`);
    return [];
  }
}

function parseRSS(xml, src) {
  const items = [];
  const blocks = xml.match(/<item[\s\S]*?<\/item>/g) || xml.match(/<entry[\s\S]*?<\/entry>/g) || [];
  for (const b of blocks.slice(0, 12)) {
    const title = pick(b, 'title');
    const desc = pick(b, 'description') || pick(b, 'summary') || pick(b, 'content') || pick(b, 'media:description');
    const link = pickLink(b);
    const pub = pick(b, 'pubDate') || pick(b, 'published') || pick(b, 'updated') || pick(b, 'dc:date');
    const img = extractImage(b) || youtubeThumb(link);
    const vid = extractVideo(b) || (src.kind === 'video' ? link : '');
    if (!title) continue;
    items.push({
      title: title.slice(0, 220),
      body: (desc || '').slice(0, 520),
      link,
      pub,
      source: src.name,
      tier: src.tier,
      imageUrl: img,
      videoUrl: vid,
      sourceKind: src.kind || 'text',
      primary: !!src.primary
    });
  }
  return items;
}

function pick(block, tag) {
  const re = new RegExp(`<${tag}[^>]*>([\\s\\S]*?)<\\/${tag}>`, 'i');
  const m = block.match(re);
  return m ? cleanText(m[1]) : '';
}

function pickLink(block) {
  const m1 = block.match(/<link[^>]*>([^<]+)<\/link>/i);
  if (m1 && m1[1].trim()) return cleanUrl(m1[1]);
  const m2 = block.match(/<link[^>]*href=["']([^"']+)["']/i);
  return m2 ? cleanUrl(m2[1]) : '';
}

function extractImage(block) {
  const patterns = [
    /<media:content[^>]*medium=["']image["'][^>]*url=["']([^"']+)["']/i,
    /<media:content[^>]*url=["']([^"']+\.(?:jpg|jpeg|png|webp|avif)[^"']*)["']/i,
    /<media:thumbnail[^>]*url=["']([^"']+)["']/i,
    /<enclosure[^>]*url=["']([^"']+)["'][^>]*type=["']image\//i,
    /<enclosure[^>]*type=["']image\/[^"']+["'][^>]*url=["']([^"']+)["']/i,
    /<itunes:image[^>]*href=["']([^"']+)["']/i,
    /<image>\s*<url>([^<]+)<\/url>/i,
    /<img[^>]*src=["']([^"']+)["']/i,
    /url=["'](https?:[^"']+\.(?:jpg|jpeg|png|webp|avif)[^"']*)["']/i
  ];
  for (const p of patterns) {
    const m = block.match(p);
    if (m && m[1]) return cleanUrl(m[1]);
  }
  return '';
}

function extractVideo(block) {
  const explicit = [
    /<media:content[^>]*medium=["']video["'][^>]*url=["']([^"']+)["']/i,
    /<media:content[^>]*url=["']([^"']+)["'][^>]*medium=["']video["']/i,
    /<enclosure[^>]*url=["']([^"']+)["'][^>]*type=["']video\//i,
    /<enclosure[^>]*type=["']video\/[^"']+["'][^>]*url=["']([^"']+)["']/i
  ];
  for (const p of explicit) {
    const m = block.match(p);
    if (m && m[1]) return cleanUrl(m[1]);
  }
  const services = [
    /(https?:\/\/(?:www\.)?youtube\.com\/watch\?[^"'\s<>]*v=[a-zA-Z0-9_-]{11}[^"'\s<>]*)/i,
    /(https?:\/\/(?:www\.)?youtube\.com\/(?:embed|shorts)\/[a-zA-Z0-9_-]{11})/i,
    /(https?:\/\/youtu\.be\/[a-zA-Z0-9_-]{11})/i,
    /(https?:\/\/(?:www\.|player\.)?vimeo\.com\/(?:video\/)?\d+)/i,
    /(https?:\/\/(?:www\.)?tiktok\.com\/[^"'\s<>]+\/video\/\d+)/i,
    /(https?:\/\/(?:twitter\.com|x\.com)\/[^/\s"']+\/status\/\d+)/i
  ];
  for (const p of services) {
    const m = block.match(p);
    if (m && m[1]) return cleanUrl(m[1]);
  }
  const iframe = block.match(/<iframe[^>]*src=["']([^"']+)["']/i);
  if (iframe && /youtube\.com\/embed|player\.vimeo\.com|tiktok\.com\/embed|platform\.twitter\.com\/embed/i.test(iframe[1])) {
    return cleanUrl(iframe[1]);
  }
  return '';
}

function youtubeThumb(url) {
  const id = youtubeId(url || '');
  return id ? `https://img.youtube.com/vi/${id}/hqdefault.jpg` : '';
}

function youtubeId(url) {
  const m = String(url).match(/(?:youtube\.com\/(?:watch\?[^#\s]*v=|shorts\/|embed\/)|youtu\.be\/)([a-zA-Z0-9_-]{11})/);
  return m ? m[1] : '';
}

function cleanUrl(s) {
  return String(s || '').replace(/&amp;/g, '&').trim();
}

function cleanText(s) {
  return String(s || '')
    .replace(/<!\[CDATA\[([\s\S]*?)\]\]>/g, '$1')
    .replace(/<[^>]*>/g, '')
    .replace(/&#x([0-9a-f]+);/gi, (_, n) => String.fromCodePoint(parseInt(n, 16)))
    .replace(/&#(\d+);/g, (_, n) => String.fromCodePoint(parseInt(n, 10)))
    .replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"').replace(/&apos;/g, "'").replace(/&nbsp;/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

function categorize(item, minutesAgo) {
  const cats = [];
  const text = `${item.title} ${item.body}`;
  if (minutesAgo <= 180) cats.push('new');
  if (UNDERREPORTED_RE.test(text)) cats.push('developing');
  if (DOCUMENT_RE.test(text)) cats.push('docs');
  if (item.sourceKind === 'video' || item.videoUrl) cats.push('video');
  return [...new Set(cats)];
}

function classifyType(item) {
  if (item.sourceKind === 'video' || item.videoUrl) return 'video';
  if (DOCUMENT_RE.test(item.title + ' ' + item.body)) return 'document';
  if (item.imageUrl) return 'image';
  return 'story';
}

function impactScore(item) {
  const text = `${item.title} ${item.body}`;
  let score = item.tier * 10;
  if (item.primary) score += 12;
  if (UNDERREPORTED_RE.test(text)) score += 28;
  if (DOCUMENT_RE.test(text)) score += 8;
  if (item.sourceKind === 'video' || item.videoUrl) score += 12;
  if (LOW_VALUE_RE.test(text)) score -= 20;
  const pubMs = item.pub ? new Date(item.pub).getTime() : 0;
  if (pubMs) {
    const hours = Math.max(0, (Date.now() - pubMs) / 36e5);
    score += Math.max(0, 10 - Math.min(10, hours / 24));
  }
  return score;
}

function toFeedItem(it, now = Date.now()) {
  const pubMs = it.pub ? new Date(it.pub).getTime() : now;
  const minutesAgo = Math.max(0, Math.round((now - pubMs) / 60000));
  return {
    id: it.id || stableId(it.title),
    tier: it.tier,
    cats: it.cats || categorize(it, minutesAgo),
    title: it.title,
    body: it.fullContent || it.body || it.summary || '',
    summary: it.summary || it.body || '',
    sources: it.sources || [it.source],
    type: it.type || classifyType(it),
    minutesAgo: Number.isFinite(it.minutesAgo) ? it.minutesAgo : minutesAgo,
    location: it.location || 'wire',
    imageUrl: it.imageUrl || youtubeThumb(it.videoUrl || it.link) || '',
    videoUrl: it.videoUrl || '',
    link: it.link || it.videoUrl || '',
    hasFullText: !!it.fullContent || !!it.hasFullText
  };
}

function stableId(title) {
  return String(title || 'item').toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '').slice(0, 80);
}

async function fetchFullText(url, timeoutMs = 9000) {
  if (!url || !/^https?:/.test(url) || /youtube\.com|youtu\.be|vimeo\.com|tiktok\.com/.test(url)) return '';
  try {
    const ctrl = new AbortController();
    const t = setTimeout(() => ctrl.abort(), timeoutMs);
    const res = await fetch('https://r.jina.ai/' + url, {
      signal: ctrl.signal,
      headers: { 'User-Agent': 'WorldFeed-bot/3.0', 'X-Return-Format': 'markdown' }
    });
    clearTimeout(t);
    if (!res.ok) return '';
    let md = await res.text();
    md = md.replace(/^Title:[^\n]*\n/m, '')
      .replace(/^URL Source:[^\n]*\n/m, '')
      .replace(/^Markdown Content:\s*\n?/m, '')
      .replace(/^Warning:[^\n]*\n/gm, '')
      .replace(/!\[\]\([^)]*\)/g, '')
      .replace(/\[!\[[^\]]*\]\([^)]*\)\]\([^)]*\)/g, '')
      .trim();
    if (/(Just a moment|Are you a robot|Verify you are human|Cloudflare Ray ID|Access Denied)/i.test(md.slice(0, 600))) return '';
    if (md.length < 160) return '';
    return md.slice(0, 4200);
  } catch (_) {
    return '';
  }
}

async function withConcurrency(items, limit, fn) {
  let i = 0;
  await Promise.all(Array.from({ length: limit }, async () => {
    while (i < items.length) {
      const idx = i++;
      try { await fn(items[idx], idx); } catch (_) {}
    }
  }));
}

function dedupe(items) {
  const seen = new Set();
  const out = [];
  for (const item of items) {
    if (!item || !item.title) continue;
    const key = (item.link || item.videoUrl || item.title).toLowerCase().replace(/\?.*$/, '');
    if (seen.has(key)) continue;
    seen.add(key);
    out.push(item);
  }
  return out;
}

function ensureVideoCoverage(items) {
  const out = dedupe(items);
  const videos = out.filter(i => i.type === 'video' || i.videoUrl);
  for (const fallback of FALLBACK_VIDEOS) {
    if (videos.length >= 3) break;
    out.push(fallback);
    videos.push(fallback);
  }
  return dedupe(out);
}

async function main() {
  const raw = [];
  await Promise.all(SOURCES.map(async (s) => {
    raw.push(...await fetchRSS(s));
  }));

  const uniqueRaw = dedupe(raw).sort((a, b) => impactScore(b) - impactScore(a));
  const textTop = uniqueRaw
    .filter(i => i.sourceKind !== 'video' && UNDERREPORTED_RE.test(`${i.title} ${i.body}`))
    .slice(0, 18);

  console.log(`Fetched ${raw.length} raw items; enriching ${textTop.length} text items.`);
  await withConcurrency(textTop, 3, async (it) => {
    const full = await fetchFullText(it.link);
    if (full && full.length > (it.body || '').length) it.fullContent = full;
  });

  const now = Date.now();
  const fetched = uniqueRaw
    .filter(i => impactScore(i) >= 35)
    .slice(0, 70)
    .map(i => toFeedItem(i, now));

  const curated = [...CURATED_ITEMS, ...FALLBACK_VIDEOS].map(i => ({ ...i }));
  const items = ensureVideoCoverage([...curated, ...fetched])
    .sort((a, b) => {
      if ((b.tier || 0) !== (a.tier || 0)) return (b.tier || 0) - (a.tier || 0);
      return (a.minutesAgo || 0) - (b.minutesAgo || 0);
    })
    .slice(0, 80);

  const out = {
    updatedAt: new Date().toISOString(),
    sourcesTried: SOURCES.length,
    itemCount: items.length,
    videoCount: items.filter(i => i.type === 'video' || i.videoUrl).length,
    focus: 'underreported-public-interest',
    items
  };

  mkdirSync('data', { recursive: true });
  writeFileSync('data/feed.json', JSON.stringify(out, null, 2));
  console.log(`Wrote ${items.length} items (${out.videoCount} videos) at ${out.updatedAt}`);
}

main().catch((e) => {
  console.error('build-feed failed:', e);
  const out = {
    updatedAt: new Date().toISOString(),
    sourcesTried: SOURCES.length,
    itemCount: CURATED_ITEMS.length + FALLBACK_VIDEOS.length,
    videoCount: FALLBACK_VIDEOS.length,
    focus: 'curated-fallback',
    items: [...CURATED_ITEMS, ...FALLBACK_VIDEOS]
  };
  mkdirSync('data', { recursive: true });
  writeFileSync('data/feed.json', JSON.stringify(out, null, 2));
  process.exit(0);
});
