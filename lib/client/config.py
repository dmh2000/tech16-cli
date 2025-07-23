"""Configuration management for the client library."""

import os
from typing import Dict, Set
from .exceptions import APIKeyMissingError, ModelNotFoundError


# Supported models for each provider
SUPPORTED_MODELS = {
    "anthropic": {
        "claude-sonnet-4-20250514",
        "claude-3-5-haiku-20241022",
    },
    "openai": {
        "o4-mini",
        "o3-mini",
        "gpt-4o-mini",
    },
    "gemini": {
        "gemini-2.5-pro",
        "gemini-2.5-flash",
    },
}

# Environment variable names for API keys
API_KEY_ENV_VARS = {
    "anthropic": "ANTHROPIC_API_KEY",
    "openai": "OPENAI_API_KEY",
    "gemini": "GOOGLE_API_KEY",
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
        raise APIKeyMissingError(
            f"API key not found. Please set {env_var} environment variable."
        )

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


def get_provider_for_model(model: str) -> str:
    """
    Get the provider name for a given model.

    Args:
        model: The model identifier

    Returns:
        str: The provider name

    Raises:
        ModelNotFoundError: If the model is not found in any provider
    """
    for provider, models in SUPPORTED_MODELS.items():
        if model in models:
            return provider

    all_models = []
    for models in SUPPORTED_MODELS.values():
        all_models.extend(sorted(models))

    raise ModelNotFoundError(
        f"Model '{model}' not found in any provider. "
        f"Available models: {', '.join(all_models)}"
    )
