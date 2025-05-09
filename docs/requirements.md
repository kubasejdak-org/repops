# repops requirements

## Functional requirements

1. App should allow making a pipeline of operations that should be applied to the given repository:
   1. A pipeline is a sequential list of operations to be executed in order on specified repositories.
   2. The primary method for defining operation pipelines should be via TUI in the console.
   3. Additionally, the app should support defining pipelines via YAML configuration files.
   4. Both TUI and YAML methods should produce the same internal representation of operations.
2. App should have a modular architecture based on plugins or set of commands (actions), that can be easily extended:
   1. The plugin system should allow adding new commands and operations even when the app is installed via pip.
   2. Users should be able to create custom plugins in separate packages that extend the core functionality.
   3. The app should provide clear documentation and examples for creating plugins.
3. App should load a list of repositories to be managed from YAML file (default name should be `repos.yml`).
   1. The app should automatically clone repositories defined in the configuration file if they are not present at the
      specified location.
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
      1. copying given files or directories from a reference repository to selected target repositories,
      2. applying given patch/diff from a reference repository to selected target repositories,
      3. performing "find" operation across specified files or entire repositories,
      4. performing "find and replace" operation across specified files or entire repositories,
      5. reflecting changes from a reference repository to all other specified repositories in a pipeline.
   3. script:
      1. executing given script or shell expression on given repository.
   4. c++:
      1. cmake:
         1. listing dependencies based on `Find*.cmake` files,
         2. creating dependency graph between repositories based on CMake dependencies,
         3. determining the topological order for repository updates based on the dependency graph,
         4. automating the process of updating dependencies across repositories in the correct order:
            1. ensuring each repository uses the latest version of its dependencies,
            2. propagating these updates through the dependency chain,
            3. updating CMake files to reference the latest versions of dependencies.
5. Repository-related operations should be independent from any programming language wherever possible, but should
   provide modules for creating a language-specific behavior.
6. PR creation should be a special type of operation in the pipeline.
7. When a PR operation is encountered in the pipeline:
   1. It should include all operations executed since the previous PR operation (or from the beginning of the pipeline
      if no previous PR operation exists).
   2. Each operation included in the PR should be represented as a separate commit.
   3. Authentication for Git operations (including PR creation) should use SSH keys configured outside the application.
8. App should provide two interface modes:
   1. TUI mode (implemented with `textual`):
      1. This should be the default and primary mode of interaction with the application.
      2. TUI should provide full access to defining and executing operation pipelines.
      3. TUI should allow browsing and selecting repositories from the configuration.
      4. TUI should display operation status and progress during pipeline execution.
   2. CLI interface:
      1. Designed for one-shot operations and automation scripts.
      2. Should provide a dedicated group of commands to manage repositories without manual editing of the
         repos config file (default `repos.yml`):
         1. Adding or removing repository from config file.
         2. Changing repository URL.
         3. Changing repository path on disk to be used.
         4. Changing default branch name to be used.
         5. All CLI commands that modify the repository configuration should directly update the config file.
      3. Allow execution of predefined pipelines from YAML configuration files.

## Non-functional requirements

1. Project should be written in Python.
2. Project should use `uv` workflow for comprehensive project management:
   1. Dependency management:
      1. Using `uv add` for installing production dependencies.
      2. Using `uv add --dev` for installing development dependencies.
      3. Maintaining a clear separation between production and development dependencies.
   2. Environment management:
      1. Using `uv venv` for creating and managing virtual environments.
      2. Ensuring reproducible environments with `uv.lock` file.
   3. Development workflows:
      1. Running tests with `uv run pytest` with coverage reporting.
      2. Running linting with `uv run ruff check`.
      3. Applying automatic fixes with `uv run ruff check --fix`.
      4. Using `uv run` for all scripts defined in `pyproject.toml`.
   4. Building and packaging:
      1. Using `uv build` to create distribution packages.
      2. Generating both source distributions (sdist) and wheel packages.
   5. Publishing:
      1. Using `uv pip publish` for publishing to PyPI or other package repositories.
3. Code quality:
   1. Project should use `ruff` for checking for formatting and linting issues.
   2. Code formatting should be enforced through automated checks in CI/CD.
4. Testing:
   1. Project should have unit and integration tests in `pytest` with code coverage support.
   2. Test coverage threshold should be defined and enforced.
5. Error handling and logging:
   1. The application should use Python's standard logging mechanism to report errors and operation status.
   2. Any error encountered during operation execution should terminate the pipeline and abort the application.
   3. Error messages should be descriptive and provide meaningful information about what went wrong.
   4. Logging levels should include DEBUG, INFO, WARNING, ERROR, and CRITICAL.
   5. Logs should be displayed in the console and optionally saved to a file.
