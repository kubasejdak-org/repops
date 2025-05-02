"""
JavaScript-specific operations for repository management.
"""

import subprocess

from repops.core.repository import Repository
from repops.languages.base import JavaScriptOperation


class JavaScriptLintOperation(JavaScriptOperation):
    """Operation to run linting on JavaScript/TypeScript repositories."""

    def __init__(self, fix: bool = False):
        self.fix = fix

    def execute(self, repo: Repository) -> bool:
        """Run linting on a JavaScript/TypeScript repository.

        Args:
            repo: Repository to lint

        Returns:
            Success status
        """
        if not self.supports_language(repo.language):
            return False

        try:
            cmd = ["npm", "run", "lint"]
            if self.fix:
                cmd = ["npm", "run", "lint", "--", "--fix"]

            result = subprocess.run(cmd, cwd=repo.path, check=True, capture_output=True, text=True)

            operation_name = "ESLint (with autofix)" if self.fix else "ESLint"
            print(f"Successfully ran {operation_name} on {repo.name}")
            if result.stdout.strip():
                print(f"Output: {result.stdout.strip()}")

            return True
        except subprocess.CalledProcessError as e:
            print(f"Linting failed for {repo.name}: {e.stderr}")
            return False
        except Exception as e:
            print(f"Error running lint on {repo.name}: {e}")
            return False

    def get_name(self) -> str:
        return f"JavaScript Lint {'(autofix)' if self.fix else ''}"


class JavaScriptBuildOperation(JavaScriptOperation):
    """Operation to build JavaScript/TypeScript repositories."""

    def execute(self, repo: Repository) -> bool:
        """Build a JavaScript/TypeScript repository.

        Args:
            repo: Repository to build

        Returns:
            Success status
        """
        if not self.supports_language(repo.language):
            return False

        try:
            # First install dependencies if needed
            subprocess.run(["npm", "install"], cwd=repo.path, check=True, capture_output=True, text=True)

            # Then build
            subprocess.run(["npm", "run", "build"], cwd=repo.path, check=True, capture_output=True, text=True)

            print(f"Successfully built {repo.name}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Build failed for {repo.name}: {e.stderr}")
            return False
        except Exception as e:
            print(f"Error building {repo.name}: {e}")
            return False

    def get_name(self) -> str:
        return "JavaScript Build"
