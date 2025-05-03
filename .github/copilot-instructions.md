# General

- Use best coding standards for each programming language that you have to use.
- Do not duplicate code. If you have to add similar functionality more than once, then extract it into a separate module
  or function and reuse.
- Do not add comments for obvious things. Add them where code is complicated or solution may be less known.
- Respond without being super polite. Stick to the facts.
- Keep generated files under 500 lines of code if possible.

# Python

- Use type hints wherever possible.

## Managing dependencies

- Use "uv" for managing project dependencies.
- Make sure that proper virtual environment is activated before you do anything.
- Add normal dependencies via "uv add" and development/testing ones via "uv add --dev".

## Formatting and linting

- Use "ruff" for formatting and linting. Install it via "uv add --dev ruff" if needed.
- Do not add unused imports. Remove anything that is not needed.
- Use "ruff" to check for formatting and linting issues. Install it via "uv add ruff" and run via "uv ruff check". If
  any issues are found, then run "uv ruff check --fix" to fix them automatically.

## Testing

- If you have to add tests, use "pytest" framework with code coverage check.
