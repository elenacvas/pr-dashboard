#!/usr/bin/env python3
"""
Generate PR Dashboard for masmovil/infrastructure
"""
import os
import sys
import argparse
from datetime import datetime
from github import Github, Auth


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

    print("\n" + "=" * 60)
    print("✅ Data collection complete")
    print("=" * 60)


if __name__ == "__main__":
    main()
