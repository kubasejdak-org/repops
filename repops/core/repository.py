"""
Repository module for handling repository operations.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class Repository:
    """Class representing a code repository."""

    name: str
    path: Path
    main_branch: str
    language: str
    remote_url: Optional[str] = None

    def __str__(self) -> str:
        return f"{self.name} ({self.path})"


class RepositoryManager:
    """Class for managing multiple repositories."""

    def __init__(self):
        self.repositories = []

    def add_repository(self, repo: Repository) -> None:
        """Add a repository to the manager.

        Args:
            repo: Repository to add
        """
        self.repositories.append(repo)

    def get_repositories(self) -> list[Repository]:
        """Get all managed repositories.

        Returns:
            List of managed repositories
        """
        return self.repositories

    def filter_repositories(self, language: Optional[str] = None) -> list[Repository]:
        """Filter repositories by language.

        Args:
            language: Programming language to filter by

        Returns:
            Filtered list of repositories
        """
        if language is None:
            return self.repositories

        return [repo for repo in self.repositories if repo.language == language]
