# repops requirements

## Functional requirements

### 1. Config

1. App should load a list of repositories to be managed from YAML file (default name should be `repos.yml`).
2. Each repository entry in the configuration file should include:
   1. URL: URL of the remote git repository,
   2. main branch name: default branch to use (e.g. `main`, `develop`),
   3. local path: local filesystem path where the repository should be cloned,
   4. server type: type of git server (GitHub, Azure DevOps, or GitLab) to properly handle platform-specific
      operations.
3. Config file should allow dividing repositories into subgroups.
4. App should allow checking if all repositories defined in config are actually available at specified location and
   fetch them if not.
5. App should allow creating, editing, saving and removing config files.

### 2. Operations

1. App should allow executing operations on the given repository.
2. Operation is a defined action that can operate on given repository to modify files, VCS config or produce other
   output to be used by other operations.
3. Operation should have a unique string ID in a form of `source.x.y.z.OperationName`.
   1. `source` should indicate operation's source type:
      1. `repops` type should translate to `repops`,
      2. `plugin` type should translate to plugin's package name,
      3. `local` type should translate to `local`.
   2. Each string separated by dot (`x`, `y`, `z`) is a name of package/module where operation is located in project's
      repo structure (e.g. creating PR on GitHub can have an ID `repops.vcs.github.pr.Create`).
   3. Last token of operation ID should be its name and equal to class which implements it.
   4. Operation ID should be created automatically upon construction.
4. All operations should inherit from base class to ensure common interface and structure, including:
   1. human readable description,
   2. source type, which can be one of: `repops`, `plugin` (with plugin's package name) or `local` (with filesystem
      location),
   3. methods for operation execution, validation, and metadata (like name, description, arguments),
   4. support for operation dependencies (operations that must be run before/after),
   5. standard error handling (via exceptions) and logging interfaces (via logger).
5. Operation can have a set of expected arguments to be used by the operation.
   1. Arguments can be of any type, which is supported by YAML syntax.
   2. Arguments should be marked as required or optional in operation definition.
6. Operation should be able to use special context for passing information from and to other operations upon execution.
7. Operation should raise proper exception when it fails to execute.
   1. Exceptions should be categorized by operation domain.
   2. There should be a separate exception category for common errors (like missing arguments etc.).
8. App should have the following list of predefined operations:
   1. vcs:
      1. git:
         1. clone repository,
         2. pull and push changes (without loosing local unstaged changes),
         3. create, remove and change branches,
         4. create tags,
         5. obtain and save to context HEAD revisions of all managed repositories,
         6. apply git patches.
      2. GitHub:
         1. create pull request (PR).
      3. Azure DevOps:
         1. create pull request (PR).
      4. GitLab:
         1. create pull request (PR).
   2. files:
      1. copy given files or directories from a reference repository to selected target repositories,
      2. apply given patch/diff from a reference repository to selected target repositories,
      3. perform "find" operation across specified files or entire repositories,
      4. perform "find and replace" operation across specified files or entire repositories,
      5. reflect changes from a reference repository to all other specified repositories in a pipeline.
   3. script:
      1. execute given script or shell expression on given repository.
   4. c++:
      1. cmake:
         1. list dependencies based on `Find*.cmake` files,
         2. create dependency graph between repositories based on CMake dependencies,
         3. determine the topological order for repository updates based on the dependency graph,
         4. update dependencies across repositories in the correct order:
            1. ensure each repository uses the latest version of its dependencies,
            2. propagate these updates through the dependency chain,
            3. update CMake files to reference the latest versions of dependencies.
9. All file operations should support path patterns for inclusion and exclusion of files:
   1. allow selecting files based on glob patterns (e.g. `*.cpp`, `src/**/*.h`),
   2. allow excluding specific files or directories from operations,
   3. support common ignore patterns (similar to .gitignore).
10. All PR operations should have the following semantics:
    1. PR should include all operations executed since the previous PR operation (or from the beginning of the pipeline
       if no previous PR operation exists),
    2. each operation included in the PR should be represented as a separate commit,
    3. app should use default branch specified in the repository configuration as target branch in the PR by default,
    4. if the specified target branch does not exist in the remote repository, app should stop execution with a clear
       error message.
11. Authentication for Git operations (including PR creation) should use SSH keys configured outside the application.

### 3. Pipelines

1. App should allow making a pipeline of operations that will be applied to the given repository.
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
8. App should be able to have a predefined builtin list of pipelines.

### 4. Plugins

1. User should be able to use custom plugins, which are external to the app, providing additional operations
   and pipeline definitions.
2. Plugins should be discoverable by the app in two forms:
   1. by installing external Python package,
   2. by pointing to the local plugin directory.
3. Internally, both methods should have a common low-level implementation.
4. Plugin system should allow defining and saving new local pipelines and operations directly from the app.
5. Plugin system should use Python's entry points mechanism (via `hatchling`).
   1. Builtin operations should be registered under a `repops.ops` entry point.
   2. External plugins should be discoverable by registering to the same entry point namespace.
   3. Each entry point should specify an operation class that implements a standard interface.
   4. App should scan for all available entry points at startup and register all discovered operations.

### 5. UI

1. App should have a 3 ways of interacting with it:
   1. console TUI mode based on `Textual` library for full application usage,
   2. console CLI mode based on command line arguments for performing simple operations,
   3. MCP server mode based on official MCP SDK to allow integratin with LLMs which support MCP servers.
2. App should be able to list all available operations.
   1. List should include operation ID, name, source and description.
   2. List should have a possibility to filter by ID, name or source patterns.

### TODO

   1. App should provide two interface modes:
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

1. Application should be reliable and handle errors gracefully, providing meaningful error messages.
2. Application should be maintainable and support modular expansion of operations.
3. Application should provide clear and informative logging with multiple log levels.
4. Application should be well-documented, including usage and plugin development guides.
5. Application should be testable, with unit and integration tests and enforced code coverage thresholds.
6. Application should enforce code quality through automated checks and formatting.

## Technical constraints

1. Project must be written in Python.
2. Project must use the `uv` tool for dependency, environment, and workflow management.
3. Project must use `pytest` for testing and `pytest-cov` for coverage.
4. Project must use `ruff` for linting and formatting.
5. Project must use `hatchling` and Python entry points for plugin discovery.
6. Project must use the `Textual` library for TUI and support CLI and MCP server modes.
7. Project must maintain a clear separation between production and development dependencies.
8. Project must use `uv.lock` for reproducible environments.
9. Project must use `uv build` for packaging and `uv pip publish` for publishing.
