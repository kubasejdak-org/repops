"""
Pipeline module for executing sequences of operations on repositories.
"""

from typing import List

from repops.core.repository import RepositoryManager
from repops.operations.base import Operation


class Pipeline:
    """Class representing a pipeline of operations to be executed on repositories."""

    def __init__(self, name: str):
        self.name = name
        self.operations: List[Operation] = []

    def add_operation(self, operation: Operation) -> None:
        """Add an operation to the pipeline.

        Args:
            operation: Operation to add
        """
        self.operations.append(operation)

    def execute(self, repo_manager: RepositoryManager) -> dict[str, list[bool]]:
        """Execute all operations in the pipeline on all repositories.

        Args:
            repo_manager: Repository manager containing repositories to operate on

        Returns:
            Dictionary mapping repository names to list of operation results
        """
        results = {}
        for repo in repo_manager.get_repositories():
            repo_results = []
            for operation in self.operations:
                print(f"Executing {operation.get_name()} on {repo.name}")
                success = operation.execute(repo)
                repo_results.append(success)

                # Stop executing operations for this repository if one fails
                if not success:
                    break

            results[repo.name] = repo_results

        return results
