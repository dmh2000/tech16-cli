#!/usr/bin/env python3
"""
Simple test runner to verify the client library functionality.
This script runs focused tests without requiring external API dependencies.
"""

import sys
import os
from unittest.mock import patch, Mock

# Add the project root to Python path
sys.path.insert(0, '/home/dmh2000/projects/tech16')

def test_imports():
    """Test that all modules can be imported successfully."""
    print("Testing imports...")
    
    try:
        from lib.client import new_anthropic, new_openai, new_gemini, get_supported_models
        from lib.client.exceptions import ClientError, APIKeyMissingError
        from lib.client.config import validate_model, get_api_key
        from lib.client.utils import validate_context, clean_response
        print("✓ All imports successful")
        return True
    except Exception as e:
        print(f"✗ Import failed: {e}")
        return False

def test_config_validation():
    """Test configuration validation functions."""
    print("Testing config validation...")
    
    try:
        from lib.client.config import validate_model, get_supported_models
        from lib.client.exceptions import ModelNotFoundError
        
        # Test supported models
        anthropic_models = get_supported_models("anthropic")
        assert len(anthropic_models) > 0
        assert "claude-3-5-sonnet-20241022" in anthropic_models
        
        # Test valid model validation
        validate_model("anthropic", "claude-3-5-sonnet-20241022")
        
        # Test invalid model validation
        try:
            validate_model("anthropic", "invalid-model")
            assert False, "Should have raised ModelNotFoundError"
        except ModelNotFoundError:
            pass
        
        print("✓ Config validation tests passed")
        return True
    except Exception as e:
        print(f"✗ Config validation failed: {e}")
        return False

def test_utils_validation():
    """Test utility functions."""
    print("Testing utils validation...")
    
    try:
        from lib.client.utils import validate_context, clean_response
        from lib.client.exceptions import InvalidContextError
        
        # Test valid context
        validate_context(["Hello", "World"])
        
        # Test invalid context
        try:
            validate_context([])
            assert False, "Should have raised InvalidContextError"
        except InvalidContextError:
            pass
        
        # Test response cleaning
        cleaned = clean_response("  Hello World!  \r\n  ")
        assert "Hello World!" in cleaned
        
        print("✓ Utils validation tests passed")
        return True
    except Exception as e:
        print(f"✗ Utils validation failed: {e}")
        return False

def test_exception_hierarchy():
    """Test exception class hierarchy."""
    print("Testing exception hierarchy...")
    
    try:
        from lib.client.exceptions import (
            ClientError, APIKeyMissingError, ModelNotFoundError,
            APICallError, InvalidContextError
        )
        
        # Test inheritance
        assert issubclass(APIKeyMissingError, ClientError)
        assert issubclass(ModelNotFoundError, ClientError)
        assert issubclass(APICallError, ClientError)
        assert issubclass(InvalidContextError, ClientError)
        assert issubclass(ClientError, Exception)
        
        # Test exception creation
        error = APIKeyMissingError("Test message")
        assert str(error) == "Test message"
        
        print("✓ Exception hierarchy tests passed")
        return True
    except Exception as e:
        print(f"✗ Exception hierarchy failed: {e}")
        return False

def test_client_initialization_without_deps():
    """Test client initialization behavior without external dependencies."""
    print("Testing client initialization (no external deps)...")
    
    try:
        from lib.client.anthropic_client import AnthropicClient
        from lib.client.openai_client import OpenAIClient  
        from lib.client.gemini_client import GeminiClient
        from lib.client.exceptions import APIKeyMissingError, APICallError
        
        # Clear environment variables to test API key missing scenario
        env_backup = {}
        api_key_vars = ['ANTHROPIC_API_KEY', 'OPENAI_API_KEY', 'GOOGLE_API_KEY']
        for var in api_key_vars:
            if var in os.environ:
                env_backup[var] = os.environ[var]
                del os.environ[var]
        
        try:
            # Test that clients fail appropriately without API keys
            try:
                AnthropicClient()
                assert False, "Should have raised APIKeyMissingError"
            except APIKeyMissingError:
                pass
                
            try:
                OpenAIClient()
                assert False, "Should have raised APIKeyMissingError"
            except APIKeyMissingError:
                pass
                
            try:
                GeminiClient()
                assert False, "Should have raised APIKeyMissingError"
            except APIKeyMissingError:
                pass
        finally:
            # Restore environment variables
            for var, value in env_backup.items():
                os.environ[var] = value
        
        print("✓ Client initialization tests passed")
        return True
    except Exception as e:
        print(f"✗ Client initialization failed: {e}")
        return False

def test_factory_functions():
    """Test factory functions with mocked environment."""
    print("Testing factory functions...")
    
    try:
        from lib.client import new_anthropic, new_openai, new_gemini
        from lib.client.exceptions import APIKeyMissingError, APICallError
        
        # Clear environment variables to test API key missing scenario
        env_backup = {}
        api_key_vars = ['ANTHROPIC_API_KEY', 'OPENAI_API_KEY', 'GOOGLE_API_KEY']
        for var in api_key_vars:
            if var in os.environ:
                env_backup[var] = os.environ[var]
                del os.environ[var]
        
        try:
            # Test that factory functions fail without API keys
            try:
                new_anthropic()
                assert False, "Should have raised APIKeyMissingError"
            except APIKeyMissingError:
                pass
                
            # Test basic functionality - we can't test library import failures
            # in this environment since the libraries might be available
            print("  - API key validation working correctly")
        finally:
            # Restore environment variables
            for var, value in env_backup.items():
                os.environ[var] = value
        
        print("✓ Factory function tests passed")
        return True
    except Exception as e:
        import traceback
        print(f"✗ Factory function tests failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    print("Client Library Test Runner")
    print("=" * 40)
    
    tests = [
        test_imports,
        test_config_validation, 
        test_utils_validation,
        test_exception_hierarchy,
        test_client_initialization_without_deps,
        test_factory_functions
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"Results: {passed}/{total} test groups passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        return 0
    else:
        print("❌ Some tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())