#!/bin/bash
# ============================================================
#  OROBOROS DEPLOY PIPELINE
#  Pushes local world-feed updates to GitHub Pages (gh-pages)
#  Usage: bash deploy.sh "Optional commit message"
#  A\ 1272 Hz
# ============================================================

set -e

SITE_DIR="C:/Users/incoguser/world-feed"
REMOTE="origin"
REPO_URL="https://github.com/oroboroslabs-ai/world-feed.git"
BRANCH="gh-pages"
TIMESTAMP=$(date +%Y.%m.%d.%H%M)
MSG="${1:-Auto-deploy WorldFeed update — $TIMESTAMP}"

echo ""
echo "============================================================"
echo "  OROBOROS DEPLOY PIPELINE"
echo "  Source:  $SITE_DIR"
echo "  Target:  $REPO_URL ($BRANCH)"
echo "  Message: $MSG"
echo "  A\\ 1272 Hz"
echo "============================================================"
echo ""

# --- Step 0: Verify we're in the right place ---
cd "$SITE_DIR"
if [ ! -d ".git" ]; then
    echo "ERROR: No .git directory found in $SITE_DIR"
    exit 1
fi
echo "[0/5] Verified git repository at $SITE_DIR"

# --- Step 1: Ensure .nojekyll exists (bypass Jekyll) ---
if [ ! -f ".nojekyll" ]; then
    echo "# .nojekyll — Bypass GitHub Pages Jekyll processing" > .nojekyll
    echo "[1/5] Created .nojekyll file"
else
    echo "[1/5] .nojekyll already exists"
fi

# --- Step 2: Stage ALL changes (including untracked files) ---
git add -A
echo "[2/5] Staged all changes"

# --- Step 3: Commit (fail gracefully if nothing to commit) ---
if git diff --cached --quiet; then
    echo "[3/5] No changes to commit — working tree is clean"
    echo "       The live site should already be up to date."
else
    git commit -m "$MSG"
    echo "[3/5] Committed: $MSG"
fi

# --- Step 4: Ensure gh-pages branch exists and switch to it ---
# Check if gh-pages branch exists locally
if git show-ref --verify --quiet refs/heads/$BRANCH; then
    git checkout $BRANCH
    echo "[4/5] Switched to existing $BRANCH branch"
else
    # Create gh-pages as an orphan branch (clean history)
    git checkout --orphan $BRANCH
    git add -A
    git commit -m "Initialize gh-pages — $TIMESTAMP"
    echo "[4/5] Created new $BRANCH branch (orphan)"
fi

# --- Step 5: Force push to remote ---
git push -u $REMOTE $BRANCH --force
echo "[5/5] Force pushed to $REMOTE/$BRANCH"

echo ""
echo "============================================================"
echo "  DEPLOY COMPLETE"
echo "  Live site: https://oroboroslabs-ai.github.io/world-feed/"
echo "  Deployed:  $TIMESTAMP"
echo "  A\\ 1272 Hz"
echo "============================================================"