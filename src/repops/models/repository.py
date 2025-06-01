"""Data models for repops application."""

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any


class ServerType(Enum):
    """Supported git server types."""

    GITHUB = "github"
    AZURE_DEVOPS = "azure-devops"
    GITLAB = "gitlab"

    @classmethod
    def from_string(cls, value: str) -> "ServerType":
        """Create ServerType from string value."""
        try:
            return cls(value.lower())
        except ValueError:
            from repops.exceptions import InvalidServerTypeError

            raise InvalidServerTypeError(value, [t.value for t in cls])


@dataclass
class Repository:
    """Represents a git repository configuration."""

    name: str
    url: str
    server_type: ServerType
    local_path: Path
    default_branch: str
    group: str = "default"

    def __post_init__(self) -> None:
        """Validate repository configuration after initialization."""
        if isinstance(self.local_path, str):
            self.local_path = Path(self.local_path)
        if isinstance(self.server_type, str):
            self.server_type = ServerType.from_string(self.server_type)

    @classmethod
    def from_dict(cls, name: str, data: dict[str, Any], group: str = "default") -> "Repository":
        """Create Repository from dictionary data."""
        from repops.exceptions import MissingRequiredFieldError

        required_fields = ["url", "server", "path", "defaultBranch"]
        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            raise MissingRequiredFieldError(missing_fields[0], f"repository '{name}' in group '{group}'")

        return cls(
            name=name,
            url=data["url"],
            server_type=ServerType.from_string(data["server"]),
            local_path=Path(data["path"]),
            default_branch=data["defaultBranch"],
            group=group,
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert Repository to dictionary."""
        return {
            "url": self.url,
            "server": self.server_type.value,
            "path": str(self.local_path),
            "defaultBranch": self.default_branch,
        }


@dataclass
class RepositoryConfig:
    """Configuration containing multiple repositories organized by groups."""

    repositories: dict[str, Repository]
    groups: dict[str, list[str]]

    def __init__(self) -> None:
        self.repositories = {}
        self.groups = {"default": []}

    def add_repository(self, repository: Repository) -> None:
        """Add a repository to the configuration."""
        self.repositories[repository.name] = repository

        if repository.group not in self.groups:
            self.groups[repository.group] = []

        if repository.name not in self.groups[repository.group]:
            self.groups[repository.group].append(repository.name)

    def remove_repository(self, name: str) -> None:
        """Remove a repository from the configuration."""
        if name not in self.repositories:
            return

        repo = self.repositories[name]
        if repo.group in self.groups and name in self.groups[repo.group]:
            self.groups[repo.group].remove(name)

        del self.repositories[name]

    def get_repositories_by_group(self, group: str) -> list[Repository]:
        """Get all repositories in a specific group."""
        if group not in self.groups:
            return []

        return [self.repositories[name] for name in self.groups[group] if name in self.repositories]

    def get_all_repositories(self) -> list[Repository]:
        """Get all repositories across all groups."""
        return list(self.repositories.values())

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "RepositoryConfig":
        """Create RepositoryConfig from dictionary data."""
        config = cls()

        for key, value in data.items():
            if isinstance(value, dict) and all(isinstance(v, dict) for v in value.values()):
                # This is a group with repositories
                for repo_name, repo_data in value.items():
                    repository = Repository.from_dict(repo_name, repo_data, group=key)
                    config.add_repository(repository)
            elif isinstance(value, dict):
                # This is a top-level repository (default group)
                repository = Repository.from_dict(key, value, group="default")
                config.add_repository(repository)

        return config

    def to_dict(self) -> dict[str, Any]:
        """Convert RepositoryConfig to dictionary."""
        result: dict[str, Any] = {}

        for group_name, repo_names in self.groups.items():
            if not repo_names:
                continue

            if group_name == "default":
                # Add default group repositories at top level
                for repo_name in repo_names:
                    if repo_name in self.repositories:
                        result[repo_name] = self.repositories[repo_name].to_dict()
            else:
                # Add grouped repositories under group name
                group_data = {}
                for repo_name in repo_names:
                    if repo_name in self.repositories:
                        group_data[repo_name] = self.repositories[repo_name].to_dict()
                if group_data:
                    result[group_name] = group_data

        return result
