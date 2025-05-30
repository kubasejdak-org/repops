---
applyTo: "**/*.py"
---

# Python guidelines

- Use type hints wherever possible.
- Use f-strings for string formatting.
- Do not add unused imports. Remove anything that is not needed.
- Write pythonic code with common Python coding conventions in mind.

## Dependencies management

- Use `uv` for managing project dependencies.
  - Use `uv venv` for creating and managing virtual environments.
  - Use `uv add` for installing production dependencies.
  - Use `uv add --dev` for installing development/testing dependencies.
- Make sure that proper virtual environment is activated before you do anything.

## Formatting and linting

- Use `ruff` for formatting and linting.
  - Use `uv run ruff check` to check for issues.
  - Use `uv run ruff check --fix` to check & automatically apply fixes.

## Testing

- Use `pytest` as test framework configured with code coverage via `pytest-cov`.
- Aim for 100% code coverage, except for handling system errors or similar cases which are hard to simulate.

## Packaging

- Use `pyproject.toml` for project metadata and dependencies.
- Use `uv build` for packaging.
- Use `uv pip publish` for publishing.
