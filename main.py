"""
Repops - A tool for managing multiple code repositories.
"""

import sys

from repops.cli import parse_args
from repops.config.config_loader import ConfigLoader
from repops.operations.base import PullRequestOperation
from repops.operations.git import GitBranchOperation, GitPullOperation
from repops.pipelines.pipeline import Pipeline


def main():
    """Main entry point for the application."""
    print("Welcome to Repops - Repository Operations Tool")
    args = parse_args()

    if not args.config:
        print("Error: Configuration file is required")
        print("Example: repops -c config.yaml")
        sys.exit(1)

    try:
        # Load repositories from configuration
        config_path = args.config
        repo_manager = ConfigLoader.load_from_file(config_path)

        # Filter repositories by language if specified
        if hasattr(args, "language") and args.language:
            filtered_repos = repo_manager.filter_repositories(args.language)
            repo_count = len(filtered_repos)
            # Create a new manager with only the filtered repositories
            filtered_manager = ConfigLoader._create_repository_manager({"repositories": []})
            for repo in filtered_repos:
                filtered_manager.add_repository(repo)
            repo_manager = filtered_manager
        else:
            repo_count = len(repo_manager.get_repositories())

        print(f"Loaded {repo_count} repositories from configuration")

        # Handle different commands
        if args.command == "pull":
            pipeline = Pipeline("Pull Pipeline")
            pipeline.add_operation(GitPullOperation())

        elif args.command == "branch":
            pipeline = Pipeline("Branch Pipeline")
            pipeline.add_operation(GitBranchOperation(args.branch_name))

        elif args.command == "pr":
            pipeline = Pipeline("PR Pipeline")
            pipeline.add_operation(PullRequestOperation(args.title, args.description))

        elif args.command == "pipeline":
            pipeline = Pipeline("Custom Pipeline")

            # Add operations based on arguments
            if args.pull:
                pipeline.add_operation(GitPullOperation())

            if args.branch:
                pipeline.add_operation(GitBranchOperation(args.branch))

            if args.pr:
                if not args.pr_title:
                    print("Error: --pr requires --pr-title")
                    sys.exit(1)
                pipeline.add_operation(PullRequestOperation(args.pr_title, args.pr_description))

        else:
            print("Error: No command specified")
            print("Available commands: pull, branch, pr, pipeline")
            sys.exit(1)

        # Execute the pipeline on all repositories
        if pipeline and pipeline.operations:
            results = pipeline.execute(repo_manager)
            print("Pipeline execution completed")

            # Display summary
            for repo_name, repo_results in results.items():
                success_count = sum(1 for result in repo_results if result)
                print(f"Repository: {repo_name} - {success_count}/{len(repo_results)} operations succeeded")
        else:
            print("No operations specified. Use command line arguments to specify operations.")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
