"""
Tests for the repository module.
"""

from pathlib import Path

import pytest

from repops.core.repository import Repository, RepositoryManager


def test_repository_creation():
    """Test that a repository can be created."""
    repo = Repository(
        name="test-repo",
        path=Path("/path/to/repo"),
        main_branch="main",
        language="python",
        remote_url="https://github.com/user/repo.git",
    )

    assert repo.name == "test-repo"
    assert repo.path == Path("/path/to/repo")
    assert repo.main_branch == "main"
    assert repo.language == "python"
    assert repo.remote_url == "https://github.com/user/repo.git"


def test_repository_str():
    """Test the string representation of a repository."""
    repo = Repository(name="test-repo", path=Path("/path/to/repo"), main_branch="main", language="python")

    assert str(repo) == "test-repo (/path/to/repo)"


@pytest.fixture
def repository_manager():
    """Create a test repository manager with test repositories."""
    manager = RepositoryManager()

    repo1 = Repository(name="repo1", path=Path("/path/to/repo1"), main_branch="main", language="python")
    repo2 = Repository(name="repo2", path=Path("/path/to/repo2"), main_branch="master", language="javascript")
    repo3 = Repository(name="repo3", path=Path("/path/to/repo3"), main_branch="main", language="python")

    return manager, repo1, repo2, repo3


def test_add_repository():
    """Test adding repositories to the manager."""
    manager = RepositoryManager()
    repo1 = Repository(name="repo1", path=Path("/path/to/repo1"), main_branch="main", language="python")
    repo2 = Repository(name="repo2", path=Path("/path/to/repo2"), main_branch="master", language="javascript")

    manager.add_repository(repo1)
    assert len(manager.get_repositories()) == 1

    manager.add_repository(repo2)
    assert len(manager.get_repositories()) == 2


def test_filter_repositories():
    """Test filtering repositories by language."""
    manager = RepositoryManager()
    repo1 = Repository(name="repo1", path=Path("/path/to/repo1"), main_branch="main", language="python")
    repo2 = Repository(name="repo2", path=Path("/path/to/repo2"), main_branch="master", language="javascript")
    repo3 = Repository(name="repo3", path=Path("/path/to/repo3"), main_branch="main", language="python")

    manager.add_repository(repo1)
    manager.add_repository(repo2)
    manager.add_repository(repo3)

    python_repos = manager.filter_repositories("python")
    assert len(python_repos) == 2
    assert python_repos[0].name == "repo1"
    assert python_repos[1].name == "repo3"

    js_repos = manager.filter_repositories("javascript")
    assert len(js_repos) == 1
    assert js_repos[0].name == "repo2"

    all_repos = manager.filter_repositories()
    assert len(all_repos) == 3
