"""Tests for the config module."""

import pytest
from unittest.mock import patch
from lib.client.config import get_api_key, validate_model, get_supported_models
from lib.client.exceptions import APIKeyMissingError, ModelNotFoundError


class TestConfig:
    """Test cases for config module."""

    def test_get_api_key_success(self, mock_env_vars):
        """Test successful API key retrieval."""
        api_key = get_api_key("anthropic")
        assert api_key == "test-anthropic-key"
        
        api_key = get_api_key("openai")
        assert api_key == "test-openai-key"
        
        api_key = get_api_key("gemini")
        assert api_key == "test-google-key"

    def test_get_api_key_unknown_provider(self):
        """Test API key retrieval with unknown provider."""
        with pytest.raises(APIKeyMissingError, match="Unknown provider"):
            get_api_key("unknown")

    def test_get_api_key_missing(self):
        """Test API key retrieval when environment variable is not set."""
        with pytest.raises(APIKeyMissingError, match="Please set ANTHROPIC_API_KEY"):
            get_api_key("anthropic")

    def test_validate_model_success(self):
        """Test successful model validation."""
        assert validate_model("anthropic", "claude-3-5-sonnet-20241022") == True
        assert validate_model("openai", "gpt-4o") == True
        assert validate_model("gemini", "gemini-1.5-pro") == True

    def test_validate_model_unknown_provider(self):
        """Test model validation with unknown provider."""
        with pytest.raises(ModelNotFoundError, match="Unknown provider"):
            validate_model("unknown", "some-model")

    def test_validate_model_unsupported_model(self):
        """Test model validation with unsupported model."""
        with pytest.raises(ModelNotFoundError, match="not supported by anthropic"):
            validate_model("anthropic", "unsupported-model")

    def test_get_supported_models(self):
        """Test getting supported models for each provider."""
        anthropic_models = get_supported_models("anthropic")
        openai_models = get_supported_models("openai")
        gemini_models = get_supported_models("gemini")
        
        assert isinstance(anthropic_models, set)
        assert isinstance(openai_models, set)
        assert isinstance(gemini_models, set)
        
        assert len(anthropic_models) > 0
        assert len(openai_models) > 0
        assert len(gemini_models) > 0
        
        assert "claude-3-5-sonnet-20241022" in anthropic_models
        assert "gpt-4o" in openai_models
        assert "gemini-1.5-pro" in gemini_models

    def test_get_supported_models_unknown_provider(self):
        """Test getting supported models for unknown provider."""
        result = get_supported_models("unknown")
        assert result == set()