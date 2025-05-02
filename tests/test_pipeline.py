"""
Tests for the pipeline module.
"""

from pathlib import Path

import pytest

from repops.core.repository import Repository, RepositoryManager
from repops.operations.base import Operation
from repops.pipelines.pipeline import Pipeline


class MockOperation(Operation):
    """Mock operation for testing."""

    def __init__(self, success=True):
        self.executed = False
        self.success = success

    def execute(self, repo: Repository) -> bool:
        self.executed = True
        return self.success

    def get_name(self) -> str:
        return "Mock Operation"


@pytest.fixture
def pipeline():
    """Create a test pipeline."""
    return Pipeline("Test Pipeline")


@pytest.fixture
def repo_manager():
    """Create a test repository manager with test repositories."""
    manager = RepositoryManager()

    repo1 = Repository(name="repo1", path=Path("/path/to/repo1"), main_branch="main", language="python")
    repo2 = Repository(name="repo2", path=Path("/path/to/repo2"), main_branch="master", language="javascript")

    manager.add_repository(repo1)
    manager.add_repository(repo2)

    return manager


def test_add_operation(pipeline):
    """Test adding operations to the pipeline."""
    op1 = MockOperation()
    op2 = MockOperation()

    pipeline.add_operation(op1)
    assert len(pipeline.operations) == 1

    pipeline.add_operation(op2)
    assert len(pipeline.operations) == 2


def test_pipeline_execution_success(pipeline, repo_manager):
    """Test pipeline execution when all operations succeed."""
    op1 = MockOperation(success=True)
    op2 = MockOperation(success=True)

    pipeline.add_operation(op1)
    pipeline.add_operation(op2)

    results = pipeline.execute(repo_manager)

    # Check that we have results for both repositories
    assert len(results) == 2
    assert "repo1" in results
    assert "repo2" in results

    # Check that both operations were executed for both repositories
    assert len(results["repo1"]) == 2
    assert len(results["repo2"]) == 2

    # Check that all operations succeeded
    assert all(results["repo1"])
    assert all(results["repo2"])


def test_pipeline_execution_failure(pipeline, repo_manager):
    """Test pipeline execution when an operation fails."""
    op1 = MockOperation(success=True)
    op2 = MockOperation(success=False)
    op3 = MockOperation(success=True)  # Should not execute after op2 fails

    pipeline.add_operation(op1)
    pipeline.add_operation(op2)
    pipeline.add_operation(op3)

    results = pipeline.execute(repo_manager)

    # Check that we have results for both repositories
    assert len(results) == 2

    # Check that the first operation succeeded but the second failed
    assert len(results["repo1"]) == 2
    assert results["repo1"][0] is True  # op1 succeeded
    assert results["repo1"][1] is False  # op2 failed

    # Check that op3 was not executed (length of results is 2, not 3)
    assert len(results["repo1"]) == 2
