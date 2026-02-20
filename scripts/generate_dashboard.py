#!/usr/bin/env python3
"""
Generate PR Dashboard for masmovil/infrastructure
"""
import os
import sys
import argparse
from datetime import datetime
from github import Github


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


def main():
    """Main entry point."""
    args = parse_args()

    if not args.token:
        print("ERROR: GitHub token required. Set GITHUB_TOKEN or use --token", file=sys.stderr)
        sys.exit(1)

    print("PR Dashboard Generator")
    print(f"Repository: {args.repo}")
    print(f"Output: {args.output}")
    print(f"Generated at: {datetime.now().isoformat()}")


if __name__ == "__main__":
    main()
