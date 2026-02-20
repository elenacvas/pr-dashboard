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
