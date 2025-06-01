"""Exception classes for repops application."""

from typing import Any


class RepopsError(Exception):
    """Base exception class for all repops errors."""

    def __init__(self, message: str, details: dict[str, Any] | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.details = details or {}


class ConfigError(RepopsError):
    """Exception raised for configuration-related errors."""

    pass


class RepositoryError(RepopsError):
    """Exception raised for repository-related errors."""

    pass


class ValidationError(RepopsError):
    """Exception raised for validation errors."""

    pass


class FileNotFoundError(RepopsError):
    """Exception raised when a required file is not found."""

    pass


class InvalidConfigError(ConfigError):
    """Exception raised when configuration is invalid."""

    pass


class MissingRequiredFieldError(ValidationError):
    """Exception raised when a required field is missing."""

    def __init__(self, field_name: str, context: str = "") -> None:
        message = f"Missing required field: {field_name}"
        if context:
            message += f" in {context}"
        super().__init__(message, {"field_name": field_name, "context": context})


class InvalidServerTypeError(ValidationError):
    """Exception raised when server type is invalid or unsupported."""

    def __init__(self, server_type: str, supported_types: list[str]) -> None:
        message = f"Invalid server type: {server_type}. Supported types: {', '.join(supported_types)}"
        super().__init__(message, {"server_type": server_type, "supported_types": supported_types})
