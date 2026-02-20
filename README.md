# PR Dashboard

GitHub Pages dashboard for visualizing Pull Request metrics from `masmovil/infrastructure`.

## Features

- 📊 Global PR metrics (all open PRs)
- 🎯 Cloud SRE specific metrics (team-review-requested)
- 📈 Age distribution and draft status tracking
- 🔄 Daily updates via GitHub Actions

## Live Dashboard

🔗 [View Dashboard](https://elenacvas.github.io/pr-dashboard)

## Architecture

- **Data Source:** GitHub API (masmovil/infrastructure)
- **Generation:** Python + PyGithub + Jinja2
- **Automation:** GitHub Actions (daily cron)
- **Hosting:** GitHub Pages

## Local Development

```bash
# Install dependencies
pip install -r scripts/requirements.txt

# Generate dashboard locally
export GITHUB_TOKEN="ghp_xxx"
python scripts/generate_dashboard.py --repo masmovil/infrastructure --output dist/

# View locally
open dist/index.html
```

## Design Document

See [Design Doc](docs/design/2026-02-20-pr-dashboard-design.md) for architecture details.

## Usage

### Manual Generation

Generate dashboard locally for testing:

```bash
# Set your GitHub token
export GITHUB_TOKEN="ghp_xxx"

# Generate dashboard
python scripts/generate_dashboard.py \
  --repo masmovil/infrastructure \
  --output dist

# View locally
open dist/index.html
```

### Automated Updates

The dashboard updates automatically via GitHub Actions:
- **Schedule:** Daily at 9:00 AM CET (8:00 AM UTC)
- **Trigger:** GitHub Actions workflow
- **Deployment:** GitHub Pages (gh-pages branch)

*(Note: GitHub Action setup pending - currently manual generation)*

## Metrics Tracked

### Global Metrics
- Total open PRs
- Draft vs non-draft count
- Age distribution (<1d, <2d, ..., >20d)

### Cloud SRE Metrics
- PRs pending Cloud SRE review
- Draft vs non-draft (Cloud SRE)
- Age distribution (Cloud SRE)

## Project Structure

```
pr-dashboard/
├── .github/workflows/     # GitHub Actions (pending)
├── scripts/               # Python generator
│   ├── generate_dashboard.py
│   ├── requirements.txt
│   ├── templates/         # Jinja2 templates
│   └── validate_dashboard.sh
├── static/                # CSS and assets
├── docs/                  # Documentation
└── dist/                  # Generated output (gitignored)
```

## Troubleshooting

### Dashboard not updating
- Check GitHub Actions for errors (when configured)
- Verify `GITHUB_TOKEN` is valid
- Check token has `repo` scope for masmovil/infrastructure

### Metrics seem wrong
- Run locally to verify data
- Check GitHub API rate limits
- Verify repository access permissions

### Charts not rendering
- Check browser console for JavaScript errors
- Verify Chart.js CDN is accessible
- Ensure metrics data is embedded in HTML
