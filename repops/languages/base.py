"""
Language-specific operations module.
"""

from abc import ABC, abstractmethod

from repops.core.repository import Repository
from repops.operations.base import Operation


class LanguageOperation(Operation, ABC):
    """Base class for language-specific operations."""

    @abstractmethod
    def supports_language(self, language: str) -> bool:
        """Check if this operation supports a specific language.

        Args:
            language: Language to check support for

        Returns:
            True if supported, False otherwise
        """
        pass


class PythonOperation(LanguageOperation):
    """Base class for Python-specific operations."""

    def supports_language(self, language: str) -> bool:
        return language.lower() == "python"

    def get_name(self) -> str:
        return "Python Operation"

    def execute(self, repo: Repository) -> bool:
        if not self.supports_language(repo.language):
            print(f"Repository {repo.name} is not a Python repository, skipping")
            return False

        # Implementation will be specific to child classes
        raise NotImplementedError()


class JavaScriptOperation(LanguageOperation):
    """Base class for JavaScript-specific operations."""

    def supports_language(self, language: str) -> bool:
        return language.lower() in ["javascript", "typescript"]

    def get_name(self) -> str:
        return "JavaScript Operation"

    def execute(self, repo: Repository) -> bool:
        if not self.supports_language(repo.language):
            print(f"Repository {repo.name} is not a JavaScript repository, skipping")
            return False

        # Implementation will be specific to child classes
        raise NotImplementedError()
