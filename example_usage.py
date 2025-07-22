#!/usr/bin/env python3
"""
Example usage of the client library.

This script demonstrates how to use the client library to query different LLM providers.
Before running, make sure to set the appropriate environment variables:

    export ANTHROPIC_API_KEY="your_anthropic_key_here"
    export OPENAI_API_KEY="your_openai_key_here"  
    export GOOGLE_API_KEY="your_google_key_here"
"""

import os
from lib.client import new_anthropic, new_openai, new_gemini, get_supported_models
from lib.client.exceptions import APIKeyMissingError, APICallError


def demonstrate_model_info():
    """Display information about supported models."""
    print("=== Supported Models ===")
    
    providers = ["anthropic", "openai", "gemini"]
    for provider in providers:
        models = get_supported_models(provider)
        print(f"\n{provider.title()} models ({len(models)}):")
        for model in sorted(models):
            print(f"  - {model}")


def test_client(client_name, client_factory, model, context):
    """Test a client with the given parameters."""
    print(f"\n=== Testing {client_name} ===")
    
    try:
        # Create client instance
        client = client_factory()
        print(f"✓ {client_name} client created successfully")
        
        # Make a query
        print(f"Querying model: {model}")
        print(f"Context: {context}")
        
        response = client.query(model, context)
        print(f"Response: {response[:200]}{'...' if len(response) > 200 else ''}")
        
        return True
        
    except APIKeyMissingError as e:
        print(f"✗ API key missing: {e}")
        return False
    except APICallError as e:
        print(f"✗ API call error: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False


def main():
    """Main demonstration function."""
    print("Client Library Usage Example")
    print("=" * 40)
    
    # Display model information
    demonstrate_model_info()
    
    # Test context
    context = [
        "You are a helpful assistant.",
        "What is the capital of France? Please provide a brief answer."
    ]
    
    # Test clients (only if API keys are available)
    clients_to_test = [
        ("Anthropic", new_anthropic, "claude-3-5-haiku-20241022"),
        ("OpenAI", new_openai, "gpt-4o-mini"),
        ("Gemini", new_gemini, "gemini-1.5-flash")
    ]
    
    successful_tests = 0
    total_tests = len(clients_to_test)
    
    for client_name, client_factory, model in clients_to_test:
        if test_client(client_name, client_factory, model, context):
            successful_tests += 1
    
    # Summary
    print(f"\n=== Summary ===")
    print(f"Tests passed: {successful_tests}/{total_tests}")
    
    if successful_tests == 0:
        print("\nNote: No tests passed. This is likely because API keys are not set.")
        print("Set the following environment variables to test the clients:")
        print("  - ANTHROPIC_API_KEY")
        print("  - OPENAI_API_KEY") 
        print("  - GOOGLE_API_KEY")


if __name__ == "__main__":
    main()