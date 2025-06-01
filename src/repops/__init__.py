"""Repops - Tool for managing multiple git repositories."""

from repops.cli.main import app


def main() -> None:
    """Main entry point for the repops application."""
    app()


__all__ = ["main"]
