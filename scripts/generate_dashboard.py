#!/usr/bin/env python3
"""
Generate PR Dashboard for masmovil/infrastructure
"""
import os
import sys
import argparse
from datetime import datetime, timezone
from github import Github, Auth
import json
import shutil
from jinja2 import Environment, FileSystemLoader, select_autoescape


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Generate PR Dashboard")
    parser.add_argument(
        "--repo",
        required=True,
        help="GitHub repository in format owner/name (e.g., masmovil/infrastructure)"
    )
    parser.add_argument(
        "--output",
        default="dist",
        help="Output directory for generated dashboard (default: dist)"
    )
    parser.add_argument(
        "--token",
        default=os.environ.get("GITHUB_TOKEN"),
        help="GitHub token (default: from GITHUB_TOKEN env var)"
    )
    return parser.parse_args()


def calculate_age_bucket(created_at):
    """
    Calculate age bucket for a PR.

    Args:
        created_at: datetime object (PR creation time)

    Returns:
        str: bucket label ('<1d', '<2d', etc.)
    """
    now = datetime.now(timezone.utc)
    age_days = (now - created_at).days

    if age_days < 1:
        return '<1d'
    elif age_days < 2:
        return '<2d'
    elif age_days < 3:
        return '<3d'
    elif age_days < 4:
        return '<4d'
    elif age_days < 5:
        return '<5d'
    elif age_days < 7:
        return '<7d'
    elif age_days < 15:
        return '<15d'
    elif age_days < 20:
        return '<20d'
    else:
        return '>20d'


def calculate_age_distribution(prs):
    """
    Calculate age distribution for a list of PRs.

    Args:
        prs: List of PR objects

    Returns:
        dict: Bucket counts (e.g., {'<1d': 5, '<2d': 3, ...})
    """
    buckets = {
        '<1d': 0, '<2d': 0, '<3d': 0, '<4d': 0, '<5d': 0,
        '<7d': 0, '<15d': 0, '<20d': 0, '>20d': 0
    }

    for pr in prs:
        bucket = calculate_age_bucket(pr.created_at)
        buckets[bucket] += 1

    return buckets


def calculate_metrics(github_data):
    """
    Calculate all dashboard metrics.

    Args:
        github_data: dict with 'all_prs' and 'cloud_sre_prs'

    Returns:
        dict: All calculated metrics
    """
    all_prs = github_data['all_prs']
    cloud_sre_prs = github_data['cloud_sre_prs']

    print("\n📊 Calculating metrics...")

    # Global metrics
    total_open = len(all_prs)
    draft_count = sum(1 for pr in all_prs if pr.draft)
    non_draft_count = total_open - draft_count

    print(f"  Global: {total_open} total ({draft_count} draft, {non_draft_count} non-draft)")

    # Cloud SRE metrics
    cloud_sre_total = len(cloud_sre_prs)
    cloud_sre_draft = sum(1 for pr in cloud_sre_prs if pr.draft)
    cloud_sre_non_draft = cloud_sre_total - cloud_sre_draft

    print(f"  Cloud SRE: {cloud_sre_total} total ({cloud_sre_draft} draft, {cloud_sre_non_draft} non-draft)")

    # Age distributions
    global_age_buckets = calculate_age_distribution(all_prs)
    cloud_sre_age_buckets = calculate_age_distribution(cloud_sre_prs)

    print(f"  Age distributions calculated")

    metrics = {
        'global': {
            'total_open': total_open,
            'draft': draft_count,
            'non_draft': non_draft_count,
            'age_buckets': global_age_buckets,
        },
        'cloud_sre': {
            'total_open': cloud_sre_total,
            'draft': cloud_sre_draft,
            'non_draft': cloud_sre_non_draft,
            'age_buckets': cloud_sre_age_buckets,
        },
        'last_updated': datetime.now(timezone.utc).isoformat()
    }

    print("✅ Metrics calculated")
    return metrics


def generate_html(metrics, output_dir):
    """
    Generate HTML dashboard from metrics.

    Args:
        metrics: dict with calculated metrics
        output_dir: Output directory path
    """
    print("\n🎨 Generating HTML dashboard...")

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Copy static files to output
    static_src = os.path.join(os.path.dirname(__file__), '..', 'static')
    static_dst = os.path.join(output_dir, 'static')
    if os.path.exists(static_src):
        if os.path.exists(static_dst):
            shutil.rmtree(static_dst)
        shutil.copytree(static_src, static_dst)

    # Setup Jinja2
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    env = Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=select_autoescape(['html', 'html.j2'])
    )
    template = env.get_template('index.html.j2')

    # Render template
    html_content = template.render(
        metrics=metrics,
        metrics_json=json.dumps(metrics, indent=2)
    )

    # Write HTML file
    output_path = os.path.join(output_dir, 'index.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"✅ Dashboard generated: {output_path}")


def fetch_github_data(repo_name, token):
    """
    Fetch PR data from GitHub.

    Args:
        repo_name: Repository in format owner/name
        token: GitHub API token

    Returns:
        dict with 'all_prs' and 'cloud_sre_prs' lists
    """
    print(f"\n📡 Connecting to GitHub API...")
    auth = Auth.Token(token)
    g = Github(auth=auth)

    try:
        repo = g.get_repo(repo_name)
        print(f"✅ Connected to {repo.full_name}")
    except Exception as e:
        print(f"❌ Failed to connect to repository: {e}", file=sys.stderr)
        sys.exit(1)

    # Fetch all open PRs
    print(f"\n📊 Fetching all open PRs...")
    all_prs = list(repo.get_pulls(state='open'))
    print(f"✅ Found {len(all_prs)} open PRs")

    # Fetch Cloud SRE PRs
    print(f"\n🎯 Fetching Cloud SRE PRs...")
    # Note: PyGithub doesn't support team-review-requested search,
    # so we filter manually
    cloud_sre_prs = [
        pr for pr in all_prs
        if any(team.slug == 'cloud-sre' for team in pr.get_review_requests()[1])
    ]
    print(f"✅ Found {len(cloud_sre_prs)} PRs awaiting Cloud SRE review")

    return {
        'all_prs': all_prs,
        'cloud_sre_prs': cloud_sre_prs,
        'repo': repo
    }


def main():
    """Main entry point."""
    args = parse_args()

    if not args.token:
        print("ERROR: GitHub token required. Set GITHUB_TOKEN or use --token", file=sys.stderr)
        sys.exit(1)

    print("=" * 60)
    print("PR DASHBOARD GENERATOR")
    print("=" * 60)
    print(f"Repository: {args.repo}")
    print(f"Output: {args.output}")
    print(f"Generated at: {datetime.now().isoformat()}")

    # Fetch data from GitHub
    github_data = fetch_github_data(args.repo, args.token)

    # Calculate metrics
    metrics = calculate_metrics(github_data)

    # Generate HTML
    generate_html(metrics, args.output)

    print("\n" + "=" * 60)
    print("✅ Dashboard generation complete")
    print("=" * 60)


if __name__ == "__main__":
    main()
