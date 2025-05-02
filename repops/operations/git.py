"""
Git operations for repository management.
"""

import subprocess

from repops.core.repository import Repository
from repops.operations.base import GitOperation


class GitPullOperation(GitOperation):
    """Operation to pull latest changes from a git repository."""

    def execute(self, repo: Repository) -> bool:
        """Pull latest changes from the repository's remote.

        Args:
            repo: Repository to pull from

        Returns:
            Success status
        """
        try:
            result = subprocess.run(
                ["git", "pull", "origin", repo.main_branch], cwd=repo.path, check=True, capture_output=True, text=True
            )
            print(f"Pulled latest changes for {repo.name}: {result.stdout.strip()}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Failed to pull changes for {repo.name}: {e.stderr}")
            return False
        except Exception as e:
            print(f"Error pulling changes for {repo.name}: {e}")
            return False

    def get_name(self) -> str:
        return "Git Pull"


class GitBranchOperation(GitOperation):
    """Operation to create a new git branch."""

    def __init__(self, branch_name: str):
        self.branch_name = branch_name

    def execute(self, repo: Repository) -> bool:
        """Create a new branch in the repository.

        Args:
            repo: Repository to create branch in

        Returns:
            Success status
        """
        try:
            # First checkout main branch
            subprocess.run(
                ["git", "checkout", repo.main_branch], cwd=repo.path, check=True, capture_output=True, text=True
            )

            # Create and checkout new branch
            subprocess.run(
                ["git", "checkout", "-b", self.branch_name], cwd=repo.path, check=True, capture_output=True, text=True
            )
            print(f"Created and switched to branch {self.branch_name} in {repo.name}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Failed to create branch {self.branch_name} in {repo.name}: {e.stderr}")
            return False
        except Exception as e:
            print(f"Error creating branch in {repo.name}: {e}")
            return False

    def get_name(self) -> str:
        return f"Create Branch: {self.branch_name}"
