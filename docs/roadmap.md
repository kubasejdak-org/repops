# Repops Implementation Roadmap

This document outlines the complete implementation plan for the repops application, divided into functional phases where each phase delivers a working application with increasing capabilities.

## Overview

Repops is a tool for configuring, managing and automating file operations across multiple git repositories. The implementation is designed to be modular, extensible, and maintainable, following modern Python development practices.

## Implementation Phases

### ✅ Phase 1: Core Foundation & Configuration Management

**Status**: ✅ **FULLY COMPLETED**  
**Goal**: Basic app structure with config loading/saving and repository validation

**Deliverables**:

- [x] Core application structure with proper module organization
- [x] Configuration management (load/save YAML configs with validation)
- [x] Repository model with validation and type safety
- [x] Basic CLI entry point with Typer
- [x] Error handling and logging foundation
- [x] Support for repository groups and server types
- [x] Path resolution (relative/absolute config paths)
- [x] Repository CRUD operations with validation
- [x] Rich CLI output with tables and error formatting

**Implementation Details**:

- **Models**: Repository dataclass with ServerType enum, RepositoryConfig with group support
- **Config Manager**: YAML loading/saving, validation, automatic config creation
- **Exception System**: RepopsError hierarchy (ConfigError, ValidationError, RepositoryError)
- **Core App**: RepopsApp class coordinating all functionality
- **CLI Interface**: 6 complete commands with proper error handling and rich output

**What works after Phase 1**:

- Load, validate, edit and save repository configurations with groups
- Add/remove repositories from configurations with full validation
- List repositories with group filtering and rich table output
- Check local and remote repository availability
- Create new configurations when files don't exist
- Comprehensive error handling with helpful messages
- Full CLI interface for configuration management

**Commands available**:

- `repops status` - Show application and configuration status
- `repops config-info` - Show detailed configuration information with groups
- `repops list-repos [--group GROUP]` - List repositories with optional group filtering
- `repops add-repo` - Add a new repository to configuration (creates config if needed)
- `repops remove-repo` - Remove a repository from configuration
- `repops check-repos` - Check local and remote repository availability

**Files Implemented**:

- `src/repops/models/repository.py` - Repository and RepositoryConfig models
- `src/repops/config/manager.py` - Configuration management with YAML support
- `src/repops/exceptions/exceptions.py` - Comprehensive exception hierarchy
- `src/repops/core/app.py` - Core application logic and coordination
- `src/repops/cli/main.py` - Complete CLI interface with Typer
- Updated `pyproject.toml` with PyYAML and Typer dependencies

---

### 🔄 Phase 2: Operation Framework & Base Operations

**Status**: 🟡 **NEXT TO IMPLEMENT**  
**Goal**: Operation system foundation with basic git operations

**Deliverables**:

- [ ] **Operation Framework** (`src/repops/operations/`)
  - [ ] `base.py` - Abstract Operation class with standard interface
  - [ ] `context.py` - Operation context for data sharing between operations
  - [ ] `registry.py` - Operation discovery and registration system
  - [ ] `exceptions.py` - Operation-specific exceptions

- [ ] **Git Operations** (`src/repops/operations/vcs/git/`)
  - [ ] `clone.py` - Repository cloning operation
  - [ ] `sync.py` - Pull/push with local change preservation
  - [ ] `branch.py` - Branch creation, switching, deletion
  - [ ] `tag.py` - Tag creation and management
  - [ ] `info.py` - Get HEAD revisions and repository information

- [ ] **File Operations** (`src/repops/operations/files/`)
  - [ ] `find.py` - Search operations with glob pattern support
  - [ ] `replace.py` - Find and replace across files with patterns
  - [ ] `patterns.py` - Pattern matching utilities (glob, gitignore-style)

- [ ] **Script Operations** (`src/repops/operations/script/`)
  - [ ] `execute.py` - Shell command execution in repository context

**Key Features**:

- **Operation ID System**: Format `repops.module.submodule.ClassName`
- **Context System**: Shared data between operations in pipeline
- **Argument Validation**: Required/optional parameters with type checking
- **Error Handling**: Operation-specific exceptions with detailed context
- **Dependency Management**: Operation execution order based on dependencies

**Implementation Plan**:

1. **Base Operation Class**: Abstract interface with metadata, validation, execution
2. **Context System**: Thread-safe data sharing between operations
3. **Registry**: Entry point-based operation discovery
4. **Git Operations**: Using GitPython for repository manipulation
5. **File Operations**: Glob pattern support with include/exclude filters
6. **Script Operations**: Safe shell execution with working directory management

**Dependencies to Add**:

```bash
uv add gitpython  # For git operations
```

**What works after Phase 2**:

- Execute git operations on configured repositories with proper error handling
- Run file operations across multiple repositories with pattern matching
- Execute custom scripts in repository contexts
- Foundation for pipeline system with operation context sharing

**New commands**:

- `repops operations list` - List all available operations with descriptions
- `repops operations info <operation-id>` - Show operation details and arguments
- `repops operations run <operation-id>` - Execute a single operation
- `repops git clone [--repo REPO]` - Clone repositories
- `repops git pull [--repo REPO]` - Pull changes from repositories
- `repops git push [--repo REPO]` - Push changes to repositories
- `repops files find <pattern> [--repo REPO]` - Find files across repositories
- `repops files replace <find> <replace> [--repo REPO]` - Replace text in files
- `repops script run <command> [--repo REPO]` - Execute script in repositories

---

### 🔄 Phase 3: Pipeline System

**Status**: PLANNED  
**Goal**: Pipeline creation, loading, and execution

**Deliverables**:

- [ ] Pipeline model and execution engine
- [ ] Pipeline YAML loading/saving with validation
- [ ] Repository selection system (patterns, groups, individual)
- [ ] Pipeline validation and operation dependency resolution
- [ ] Context passing between operations
- [ ] Commit message and PR description editing system
- [ ] Built-in pipeline definitions

**What works after Phase 3**:

- Create, save, and execute pipelines of operations across multiple repositories
- Load pipelines from YAML files
- Select repositories for pipeline execution using flexible patterns
- Validate pipeline configurations before execution

**New commands**:

- `repops pipeline list` - List available pipelines
- `repops pipeline create` - Create a new pipeline interactively
- `repops pipeline run` - Execute a pipeline
- `repops pipeline validate` - Validate pipeline configuration

---

### 🔄 Phase 4: Advanced Git Operations & PR System

**Status**: PLANNED  
**Goal**: Platform-specific git operations and pull request creation

**Deliverables**:

- [ ] Authentication system using SSH keys
- [ ] Platform-specific PR operations:
  - [ ] GitHub PR creation
  - [ ] Azure DevOps PR creation
  - [ ] GitLab PR (Merge Request) creation
- [ ] Advanced git operations:
  - [ ] Branch management with remote validation
  - [ ] Commit grouping and PR organization
  - [ ] Conflict detection and resolution helpers
- [ ] PR workflow management:
  - [ ] Multiple commits per PR based on operations
  - [ ] Target branch validation
  - [ ] PR description templating

**What works after Phase 4**:

- Create pull requests on GitHub, GitLab, and Azure DevOps
- Manage complex git workflows across multiple repositories
- Automatic PR creation with proper commit organization

**New commands**:

- `repops pr create` - Create pull requests
- `repops git branch` - Advanced branch management
- `repops auth status` - Check authentication status

---

### 🔄 Phase 5: C++ Ecosystem Support

**Status**: PLANNED  
**Goal**: Specialized operations for C++ projects with CMake

**Deliverables**:

- [ ] CMake dependency analysis:
  - [ ] Parse `Find*.cmake` files
  - [ ] Create dependency graphs between repositories
  - [ ] Determine topological update order
- [ ] Dependency update automation:
  - [ ] Update dependencies in correct order
  - [ ] Propagate changes through dependency chain
  - [ ] Update CMake files to latest versions
- [ ] C++ project validation and health checks

**What works after Phase 5**:

- Analyze and manage C++ project dependencies across repositories
- Automatically update dependency chains in correct order
- Validate C++ project configurations

**New commands**:

- `repops cpp deps list` - List CMake dependencies
- `repops cpp deps graph` - Show dependency graph
- `repops cpp deps update` - Update dependencies in order

---

### 🔄 Phase 6: Plugin System

**Status**: PLANNED  
**Goal**: Extensible plugin architecture for custom operations

**Deliverables**:

- [ ] Plugin discovery system using Python entry points
- [ ] External plugin support (installable packages)
- [ ] Local plugin support (filesystem directories)
- [ ] Plugin validation and loading system
- [ ] Plugin development utilities and templates
- [ ] Documentation for plugin development

**What works after Phase 6**:

- Install and use external plugins from PyPI
- Create and use local custom plugins
- Extend repops functionality without modifying core code

**New commands**:

- `repops plugin list` - List installed plugins
- `repops plugin install` - Install external plugins
- `repops plugin create` - Create new plugin template

---

### 🔄 Phase 7: TUI Interface

**Status**: PLANNED  
**Goal**: Rich terminal user interface using Textual

**Deliverables**:

- [ ] TUI application structure with Textual
- [ ] Interactive configuration management screens
- [ ] Pipeline creation and editing interface
- [ ] Repository selection and management
- [ ] Real-time operation execution with progress
- [ ] Interactive forms for operation parameters
- [ ] VCS changes preview and commit message editing

**What works after Phase 7**:

- Full graphical terminal interface for all operations
- Interactive pipeline creation and execution
- Real-time progress monitoring
- Enhanced user experience for complex operations

**New mode**:

- `repops tui` - Launch terminal user interface

---

### 🔄 Phase 8: MCP Server Integration

**Status**: PLANNED  
**Goal**: Model Context Protocol server for LLM integration

**Deliverables**:

- [ ] MCP server implementation using official SDK
- [ ] All repops functionality exposed via MCP protocol
- [ ] LLM-friendly operation descriptions and schemas
- [ ] Context-aware repository and pipeline management
- [ ] Integration examples with popular LLMs

**What works after Phase 8**:

- Full repops functionality available to LLMs via MCP
- AI-assisted repository management and automation
- Natural language interaction with repops operations

**New mode**:

- `repops mcp` - Start MCP server

---

## Technical Architecture

### Core Principles

1. **Separation of Concerns**: UI layers are clients of core business logic
2. **Modularity**: Each phase builds on previous phases without breaking existing functionality
3. **Extensibility**: Plugin system allows custom operations and pipelines
4. **Type Safety**: Comprehensive type hints and validation throughout
5. **Error Handling**: Graceful error handling with meaningful messages
6. **Testing**: High code coverage with unit and integration tests

### Technology Stack

- **Language**: Python 3.12+
- **Dependency Management**: uv
- **CLI Framework**: Typer
- **TUI Framework**: Textual
- **Configuration Format**: YAML
- **Code Quality**: Ruff (linting/formatting)
- **Testing**: pytest with coverage
- **Packaging**: hatchling with entry points

### Module Organization

```
src/repops/
├── __init__.py           # Main entry point
├── core/                 # Core business logic
├── config/               # Configuration management
├── models/               # Data models and validation
├── exceptions/           # Error handling
├── operations/           # Operation system and implementations
├── pipelines/            # Pipeline system
├── plugins/              # Plugin system
├── cli/                  # Command-line interface
├── tui/                  # Terminal user interface
└── mcp/                  # MCP server implementation
```

## Development Guidelines

### Quality Standards

- **Code Coverage**: Target 100% coverage (except system errors)
- **Type Safety**: All functions and methods must have type hints
- **Documentation**: Comprehensive docstrings and user guides
- **Code Style**: Enforced via Ruff with consistent formatting
- **Error Handling**: Custom exceptions with detailed context

### Testing Strategy

- **Unit Tests**: Individual component testing with mocks
- **Integration Tests**: End-to-end workflow testing
- **CLI Tests**: Command-line interface functionality
- **Configuration Tests**: YAML loading/saving validation
- **Performance Tests**: Operation execution benchmarks

### Release Strategy

- Each phase represents a functional release
- Semantic versioning (0.1.0 for Phase 1, 0.2.0 for Phase 2, etc.)
- Comprehensive changelog with examples
- Migration guides for configuration changes

## Success Metrics

### Phase 1 ✅

- [x] Load/save YAML configurations
- [x] Repository validation and management
- [x] CLI commands for basic operations
- [x] Error handling and logging

### Future Phases

- [ ] **Phase 2**: Execute git operations on multiple repositories
- [ ] **Phase 3**: Run complex pipelines across repository sets
- [ ] **Phase 4**: Create pull requests automatically
- [ ] **Phase 5**: Manage C++ dependency chains
- [ ] **Phase 6**: Support custom plugins
- [ ] **Phase 7**: Interactive TUI for complex workflows
- [ ] **Phase 8**: LLM integration via MCP

## Current Status

**Phase 1** ✅ is **FULLY COMPLETE** and production-ready. The application provides:

### ✅ Completed Features (Phase 1)

- **Configuration Management**: Full YAML config loading/saving with validation
- **Repository Management**: CRUD operations with group support and server type validation  
- **CLI Interface**: 6 comprehensive commands with rich output and error handling
- **Path Resolution**: Supports both relative and absolute config paths
- **Error Handling**: Comprehensive exception hierarchy with helpful messages
- **Validation**: Repository data validation (URLs, paths, branches, server types)
- **Group Support**: Repository organization with automatic "default" group handling

### ✅ Working Commands

```bash
repops status                    # Application and config status
repops config-info              # Detailed configuration with groups
repops list-repos [--group G]   # List repos with optional group filter  
repops add-repo                 # Interactive repository addition
repops remove-repo              # Interactive repository removal
repops check-repos              # Local/remote availability check
```

### ✅ Solid Foundation

- **Architecture**: Clean separation between models, config, core logic, and CLI
- **Type Safety**: Comprehensive type hints with dataclass validation
- **Code Quality**: Ruff-compliant code with proper error handling
- **Dependencies**: Minimal, focused dependency set (PyYAML, Typer)
- **Extensibility**: Ready for operation framework and plugin system

### 🟡 Next: Phase 2 Implementation

Ready to begin **Phase 2: Operation Framework & Base Operations** which will add:

- Operation system with base classes and context sharing
- Git operations (clone, pull, push, branch management, tags)
- File operations (find, replace with pattern matching)
- Script execution operations
- Foundation for pipeline system

The codebase is well-structured and thoroughly tested manually. All Phase 1 functionality works correctly with proper error handling and user-friendly output.
