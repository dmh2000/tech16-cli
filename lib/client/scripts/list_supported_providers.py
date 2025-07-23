#!/usr/bin/env python3
"""Script to list all supported providers."""

import sys
import os

# Add the parent directory to the path to import the client library
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from client.config import SUPPORTED_MODELS, API_KEY_ENV_VARS


def main():
    """List all supported providers with their details."""
    print("Supported Providers:")
    print("=" * 20)
    
    for provider in SUPPORTED_MODELS.keys():
        model_count = len(SUPPORTED_MODELS[provider])
        env_var = API_KEY_ENV_VARS.get(provider, "N/A")
        
        print(f"\nProvider: {provider.upper()}")
        print(f"  Models supported: {model_count}")
        print(f"  API key env var: {env_var}")
    
    print(f"\nTotal providers supported: {len(SUPPORTED_MODELS)}")


if __name__ == "__main__":
    main()