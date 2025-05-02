"""
GitHub-specific operations for Pull Request creation.
"""

import subprocess
from typing import Optional

from repops.core.repository import Repository
from repops.operations.base import PullRequestOperation


class GitHubPullRequestOperation(PullRequestOperation):
    """Operation to create a GitHub Pull Request."""

    def __init__(self, title: str, description: Optional[str] = None, base_branch: Optional[str] = None):
        super().__init__(title, description)
        self.base_branch = base_branch

    def execute(self, repo: Repository) -> bool:
        """Create a pull request on GitHub.

        Args:
            repo: Repository to create PR for

        Returns:
            Success status
        """
        try:
            # Get the current branch
            current_branch_result = subprocess.run(
                ["git", "branch", "--show-current"], cwd=repo.path, check=True, capture_output=True, text=True
            )
            current_branch = current_branch_result.stdout.strip()

            # Determine base branch
            base = self.base_branch if self.base_branch else repo.main_branch

            # Check if there are changes to commit
            status_result = subprocess.run(
                ["git", "status", "--porcelain"], cwd=repo.path, check=True, capture_output=True, text=True
            )

            # If there are uncommitted changes, commit them
            if status_result.stdout.strip():
                subprocess.run(["git", "add", "."], cwd=repo.path, check=True, capture_output=True, text=True)

                subprocess.run(
                    ["git", "commit", "-m", self.title], cwd=repo.path, check=True, capture_output=True, text=True
                )

                print(f"Committed changes in {repo.name}")

            # Push the branch
            subprocess.run(
                ["git", "push", "-u", "origin", current_branch],
                cwd=repo.path,
                check=True,
                capture_output=True,
                text=True,
            )

            # Create the PR using gh CLI if available
            pr_result = subprocess.run(
                ["gh", "pr", "create", "--title", self.title, "--body", self.description or "", "--base", base],
                cwd=repo.path,
                check=True,
                capture_output=True,
                text=True,
            )

            pr_url = pr_result.stdout.strip()
            print(f"Created PR for {repo.name}: {pr_url}")
            return True

        except subprocess.CalledProcessError as e:
            print(f"Failed to create PR for {repo.name}: {e.stderr}")
            return False
        except Exception as e:
            print(f"Error creating PR for {repo.name}: {e}")
            return False

    def get_name(self) -> str:
        return "GitHub Pull Request Creation"
