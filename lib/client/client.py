"""Abstract Client interface for LLM providers."""

from abc import ABC, abstractmethod
from typing import List

from .exceptions import ModelNotFoundError, APIKeyMissingError, error_exit
from .config import get_provider_for_model


class Client(ABC):
    """Abstract base class for all LLM client implementations."""

    @abstractmethod
    def query(self, model: str, context: List[str]) -> str:
        """
        Query the LLM with the given model and context.

        Args:
            model: The model identifier to use for the query
            context: List of strings that make up the context/conversation

        Returns:
            str: The response from the LLM or an error message

        Raises:
            APIKeyMissingError: If required API key is not found
            ModelNotFoundError: If the specified model is not available
            APICallError: If the API call fails
            InvalidContextError: If the context format is invalid
        """
        pass


def create_client(model: str):
    """Create appropriate client instance for the given model."""
    from .anthropic_client import AnthropicClient
    from .gemini_client import GeminiClient
    from .openai_client import OpenAIClient

    try:
        provider = get_provider_for_model(model)
    except ModelNotFoundError as e:
        error_exit(str(e))

    try:
        if provider == "anthropic":
            return AnthropicClient()
        elif provider == "openai":
            return OpenAIClient()
        elif provider == "gemini":
            return GeminiClient()
        else:
            error_exit(f"Unknown provider: {provider}")
    except APIKeyMissingError as e:
        error_exit(str(e))
    except Exception as e:
        error_exit(f"Failed to create client for provider '{provider}': {e}")
