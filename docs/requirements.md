# repops requirements

## Functional requirements

1. App should allow creating pull requests (PR) on the following platforms:
    1. GitHub,
    2. Azure DevOps,
    3. GitLab.
2. App should be independent from any programming language wherever possible, but should provide modules for creating a
   language-specific behavior.
3. App should have a modular architecture based on plugins or set of commands (actions), that can be easily extended.
4. App should allow making a pipeline of operations that should be applied to the given repository.
5. App should allow launching in TUI mode implemented with `textual`.
6. App should support at least the following operations:
    1. common:
        1. git:
            1. cloning repository,
            2. pulling changes (without loosing local unstaged changes),
            3. creating pull requests (PR),
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

## Non-functional requirements

1. Project should be written in Python.
2. Project should use `uv` workflow for managing build system and dependencies.
3. Project should use `ruff` for checking for formatting and linting issues.
4. Project should have unit and integration tests in `pytest` with code coverage support.







4. Procesy modyfikowacji repozytorów powinny być oddzielone od procesu tworzeniach PR ze zmianami.
6. W przypadku gdy jest kilka operacji modyfikacji po sobie, oznacza to że każda z tych operacji jest osobnym commitem w repozytorium, ale są częścią tego samego potencjalnego PR.
7. Aplikacja powinna ładować plik YAML (domyślnie `repos.yml`) z listą repozytoriów do zarządzania.
8. Aplikacja powinna mieć interfejs CLI do modyfikowania pliku z listą repozytoriów:
    1. dodawanie i usuwanie repozytorium
    2. aktualizacja ścieżki na dysku, URL lub nazwy gałęzi głównej
