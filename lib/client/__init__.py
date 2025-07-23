"""
Client library for querying multiple LLM providers.

This package provides a unified interface for querying LLM providers including:
- Anthropic Claude
- OpenAI GPT
- Google Gemini

Usage:
    from lib.client import new_anthropic, new_openai, new_gemini
    
    # Create clients
    anthropic_client = new_anthropic()
    openai_client = new_openai()  
    gemini_client = new_gemini()
    
    # Query models
    context = ["You are a helpful assistant.", "What is the capital of France?"]
    response = anthropic_client.query("claude-3-5-sonnet-20241022", context)
"""

from .client import Client
from .anthropic_client import AnthropicClient
from .openai_client import OpenAIClient
from .gemini_client import GeminiClient
from .exceptions import (
    ClientError,
    APIKeyMissingError,
    ModelNotFoundError,
    APICallError,
    InvalidContextError
)
from .config import get_supported_models


def new_anthropic() -> AnthropicClient:
    """
    Create and return a new Anthropic client instance.
    
    Returns:
        AnthropicClient: Configured Anthropic client
        
    Raises:
        APIKeyMissingError: If ANTHROPIC_API_KEY environment variable is not set
        APICallError: If the Anthropic library is not installed
    """
    return AnthropicClient()


def new_openai() -> OpenAIClient:
    """
    Create and return a new OpenAI client instance.
    
    Returns:
        OpenAIClient: Configured OpenAI client
        
    Raises:
        APIKeyMissingError: If OPENAI_API_KEY environment variable is not set
        APICallError: If the OpenAI library is not installed
    """
    return OpenAIClient()


def new_gemini() -> GeminiClient:
    """
    Create and return a new Gemini client instance.
    
    Returns:
        GeminiClient: Configured Gemini client
        
    Raises:
        APIKeyMissingError: If GOOGLE_API_KEY environment variable is not set
        APICallError: If the google-generativeai library is not installed
    """
    return GeminiClient()


__all__ = [
    'Client',
    'AnthropicClient', 
    'OpenAIClient',
    'GeminiClient',
    'new_anthropic',
    'new_openai', 
    'new_gemini',
    'ClientError',
    'APIKeyMissingError',
    'ModelNotFoundError', 
    'APICallError',
    'InvalidContextError',
    'get_supported_models'
]