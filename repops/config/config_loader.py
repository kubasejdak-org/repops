"""
Configuration module for loading and managing repository configurations.
"""

from pathlib import Path
from typing import Any, Dict

import yaml

from repops.core.repository import Repository, RepositoryManager


class ConfigLoader:
    """Class for loading repository configurations."""

    @staticmethod
    def load_from_file(config_path: Path) -> RepositoryManager:
        """Load repository configurations from a file.

        Args:
            config_path: Path to configuration file

        Returns:
            Repository manager with loaded repositories

        Raises:
            FileNotFoundError: If configuration file doesn't exist
            ValueError: If configuration file is invalid
        """
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file {config_path} not found")

        try:
            with open(config_path, "r") as file:
                config_data = yaml.safe_load(file)
        except Exception as e:
            raise ValueError(f"Failed to load configuration: {e}")

        return ConfigLoader._create_repository_manager(config_data)

    @staticmethod
    def _create_repository_manager(config_data: Dict[str, Any]) -> RepositoryManager:
        """Create a repository manager from configuration data.

        Args:
            config_data: Parsed configuration data

        Returns:
            Repository manager with repositories from configuration

        Raises:
            ValueError: If configuration data is invalid
        """
        if "repositories" not in config_data:
            raise ValueError("No repositories defined in configuration")

        repo_manager = RepositoryManager()

        for repo_config in config_data["repositories"]:
            try:
                repo = Repository(
                    name=repo_config["name"],
                    path=Path(repo_config["path"]),
                    main_branch=repo_config.get("main_branch", "main"),
                    language=repo_config["language"],
                    remote_url=repo_config.get("remote_url"),
                )
                repo_manager.add_repository(repo)
            except KeyError as e:
                print(f"Warning: Skipping invalid repository configuration: {e}")

        return repo_manager


def get_sample_config() -> Dict[str, Any]:
    """Generate a sample configuration.

    Returns:
        Sample configuration dictionary
    """
    return {
        "repositories": [
            {
                "name": "repo1",
                "path": "/path/to/repo1",
                "main_branch": "main",
                "language": "python",
                "remote_url": "https://github.com/username/repo1.git",
            },
            {
                "name": "repo2",
                "path": "/path/to/repo2",
                "main_branch": "master",
                "language": "javascript",
                "remote_url": "https://github.com/username/repo2.git",
            },
        ]
    }
