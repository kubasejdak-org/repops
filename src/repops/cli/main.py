"""CLI interface for repops application."""

import functools
from pathlib import Path
from typing import Annotated, Optional

import typer
from rich.console import Console
from rich.table import Table

from repops.core import RepopsApp
from repops.exceptions import RepopsError

app = typer.Typer(name="repops", help="Tool for managing multiple git repositories")
console = Console()


def handle_error(func):
    """Decorator to handle RepopsError exceptions."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except RepopsError as e:
            console.print(f"[red]Error: {e.message}[/red]")
            if e.details:
                console.print(f"[yellow]Details: {e.details}[/yellow]")
            raise typer.Exit(1)
        except Exception as e:
            console.print(f"[red]Unexpected error: {e}[/red]")
            raise typer.Exit(1)

    return wrapper


@app.command()
@handle_error
def status(
    config_path: Annotated[Optional[Path], typer.Option("--config", "-c", help="Path to config file")] = None,
) -> None:
    """Show status of the repops application and configuration."""
    if config_path:
        config_path = config_path.resolve()  # Convert to absolute path
    repops_app = RepopsApp(config_path)

    try:
        # Try to load config if a path was provided
        if config_path:
            repops_app.load_config()
        status_info = repops_app.get_app_status()

        console.print("[bold blue]Repops Application Status[/bold blue]")
        console.print()

        # Configuration status
        config_info = status_info["config"]
        if config_info["loaded"]:
            console.print(f"[green]✓[/green] Configuration loaded from: {config_info['path']}")
            console.print(f"  Total repositories: {config_info['total_repositories']}")
            console.print(f"  Groups: {len(config_info['groups'])}")

            if config_info.get("server_types"):
                console.print("  Server types:")
                for server, count in config_info["server_types"].items():
                    console.print(f"    {server}: {count}")
        else:
            console.print("[red]✗[/red] Configuration not loaded")
            if "error" in config_info:
                console.print(f"  Error: {config_info['error']}")

        # Validation issues
        if status_info["validation_issues"]:
            console.print()
            console.print("[yellow]Validation Issues:[/yellow]")
            for issue in status_info["validation_issues"]:
                console.print(f"  [yellow]•[/yellow] {issue}")

        # Overall health
        console.print()
        if status_info["is_healthy"]:
            console.print("[green]✓ Application is healthy[/green]")
        else:
            console.print("[red]✗ Application has issues[/red]")

    except Exception as e:
        console.print(f"[red]Error getting status: {e}[/red]")


@app.command()
@handle_error
def list_repos(
    config_path: Annotated[Optional[Path], typer.Option("--config", "-c", help="Path to config file")] = None,
    group: Annotated[Optional[str], typer.Option("--group", "-g", help="Filter by group")] = None,
) -> None:
    """List all configured repositories."""
    repops_app = RepopsApp(config_path)

    if group:
        repositories = repops_app.get_repositories_by_group(group)
        title = f"Repositories in group '{group}'"
    else:
        repositories = repops_app.get_all_repositories()
        title = "All repositories"

    if not repositories:
        console.print(f"[yellow]No repositories found{' in group ' + group if group else ''}[/yellow]")
        return

    table = Table(title=title)
    table.add_column("Name", style="cyan")
    table.add_column("Group", style="magenta")
    table.add_column("Server", style="green")
    table.add_column("URL", style="blue")
    table.add_column("Local Path", style="yellow")
    table.add_column("Default Branch", style="red")

    for repo in repositories:
        table.add_row(
            repo.name,
            repo.group,
            repo.server_type.value,
            repo.url,
            str(repo.local_path),
            repo.default_branch,
        )

    console.print(table)


@app.command()
@handle_error
def add_repo(
    name: Annotated[str, typer.Argument(help="Repository name")],
    url: Annotated[str, typer.Argument(help="Repository URL")],
    server: Annotated[str, typer.Argument(help="Server type (github, gitlab, azure-devops)")],
    path: Annotated[Path, typer.Argument(help="Local path for repository")],
    branch: Annotated[str, typer.Argument(help="Default branch name")],
    config_path: Annotated[Optional[Path], typer.Option("--config", "-c", help="Path to config file")] = None,
    group: Annotated[str, typer.Option("--group", "-g", help="Group name")] = "default",
    save: Annotated[bool, typer.Option("--save/--no-save", help="Save config after adding")] = True,
) -> None:
    """Add a new repository to the configuration."""
    if config_path:
        config_path = config_path.resolve()
    repops_app = RepopsApp(config_path)

    # Try to load existing config, or create new one if it doesn't exist
    try:
        if config_path and config_path.exists():
            repops_app.load_config()
        elif config_path:
            # Create new config for specified path
            repops_app.create_new_config()
        # For default path, let the app handle loading/creating as needed
    except Exception as e:
        console.print(f"[red]Error loading config: {e}[/red]")
        return

    repops_app.add_repository(
        name=name,
        url=url,
        server_type=server,
        local_path=path,
        default_branch=branch,
        group=group,
    )

    console.print(f"[green]✓[/green] Added repository '{name}' to group '{group}'")

    if save:
        repops_app.save_config()
        console.print("[green]✓[/green] Configuration saved")


@app.command()
@handle_error
def remove_repo(
    name: Annotated[str, typer.Argument(help="Repository name to remove")],
    config_path: Annotated[Optional[Path], typer.Option("--config", "-c", help="Path to config file")] = None,
    save: Annotated[bool, typer.Option("--save/--no-save", help="Save config after removing")] = True,
) -> None:
    """Remove a repository from the configuration."""
    repops_app = RepopsApp(config_path)

    repo = repops_app.get_repository(name)
    if not repo:
        console.print(f"[red]Repository '{name}' not found[/red]")
        raise typer.Exit(1)

    repops_app.remove_repository(name)
    console.print(f"[green]✓[/green] Removed repository '{name}'")

    if save:
        repops_app.save_config()
        console.print("[green]✓[/green] Configuration saved")


@app.command()
@handle_error
def check_repos(
    config_path: Annotated[Optional[Path], typer.Option("--config", "-c", help="Path to config file")] = None,
    name: Annotated[Optional[str], typer.Option("--name", "-n", help="Check specific repository")] = None,
) -> None:
    """Check availability of repositories (local and remote)."""
    repops_app = RepopsApp(config_path)

    if name:
        repo = repops_app.get_repository(name)
        if not repo:
            console.print(f"[red]Repository '{name}' not found[/red]")
            raise typer.Exit(1)
        results = {name: repops_app.check_repository_availability(repo)}
    else:
        results = repops_app.check_all_repositories()

    table = Table(title="Repository Availability Check")
    table.add_column("Repository", style="cyan")
    table.add_column("Local", style="green")
    table.add_column("Remote", style="blue")
    table.add_column("Issues", style="red")

    for repo_name, result in results.items():
        local_status = "✓" if result["local_exists"] else "✗"
        remote_status = "✓" if result["remote_accessible"] else "✗"
        issues = "; ".join(result["errors"]) if result["errors"] else "None"

        table.add_row(repo_name, local_status, remote_status, issues)

    console.print(table)


@app.command()
@handle_error
def config_info(
    config_path: Annotated[Optional[Path], typer.Option("--config", "-c", help="Path to config file")] = None,
) -> None:
    """Show detailed information about the configuration."""
    if config_path:
        config_path = config_path.resolve()  # Convert to absolute path
    repops_app = RepopsApp(config_path)

    try:
        # Try to load config if a path was provided
        if config_path:
            repops_app.load_config()
        info = repops_app.get_config_info()
    except Exception as e:
        console.print(f"[red]Error getting config info: {e}[/red]")
        return

    console.print("[bold blue]Configuration Information[/bold blue]")
    console.print(f"Path: {info['path']}")
    console.print(f"Loaded: {'Yes' if info['loaded'] else 'No'}")

    if info["loaded"]:
        console.print(f"Total repositories: {info['total_repositories']}")

        console.print()
        console.print("[bold]Groups:[/bold]")
        for group, count in info["groups"].items():
            console.print(f"  {group}: {count} repositories")

        if info.get("server_types"):
            console.print()
            console.print("[bold]Server types:[/bold]")
            for server, count in info["server_types"].items():
                console.print(f"  {server}: {count} repositories")


if __name__ == "__main__":
    app()
