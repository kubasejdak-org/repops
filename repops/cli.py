"""
Command-line interface module for repops.
"""

import argparse
from pathlib import Path


def create_parser() -> argparse.ArgumentParser:
    """Create the command-line argument parser.

    Returns:
        Configured argument parser
    """
    parser = argparse.ArgumentParser(description="Repops - A tool for managing multiple code repositories")

    # Configuration
    parser.add_argument("-c", "--config", type=Path, help="Path to configuration file")

    # Create a subparser for different operations
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Pull command
    pull_parser = subparsers.add_parser("pull", help="Pull changes from remotes")
    pull_parser.add_argument("--language", help="Filter repositories by language")

    # Branch command
    branch_parser = subparsers.add_parser("branch", help="Create a new branch")
    branch_parser.add_argument("branch_name", help="Name of the branch to create")
    branch_parser.add_argument("--language", help="Filter repositories by language")

    # PR command
    pr_parser = subparsers.add_parser("pr", help="Create pull requests")
    pr_parser.add_argument("--title", required=True, help="Title of the pull request")
    pr_parser.add_argument("--description", help="Description of the pull request")
    pr_parser.add_argument("--language", help="Filter repositories by language")

    # Pipeline command
    pipeline_parser = subparsers.add_parser("pipeline", help="Execute a sequence of operations")
    pipeline_parser.add_argument("--pull", action="store_true", help="Include pull operation in pipeline")
    pipeline_parser.add_argument("--branch", help="Create a branch (specify branch name)")
    pipeline_parser.add_argument("--pr", action="store_true", help="Create pull requests (requires --pr-title)")
    pipeline_parser.add_argument("--pr-title", help="Title for pull requests")
    pipeline_parser.add_argument("--pr-description", help="Description for pull requests")
    pipeline_parser.add_argument("--language", help="Filter repositories by language")

    return parser


def parse_args(args=None):
    """Parse command line arguments.

    Args:
        args: Command line arguments (defaults to sys.argv[1:])

    Returns:
        Parsed arguments
    """
    parser = create_parser()
    return parser.parse_args(args)
