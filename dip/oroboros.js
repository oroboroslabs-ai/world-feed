// oroboros.js — Frontend Client for DIP
// A\ 1272 Hz
// Oroboros Labs — Decoupled Frontend Integration

class OroborosClient {
    constructor(config = {}) {
        this.dipEndpoint = config.dipEndpoint || 'http://localhost:8081';
        this.controlEndpoint = config.controlEndpoint || 'http://localhost:8080';
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

    // Fetch feed through DIP
    async fetchFeed(options = {}) {
        const cacheKey = `feed_${this.userID}`;
        
        // Check local cache
        if (this.cache.has(cacheKey)) {
            const cached = this.cache.get(cacheKey);
            if (Date.now() - cached.timestamp < this.cacheTTL) {
                console.log('[Oroboros] Cache HIT — Resonance:', this.resonanceHz, 'Hz');
                return cached.data;
            }
        }

        try {
            const response = await fetch(`${this.dipEndpoint}/api/oroboros/feed/${this.userID}`, {
                method: 'GET',
                headers: {
                    'X-Resonance': `${this.resonanceHz} Hz`,
                    'X-Strata': this.strata,
                    'X-Component': 'OroborosClient'
                }
            });

            if (!response.ok) {
                throw new Error(`DIP responded with ${response.status}`);
            }

            const data = await response.json();
            
            // Cache the result
            this.cache.set(cacheKey, {
                data: data,
                timestamp: Date.now()
            });

            console.log('[Oroboros] Feed fetched — Strata:', this.strata);
            return data;

        } catch (error) {
            console.error('[Oroboros] Feed fetch failed:', error.message);
            return this.getDefaultFeed();
        }
    }

    // Get DIP health status
    async getHealth() {
        try {
            const response = await fetch(`${this.dipEndpoint}/api/oroboros/health`);
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
            const response = await fetch(`${this.dipEndpoint}/api/oroboros/strata`);
            return await response.json();
        } catch (error) {
            return {
                error: 'Unable to fetch strata',
                resonance: this.resonanceHz
            };
        }
    }

    // Default feed on failure
    getDefaultFeed() {
        return [{
            id: 'default-1',
            content: 'Welcome to Anti-Algo News Network — Your sovereignty-protected feed',
            author: 'system',
            timestamp: new Date().toISOString(),
            confidence: 0.99,
            strata: 'S1',
            resonance: this.resonanceHz,
            processed: true,
            filtered: false
        }];
    }

    // Render feed to DOM
    renderFeed(container, posts) {
        if (typeof container === 'string') {
            container = document.querySelector(container);
        }

        if (!container) {
            console.error('[Oroboros] Container not found');
            return;
        }

        container.innerHTML = '';

        posts.forEach(post => {
            const postElement = this.createPostElement(post);
            container.appendChild(postElement);
        });

        console.log('[Oroboros] Rendered', posts.length, 'posts');
    }

    // Create post element
    createPostElement(post) {
        const article = document.createElement('article');
        article.className = 'oroboros-post';
        article.setAttribute('data-strata', post.strata || 'S1');
        article.setAttribute('data-resonance', post.resonance || this.resonanceHz);

        article.innerHTML = `
            <div class="post-header">
                <span class="post-author">@${post.author || 'unknown'}</span>
                <span class="post-strata">${post.strata || 'S1'}</span>
                <span class="post-confidence">${((post.confidence || 0.99) * 100).toFixed(0)}%</span>
            </div>
            <div class="post-content">${this.sanitizeContent(post.content || '')}</div>
            <div class="post-footer">
                <time class="post-timestamp">${new Date(post.timestamp || Date.now()).toLocaleString()}</time>
                <span class="post-resonance">${this.resonanceHz} Hz</span>
            </div>
        `;

        return article;
    }

    // Sanitize content for safe rendering
    sanitizeContent(content) {
        const div = document.createElement('div');
        div.textContent = content;
        return div.innerHTML;
    }

    // Initialize with auto-refresh
    initialize(options = {}) {
        const refreshInterval = options.refreshInterval || 30000;
        const container = options.container || '#oroboros-feed';

        console.log('[Oroboros] Initializing — Resonance:', this.resonanceHz, 'Hz');
        console.log('[Oroboros] Strata:', this.strata);
        console.log('[Oroboros] User ID:', this.userID);

        // Initial fetch
        this.fetchFeed().then(posts => {
            this.renderFeed(container, posts);
        });

        // Auto-refresh
        setInterval(async () => {
            const posts = await this.fetchFeed();
            this.renderFeed(container, posts);
        }, refreshInterval);

        return this;
    }
}

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = OroborosClient;
}

// Auto-initialize if container exists
if (typeof document !== 'undefined') {
    document.addEventListener('DOMContentLoaded', () => {
        const container = document.querySelector('#oroboros-feed');
        if (container) {
            window.oroborosClient = new OroborosClient({
                dipEndpoint: window.DIP_ENDPOINT || 'http://localhost:8081',
                resonanceHz: window.RESONANCE_HZ || 1272
            }).initialize({
                container: '#oroboros-feed',
                refreshInterval: 30000
            });
        }
    });
}