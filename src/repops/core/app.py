"""Core application logic for repops."""

import logging
from pathlib import Path
from typing import Any

from repops.config import ConfigManager
from repops.models import Repository, RepositoryConfig

logger = logging.getLogger(__name__)


class RepopsApp:
    """Main application class that coordinates all repops functionality."""

    def __init__(self, config_path: Path | None = None) -> None:
        """Initialize RepopsApp with optional custom config path."""
        self.config_manager = ConfigManager(config_path)
        self._setup_logging()

    def _setup_logging(self) -> None:
        """Configure logging for the application."""
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

    # Configuration Management
    def load_config(self, config_path: Path | None = None) -> RepositoryConfig:
        """Load repository configuration."""
        try:
            return self.config_manager.load_config(config_path)
        except Exception as e:
            logger.error(f"Failed to load configuration: {e}")
            raise

    def save_config(self, config_path: Path | None = None) -> None:
        """Save current configuration."""
        try:
            self.config_manager.save_config(config_path)
        except Exception as e:
            logger.error(f"Failed to save configuration: {e}")
            raise

    def create_new_config(self) -> RepositoryConfig:
        """Create a new empty configuration."""
        return self.config_manager.create_new_config()

    def get_config(self) -> RepositoryConfig:
        """Get the current configuration."""
        return self.config_manager.config

    def validate_config(self) -> list[str]:
        """Validate the current configuration."""
        return self.config_manager.validate_config()

    def get_config_info(self) -> dict[str, Any]:
        """Get information about the current configuration."""
        return self.config_manager.get_config_info()

    # Repository Management
    def add_repository(
        self,
        name: str,
        url: str,
        server_type: str,
        local_path: Path | str,
        default_branch: str,
        group: str = "default",
    ) -> None:
        """Add a new repository to the configuration."""
        from repops.models import ServerType

        try:
            repository = Repository(
                name=name,
                url=url,
                server_type=ServerType.from_string(server_type),
                local_path=Path(local_path) if isinstance(local_path, str) else local_path,
                default_branch=default_branch,
                group=group,
            )
            self.config_manager.config.add_repository(repository)
            logger.info(f"Added repository '{name}' to group '{group}'")
        except Exception as e:
            logger.error(f"Failed to add repository '{name}': {e}")
            raise

    def remove_repository(self, name: str) -> None:
        """Remove a repository from the configuration."""
        try:
            self.config_manager.config.remove_repository(name)
            logger.info(f"Removed repository '{name}'")
        except Exception as e:
            logger.error(f"Failed to remove repository '{name}': {e}")
            raise

    def get_repository(self, name: str) -> Repository | None:
        """Get a specific repository by name."""
        return self.config_manager.config.repositories.get(name)

    def get_repositories_by_group(self, group: str) -> list[Repository]:
        """Get all repositories in a specific group."""
        return self.config_manager.config.get_repositories_by_group(group)

    def get_all_repositories(self) -> list[Repository]:
        """Get all repositories across all groups."""
        return self.config_manager.config.get_all_repositories()

    def list_groups(self) -> list[str]:
        """Get list of all groups."""
        return list(self.config_manager.config.groups.keys())

    # Repository Validation
    def check_repository_availability(self, repository: Repository) -> dict[str, Any]:
        """Check if repository is available locally and remotely."""
        result = {
            "name": repository.name,
            "local_exists": False,
            "remote_accessible": False,
            "local_path": str(repository.local_path),
            "url": repository.url,
            "errors": [],
        }

        # Check local availability
        try:
            if repository.local_path.exists():
                if (repository.local_path / ".git").exists():
                    result["local_exists"] = True
                else:
                    result["errors"].append("Directory exists but is not a git repository")
            else:
                result["errors"].append("Local directory does not exist")
        except Exception as e:
            result["errors"].append(f"Error checking local path: {e}")

        # Check remote accessibility (placeholder for now)
        # TODO: Implement actual git remote check in Phase 2
        result["remote_accessible"] = True  # Assume accessible for now

        return result

    def check_all_repositories(self) -> dict[str, dict[str, Any]]:
        """Check availability of all configured repositories."""
        results = {}
        for repository in self.get_all_repositories():
            results[repository.name] = self.check_repository_availability(repository)
        return results

    # Utility Methods
    def get_app_status(self) -> dict[str, Any]:
        """Get overall application status."""
        try:
            config_info = self.get_config_info()
            validation_issues = self.validate_config()

            return {
                "config": config_info,
                "validation_issues": validation_issues,
                "is_healthy": len(validation_issues) == 0,
            }
        except Exception as e:
            return {
                "config": {"loaded": False, "error": str(e)},
                "validation_issues": [f"Failed to get status: {e}"],
                "is_healthy": False,
            }
