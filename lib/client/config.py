"""Configuration management for the client library."""

import os
from typing import Dict, Set
from .exceptions import APIKeyMissingError, ModelNotFoundError


# Supported models for each provider
SUPPORTED_MODELS = {
    "anthropic": {
        "claude-3-5-sonnet-20241022",
        "claude-3-5-haiku-20241022", 
        "claude-3-opus-20240229",
        "claude-3-sonnet-20240229",
        "claude-3-haiku-20240307"
    },
    "openai": {
        "gpt-4o",
        "gpt-4o-mini",
        "gpt-4-turbo",
        "gpt-4",
        "gpt-3.5-turbo"
    },
    "gemini": {
        "gemini-1.5-pro",
        "gemini-1.5-flash",
        "gemini-1.0-pro"
    }
}

# Environment variable names for API keys
API_KEY_ENV_VARS = {
    "anthropic": "ANTHROPIC_API_KEY",
    "openai": "OPENAI_API_KEY", 
    "gemini": "GOOGLE_API_KEY"
}


def get_api_key(provider: str) -> str:
    """
    Get API key from environment variables.
    
    Args:
        provider: The provider name (anthropic, openai, gemini)
        
    Returns:
        str: The API key
        
    Raises:
        APIKeyMissingError: If the API key is not found
    """
    if provider not in API_KEY_ENV_VARS:
        raise APIKeyMissingError(f"Unknown provider: {provider}")
    
    env_var = API_KEY_ENV_VARS[provider]
    api_key = os.getenv(env_var)
    
    if not api_key:
        raise APIKeyMissingError(f"API key not found. Please set {env_var} environment variable.")
    
    return api_key


def validate_model(provider: str, model: str) -> bool:
    """
    Validate if a model is supported by the provider.
    
    Args:
        provider: The provider name
        model: The model identifier
        
    Returns:
        bool: True if model is supported
        
    Raises:
        ModelNotFoundError: If model is not supported by the provider
    """
    if provider not in SUPPORTED_MODELS:
        raise ModelNotFoundError(f"Unknown provider: {provider}")
    
    if model not in SUPPORTED_MODELS[provider]:
        supported = ", ".join(sorted(SUPPORTED_MODELS[provider]))
        raise ModelNotFoundError(
            f"Model '{model}' not supported by {provider}. "
            f"Supported models: {supported}"
        )
    
    return True


def get_supported_models(provider: str) -> Set[str]:
    """
    Get the set of supported models for a provider.
    
    Args:
        provider: The provider name
        
    Returns:
        Set[str]: Set of supported model identifiers
    """
    return SUPPORTED_MODELS.get(provider, set())