"""Custom exceptions for the client library."""


class ClientError(Exception):
    """Base exception for all client-related errors."""
    pass


class APIKeyMissingError(ClientError):
    """Raised when a required API key is not found in environment variables."""
    pass


class ModelNotFoundError(ClientError):
    """Raised when the specified model is not available for the provider."""
    pass


class APICallError(ClientError):
    """Raised when the underlying API call fails."""
    pass


class InvalidContextError(ClientError):
    """Raised when the context format is invalid."""
    pass