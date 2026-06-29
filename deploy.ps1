# ============================================================
#  OROBOROS DEPLOY PIPELINE (PowerShell)
#  Pushes local world-feed updates to GitHub Pages (gh-pages)
#  Usage: .\deploy.ps1 "Optional commit message"
#  A\ 1272 Hz
# ============================================================

param(
    [string]$CommitMessage = ""
)

$ErrorActionPreference = "Stop"
$SiteDir = "C:\Users\incoguser\world-feed"
$Remote = "origin"
$RepoUrl = "https://github.com/oroboroslabs-ai/world-feed.git"
$Branch = "gh-pages"
$Timestamp = Get-Date -Format "yyyy.MM.dd.HHmm"

if ([string]::IsNullOrWhiteSpace($CommitMessage)) {
    $CommitMessage = "Auto-deploy WorldFeed update - $Timestamp"
}

Write-Host ""
Write-Host "============================================================"
Write-Host "  OROBOROS DEPLOY PIPELINE"
Write-Host "  Source:  $SiteDir"
Write-Host "  Target:  $RepoUrl ($Branch)"
Write-Host "  Message: $CommitMessage"
Write-Host "  A\ 1272 Hz"
Write-Host "============================================================"
Write-Host ""

# --- Step 0: Verify we are in the right place ---
Set-Location $SiteDir
if (-not (Test-Path ".git")) {
    Write-Host "ERROR: No .git directory found in $SiteDir" -ForegroundColor Red
    exit 1
}
Write-Host "[0/5] Verified git repository at $SiteDir"

# --- Step 1: Ensure .nojekyll exists (bypass Jekyll) ---
if (-not (Test-Path ".nojekyll")) {
    "# .nojekyll - Bypass GitHub Pages Jekyll processing" | Out-File -FilePath ".nojekyll" -Encoding utf8
    Write-Host "[1/5] Created .nojekyll file"
} else {
    Write-Host "[1/5] .nojekyll already exists"
}

# --- Step 2: Stage ALL changes (including untracked files) ---
git add -A
Write-Host "[2/5] Staged all changes"

# --- Step 3: Commit (skip if nothing to commit) ---
$status = git status --porcelain
if ([string]::IsNullOrWhiteSpace($status)) {
    Write-Host "[3/5] No changes to commit - working tree is clean"
    Write-Host "       The live site should already be up to date."
} else {
    git commit -m $CommitMessage
    Write-Host "[3/5] Committed: $CommitMessage"
}

# --- Step 4: Ensure gh-pages branch exists and switch to it ---
$branches = git branch --list $Branch
if ($branches -match $Branch) {
    git checkout $Branch
    Write-Host "[4/5] Switched to existing $Branch branch"
} else {
    git checkout --orphan $Branch
    git add -A
    git commit -m "Initialize gh-pages - $Timestamp"
    Write-Host "[4/5] Created new $Branch branch (orphan)"
}

# --- Step 5: Force push to remote ---
git push -u $Remote $Branch --force
Write-Host "[5/5] Force pushed to $Remote/$Branch"

Write-Host ""
Write-Host "============================================================"
Write-Host "  DEPLOY COMPLETE"
Write-Host "  Live site: https://oroboroslabs-ai.github.io/world-feed/"
Write-Host "  Deployed:  $Timestamp"
Write-Host "  A\ 1272 Hz"
Write-Host "============================================================"