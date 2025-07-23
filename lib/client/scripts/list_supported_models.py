#!/usr/bin/env python3
"""Script to list all supported models from all providers."""

import sys
import os

# Add the parent directory to the path to import the client library
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from client.config import SUPPORTED_MODELS


def main():
    """List all supported models grouped by provider."""
    print("Supported Models by Provider:")
    print("=" * 30)
    
    for provider, models in SUPPORTED_MODELS.items():
        print(f"\n{provider.upper()}:")
        for model in sorted(models):
            print(f"  - {model}")
    
    # Also show total count
    total_models = sum(len(models) for models in SUPPORTED_MODELS.values())
    print(f"\nTotal models supported: {total_models}")


if __name__ == "__main__":
    main()