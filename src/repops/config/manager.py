"""Configuration management for repops application."""

import logging
from pathlib import Path
from typing import Any

import yaml

from repops.exceptions import ConfigError, FileNotFoundError, InvalidConfigError
from repops.models import RepositoryConfig

logger = logging.getLogger(__name__)


class ConfigManager:
    """Manages loading, saving, and validation of repository configurations."""

    DEFAULT_CONFIG_PATH = Path.home() / ".config" / "repops" / "repos.yml"

    def __init__(self, config_path: Path | None = None) -> None:
        """Initialize ConfigManager with optional custom config path."""
        self.config_path = config_path or self.DEFAULT_CONFIG_PATH
        self._config: RepositoryConfig | None = None

    @property
    def config(self) -> RepositoryConfig:
        """Get the current configuration, loading it if necessary."""
        if self._config is None:
            self.load_config()
        assert self._config is not None
        return self._config

    def load_config(self, config_path: Path | None = None) -> RepositoryConfig:
        """Load repository configuration from YAML file."""
        if config_path:
            self.config_path = config_path

        if not self.config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")

        try:
            with self.config_path.open("r") as file:
                data = yaml.safe_load(file)

            if data is None:
                data = {}

            self._config = RepositoryConfig.from_dict(data)
            logger.info(f"Loaded configuration from {self.config_path}")
            return self._config

        except yaml.YAMLError as e:
            raise InvalidConfigError(f"Invalid YAML in config file: {e}")
        except Exception as e:
            raise ConfigError(f"Failed to load configuration: {e}")

    def save_config(self, config_path: Path | None = None) -> None:
        """Save current configuration to YAML file."""
        if config_path:
            self.config_path = config_path

        if self._config is None:
            raise ConfigError("No configuration to save")

        try:
            # Ensure directory exists
            self.config_path.parent.mkdir(parents=True, exist_ok=True)

            with self.config_path.open("w") as file:
                yaml.dump(
                    self._config.to_dict(),
                    file,
                    default_flow_style=False,
                    sort_keys=False,
                    indent=2,
                )

            logger.info(f"Saved configuration to {self.config_path}")

        except Exception as e:
            raise ConfigError(f"Failed to save configuration: {e}")

    def create_new_config(self) -> RepositoryConfig:
        """Create a new empty configuration."""
        self._config = RepositoryConfig()
        return self._config

    def validate_config(self) -> list[str]:
        """Validate the current configuration and return list of issues."""
        if self._config is None:
            return ["No configuration loaded"]

        issues = []

        for repo in self._config.get_all_repositories():
            # Check if local path is absolute
            if not repo.local_path.is_absolute():
                issues.append(f"Repository '{repo.name}': local path must be absolute")

            # Check if URL is not empty
            if not repo.url.strip():
                issues.append(f"Repository '{repo.name}': URL cannot be empty")

            # Check if default branch is not empty
            if not repo.default_branch.strip():
                issues.append(f"Repository '{repo.name}': default branch cannot be empty")

        return issues

    def get_config_info(self) -> dict[str, Any]:
        """Get information about the current configuration."""
        if self._config is None:
            return {"loaded": False, "path": str(self.config_path)}

        all_repos = self._config.get_all_repositories()
        groups_info = {}

        for group_name, repo_names in self._config.groups.items():
            if repo_names:
                groups_info[group_name] = len(repo_names)

        return {
            "loaded": True,
            "path": str(self.config_path),
            "total_repositories": len(all_repos),
            "groups": groups_info,
            "server_types": {
                server_type.value: len([r for r in all_repos if r.server_type == server_type])
                for server_type in {r.server_type for r in all_repos}
            },
        }
