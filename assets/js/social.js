/**
 * Social Frontend - Mastodon Federation Integration
 * A\ 1272 Hz
 * 
 * Connects the DIP feed to Mastodon for:
 * - User authentication (sign in via Mastodon)
 * - Post federation (share to Mastodon)
 * - Social interactions (like, boost, reply)
 */

// Mastodon instances for federation
const MASTODON_INSTANCES = {
    primary: 'https://mastodon.social',
    tech: 'https://fosstodon.org',
    backup: 'https://mastodon.online'
};

// API endpoint
const SOCIAL_API = '/api/social';

class SocialClient {
    constructor() {
        this.sessionId = localStorage.getItem('mastodon_session_id');
        this.account = JSON.parse(localStorage.getItem('mastodon_account') || 'null');
        this.instance = localStorage.getItem('mastodon_instance') || MASTODON_INSTANCES.primary;
        this.accessToken = localStorage.getItem('mastodon_access_token');
    }

    /**
     * Check if user is authenticated
     */
    isAuthenticated() {
        return this.sessionId && this.account;
    }

    /**
     * Get current account info
     */
    getAccount() {
        return this.account;
    }

    /**
     * Initiate Mastodon sign in
     */
    async signIn(instance = null) {
        if (instance) {
            this.instance = instance;
        }

        try {
            const response = await fetch(`${SOCIAL_API}/signin?instance=${encodeURIComponent(this.instance)}`);
            const data = await response.json();

            if (data.status === 'success') {
                // Store instance for callback
                localStorage.setItem('mastodon_instance', this.instance);
                
                // Redirect to Mastodon OAuth
                window.location.href = data.oauth_url;
            } else {
                throw new Error(data.message || 'Failed to get OAuth URL');
            }
        } catch (error) {
            console.error('[SocialClient] Sign in error:', error);
            throw error;
        }
    }

    /**
     * Complete sign in after OAuth callback
     */
    async completeSignIn(authCode) {
        try {
            const response = await fetch(`${SOCIAL_API}/callback?code=${encodeURIComponent(authCode)}`);
            const data = await response.json();

            if (data.status === 'success') {
                this.sessionId = data.session_id;
                this.account = data.account;
                
                // Store in localStorage
                localStorage.setItem('mastodon_session_id', this.sessionId);
                localStorage.setItem('mastodon_account', JSON.stringify(this.account));
                
                return data;
            } else {
                throw new Error(data.message || 'Authentication failed');
            }
        } catch (error) {
            console.error('[SocialClient] Complete sign in error:', error);
            throw error;
        }
    }

    /**
     * Sign out
     */
    async signOut() {
        try {
            const response = await fetch(`${SOCIAL_API}/signout`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ session_id: this.sessionId })
            });

            // Clear local storage
            localStorage.removeItem('mastodon_session_id');
            localStorage.removeItem('mastodon_account');
            localStorage.removeItem('mastodon_access_token');
            localStorage.removeItem('mastodon_instance');
            
            this.sessionId = null;
            this.account = null;
            this.accessToken = null;

            return { status: 'success', message: 'Signed out successfully' };
        } catch (error) {
            console.error('[SocialClient] Sign out error:', error);
            throw error;
        }
    }

    /**
     * Post to Mastodon
     */
    async post(content, visibility = 'public', mediaUrls = null) {
        if (!this.isAuthenticated()) {
            throw new Error('Not authenticated');
        }

        try {
            const response = await fetch(`${SOCIAL_API}/post`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    session_id: this.sessionId,
                    content: content,
                    visibility: visibility,
                    media_urls: mediaUrls
                })
            });

            const data = await response.json();
            return data;
        } catch (error) {
            console.error('[SocialClient] Post error:', error);
            throw error;
        }
    }

    /**
     * Get Oroboros Mastodon feed
     */
    async getOroborosFeed(limit = 20) {
        try {
            const response = await fetch(`${SOCIAL_API}/feed/oroboros?limit=${limit}`);
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('[SocialClient] Get feed error:', error);
            return [];
        }
    }

    /**
     * Get federated public timeline
     */
    async getFederatedFeed(limit = 20) {
        try {
            const response = await fetch(`${SOCIAL_API}/feed/federated?limit=${limit}`);
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('[SocialClient] Get federated feed error:', error);
            return [];
        }
    }

    /**
     * Favourite (like) a status
     */
    async favourite(statusId) {
        return this.interact(statusId, 'favourite');
    }

    /**
     * Reblog (boost) a status
     */
    async reblog(statusId) {
        return this.interact(statusId, 'reblog');
    }

    /**
     * Interact with a status
     */
    async interact(statusId, action) {
        if (!this.isAuthenticated()) {
            throw new Error('Not authenticated');
        }

        try {
            const response = await fetch(`${SOCIAL_API}/interact`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    session_id: this.sessionId,
                    status_id: statusId,
                    action: action
                })
            });

            const data = await response.json();
            return data;
        } catch (error) {
            console.error('[SocialClient] Interact error:', error);
            throw error;
        }
    }
}

/**
 * Social UI Components
 */
class SocialUI {
    constructor(socialClient) {
        this.client = socialClient;
        this.signInModal = null;
    }

    /**
     * Initialize social UI
     */
    init() {
        this.createSignInModal();
        this.updateUI();
    }

    /**
     * Create sign in modal
     */
    createSignInModal() {
        const modal = document.createElement('div');
        modal.id = 'mastodon-signin-modal';
        modal.className = 'modal';
        modal.style.display = 'none';
        modal.innerHTML = `
            <div class="modal-content" style="background: #16181c; border-radius: 16px; padding: 24px; max-width: 400px; margin: 100px auto;">
                <h2 style="color: #00ff88; margin-bottom: 16px;">Sign in with Mastodon</h2>
                <p style="color: #71767b; margin-bottom: 20px;">Choose your Mastodon instance to sign in:</p>
                
                <div style="display: flex; flex-direction: column; gap: 12px; margin-bottom: 20px;">
                    <button class="instance-btn" data-instance="${MASTODON_INSTANCES.primary}" style="background: #1d9bf0; color: white; border: none; padding: 12px 20px; border-radius: 9999px; cursor: pointer; font-weight: 600;">
                        🦣 mastodon.social (Primary)
                    </button>
                    <button class="instance-btn" data-instance="${MASTODON_INSTANCES.tech}" style="background: #1d9bf0; color: white; border: none; padding: 12px 20px; border-radius: 9999px; cursor: pointer; font-weight: 600;">
                        🦣 fosstodon.org (Tech)
                    </button>
                    <button class="instance-btn" data-instance="${MASTODON_INSTANCES.backup}" style="background: #1d9bf0; color: white; border: none; padding: 12px 20px; border-radius: 9999px; cursor: pointer; font-weight: 600;">
                        🦣 mastodon.online (Backup)
                    </button>
                </div>
                
                <div style="margin-bottom: 20px;">
                    <label style="color: #71767b; display: block; margin-bottom: 8px;">Or enter custom instance:</label>
                    <input type="text" id="custom-instance" placeholder="https://mastodon.example" style="width: 100%; padding: 12px; border-radius: 8px; border: 1px solid #2f3336; background: #000; color: #fff;">
                </div>
                
                <button id="custom-signin-btn" style="background: #00ff88; color: #000; border: none; padding: 12px 24px; border-radius: 9999px; cursor: pointer; font-weight: 700; width: 100%;">
                    Sign in with Custom Instance
                </button>
                
                <button id="close-modal-btn" style="background: transparent; color: #71767b; border: none; padding: 12px; cursor: pointer; margin-top: 16px; width: 100%;">
                    Cancel
                </button>
            </div>
        `;

        document.body.appendChild(modal);
        this.signInModal = modal;

        // Add event listeners
        modal.querySelectorAll('.instance-btn').forEach(btn => {
            btn.addEventListener('click', () => this.handleSignIn(btn.dataset.instance));
        });

        modal.querySelector('#custom-signin-btn').addEventListener('click', () => {
            const customInstance = modal.querySelector('#custom-instance').value.trim();
            if (customInstance) {
                this.handleSignIn(customInstance);
            }
        });

        modal.querySelector('#close-modal-btn').addEventListener('click', () => {
            this.hideSignInModal();
        });
    }

    /**
     * Handle sign in
     */
    async handleSignIn(instance) {
        try {
            await this.client.signIn(instance);
        } catch (error) {
            console.error('[SocialUI] Sign in error:', error);
            alert('Failed to sign in. Please try again.');
        }
    }

    /**
     * Show sign in modal
     */
    showSignInModal() {
        if (this.signInModal) {
            this.signInModal.style.display = 'block';
        }
    }

    /**
     * Hide sign in modal
     */
    hideSignInModal() {
        if (this.signInModal) {
            this.signInModal.style.display = 'none';
        }
    }

    /**
     * Update UI based on authentication state
     */
    updateUI() {
        const accountBadge = document.getElementById('account-badge');
        const signInBtn = document.getElementById('signin-btn');
        
        if (this.client.isAuthenticated()) {
            // Show account info
            if (accountBadge) {
                accountBadge.style.display = 'flex';
                accountBadge.innerHTML = `
                    <img src="${this.client.account.avatar_url}" alt="${this.client.account.username}" style="width: 32px; height: 32px; border-radius: 50%;">
                    <span style="color: #fff; margin-left: 8px;">${this.client.account.display_name || this.client.account.username}</span>
                `;
            }
            
            if (signInBtn) {
                signInBtn.style.display = 'none';
            }
        } else {
            // Show sign in button
            if (accountBadge) {
                accountBadge.style.display = 'none';
            }
            
            if (signInBtn) {
                signInBtn.style.display = 'block';
            }
        }
    }

    /**
     * Create post composer
     */
    createPostComposer() {
        const composer = document.createElement('div');
        composer.className = 'post-composer';
        composer.innerHTML = `
            <div style="background: #16181c; border-radius: 16px; padding: 16px; margin-bottom: 16px;">
                <textarea id="post-content" placeholder="What's happening?" style="width: 100%; min-height: 80px; background: #000; border: 1px solid #2f3336; border-radius: 8px; padding: 12px; color: #fff; resize: vertical;"></textarea>
                
                <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 12px;">
                    <div style="display: flex; gap: 16px;">
                        <button class="compose-btn" title="Add image" style="background: transparent; border: none; color: #00ff88; cursor: pointer;">
                            🖼️
                        </button>
                        <button class="compose-btn" title="Add video" style="background: transparent; border: none; color: #00ff88; cursor: pointer;">
                            🎥
                        </button>
                        <button class="compose-btn" title="Add poll" style="background: transparent; border: none; color: #00ff88; cursor: pointer;">
                            📊
                        </button>
                    </div>
                    
                    <select id="post-visibility" style="background: #000; border: 1px solid #2f3336; border-radius: 8px; padding: 8px; color: #fff;">
                        <option value="public">🌍 Public</option>
                        <option value="unlisted">🔓 Unlisted</option>
                        <option value="private">🔒 Followers only</option>
                        <option value="direct">✉️ Direct</option>
                    </select>
                </div>
                
                <button id="post-submit-btn" style="background: #00ff88; color: #000; border: none; padding: 12px 24px; border-radius: 9999px; cursor: pointer; font-weight: 700; margin-top: 12px; width: 100%;">
                    Post
                </button>
            </div>
        `;

        // Add event listener for post submission
        composer.querySelector('#post-submit-btn').addEventListener('click', () => this.handlePost());

        return composer;
    }

    /**
     * Handle post submission
     */
    async handlePost() {
        const content = document.getElementById('post-content').value.trim();
        const visibility = document.getElementById('post-visibility').value;

        if (!content) {
            alert('Please enter some content');
            return;
        }

        try {
            const result = await this.client.post(content, visibility);
            
            if (result.status === 'success') {
                alert('Posted to Mastodon successfully!');
                document.getElementById('post-content').value = '';
                // Refresh feed
                if (typeof loadFeed === 'function') {
                    loadFeed();
                }
            } else {
                throw new Error(result.message || 'Failed to post');
            }
        } catch (error) {
            console.error('[SocialUI] Post error:', error);
            alert('Failed to post. Please try again.');
        }
    }

    /**
     * Create social action buttons for a post
     */
    createSocialActions(postId, status) {
        const actions = document.createElement('div');
        actions.className = 'social-actions';
        actions.style.display = 'flex';
        actions.style.gap = '60px';
        actions.style.color = '#71767b';
        actions.innerHTML = `
            <div class="social-action" style="display: flex; align-items: center; gap: 8px; cursor: pointer;" data-action="reply" data-id="${postId}">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M1.751 10.011a.75.75 0 0 1 .676-.727c2.868-.278 5.21-1.097 6.9-2.525 1.703-1.44 2.823-3.513 3.323-6.14a.75.75 0 0 1 .744-.619h.003c.4 0 .727.313.75.713.18 2.868 1.02 5.21 2.45 6.9 1.44 1.703 3.513 2.823 6.14 3.323a.75.75 0 0 1-.019 1.482c-2.868.278-5.21 1.097-6.9 2.525-1.703 1.44-2.823 3.513-3.323 6.14a.75.75 0 0 1-1.474.019c-.18-2.868-1.02-5.21-2.45-6.9-1.44-1.703-3.513-2.823-6.14-3.323a.75.75 0 0 1-.62-.727z"/></svg>
                <span>${status.replies_count || 0}</span>
            </div>
            <div class="social-action" style="display: flex; align-items: center; gap: 8px; cursor: pointer;" data-action="reblog" data-id="${postId}">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M4.75 4.5a.75.75 0 0 1 .75.75v9.5c0 .414.336.75.75.75h9.19l-2.72-2.72a.75.75 0 0 1 1.06-1.06l4 4a.75.75 0 0 1 0 1.06l-4 4a.75.75 0 0 1-1.06-1.06l2.72-2.72H6.25A2.25 2.25 0 0 1 4 13.75v-9.5a.75.75 0 0 1 .75-.75zm14.5 0a.75.75 0 0 1 .75.75v9.5a.75.75 0 0 1-1.5 0v-9.5a.75.75 0 0 1 .75-.75z"/></svg>
                <span>${status.reblogs_count || 0}</span>
            </div>
            <div class="social-action" style="display: flex; align-items: center; gap: 8px; cursor: pointer;" data-action="favourite" data-id="${postId}">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/></svg>
                <span>${status.favourites_count || 0}</span>
            </div>
            <div class="social-action" style="display: flex; align-items: center; gap: 8px; cursor: pointer;" data-action="share" data-id="${postId}">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M18 16.08c-.76 0-1.44.3-1.96.77L8.91 12.7c.05-.23.09-.46.09-.7s-.04-.47-.09-.7l7.05-4.11c.54.47 1.2.77 1.96.77 1.66 0 3-1.34 3-3s-1.34-3-3-3-3 1.34-3 3c0 .24.04.47.09.7L8.04 9.81C7.5 9.34 6.84 9.04 6.08 9.04c-1.66 0-3 1.34-3 3s1.34 3 3 3c.76 0 1.44-.3 1.96-.77l7.05 4.11c-.05.23-.09.46-.09.7 0 1.66 1.34 3 3 3s3-1.34 3-3-1.34-3-3-3z"/></svg>
            </div>
        `;

        // Add event listeners
        actions.querySelectorAll('.social-action').forEach(action => {
            action.addEventListener('click', () => this.handleAction(action.dataset.action, action.dataset.id, status));
        });

        return actions;
    }

    /**
     * Handle social action
     */
    async handleAction(action, postId, status) {
        if (!this.client.isAuthenticated()) {
            this.showSignInModal();
            return;
        }

        try {
            let result;
            
            switch (action) {
                case 'favourite':
                    result = await this.client.favourite(postId);
                    break;
                case 'reblog':
                    result = await this.client.reblog(postId);
                    break;
                case 'reply':
                    // Open reply composer
                    const replyContent = prompt('Enter your reply:');
                    if (replyContent) {
                        result = await this.client.post(replyContent, 'public');
                    }
                    break;
                case 'share':
                    // Copy link to clipboard
                    navigator.clipboard.writeText(status.url);
                    alert('Link copied to clipboard!');
                    return;
            }

            if (result && result.status === 'success') {
                // Update UI
                if (typeof loadFeed === 'function') {
                    loadFeed();
                }
            }
        } catch (error) {
            console.error('[SocialUI] Action error:', error);
        }
    }
}

// Export for use in other scripts
window.SocialClient = SocialClient;
window.SocialUI = SocialUI;
window.MASTODON_INSTANCES = MASTODON_INSTANCES;