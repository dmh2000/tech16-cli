#!/usr/bin/env python3
"""Script to get the provider for a given model."""

import sys
import os

# Add the parent directory to the path to import the client library
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from client.config import get_provider_for_model
from client.exceptions import ModelNotFoundError


def main():
    """Get the provider for a model specified as a command line argument."""
    if len(sys.argv) != 2:
        print("Usage: python3 get_provider_for_model.py <model_name>")
        print("\nExample: python3 get_provider_for_model.py claude-sonnet-4")
        sys.exit(1)
    
    model_name = sys.argv[1]
    
    try:
        provider = get_provider_for_model(model_name)
        print(f"Model '{model_name}' is provided by: {provider}")
    except ModelNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()