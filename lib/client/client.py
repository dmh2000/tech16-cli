"""Abstract Client interface for LLM providers."""

from abc import ABC, abstractmethod
from typing import List


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