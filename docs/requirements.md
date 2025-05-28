# repops requirements

## Functional requirements

### 1. Config

1. App should load a list of repositories to be managed from YAML file (default name should be `repos.yml`).
2. Each repository entry in the configuration file should include:
   1. URL: URL of the remote git repository.
   2. Main Branch Name: Default branch to use (e.g., main, master).
   3. Local Path: The local filesystem path where the repository should be cloned.
   4. Server Type: The type of git server (GitHub, Azure DevOps, or GitLab) to properly handle platform-specific
      operations.
3. App should allow checking if all defined in config repositories are actually available at specified location and
   clone them if not.

### 2. Operations

1. App should allow executing operations on the given repository.
2. Operation is a defined action that can operate on given repository to modify files, VCS config or produce other
   output to be used by other operations.
3. Operation should have a unique string ID in a form of "x.y.z.OperationName" where each string separated by dot is a
   name of package/module where operation is located in repo structure (e.g. creating PR on GitHub could have an ID
   "vcs.github.pr.Create").
   1. Operation ID should be constructed automatically using its source code location relative to "ops" package.
   2. Last token of operation ID should be its name and equal to class which implements it.
4. All operations should inherit from base class to ensure common interface and structure, including:
   1. human readable description.
   2. source type, which can be one of: predefined, plugin (with plugin/package name) or local (with filesystem
      location),
   3. methods for operation execution, validation, and metadata (like name, description, parameters),
   4. support for operation dependencies (operations that must be run before/after),
   5. standard error handling and logging interfaces.
5. Operation can have a set of expected arguments to be used by the operation.
   1. Arguments can be of any type, which is supported by YAML syntax.
   2. Arguments should be marked as required or optional in operation definition.
6. Operation should be able to use special context for passing information from and to other operations.
7. Operation should raise special exception when it fails to execute.
   1. Exceptions should be categorized by operation domain.
   2. There should be a separate exception category for common errors (like missing arguments etc.).
8. App should have the following list of predefined operations:
   1. vcs:
      1. git:
         1. cloning repository,
         2. pulling changes (without loosing local unstaged changes),
         3. creating pull requests (PR) on the following platforms:
            1. GitHub,
            2. Azure DevOps,
            3. GitLab.
         4. creating, removing and changing branches,
         5. creating tags,
         6. obtaining and saving HEAD revisions of all managed repositories,
         7. applying git patches.
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
9. All file operations should support path patterns for inclusion and exclusion of files:
   1. allow selecting files based on glob patterns (e.g., `*.cpp`, `src/**/*.h`),
   2. allow excluding specific files or directories from operations,
   3. support common ignore patterns (similar to .gitignore).
10. When a PR operation is encountered in the pipeline:
    1. it should include all operations executed since the previous PR operation (or from the beginning of the pipeline
       if no previous PR operation exists),
    2. each operation included in the PR should be represented as a separate commit,
    3. app should use the default branch specified in the repository configuration as target branch in the PR.
11. Authentication for Git operations (including PR creation) should use SSH keys configured outside the application.

### 3. Pipelines

1. App should allow making a pipeline of operations that should be applied to the given repository.
2. Pipeline is a sequential list of operations to be executed in order.
3. App should allow specifying repositories for pipeline to operate on.
   1. Repository selection should be separate from the pipeline mechanics.
   2. Repository selection should be flexible, supporting:
      1. selecting all repositories from the configuration,
      2. selecting a subset of repositories based on name patterns,
      3. selecting individual repositories by name.
   3. Pipelines loaded from files can have an optional predefined list of repositories to operate on by default.
4. Each operation in pipeline can have a list of arguments with its values, with respect to which arguments are
   required and which are optional.
5. All data which are part of pipeline (operations, their order, arguments, repositories to operate on, etc.) should be
   possible to be overwritten in app once loaded.
6. Pipelines can be created by two methods:
   1. by loading its full defeinition from YAML file,
   2. by manually constructing it in the app from scratch.
7. App should allow loading and saving pipeline to and from YAML file.
8. App should be able to have a predefined local list of pipelines.

### 4. Plugins

1. User should be able to use custom plugins providing additional operations and pipeline definitions.
2. Plugins should be discoverable by the app in two forms:
   1. by installing external Python package,
   2. by pointing to the local plugin directory.
3. Internally, both methods should have a common low-level implementation.
4. Plugin system should allow defining and saving new local pipelines and operations.
5. Plugin system should use Python's entry points mechanism (via `hatchling`):
   1. Core operations should be registered under a "repops.ops" entry point.
   2. External plugins should be discoverable by registering to the same entry point namespace.
   3. Each entry point should specify an operation class that implements a standard interface.
   4. App should scan for all available entry points at startup and register all discovered operations.

### 5. UI

1. App should have a 3 ways of interacting with it:
   1. console TUI mode based on Textual library for full application usage,
   2. console CLI mode based on command line arguments for performing simple operations,
   3. MCP server mode based on official MCP SDK to allow integratin with LLMs which support MCP servers.
2. App should be able to list all available operations.
   1. List should include operation ID, name, source and description.
   2. List should have a possibility to filter by ID, name or source patterns.

### TODO

   1. If the specified default branch does not exist on the remote repository, the app should stop execution with a
      clear error message.
   2. App should provide two interface modes:
      1. TUI mode (implemented with `textual`):
         1. This should be the default and primary mode of interaction with the application.
         2. TUI should provide full access to defining and executing operation pipelines.
         3. TUI should allow browsing and selecting repositories from the configuration.
         4. TUI should display operation status and progress during pipeline execution.
      2. CLI interface:
         1. Designed for one-shot operations and automation scripts.
         2. Should provide a dedicated group of commands to manage repositories without manual editing of the repos config
               file (default `repos.yml`):
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
3. Architecture:
   1. App should have a modular architecture, allowing to expand list of operations.
   2. Predefined operations should be categorized within the app by their domain.
4. Documentation:
   1. App should provide clear documentation and examples for creating plugins.
5. Code quality:
   1. Project should use `ruff` for checking for formatting and linting issues.
   2. Code formatting should be enforced through automated checks in CI/CD.
6. Testing:
   1. Project should have unit and integration tests in `pytest` with code coverage support via `pytest-cov`.
   2. Test coverage threshold should be defined and enforced.
7. Error handling and logging:
   1. Application should use Python's standard logging mechanism to report errors and operation status.
   2. Any error encountered during operation execution should terminate the pipeline and abort the application.
   3. Error messages should be descriptive and provide meaningful information about what went wrong.
   4. Logging levels should include DEBUG, INFO, WARNING, ERROR, and CRITICAL.
   5. Logs should be displayed in the console and optionally saved to a file.
