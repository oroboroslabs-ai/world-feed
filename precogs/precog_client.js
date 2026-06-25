// precog_client.js — Frontend Client for Precog Pipeline
// A\ 1272 Hz
// Oroboros Labs — Three Precog Architecture

class PrecogClient {
    constructor(config = {}) {
        this.precogEndpoint = config.precogEndpoint || 'http://localhost:8082';
        this.resonanceHz = config.resonanceHz || 1272;
        this.strata = config.strata || 'S1-S12';
        this.userID = config.userID || this.generateUserID();
        this.cache = new Map();
        this.cacheTTL = 30000; // 30 seconds
    }

    // Generate unique user ID
    generateUserID() {
        return 'user_' + Math.random().toString(36).substr(2, 9) + '_' + Date.now();
    }

    // Fetch unified feed from all precogs
    async fetchFeed(options = {}) {
        const cacheKey = `feed_${this.userID}`;
        
        // Check local cache
        if (this.cache.has(cacheKey)) {
            const cached = this.cache.get(cacheKey);
            if (Date.now() - cached.timestamp < this.cacheTTL) {
                console.log('[Precog] Cache HIT — Resonance:', this.resonanceHz, 'Hz');
                return cached.data;
            }
        }

        try {
            const writingCount = options.writing || 10;
            const videoCount = options.video || 5;
            const imageCount = options.image || 5;
            
            const response = await fetch(
                `${this.precogEndpoint}/api/precog/feed?writing=${writingCount}&video=${videoCount}&image=${imageCount}`,
                {
                    method: 'GET',
                    headers: {
                        'X-Resonance': `${this.resonanceHz} Hz`,
                        'X-Strata': this.strata,
                        'X-Component': 'PrecogClient'
                    }
                }
            );

            if (!response.ok) {
                throw new Error(`Precog API responded with ${response.status}`);
            }

            const result = await response.json();
            
            // Cache the result
            this.cache.set(cacheKey, {
                data: result,
                timestamp: Date.now()
            });

            console.log('[Precog] Feed fetched — Strata:', this.strata);
            return result;

        } catch (error) {
            console.error('[Precog] Feed fetch failed:', error.message);
            return this.getDefaultFeed();
        }
    }

    // Fetch written content
    async fetchWriting(count = 10, category = null) {
        try {
            let url = `${this.precogEndpoint}/api/precog/writing?count=${count}`;
            if (category) url += `&category=${category}`;
            
            const response = await fetch(url);
            return await response.json();
        } catch (error) {
            console.error('[Precog] Writing fetch failed:', error.message);
            return { status: 'error', error: error.message };
        }
    }

    // Fetch video content
    async fetchVideo(count = 5, category = null) {
        try {
            let url = `${this.precogEndpoint}/api/precog/video?count=${count}`;
            if (category) url += `&category=${category}`;
            
            const response = await fetch(url);
            return await response.json();
        } catch (error) {
            console.error('[Precog] Video fetch failed:', error.message);
            return { status: 'error', error: error.message };
        }
    }

    // Fetch image content
    async fetchImage(count = 5, category = null) {
        try {
            let url = `${this.precogEndpoint}/api/precog/image?count=${count}`;
            if (category) url += `&category=${category}`;
            
            const response = await fetch(url);
            return await response.json();
        } catch (error) {
            console.error('[Precog] Image fetch failed:', error.message);
            return { status: 'error', error: error.message };
        }
    }

    // Get pipeline status
    async getStatus() {
        try {
            const response = await fetch(`${this.precogEndpoint}/api/precog/status`);
            return await response.json();
        } catch (error) {
            return {
                status: 'error',
                error: error.message,
                resonance: this.resonanceHz
            };
        }
    }

    // Get strata information
    async getStrata() {
        try {
            const response = await fetch(`${this.precogEndpoint}/api/precog/strata`);
            return await response.json();
        } catch (error) {
            return {
                error: 'Unable to fetch strata',
                resonance: this.resonanceHz
            };
        }
    }

    // User operations
    async getProfile() {
        try {
            const response = await fetch(`${this.precogEndpoint}/api/user/profile`);
            return await response.json();
        } catch (error) {
            return { status: 'error', error: error.message };
        }
    }

    async updateProfile(profile) {
        try {
            const response = await fetch(`${this.precogEndpoint}/api/user/profile`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(profile)
            });
            return await response.json();
        } catch (error) {
            return { status: 'error', error: error.message };
        }
    }

    async getPreferences() {
        try {
            const response = await fetch(`${this.precogEndpoint}/api/user/preferences`);
            return await response.json();
        } catch (error) {
            return { status: 'error', error: error.message };
        }
    }

    async updatePreferences(preferences) {
        try {
            const response = await fetch(`${this.precogEndpoint}/api/user/preferences`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(preferences)
            });
            return await response.json();
        } catch (error) {
            return { status: 'error', error: error.message };
        }
    }

    // Default feed on failure
    getDefaultFeed() {
        return {
            status: 'success',
            cached: false,
            data: {
                feed: [{
                    id: 'default-1',
                    type: 'written',
                    content: {
                        title: 'Welcome to DIP — Data Interception Proxy',
                        content: 'Your sovereignty-protected feed is initializing. The Three Precog Pipeline is connecting at 1272 Hz resonance.',
                        author: 'system',
                        category: 'system',
                        confidence: 0.99
                    },
                    confidence: 0.99,
                    resonance: this.resonanceHz,
                    strata: 'S1',
                    timestamp: new Date().toISOString(),
                    source: 'system'
                }],
                metadata: {
                    generated_at: new Date().toISOString(),
                    resonance: this.resonanceHz,
                    total_items: 1
                }
            }
        };
    }

    // Render feed to DOM
    renderFeed(container, feedData) {
        if (typeof container === 'string') {
            container = document.querySelector(container);
        }

        if (!container) {
            console.error('[Precog] Container not found');
            return;
        }

        container.innerHTML = '';

        const items = feedData.data?.feed || [];
        
        items.forEach(item => {
            const element = this.createFeedElement(item);
            container.appendChild(element);
        });

        console.log('[Precog] Rendered', items.length, 'items');
    }

    // Create feed element
    createFeedElement(item) {
        const article = document.createElement('article');
        article.className = 'precog-item';
        article.setAttribute('data-type', item.type);
        article.setAttribute('data-strata', item.strata || 'S1');
        article.setAttribute('data-resonance', item.resonance || this.resonanceHz);

        const content = item.content || {};
        
        if (item.type === 'written') {
            article.innerHTML = `
                <div class="item-header">
                    <span class="item-author">@${content.author || 'unknown'}</span>
                    <span class="item-category">${content.category || 'general'}</span>
                    <span class="item-strata">${item.strata || 'S1'}</span>
                    <span class="item-confidence">${((item.confidence || 0.99) * 100).toFixed(0)}%</span>
                </div>
                <div class="item-title">${this.sanitize(content.title || 'Untitled')}</div>
                <div class="item-content">${this.sanitize(content.content || '')}</div>
                <div class="item-footer">
                    <time class="item-timestamp">${new Date(item.timestamp || Date.now()).toLocaleString()}</time>
                    <span class="item-resonance">${this.resonanceHz} Hz</span>
                    <span class="item-source">${item.source || 'precog'}</span>
                </div>
            `;
        } else if (item.type === 'video') {
            article.innerHTML = `
                <div class="item-header">
                    <span class="item-type">🎬 Video</span>
                    <span class="item-category">${content.category || 'general'}</span>
                    <span class="item-strata">${item.strata || 'S1'}</span>
                    <span class="item-confidence">${((item.confidence || 0.99) * 100).toFixed(0)}%</span>
                </div>
                <div class="item-title">${this.sanitize(content.title || 'Untitled Video')}</div>
                <div class="item-description">${this.sanitize(content.description || '')}</div>
                <div class="item-meta">
                    <span class="item-duration">⏱️ ${Math.floor((content.duration || 0) / 60)}m</span>
                    <span class="item-resonance">${this.resonanceHz} Hz</span>
                </div>
                <div class="item-footer">
                    <time class="item-timestamp">${new Date(item.timestamp || Date.now()).toLocaleString()}</time>
                    <span class="item-source">${item.source || 'precog'}</span>
                </div>
            `;
        } else if (item.type === 'image') {
            article.innerHTML = `
                <div class="item-header">
                    <span class="item-type">🖼️ Image</span>
                    <span class="item-category">${content.category || 'general'}</span>
                    <span class="item-strata">${item.strata || 'S1'}</span>
                    <span class="item-confidence">${((item.confidence || 0.99) * 100).toFixed(0)}%</span>
                </div>
                <div class="item-title">${this.sanitize(content.title || 'Untitled Image')}</div>
                <div class="item-description">${this.sanitize(content.description || '')}</div>
                <div class="item-meta">
                    <span class="item-dimensions">📐 ${content.width || 0}x${content.height || 0}</span>
                    <span class="item-resonance">${this.resonanceHz} Hz</span>
                </div>
                <div class="item-footer">
                    <time class="item-timestamp">${new Date(item.timestamp || Date.now()).toLocaleString()}</time>
                    <span class="item-source">${item.source || 'precog'}</span>
                </div>
            `;
        }

        return article;
    }

    // Sanitize content for safe rendering
    sanitize(content) {
        const div = document.createElement('div');
        div.textContent = content || '';
        return div.innerHTML;
    }

    // Initialize with auto-refresh
    initialize(options = {}) {
        const refreshInterval = options.refreshInterval || 30000;
        const container = options.container || '#precog-feed';

        console.log('[Precog] Initializing — Resonance:', this.resonanceHz, 'Hz');
        console.log('[Precog] Strata:', this.strata);
        console.log('[Precog] User ID:', this.userID);

        // Initial fetch
        this.fetchFeed().then(result => {
            this.renderFeed(container, result);
        });

        // Auto-refresh
        setInterval(async () => {
            const result = await this.fetchFeed();
            this.renderFeed(container, result);
        }, refreshInterval);

        return this;
    }
}

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = PrecogClient;
}

// Auto-initialize if container exists
if (typeof document !== 'undefined') {
    document.addEventListener('DOMContentLoaded', () => {
        const container = document.querySelector('#precog-feed');
        if (container) {
            window.precogClient = new PrecogClient({
                precogEndpoint: window.PRECOG_ENDPOINT || 'http://localhost:8082',
                resonanceHz: window.RESONANCE_HZ || 1272
            }).initialize({
                container: '#precog-feed',
                refreshInterval: 30000
            });
        }
    });
}