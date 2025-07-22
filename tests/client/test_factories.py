"""Tests for factory functions."""

import pytest
from unittest.mock import patch
from lib.client import new_anthropic, new_openai, new_gemini
from lib.client.anthropic_client import AnthropicClient
from lib.client.openai_client import OpenAIClient
from lib.client.gemini_client import GeminiClient
from lib.client.exceptions import APIKeyMissingError, APICallError


class TestFactoryFunctions:
    """Test cases for factory functions."""

    @patch('lib.client.anthropic_client.Anthropic')
    def test_new_anthropic_success(self, mock_anthropic_class, mock_env_vars):
        """Test successful Anthropic client creation."""
        client = new_anthropic()
        
        assert isinstance(client, AnthropicClient)
        assert client.provider == "anthropic"

    def test_new_anthropic_missing_api_key(self):
        """Test Anthropic client creation with missing API key."""
        with pytest.raises(APIKeyMissingError):
            new_anthropic()

    @patch('lib.client.openai_client.OpenAI')
    def test_new_openai_success(self, mock_openai_class, mock_env_vars):
        """Test successful OpenAI client creation."""
        client = new_openai()
        
        assert isinstance(client, OpenAIClient)
        assert client.provider == "openai"

    def test_new_openai_missing_api_key(self):
        """Test OpenAI client creation with missing API key."""
        with pytest.raises(APIKeyMissingError):
            new_openai()

    @patch('lib.client.gemini_client.genai')
    def test_new_gemini_success(self, mock_genai, mock_env_vars):
        """Test successful Gemini client creation."""
        client = new_gemini()
        
        assert isinstance(client, GeminiClient)
        assert client.provider == "gemini"

    def test_new_gemini_missing_api_key(self):
        """Test Gemini client creation with missing API key."""
        with pytest.raises(APIKeyMissingError):
            new_gemini()

    @patch('lib.client.anthropic_client.Anthropic')
    def test_new_anthropic_missing_library(self, mock_anthropic_class, mock_env_vars):
        """Test Anthropic client creation with missing library."""
        with patch.dict('sys.modules', {'anthropic': None}):
            with pytest.raises(APICallError, match="Anthropic library not installed"):
                new_anthropic()

    @patch('lib.client.openai_client.OpenAI')
    def test_new_openai_missing_library(self, mock_openai_class, mock_env_vars):
        """Test OpenAI client creation with missing library."""
        with patch.dict('sys.modules', {'openai': None}):
            with pytest.raises(APICallError, match="OpenAI library not installed"):
                new_openai()

    @patch('lib.client.gemini_client.genai')
    def test_new_gemini_missing_library(self, mock_genai, mock_env_vars):
        """Test Gemini client creation with missing library."""
        with patch.dict('sys.modules', {'google.generativeai': None}):
            with pytest.raises(APICallError, match="Google GenAI library not installed"):
                new_gemini()