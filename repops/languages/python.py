"""
Python-specific operations for repository management.
"""

import os
import subprocess
from typing import Optional

from repops.core.repository import Repository
from repops.languages.base import PythonOperation


class PythonLintOperation(PythonOperation):
    """Operation to run linting on Python repositories."""

    def __init__(self, fix: bool = False):
        self.fix = fix

    def execute(self, repo: Repository) -> bool:
        """Run linting on a Python repository.

        Args:
            repo: Repository to lint

        Returns:
            Success status
        """
        if not self.supports_language(repo.language):
            return False

        try:
            cmd = ["flake8", str(repo.path)]
            if self.fix:
                cmd = ["autopep8", "--in-place", "--recursive", str(repo.path)]

            result = subprocess.run(cmd, check=True, capture_output=True, text=True)

            operation_name = "autopep8 (autofix)" if self.fix else "flake8"
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
        return f"Python Lint {'(autofix)' if self.fix else ''}"


class PythonUnitTestOperation(PythonOperation):
    """Operation to run unit tests on Python repositories."""

    def __init__(self, test_path: Optional[str] = None):
        self.test_path = test_path

    def execute(self, repo: Repository) -> bool:
        """Run unit tests on a Python repository.

        Args:
            repo: Repository to run tests on

        Returns:
            Success status
        """
        if not self.supports_language(repo.language):
            return False

        try:
            test_location = self.test_path if self.test_path else os.path.join(repo.path, "tests")
            cmd = ["pytest", test_location, "-v"]

            result = subprocess.run(cmd, cwd=repo.path, check=True, capture_output=True, text=True)

            print(f"Successfully ran tests on {repo.name}")
            print(f"Test output: {result.stdout.strip()}")

            return True
        except subprocess.CalledProcessError as e:
            print(f"Tests failed for {repo.name}: {e.stderr}")
            return False
        except Exception as e:
            print(f"Error running tests on {repo.name}: {e}")
            return False

    def get_name(self) -> str:
        return "Python Unit Tests"
