// WorldFeed - anti-algo news surface.
// Ranked by verification, recency, and public-interest weight. No engagement ranking.

(function () {
    'use strict';

    const FALLBACK_VIDEOS = [
        {
            id: 'video-un-car',
            tier: 4,
            cats: ['new', 'video', 'developing'],
            title: 'UN field briefing: Central African Republic remains fragile but hopeful',
            body: 'A United Nations field briefing from a crisis that rarely leads the feed. WorldFeed keeps these source videos pinned so the rail never goes blank.',
            sources: ['United Nations video'],
            type: 'video',
            minutesAgo: 90,
            location: 'UN video',
            imageUrl: 'https://img.youtube.com/vi/MleE9I3rjGUo/hqdefault.jpg',
            videoUrl: 'https://www.youtube.com/watch?v=MleE9I3rjGUo',
            link: 'https://www.youtube.com/watch?v=MleE9I3rjGUo'
        },
        {
            id: 'video-un-briefing',
            tier: 4,
            cats: ['video', 'verified'],
            title: 'UN daily briefing tracks Lebanon, health alerts, and overlooked field updates',
            body: 'Daily UN briefings are a reliable backstop for the video pipeline when single-source embeds or RSS entries fail.',
            sources: ['United Nations video'],
            type: 'video',
            minutesAgo: 140,
            location: 'UN briefing',
            imageUrl: 'https://img.youtube.com/vi/B9ui_khfryo/hqdefault.jpg',
            videoUrl: 'https://www.youtube.com/watch?v=B9ui_khfryo',
            link: 'https://www.youtube.com/watch?v=B9ui_khfryo'
        },
        {
            id: 'video-aj-energy',
            tier: 4,
            cats: ['video', 'docs'],
            title: 'Source video: energy dependency and infrastructure risk in the United States',
            body: 'Long-form source video from Al Jazeera English. The video rail prefers public-interest feeds over entertainment clips.',
            sources: ['Al Jazeera English video'],
            type: 'video',
            minutesAgo: 180,
            location: 'video source',
            imageUrl: 'https://img.youtube.com/vi/fEwr_u_TRAI/hqdefault.jpg',
            videoUrl: 'https://www.youtube.com/watch?v=fEwr_u_TRAI',
            link: 'https://www.youtube.com/watch?v=fEwr_u_TRAI'
        }
    ];

    const SEED = [
        {
            id: 'anthropic-claude-4-sonnet',
            tier: 5,
            cats: ['new', 'verified', 'developing'],
            title: 'Claude 4 Sonnet: Anthropic releases next-generation reasoning model',
            body: 'Anthropic announces Claude 4 Sonnet with breakthrough capabilities in complex reasoning, mathematical problem-solving, and long-context understanding. The model demonstrates unprecedented performance on benchmarks requiring multi-step logical deduction.',
            sources: ['Anthropic', 'Claude.ai'],
            type: 'story',
            minutesAgo: 12,
            location: 'San Francisco',
            imageUrl: '',
            videoUrl: '',
            link: 'https://www.anthropic.com/claude-4'
        },
        {
            id: 'anthropic-constitutional-ai',
            tier: 5,
            cats: ['verified', 'docs'],
            title: 'Constitutional AI: Building safer AI systems through explicit principles',
            body: 'Anthropic\'s Constitutional AI methodology uses explicit constitutional principles to guide AI behavior, reducing harmful outputs while maintaining helpfulness. The approach represents a paradigm shift from RLHF to more transparent alignment methods.',
            sources: ['Anthropic Research', 'arXiv'],
            type: 'document',
            minutesAgo: 38,
            location: 'Research',
            imageUrl: '',
            videoUrl: '',
            link: 'https://www.anthropic.com/constitutional-ai'
        },
        {
            id: 'anthropic-safety-interpreter',
            tier: 5,
            cats: ['new', 'verified', 'developing'],
            title: 'Anthropic releases interpretability tools for understanding AI reasoning',
            body: 'New research from Anthropic introduces methods for interpreting neural network activations, allowing researchers to understand how models arrive at conclusions. The work advances AI safety by making model behavior more transparent.',
            sources: ['Anthropic Research', 'AI Safety'],
            type: 'story',
            minutesAgo: 55,
            location: 'AI Research',
            imageUrl: '',
            videoUrl: '',
            link: 'https://www.anthropic.com/research'
        },
        {
            id: 'anthropic-mechanistic-interpretability',
            tier: 5,
            cats: ['verified', 'docs'],
            title: 'Mechanistic interpretability: Opening the black box of large language models',
            body: 'Anthropic\'s mechanistic interpretability research identifies specific neural circuits responsible for behaviors like induction, copying, and factual recall. This work enables precise control over model capabilities.',
            sources: ['Anthropic', 'AI Alignment'],
            type: 'document',
            minutesAgo: 72,
            location: 'Technical',
            imageUrl: '',
            videoUrl: '',
            link: 'https://www.anthropic.com/research/mechanistic-interpretability'
        },
        {
            id: 'anthropic-long-context',
            tier: 5,
            cats: ['verified', 'docs'],
            title: 'Claude\'s 200K token context window enables new AI applications',
            body: 'Anthropic extends Claude\'s context window to 200K tokens, enabling analysis of entire codebases, long documents, and complex multi-turn conversations. The breakthrough maintains coherence across unprecedented context lengths.',
            sources: ['Anthropic', 'Developer'],
            type: 'document',
            minutesAgo: 96,
            location: 'Developer',
            imageUrl: '',
            videoUrl: '',
            link: 'https://www.anthropic.com/api'
        },
        {
            id: 'anthropic-ai-safety-research',
            tier: 4,
            cats: ['developing', 'verified'],
            title: 'Anthropic publishes research on scalable AI alignment techniques',
            body: 'New alignment research from Anthropic explores methods for ensuring AI systems remain aligned with human values as capabilities increase. The work addresses core challenges in AI safety and beneficial AI development.',
            sources: ['Anthropic Research', 'AI Safety'],
            type: 'story',
            minutesAgo: 130,
            location: 'Research',
            imageUrl: '',
            videoUrl: '',
            link: 'https://www.anthropic.com/research'
        },
        {
            id: 'anthropic-api-enterprise',
            tier: 4,
            cats: ['developing'],
            title: 'Claude for Enterprise: Anthropic launches enterprise AI platform',
            body: 'Anthropic introduces Claude for Enterprise with enhanced security features, custom deployment options, SOC 2 compliance, and enterprise-grade support. The platform targets organizations requiring robust AI infrastructure.',
            sources: ['Anthropic', 'Enterprise'],
            type: 'story',
            minutesAgo: 165,
            location: 'Business',
            imageUrl: '',
            videoUrl: '',
            link: 'https://www.anthropic.com/enterprise'
        },
        {
            id: 'anthropic-responsible-scaling',
            tier: 4,
            cats: ['developing', 'docs'],
            title: 'Responsible Scaling Policy: Anthropic\'s framework for safe AI development',
            body: 'Anthropic\'s Responsible Scaling Policy outlines safety practices for developing increasingly capable AI systems. The policy includes evaluation frameworks, deployment safeguards, and transparency commitments.',
            sources: ['Anthropic Policy'],
            type: 'story',
            minutesAgo: 210,
            location: 'Policy',
            imageUrl: '',
            videoUrl: '',
            link: 'https://www.anthropic.com/responsible-scaling'
        }
    ];

    const tierLabel = {
        5: 'VERIFIED',
        4: 'RELIABLE',
        3: 'PLAUSIBLE',
        2: 'UNVERIFIED',
        1: 'UNRELIABLE',
        0: 'UNKNOWN'
    };

    const VIDEO_PROVIDERS = [
        {
            name: 'youtube',
            re: /(?:youtube\.com\/(?:watch\?[^#\s]*v=|shorts\/|embed\/)|youtu\.be\/)([a-zA-Z0-9_-]{11})/,
            embed: id => 'https://www.youtube.com/embed/' + id,
            thumb: id => 'https://img.youtube.com/vi/' + id + '/hqdefault.jpg'
        },
        { name: 'vimeo', re: /vimeo\.com\/(?:video\/)?(\d+)/, embed: id => 'https://player.vimeo.com/video/' + id, thumb: null },
        { name: 'x', re: /(?:twitter\.com|x\.com)\/[^/]+\/status\/(\d+)/, embed: id => 'https://platform.twitter.com/embed/Tweet.html?id=' + id, thumb: null },
        { name: 'tiktok', re: /tiktok\.com\/(?:[^/]+\/video|embed\/v2)\/(\d+)/, embed: id => 'https://www.tiktok.com/embed/v2/' + id, thumb: null }
    ];
    const VIDEO_PRIORITY_RE = /\b(sudan|myanmar|haiti|congo|drc|yemen|sahel|somalia|ethiopia|afghanistan|mali|burkina|niger|chad|gaza|lebanon|central african republic|refugee|displacement|famine|hunger|malnutrition|food insecurity|cholera|outbreak|water|humanitarian|aid|rights|investigation|climate|forest|infrastructure|energy)\b/i;

    const USER_KEY = 'worldfeed-user-stories';
    const ACCOUNT_KEY = 'worldfeed-account';
    const PAGE = 8;

    let userStories = loadUserStories();
    let basePosts = ensureVideoCoverage(SEED);
    let allPosts = mergeFeeds(basePosts);
    let renderedCount = 0;
    let activeFilter = 'all';
    let activeQuery = '';
    let searchTimer;

    const feed = document.getElementById('feed');
    const loader = document.getElementById('loader');
    const filters = document.getElementById('filters');
    const search = document.getElementById('searchInput');
    const feedTitle = document.getElementById('feedTitle');

    function fmtTime(min) {
        const n = Number.isFinite(min) ? min : 0;
        if (n < 1) return 'just now';
        if (n < 60) return Math.round(n) + 'm ago';
        const h = Math.floor(n / 60);
        if (h < 24) return h + 'h ago';
        const d = Math.floor(h / 24);
        return d + 'd ago';
    }

    function escapeHtml(s) {
        const d = document.createElement('div');
        d.textContent = s == null ? '' : s;
        return d.innerHTML;
    }

    function escapeAttr(s) {
        return escapeHtml(s).replace(/"/g, '&quot;');
    }

    function detectVideo(url) {
        if (!url) return null;
        for (const p of VIDEO_PROVIDERS) {
            const m = String(url).match(p.re);
            if (m) return { provider: p.name, id: m[1], embed: p.embed(m[1]), thumb: p.thumb ? p.thumb(m[1]) : null };
        }
        return null;
    }

    function firstPlayableUrl(p) {
        if (!p) return '';
        return p.videoUrl || (/youtube\.com|youtu\.be|vimeo\.com|tiktok\.com|x\.com|twitter\.com/i.test(p.link || '') ? p.link : '');
    }

    function videoHtml(p) {
        const v = detectVideo(firstPlayableUrl(p));
        if (!v) return '';
        if (v.thumb) {
            return `<div class="post-video has-thumb" data-embed="${escapeAttr(v.embed)}" style="background-image:url('${escapeAttr(v.thumb)}');"><div class="post-play">PLAY</div><span class="post-media-tag">VIDEO - ${v.provider.toUpperCase()}</span></div>`;
        }
        return `<div class="post-video"><iframe src="${escapeAttr(v.embed)}" loading="lazy" allow="autoplay; fullscreen; encrypted-media" allowfullscreen></iframe><span class="post-media-tag">VIDEO - ${v.provider.toUpperCase()}</span></div>`;
    }

    function sourceLinkHtml(p) {
        if (!p.link) return '';
        let host = p.link;
        try { host = new URL(p.link).hostname.replace(/^www\./, ''); } catch (_) {}
        return `<a class="post-source-link" href="${escapeAttr(p.link)}" target="_blank" rel="noopener noreferrer">Read source at ${escapeHtml(host)} <span class="arrow">open</span></a>`;
    }

    function loadUserStories() {
        try { return JSON.parse(localStorage.getItem(USER_KEY) || '[]'); }
        catch (_) { return []; }
    }

    function saveUserStories(arr) {
        try { localStorage.setItem(USER_KEY, JSON.stringify(arr.slice(0, 100))); }
        catch (_) {}
    }

    function getAccount() {
        try { return JSON.parse(localStorage.getItem(ACCOUNT_KEY) || 'null'); }
        catch (_) { return null; }
    }

    function setAccount(acc) {
        if (acc) localStorage.setItem(ACCOUNT_KEY, JSON.stringify(acc));
        else localStorage.removeItem(ACCOUNT_KEY);
    }

    function isLoggedIn() {
        return !!getAccount();
    }

    function starsHtml(t) {
        const tier = Math.max(0, Math.min(5, Number(t) || 0));
        let h = '<span class="stars" aria-label="' + tier + ' of 5">';
        for (let i = 1; i <= 5; i++) h += i <= tier ? '<span class="filled">&#9733;</span>' : '<span class="empty">&#9733;</span>';
        return h + '</span><span class="tier-label tier-' + tier + '">' + tierLabel[tier] + '</span>';
    }

    function mediaHtml(p) {
        if (!p.imageUrl) return '';
        const tag = p.type === 'video' ? 'VIDEO' : 'IMAGE';
        const overlay = p.type === 'video' ? '<div class="post-play">PLAY</div>' : '';
        const safeUrl = String(p.imageUrl).replace(/"/g, '%22');
        return `<div class="post-media has-img" style="background-image:url('${escapeAttr(safeUrl)}'); background-size:cover; background-position:center;"><span class="post-media-tag">${tag}</span>${overlay}</div>`;
    }

    function bodyHtml(p) {
        const raw = String(p.body || '');
        if (!raw.trim()) return '';
        const isLong = raw.length > 720;
        const visible = isLong && !p.expanded ? raw.slice(0, 720) + '...' : raw;
        let html = escapeHtml(visible)
            .replace(/!\[([^\]]*)\]\((https?:[^)\s]+)\)/g, '<img class="post-inline-img" alt="$1" src="$2" loading="lazy">')
            .replace(/\[([^\]]+)\]\((https?:[^)\s]+)\)/g, '<a href="$2" target="_blank" rel="noopener noreferrer">$1</a>')
            .replace(/^#{1,6}\s*(.+)$/gm, '<strong>$1</strong>')
            .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
            .replace(/\n{2,}/g, '</p><p>')
            .replace(/\n/g, '<br>');
        html = '<p>' + html + '</p>';
        const expandBtn = isLong
            ? `<button class="post-expand-btn" data-idx="${p.__idx}">${p.expanded ? 'Show less' : 'Read full story'}</button>`
            : '';
        return `<div class="post-body-full">${html}${expandBtn}</div>`;
    }

    function renderPost(p, idx) {
        p.__idx = idx;
        const sourcesLine = p.sources && p.sources.length
            ? p.sources.map(s => '<span>source: ' + escapeHtml(s) + '</span>').join('')
            : '<span style="color:var(--fg-dim)">open call for verification</span>';
        const userClass = p.isUser ? ' is-user' : '';
        const userTag = p.isUser ? '<span class="post-user-tag">USER SIGNAL</span>' : '';
        const video = videoHtml(p);
        const media = video ? '' : mediaHtml(p);
        const srcLink = sourceLinkHtml(p);
        const titleHtml = p.link
            ? `<h3 class="post-title"><a class="post-title-link" href="${escapeAttr(p.link)}" target="_blank" rel="noopener noreferrer">${escapeHtml(p.title)}</a></h3>`
            : `<h3 class="post-title">${escapeHtml(p.title)}</h3>`;

        return `
        <article class="post${userClass}" data-tier="${escapeAttr(p.tier)}" data-type="${escapeAttr(p.type)}" data-min="${escapeAttr(p.minutesAgo)}" data-cats="${escapeAttr((p.cats || []).join(','))}" data-idx="${idx}">
            <div class="post-head">
                ${starsHtml(p.tier)}
                ${userTag}
                <span class="post-meta">${p.location === 'wire' ? '<span class="feed-indicator">FEED</span>' : escapeHtml(p.location || 'global')} - ${fmtTime(p.minutesAgo)}</span>
            </div>
            ${titleHtml}
            ${video}
            ${media}
            ${bodyHtml(p)}
            <div class="post-sources">${sourcesLine}</div>
            ${srcLink}
            <div class="post-actions">
                <button class="post-action" data-act="verify">Verify</button>
                <button class="post-action" data-act="amplify">Amplify</button>
                <button class="post-action" data-act="save">Save</button>
                <button class="post-action" data-act="translate">Translate</button>
                <button class="post-action" data-act="share">Share</button>
            </div>
        </article>`;
    }

    function rankFeed(items) {
        return (items || []).slice().sort((a, b) => {
            if ((b.tier || 0) !== (a.tier || 0)) return (b.tier || 0) - (a.tier || 0);
            return (a.minutesAgo || 0) - (b.minutesAgo || 0);
        });
    }

    function mergeFeeds(liveItems) {
        const now = Date.now();
        const aged = userStories.map(s => ({
            ...s,
            minutesAgo: Math.max(0, Math.round((now - (s.postedAt || now)) / 60000))
        }));
        return rankFeed([...aged, ...(liveItems || [])]);
    }

    function ensureVideoCoverage(items) {
        const seen = new Set();
        const out = [];
        for (const item of [...(items || []), ...FALLBACK_VIDEOS]) {
            if (!item || !item.title) continue;
            const key = (item.link || item.videoUrl || item.title).toLowerCase();
            if (seen.has(key)) continue;
            seen.add(key);
            out.push(item);
        }
        return rankFeed(out);
    }

    function setBasePosts(items) {
        basePosts = ensureVideoCoverage(items);
        allPosts = mergeFeeds(basePosts);
    }

    function visiblePosts() {
        return allPosts.filter(p => {
            if (activeFilter === 'all') return true;
            if (activeFilter === 'recent') return p.minutesAgo <= 90;
            if (activeFilter === 'video') return p.type === 'video' || p.type === 'livestream' || !!detectVideo(firstPlayableUrl(p));
            if (activeFilter === 'docs') return p.type === 'document';
            if (activeFilter === 'new') return (p.cats || []).includes('new') || p.minutesAgo <= 120;
            if (activeFilter === 'viral') return (p.cats || []).includes('developing') || (p.cats || []).includes('watch');
            const n = parseInt(activeFilter, 10);
            if (!isNaN(n)) return Number(p.tier) === n;
            return true;
        }).filter(p => {
            if (!activeQuery) return true;
            const q = activeQuery.toLowerCase();
            return (p.title + ' ' + p.body + ' ' + (p.sources || []).join(' ') + ' ' + (p.location || '')).toLowerCase().includes(q);
        });
    }

    function paint(reset) {
        if (!feed || !loader) return;
        if (reset) {
            feed.innerHTML = '';
            renderedCount = 0;
        }
        const list = visiblePosts();
        const slice = list.slice(renderedCount, renderedCount + PAGE);
        if (slice.length === 0 && renderedCount === 0) {
            feed.innerHTML = '<div class="loader" style="padding:60px 20px">NO SIGNALS MATCH - TRY A DIFFERENT FILTER OR SEARCH</div>';
            loader.style.display = 'none';
            updateFieldVideo();
            return;
        }
        const html = slice.map((p, i) => renderPost(p, renderedCount + i)).join('');
        feed.insertAdjacentHTML('beforeend', html);
        renderedCount += slice.length;
        loader.style.display = renderedCount >= list.length ? 'none' : '';
        updateFieldVideo();
        updateWatchList();
    }

    if (filters) {
        filters.addEventListener('click', e => {
            const link = e.target.closest('.sort-link');
            if (!link) return;
            e.preventDefault();
            const wasActive = link.classList.contains('active');
            filters.querySelectorAll('.sort-link').forEach(l => l.classList.remove('active'));
            activeFilter = wasActive ? 'all' : link.dataset.filter;
            if (!wasActive) link.classList.add('active');
            paint(true);
            updateHero();
        });
    }

    document.querySelectorAll('.nav-item[data-view]').forEach(n => {
        n.addEventListener('click', () => {
            document.querySelectorAll('.nav-item[data-view]').forEach(x => x.classList.remove('active'));
            n.classList.add('active');
            const view = n.dataset.view || 'latest';
            const titleMap = {
                latest: 'WorldFeed - underreported live',
                new: 'WorldFeed - new signals',
                verified: 'WorldFeed - verified',
                viral: 'WorldFeed - developing watch',
                developing: 'WorldFeed - developing',
                video: 'WorldFeed - field video',
                docs: 'WorldFeed - source documents',
                federation: 'WorldFeed - federation status',
                saved: 'WorldFeed - saved',
                about: 'WorldFeed - about'
            };
            if (feedTitle) feedTitle.textContent = titleMap[view] || titleMap.latest;
            const map = { latest: 'all', new: 'new', verified: '5', viral: 'viral', developing: 'viral', video: 'video', docs: 'docs', saved: 'all', federation: 'all', about: 'all' };
            activeFilter = map[view] || 'all';
            if (filters) filters.querySelectorAll('.sort-link').forEach(l => l.classList.toggle('active', l.dataset.filter === activeFilter));
            paint(true);
            updateHero();
        });
    });

    if (search) {
        search.addEventListener('input', () => {
            clearTimeout(searchTimer);
            searchTimer = setTimeout(() => {
                activeQuery = search.value.trim();
                paint(true);
            }, 120);
        });
    }

    if (loader && 'IntersectionObserver' in window) {
        const observer = new IntersectionObserver(entries => {
            if (entries[0].isIntersecting) paint(false);
        }, { rootMargin: '400px' });
        observer.observe(loader);
    }

    if (feed) {
        feed.addEventListener('click', e => {
            const vid = e.target.closest('.post-video.has-thumb');
            if (vid) {
                e.preventDefault();
                e.stopPropagation();
                const embed = vid.dataset.embed + (vid.dataset.embed.includes('?') ? '&' : '?') + 'autoplay=1&rel=0';
                const tag = vid.querySelector('.post-media-tag');
                const tagHtml = tag ? tag.outerHTML : '';
                vid.outerHTML = `<div class="post-video"><iframe src="${escapeAttr(embed)}" allow="autoplay; fullscreen; encrypted-media" allowfullscreen loading="lazy"></iframe>${tagHtml}</div>`;
                return;
            }
            const exp = e.target.closest('.post-expand-btn');
            if (exp) {
                e.preventDefault();
                e.stopPropagation();
                const idx = parseInt(exp.dataset.idx, 10);
                const post = allPosts[idx];
                if (post) {
                    post.expanded = !post.expanded;
                    paint(true);
                }
                return;
            }
            const btn = e.target.closest('.post-action');
            if (!btn) return;
            e.preventDefault();
            e.stopPropagation();
            btn.classList.toggle('active');
            if (btn.dataset.act === 'share' && navigator.share) {
                const post = btn.closest('.post');
                const title = post.querySelector('.post-title')?.textContent || 'WorldFeed';
                navigator.share({ title, text: title, url: location.href }).catch(() => {});
            }
        });
    }

    const modal = document.getElementById('submitModal');
    const loginModal = document.getElementById('loginModal');
    const newPostBtn = document.getElementById('newPostBtn');
    const accountBadge = document.getElementById('accountBadge');

    function refreshAccountUI() {
        const acc = getAccount();
        if (!accountBadge) return;
        if (acc) {
            accountBadge.innerHTML = '<span class="acc-dot"></span>@' + escapeHtml(acc.username) + ' <button class="acc-logout" id="logoutBtn">logout</button>';
            document.getElementById('logoutBtn')?.addEventListener('click', (e) => {
                e.stopPropagation();
                setAccount(null);
                refreshAccountUI();
            });
        } else {
            accountBadge.innerHTML = '<button class="acc-login-trigger" id="loginTrigger">Sign in to signal</button>';
            document.getElementById('loginTrigger')?.addEventListener('click', () => loginModal?.classList.add('show'));
        }
    }

    refreshAccountUI();

    newPostBtn?.addEventListener('click', () => {
        if (!isLoggedIn() && loginModal) {
            loginModal.classList.add('show');
            return;
        }
        modal?.classList.add('show');
    });
    document.getElementById('cancelSubmit')?.addEventListener('click', () => modal?.classList.remove('show'));
    modal?.addEventListener('click', e => { if (e.target === modal) modal.classList.remove('show'); });

    if (loginModal) {
        const close = () => loginModal.classList.remove('show');
        document.getElementById('cancelLogin')?.addEventListener('click', close);
        loginModal.addEventListener('click', e => { if (e.target === loginModal) close(); });
        document.getElementById('confirmLogin')?.addEventListener('click', () => {
            const username = (document.getElementById('loginUsername')?.value || '').trim().replace(/^@/, '');
            const email = (document.getElementById('loginEmail')?.value || '').trim();
            if (!username || username.length < 2) {
                alert('Choose a username with at least 2 characters.');
                return;
            }
            setAccount({ username, email, since: Date.now() });
            refreshAccountUI();
            close();
            modal?.classList.add('show');
        });
    }

    function readImageFile(file) {
        return new Promise((resolve, reject) => {
            if (!file) return resolve('');
            if (file.size > 800 * 1024) return reject(new Error('Image too large. Max 800KB.'));
            const r = new FileReader();
            r.onload = () => resolve(r.result);
            r.onerror = () => reject(new Error('Failed to read image.'));
            r.readAsDataURL(file);
        });
    }

    document.getElementById('confirmSubmit')?.addEventListener('click', async () => {
        if (!isLoggedIn()) {
            loginModal?.classList.add('show');
            return;
        }
        const acc = getAccount();
        const title = document.getElementById('postTitle')?.value.trim() || '';
        const body = document.getElementById('postBody')?.value.trim() || '';
        const type = document.getElementById('postType')?.value || 'story';
        const videoUrl = (document.getElementById('postVideo')?.value || '').trim();
        const sourcesRaw = (document.getElementById('postSources')?.value || '').split('\n').map(s => s.trim()).filter(Boolean);
        const fileInput = document.getElementById('postImage');
        if (!title || !body) {
            alert('Headline and body required.');
            return;
        }
        let imageDataUrl = '';
        if (fileInput?.files?.[0]) {
            try { imageDataUrl = await readImageFile(fileInput.files[0]); }
            catch (err) { alert(err.message); return; }
        }
        const firstUrl = sourcesRaw.find(s => /^https?:\/\//i.test(s)) || '';
        const tier = sourcesRaw.length >= 5 ? 5 : sourcesRaw.length >= 3 ? 4 : sourcesRaw.length >= 2 ? 3 : sourcesRaw.length === 1 ? 2 : 0;
        const story = {
            id: 'u' + Date.now(),
            tier,
            cats: ['new'],
            title,
            body,
            sources: ['@' + acc.username, ...sourcesRaw],
            type: videoUrl ? 'video' : (imageDataUrl ? 'image' : type),
            location: '@' + acc.username,
            link: firstUrl || videoUrl,
            videoUrl,
            imageUrl: imageDataUrl,
            isUser: true,
            author: acc.username,
            postedAt: Date.now(),
            minutesAgo: 0
        };
        userStories.unshift(story);
        saveUserStories(userStories);
        allPosts = mergeFeeds(basePosts);
        modal?.classList.remove('show');
        ['postTitle', 'postBody', 'postSources', 'postVideo'].forEach(id => {
            const el = document.getElementById(id);
            if (el) el.value = '';
        });
        if (fileInput) fileInput.value = '';
        paint(true);
        updateHero();
    });

    function updateHero() {
        const hero = document.getElementById('zHero');
        const bg = document.getElementById('zHeroBg');
        const title = document.getElementById('zHeroTitle');
        const meta = document.getElementById('zHeroMeta');
        if (!hero || !bg || !title || !meta) return;
        const top = allPosts.filter(p => Number(p.tier) >= 4).slice(0, 1)[0];
        if (!top) {
            hero.style.display = 'none';
            return;
        }
        title.textContent = top.title || 'WorldFeed';
        const srcCount = top.sources ? top.sources.length : 0;
        const srcs = top.sources ? top.sources.slice(0, 3).join(', ') : '';
        meta.textContent = (top.location || 'global') + ' - ' + fmtTime(top.minutesAgo) + ' - ' + srcCount + ' sources - ' + srcs;
        if (top.imageUrl) bg.style.backgroundImage = "url('" + String(top.imageUrl).replace(/"/g, '%22') + "')";
        hero.style.display = '';
        hero.dataset.link = top.link || '';
    }

    document.addEventListener('click', function (e) {
        const hero = e.target.closest('.z-hero');
        if (hero && hero.dataset.link) window.open(hero.dataset.link, '_blank');
    });

    function normalizeFeedItem(item, idx) {
        if (!item || !item.title) return null;
        const playable = firstPlayableUrl(item);
        const isVideo = item.type === 'video' || item.type === 'livestream' || !!detectVideo(playable);
        return {
            id: item.id || 'feed-' + idx,
            tier: Number.isFinite(Number(item.tier)) ? Number(item.tier) : 3,
            cats: Array.isArray(item.cats) ? item.cats : [],
            title: String(item.title || '').trim(),
            body: String(item.body || item.summary || '').trim(),
            summary: item.summary || '',
            sources: Array.isArray(item.sources) ? item.sources : (item.source ? [item.source] : []),
            type: isVideo ? 'video' : (item.type || 'story'),
            minutesAgo: Number.isFinite(Number(item.minutesAgo)) ? Number(item.minutesAgo) : 999,
            location: item.location || 'wire',
            imageUrl: item.imageUrl || '',
            videoUrl: item.videoUrl || (isVideo ? item.link : ''),
            link: item.link || item.videoUrl || '',
            hasFullText: !!item.hasFullText
        };
    }

    function validateFeedItems(items) {
        if (!Array.isArray(items)) return [];
        return items.map(normalizeFeedItem).filter(Boolean);
    }

    function loadLiveFeed(isInitial) {
        fetch('data/feed.json?t=' + Date.now(), { cache: 'no-store' })
            .then(r => r.ok ? r.json() : null)
            .then(j => {
                if (!j || !Array.isArray(j.items)) return;
                const valid = validateFeedItems(j.items);
                if (!valid.length) {
                    if (isInitial) console.warn('WorldFeed: live feed empty, keeping bundled seed.');
                    return;
                }
                setBasePosts(valid);
                paint(true);
                updateHero();
                if (isInitial) console.log('WorldFeed live - ' + valid.length + ' items - updated ' + j.updatedAt);
            })
            .catch(() => { /* Keep bundled seed. */ });
    }

    function scheduleHourlyRefresh() {
        const now = new Date();
        const next = new Date(now);
        next.setHours(now.getHours() + 1, 0, 30, 0);
        setTimeout(() => {
            loadLiveFeed(false);
            scheduleHourlyRefresh();
        }, next.getTime() - now.getTime());
    }

    function updateWatchList() {
        const wrap = document.getElementById('watchList');
        if (!wrap) return;
        const watch = basePosts
            .filter(p => p.tier >= 4 && p.type !== 'video')
            .slice(0, 4);
        if (watch.length < 4) return;
        wrap.innerHTML = watch.map(p => {
            const meta = '*'.repeat(Math.max(1, Math.min(5, p.tier))) + ' - ' + (p.sources?.length || 0) + ' sources - ' + fmtTime(p.minutesAgo);
            return `<div class="item">${escapeHtml(p.title)}<div class="item-meta">${escapeHtml(meta)}</div></div>`;
        }).join('');
    }

    function railVideoHtml(v) {
        const playable = firstPlayableUrl(v) || v.link || '#';
        const detected = detectVideo(playable);
        const thumb = v.imageUrl || detected?.thumb || '';
        const src = v.sources && v.sources[0] ? v.sources[0] : 'verified source';
        const bg = thumb ? ` style="background-image:url('${escapeAttr(thumb)}')"` : '';
        return `<div class="rail-video-item" data-url="${escapeAttr(playable || v.link || '')}">
            <div class="rail-video-thumb"${bg}></div>
            <div>
                <div class="rail-video-title">${escapeHtml(v.title)}</div>
                <div class="rail-video-source">${escapeHtml(src)} - ${fmtTime(v.minutesAgo)}</div>
            </div>
        </div>`;
    }

    function updateFieldVideo() {
        const slots = ['torVideo1', 'torVideo2', 'torVideo3'].map(id => document.getElementById(id)).filter(Boolean);
        if (!slots.length) return;
        const liveVideos = ensureVideoCoverage(basePosts)
            .filter(p => p.type === 'video' || p.type === 'livestream' || !!detectVideo(firstPlayableUrl(p)))
            .filter(p => firstPlayableUrl(p));
        const videos = ensureVideoCoverage([
            ...liveVideos.filter(p => VIDEO_PRIORITY_RE.test((p.title || '') + ' ' + (p.body || ''))),
            ...FALLBACK_VIDEOS,
            ...liveVideos
        ]).filter(p => firstPlayableUrl(p)).slice(0, slots.length);
        slots.forEach((el, i) => {
            const v = videos[i] || FALLBACK_VIDEOS[i % FALLBACK_VIDEOS.length];
            el.innerHTML = railVideoHtml(v);
            el.style.cursor = 'pointer';
            el.onclick = function () {
                const url = firstPlayableUrl(v) || v.link;
                if (url) window.open(url, '_blank');
            };
        });
    }

    paint(true);
    updateHero();
    updateWatchList();
    loadLiveFeed(true);
    scheduleHourlyRefresh();
})();

// === Precog API Integration (Anti-Algo) ===
// Global functions for all pages

function loadPrecogFeed(filter) {
    console.log('[Anti-Algo] Loading precog feed...');
    const feedEl = document.getElementById('wf-feed');
    const loader = document.getElementById('wf-loader');
    
    if (!feedEl) return;
    
    const filterParam = filter || '5';
    const url = '/api/precog/feed?writing=10&video=5&image=5&filter=' + filterParam;

    fetch(url)
        .then(response => {
            if (!response.ok) throw new Error('API not available');
            return response.json();
        })
        .then(data => {
            console.log('[Anti-Algo] Precog feed loaded:', data);
            if (data && data.data && data.data.feed) {
                displayFeed(data.data.feed, feedEl);
                if (loader) loader.style.display = 'none';
            }
        })
        .catch(error => {
            console.log('[Anti-Algo] Using offline data - API not available');
            if (loader) loader.textContent = 'Connect Precog API to load live feed.';
        });
}

function displayFeed(items, container) {
    if (!container) return;
    container.innerHTML = '';
    
    items.forEach(item => {
        const c = item.content || item;
        const type = item.type || 'written';
        const author = (c.author || 'precog').replace(/_/g, ' ');
        const title = c.title || '';
        const desc = c.description || c.content || c.body || '';
        const img = c.image_url || c.thumbnail_url || c.photo_url || '';
        const hz = item.resonance || c.resonance || 1272;
        const initial = author.charAt(0).toUpperCase();
        
        let mediaHtml = '';
        if (type === 'video' && c.video_url) {
            mediaHtml = '<div class="wf-status-media"><video src="' + c.video_url + '" poster="' + img + '" controls></video></div>';
        } else if (img) {
            mediaHtml = '<div class="wf-status-media"><img src="' + img + '" alt="' + title + '" loading="lazy"></div>';
        }
        
        const article = document.createElement('article');
        article.className = 'wf-status';
        article.setAttribute('role', 'article');
        article.innerHTML =
            '<div class="wf-status-avatar">' + initial + '</div>' +
            '<div class="wf-status-body">' +
                '<div class="wf-status-header">' +
                    '<span class="wf-status-name">' + author + '</span>' +
                    '<span class="wf-status-handle">@precog · ' + hz + ' Hz</span>' +
                '</div>' +
                (title ? '<div class="wf-status-title">' + title + '</div>' : '') +
                '<div class="wf-status-content">' + desc.substring(0, 280) + (desc.length > 280 ? '…' : '') + '</div>' +
                mediaHtml +
                '<div class="wf-status-actions">' +
                    '<span class="wf-action">💬 <span>Reply</span></span>' +
                    '<span class="wf-action">🔁 <span>Boost</span></span>' +
                    '<span class="wf-action">❤ <span>Like</span></span>' +
                    '<span class="wf-action">📤 <span>Share</span></span>' +
                '</div>' +
            '</div>';
        
        container.appendChild(article);
    });
}
