# PR Dashboard Design - GitHub Metrics Visualization

**Date:** 2026-02-20
**Author:** Elena Cuevas
**Status:** Approved

## Overview

Dashboard for visualizing Pull Request metrics from `masmovil/infrastructure` repository with global and Cloud SRE-specific views. Prototyped on personal GitHub Pages, designed for future migration to Grafana.

## Requirements

### Metrics to Track

**Global (All PRs):**
- Total PRs open (draft + non-draft)
- PRs opened per day/hour
- PRs by age buckets: <1d, <2d, <3d, <4d, <5d, <7d, <15d, <20d, >20d
- Draft vs non-draft distribution

**Cloud SRE Specific:**
- PRs pending review by `masmovil/cloud-sre` team
- Age distribution of PRs awaiting Cloud SRE review
- PRs resolved by Cloud SRE (weekly/monthly)
- Draft vs non-draft awaiting Cloud SRE

### Update Frequency

- **GitHub Pages (MVP):** Daily at 9:00 AM CET
- **Grafana (future):** Every 5 minutes (if no cost) or every 12 hours (if cost exists)

### Scope

- Repository: `masmovil/infrastructure` only
- Team identification: Based on actual PR reviewers (`pr.requested_teams`), not inferred from CODEOWNERS
- Authentication: Personal Access Token (PAT) for prototype, GitHub App for production

## Architecture

### Selected Approach: Python + Static HTML + GitHub Actions

**Rationale:**
- Simple and maintainable (Python familiar to infrastructure teams)
- Zero cost (GitHub Actions + GitHub Pages free)
- Easy migration path to Grafana (same script, different output)
- Fast load times (static HTML)

**Components:**

1. **Python Script (`generate_dashboard.py`)**
   - Uses PyGithub to query GitHub API
   - Extracts metrics from PR data
   - Generates static HTML using Jinja2 templates

2. **GitHub Action (`.github/workflows/pr-dashboard.yml`)**
   - Runner: `general-ubuntu` (self-hosted, matching existing workflows)
   - Schedule: Daily cron at 8:00 AM UTC (9:00 AM CET)
   - Generates token from GitHub App (same pattern as `label-stale-prs.yml`)
   - Publishes to GitHub Pages (`gh-pages` branch)

3. **Static Dashboard**
   - HTML with Chart.js visualizations
   - MasOrange corporate identity (colors, fonts, logo)
   - Responsive design

4. **Historical Data (Future)**
   - Append-only JSON Lines file (`history.jsonl`)
   - Separate trends page for historical analysis

### Data Flow

```
GitHub API → Python Script → Calculate Metrics → Jinja2 Template → HTML/CSS/JS → GitHub Pages
                                                         ↓
                                                   history.jsonl (append daily)
```

## Team Assignment Strategy

### Using Real Reviewers (Not CODEOWNERS)

For each PR, extract teams directly from GitHub API:
```python
pr.requested_teams  # List of teams like @masmovil/cloud-sre
```

**Advantages:**
- Reflects actual reviewer assignments
- Captures manual reviewer changes
- Simpler implementation (no CODEOWNERS parsing)
- More accurate data

**Edge Cases:**
- PRs without team reviewers → "No team assigned" category
- PRs with multiple teams → Count in each team's metrics (correct behavior)

## Dashboard Structure

### Two-Level View

**Level 1: Global Metrics**
```
📊 GLOBAL - masmovil/infrastructure
Total PRs: 45    Draft: 12    No-Draft: 33
[Chart: PRs by age buckets]
[Chart: PRs opened last 7 days]
```

**Level 2: Cloud SRE Metrics**
```
🎯 CLOUD SRE - Pending Review
Pending: 18    Draft: 3    No-Draft: 15
[Chart: Age distribution of Cloud SRE PRs]
[Table: Breakdown <1d, <2d, ..., >20d]
PRs closed this week: 12
```

## Data Pipeline

### Extraction Queries

**Global - All open PRs:**
```bash
gh pr list --state open --json number,title,createdAt,isDraft,reviewRequests
```

**Cloud SRE - Pending review:**
```bash
gh pr list --search "team-review-requested:masmovil/cloud-sre" \
           --state open --json number,title,createdAt,isDraft
```

**Cloud SRE - Resolved PRs:**
```bash
gh pr list --search "team-review-requested:masmovil/cloud-sre is:merged updated:>=YYYY-MM-DD"
```

### Metrics Calculation

```python
metrics = {
    "global": {
        "total_open": int,
        "draft": int,
        "non_draft": int,
        "age_buckets": {
            "<1d": int, "<2d": int, "<3d": int, "<4d": int,
            "<5d": int, "<7d": int, "<15d": int, "<20d": int, ">20d": int
        },
        "prs_opened_by_day": [{"date": str, "count": int}, ...]
    },
    "cloud_sre": {
        "pending": int,
        "draft": int,
        "non_draft": int,
        "age_buckets": {...},
        "resolved_this_week": int
    },
    "last_updated": str  # ISO 8601 timestamp
}
```

### Age Bucket Logic

For each PR: `age_days = (now - pr.created_at).days`

- `< 1 día`: age_days < 1
- `< 2 días`: 1 <= age_days < 2
- `< 3 días`: 2 <= age_days < 3
- `< 4 días`: 3 <= age_days < 4
- `< 5 días`: 4 <= age_days < 5
- `< 7 días`: 5 <= age_days < 7
- `< 15 días`: 7 <= age_days < 15
- `< 20 días`: 15 <= age_days < 20
- `> 20 días`: age_days >= 20

## Technical Implementation

### Project Structure

```
pr-dashboard/
├── .github/
│   └── workflows/
│       └── pr-dashboard.yml          # GitHub Action with self-hosted runner
├── scripts/
│   ├── generate_dashboard.py         # Main Python script
│   ├── requirements.txt               # PyGithub, Jinja2, requests
│   └── templates/
│       ├── index.html.j2              # Main dashboard template
│       └── trends.html.j2             # Trends page (future)
├── static/
│   ├── style.css                      # MasOrange styles
│   └── logo.png                       # MasOrange logo
└── README.md
```

### Dependencies

```
PyGithub==2.1.1
Jinja2==3.1.3
python-dateutil==2.8.2
```

### GitHub Action Configuration

**Key settings:**
- `runs-on: general-ubuntu` (self-hosted runner)
- `cron: '0 8 * * *'` (daily 9:00 AM CET)
- `workflow_dispatch` (manual trigger)
- Token generation from GitHub App (matching `label-stale-prs.yml` pattern)
- Publish to `gh-pages` branch of personal repo

**Required Secrets:**
- `DASHBOARD_APP_ID` (GitHub App ID)
- `DASHBOARD_APP_PRIVATE_KEY` (GitHub App private key)

### Visualizations

**Chart.js components:**
1. Horizontal bar chart: PR age buckets
2. Donut/Pie chart: Draft vs No-Draft
3. Line chart: PRs opened over time (last 7 days)
4. Number cards: Totals and key metrics

**MasOrange Corporate Identity:**
- Primary: Orange #FF7800
- Text: Black #000000
- Secondary: Gray #86868E
- Warnings: Yellow #FFE000 (for PRs >15 days)
- Font: Arial

### Error Handling

**Scenarios:**
- GitHub API rate limit → Display message in dashboard + retry with backoff
- Invalid token → Fail GitHub Action with clear error
- No historical data → Initialize empty `history.jsonl`
- No PRs found → Display "No open PRs" (not an error)

## Testing Strategy

### Local Development

```bash
export GITHUB_TOKEN="ghp_xxx"
python scripts/generate_dashboard.py --repo masmovil/infrastructure --output test_output/
open test_output/index.html
```

### GitHub Action Testing

```bash
# Manual trigger
gh workflow run pr-dashboard.yml

# Check logs
gh run list --workflow=pr-dashboard.yml
gh run view <run-id> --log
```

### Data Validation

Script must verify:
- ✅ Token has read permissions to repo
- ✅ At least 1 PR found (if not, warning but not error)
- ✅ Age buckets sum to total PRs
- ✅ Generated JSON is valid
- ✅ HTML renders correctly

### Visual Validation Checklist

- [ ] Dashboard loads on GitHub Pages
- [ ] MasOrange logo visible
- [ ] Charts render correctly
- [ ] Corporate colors applied
- [ ] Numbers match GitHub UI
- [ ] Responsive on mobile/tablet

## Success Criteria

### Phase 1: Prototype (Personal Repo)

- ✅ Dashboard updates daily without errors
- ✅ Metrics accurate vs GitHub UI
- ✅ Loads in <2 seconds
- ✅ Positive feedback from Cloud SRE team

### Phase 2: Production (Future Decision)

- Evaluate migration to Grafana
- Evaluate publishing on corporate domain
- Evaluate adding more teams beyond Cloud SRE

## Rollout Plan

### Week 1: Development
- Create repo `github.com/elenacvas/pr-dashboard`
- Implement Python script
- Configure GitHub Action with PAT

### Week 2: Testing
- Validate data vs GitHub UI
- Adjust visualizations
- Gather initial feedback

### Week 3: Production
- Migrate to GitHub App if prototype works
- Share URL with Cloud SRE team
- Evaluate next steps (Grafana, multi-team, etc.)

## Deployment Details

**Repository:** `github.com/elenacvas/pr-dashboard`
**GitHub Pages URL:** `https://elenacvas.github.io/pr-dashboard`
**Branch:** Main branch for code, `gh-pages` for published site

## Future Enhancements

**Trends Page:**
- Historical data visualization (30-90 days)
- Trend analysis (improving/worsening metrics)
- Separate page: `trends.html`

**Grafana Migration:**
- Export metrics to Prometheus/InfluxDB
- Update frequency: 5 minutes (if no cost) or 12 hours (if cost exists)
- Real-time dashboards with alerting

**Multi-Team Support:**
- Extend beyond Cloud SRE to other teams
- Team selector/filter in UI
- Comparative metrics across teams

## Migration Path to Grafana

When migrating to Grafana:

1. Same Python script extracts metrics
2. Export to time-series database (Prometheus/InfluxDB)
3. Create Grafana datasource
4. Build dashboards with Grafana UI
5. Set up alerting for old PRs (>7 days)

**Key advantage:** Core data extraction logic remains unchanged, only output format changes.
