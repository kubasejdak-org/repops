"""
Entry point module for repops package.
"""

from repops.core.repository import Repository, RepositoryManager
from repops.operations.base import GitOperation, Operation, PullRequestOperation
from repops.pipelines.pipeline import Pipeline

__version__ = "0.1.0"

__all__ = [
    "Repository",
    "RepositoryManager",
    "Operation",
    "GitOperation",
    "PullRequestOperation",
    "Pipeline",
]
