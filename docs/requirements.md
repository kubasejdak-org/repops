# repops requirements

## Functional requirements

1. App should allow making a pipeline of operations that should be applied to the given repository.
2. App should have a modular architecture based on plugins or set of commands (actions), that can be easily extended.
3. App should load a list of repositories to be managed from YAML file (default name should be `repos.yml`).
4. App should support at least the following operations:
    1. common:
        1. git:
            1. cloning repository,
            2. pulling changes (without loosing local unstaged changes),
            3. creating pull requests (PR) on the following platforms:
                1. GitHub,
                2. Azure DevOps,
                3. GitLab.
            4. creating, removing and changing branches,
            5. creating tags,
            6. obtaining and saving HEAD revisions of all managed repositories.
        2. files:
            1. copying given files or directories to the selected repository,
            2. applying given patch/diff to the selected repository,
            3. performing "find" operation,
            4. performing "find and replace" operation.
        3. script:
            1. executing given script or shell expression on given repository.
    2. c++:
        1. cmake:
            1. listing dependencies based on `Find*.cmake` files,
            2. creating dependency graph between repositories (to know the order in which changes should be applied),
            3. updating dependencies for given repository to HEAD revisions according to the dependency graph.
5. Repository-related operations should be independent from any programming language wherever possible, but should
   provide modules for creating a language-specific behavior.
6. App should treat each defined operation as separate commit to the given repository within the same PR.
7. Each PR operation should include commits with operations between this PR operation and the previous one (or all if no
   other PR was defined).
8. App should allow launching in TUI mode implemented with `textual`.
9. CLI interface should allow:
    1. Adding or removing repository from config file.
    2. Changing repository URL.
    3. Changing repository path on disk to be used.
    4. Changing default branch name to be used.

## Non-functional requirements

1. Project should be written in Python.
2. Project should use `uv` workflow for managing build system and dependencies.
3. Project should use `ruff` for checking for formatting and linting issues.
4. Project should have unit and integration tests in `pytest` with code coverage support.
