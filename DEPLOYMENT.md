# Dashboard Deployment

## Live URL
https://elenacvas.github.io/pr-dashboard

## Initial Deployment
**Date:** 2026-02-20 22:03 CET

**Deployment Method:** Manual deployment to GitHub Pages

## Current Metrics
- Total PRs: 130 (41 draft, 89 non-draft)
- Cloud SRE PRs: 50 (13 draft, 37 non-draft)

## Deployment Process

### 1. Generated Dashboard
```bash
python scripts/generate_dashboard.py --repo masmovil/infrastructure --output dist
```

### 2. Created gh-pages Branch
```bash
git checkout --orphan gh-pages
git rm -rf .
cp -r dist/* .
git add index.html static/
git commit -m "docs: initial dashboard deployment"
git push -u origin gh-pages
```

### 3. Enable GitHub Pages (Manual)
Go to: https://github.com/elenacvas/pr-dashboard/settings/pages

Settings:
- Source: Deploy from a branch
- Branch: `gh-pages` / `root`

### 4. Verification
Wait 1-2 minutes, then visit: https://elenacvas.github.io/pr-dashboard

## Next Steps

### Automated Deployment (Monday)
GitHub Action will be configured to:
1. Run daily at 08:00 CET
2. Fetch latest PR data
3. Regenerate dashboard
4. Deploy to gh-pages automatically

### Manual Updates (Until Monday)
To update the dashboard manually:

```bash
# Generate fresh dashboard
source .venv/bin/activate
export GITHUB_TOKEN=$(gh auth token)
python scripts/generate_dashboard.py --repo masmovil/infrastructure --output dist

# Deploy to gh-pages
git checkout gh-pages
cp -r dist/* .
git add index.html static/
git commit -m "docs: update dashboard $(date +%Y-%m-%d)"
git push
git checkout main
```

## Repository Structure

```
pr-dashboard/
├── main branch              # Source code
│   ├── scripts/
│   │   ├── generate_dashboard.py
│   │   └── templates/
│   ├── static/
│   └── dist/               # Generated output
└── gh-pages branch         # Deployment
    ├── index.html
    └── static/
```

## Troubleshooting

### Dashboard Not Loading
1. Check GitHub Pages status: Settings → Pages
2. Verify gh-pages branch exists and has index.html
3. Wait 2-3 minutes after pushing changes

### Data Not Updating
1. Regenerate dashboard with fresh data
2. Commit and push to gh-pages branch
3. Clear browser cache

### Authentication Issues
```bash
# Verify GitHub token
gh auth status

# Refresh if needed
gh auth refresh
```
