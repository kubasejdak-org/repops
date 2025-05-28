---
applyTo: "**/*.py"
---

# Python guidelines

- Use type hints wherever possible.
- Use f-strings for string formatting.
- Do not add unused imports. Remove anything that is not needed.
- Write pythonic code with common Python coding conventions in mind.

## Dependencies management

- Use "uv" for managing project dependencies.
- Add normal dependencies via "uv add" and development/testing ones via "uv add --dev".
- Make sure that proper virtual environment is activated before you do anything.

## Formatting and linting

- Use "ruff" for formatting and linting.

## Testing

- Use "pytest" as test framework configured with code coverage via "pytest-cov".
- Aim for 100% code coverage, except for handling system errors or similar cases which are hard to simulate.
