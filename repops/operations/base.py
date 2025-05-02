"""
Operation module defining the base operation interface and common operations.
"""

from abc import ABC, abstractmethod
from typing import Optional

from repops.core.repository import Repository


class Operation(ABC):
    """Base class for repository operations."""

    @abstractmethod
    def execute(self, repo: Repository) -> bool:
        """Execute the operation on a repository.

        Args:
            repo: Repository to operate on

        Returns:
            Success status
        """
        pass

    @abstractmethod
    def get_name(self) -> str:
        """Get the name of the operation.

        Returns:
            Operation name
        """
        pass


class GitOperation(Operation):
    """Base class for Git-specific operations."""

    def execute(self, repo: Repository) -> bool:
        """Execute a Git operation.

        Args:
            repo: Repository to operate on

        Returns:
            Success status
        """
        # Implementation will be specific to child classes
        raise NotImplementedError()

    def get_name(self) -> str:
        return "Git Operation"


class PullRequestOperation(GitOperation):
    """Operation for creating pull requests."""

    def __init__(self, title: str, description: Optional[str] = None):
        self.title = title
        self.description = description

    def execute(self, repo: Repository) -> bool:
        """Create a pull request for the repository.

        Args:
            repo: Repository to create PR for

        Returns:
            Success status
        """
        # Placeholder for PR creation logic
        print(f"Creating PR for {repo.name}: {self.title}")
        return True

    def get_name(self) -> str:
        return "Pull Request Creation"
