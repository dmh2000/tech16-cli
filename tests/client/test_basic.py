"""Basic tests that can run without external dependencies."""

import pytest
import os
from unittest.mock import patch
from lib.client import get_supported_models
from lib.client.exceptions import ClientError, APIKeyMissingError, ModelNotFoundError
from lib.client.config import validate_model
from lib.client.utils import validate_context, clean_response


class TestBasicFunctionality:
    """Basic tests for the client library."""

    def test_imports(self):
        """Test that all modules can be imported."""
        from lib.client import new_anthropic, new_openai, new_gemini
        from lib.client.exceptions import ClientError
        from lib.client.config import get_api_key
        # If we get here, imports succeeded
        assert True

    def test_supported_models(self):
        """Test getting supported models."""
        anthropic_models = get_supported_models("anthropic")
        openai_models = get_supported_models("openai")
        gemini_models = get_supported_models("gemini")
        
        assert isinstance(anthropic_models, set)
        assert isinstance(openai_models, set)
        assert isinstance(gemini_models, set)
        
        assert len(anthropic_models) > 0
        assert len(openai_models) > 0
        assert len(gemini_models) > 0

    def test_model_validation(self):
        """Test model validation."""
        # Valid models should pass
        assert validate_model("anthropic", "claude-sonnet-4-20250514") == True
        assert validate_model("openai", "gpt-4o-mini") == True
        assert validate_model("gemini", "gemini-2.5-pro") == True
        
        # Invalid models should raise exception
        with pytest.raises(ModelNotFoundError):
            validate_model("anthropic", "invalid-model")
        
        with pytest.raises(ModelNotFoundError):
            validate_model("unknown-provider", "some-model")

    def test_context_validation(self):
        """Test context validation."""
        # Valid context should pass
        validate_context(["Hello", "World"])
        validate_context(["Single message"])
        
        # Invalid context should raise exception
        with pytest.raises(Exception):
            validate_context([])
        
        with pytest.raises(Exception):
            validate_context(["Hello", ""])
        
        with pytest.raises(Exception):
            validate_context("not a list")

    def test_response_cleaning(self):
        """Test response cleaning functionality."""
        # Test basic cleaning
        result = clean_response("  Hello World!  ")
        assert "Hello World!" in result
        
        # Test with various whitespace
        result = clean_response("\n  Test  \r\n")
        assert "Test" in result
        
        # Test with non-string input
        result = clean_response(123)
        assert result == "123"

    def test_exception_hierarchy(self):
        """Test exception class hierarchy."""
        from lib.client.exceptions import (
            ClientError, APIKeyMissingError, ModelNotFoundError,
            APICallError, InvalidContextError
        )
        
        # Test inheritance
        assert issubclass(APIKeyMissingError, ClientError)
        assert issubclass(ModelNotFoundError, ClientError)
        assert issubclass(APICallError, ClientError)
        assert issubclass(InvalidContextError, ClientError)

    def test_api_key_missing_behavior(self):
        """Test behavior when API keys are missing."""
        from lib.client import new_anthropic, new_openai, new_gemini
        
        # Clear environment variables
        env_vars = ['ANTHROPIC_API_KEY', 'OPENAI_API_KEY', 'GOOGLE_API_KEY']
        with patch.dict(os.environ, {}, clear=True):
            # All factory functions should raise APIKeyMissingError
            with pytest.raises(APIKeyMissingError):
                new_anthropic()
            
            with pytest.raises(APIKeyMissingError):
                new_openai()
            
            with pytest.raises(APIKeyMissingError):
                new_gemini()