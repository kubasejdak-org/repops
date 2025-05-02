# Repops - Repository Operations Tool

Repops is a Python application designed to help maintain multiple code repositories by performing operations in bulk, including creating pull requests.

## Features

- Perform operations on multiple repositories in bulk
- Configure and manage repositories with a YAML configuration file
- Modular structure allowing extension of supported operations
- Language-specific operations for different programming languages
- Pipeline processing to execute operations sequentially
- Pull request creation support

## Project Structure

```
repops/
├── repops/
│   ├── core/           # Core functionality
│   ├── operations/     # Repository operations
│   ├── pipelines/      # Pipeline processing
│   ├── languages/      # Language-specific operations
│   └── config/         # Configuration handling
├── tests/              # Unit tests
├── main.py             # Entry point
├── pyproject.toml      # Project metadata and dependencies
└── config_sample.yaml  # Sample configuration
```

## Installation

Repops requires Python 3.12 or later and uses the `uv` package manager.

```bash
# Clone the repository
git clone https://github.com/username/repops.git
cd repops

# Install dependencies using uv
uv pip install -e .
```

## Usage

Create a configuration file with your repositories:

```yaml
repositories:
  - name: repo1
    path: /path/to/repo1
    main_branch: main
    language: python
    remote_url: https://github.com/username/repo1.git
  
  - name: repo2
    path: /path/to/repo2
    main_branch: master
    language: javascript
    remote_url: https://github.com/username/repo2.git
```

Then run Repops with the configuration:

```bash
python -m repops -c config.yaml --create-pr
```

## Extending Repops

Repops is designed to be easily extended with new operations:

1. Create a new operation class that inherits from `Operation` or one of its subclasses
2. Implement the `execute` and `get_name` methods
3. Add the operation to a pipeline

Example:

```python
from repops.operations.base import Operation
from repops.core.repository import Repository

class CustomOperation(Operation):
    def execute(self, repo: Repository) -> bool:
        # Implement your operation logic
        print(f"Custom operation on {repo.name}")
        return True
        
    def get_name(self) -> str:
        return "Custom Operation"
```

## License

See the LICENSE file for details.
