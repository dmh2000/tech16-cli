"""Tests for the Anthropic client."""

import pytest
from unittest.mock import patch, Mock
import sys
from lib.client.anthropic_client import AnthropicClient
from lib.client.exceptions import APIKeyMissingError, APICallError, ModelNotFoundError


class TestAnthropicClient:
    """Test cases for AnthropicClient."""

    @patch('anthropic.Anthropic')
    def test_init_success(self, mock_anthropic_class, mock_env_vars):
        """Test successful client initialization."""
        mock_anthropic_class.return_value = Mock()
        client = AnthropicClient()
        
        assert client.provider == "anthropic"
        assert client.api_key == "test-anthropic-key"
        mock_anthropic_class.assert_called_once_with(api_key="test-anthropic-key")

    def test_init_missing_api_key(self):
        """Test initialization fails when API key is missing."""
        with patch.dict('os.environ', {}, clear=True):
            with pytest.raises(APIKeyMissingError):
                AnthropicClient()

    def test_init_missing_library(self, mock_env_vars):
        """Test initialization fails when Anthropic library is not installed."""
        with patch.dict(sys.modules, {'anthropic': None}):
            with pytest.raises(APICallError, match="Anthropic library not installed"):
                AnthropicClient()

    @patch('anthropic.Anthropic')
    def test_query_success(self, mock_anthropic_class, mock_env_vars, sample_context, mock_anthropic_client):
        """Test successful query."""
        mock_anthropic_class.return_value = mock_anthropic_client
        client = AnthropicClient()
        
        response = client.query("claude-sonnet-4-20250514", sample_context)
        
        assert response == "The capital of France is Paris."
        mock_anthropic_client.messages.create.assert_called_once()

    @patch('anthropic.Anthropic')
    def test_query_invalid_model(self, mock_anthropic_class, mock_env_vars, sample_context):
        """Test query with invalid model."""
        mock_anthropic_class.return_value = Mock()
        client = AnthropicClient()
        
        response = client.query("invalid-model", sample_context)
        
        assert "Model 'invalid-model' not supported" in response

    @patch('anthropic.Anthropic')
    def test_query_empty_context(self, mock_anthropic_class, mock_env_vars):
        """Test query with empty context."""
        mock_anthropic_class.return_value = Mock()
        client = AnthropicClient()
        
        response = client.query("claude-sonnet-4-20250514", [])
        
        assert "Context cannot be empty" in response

    @patch('anthropic.Anthropic')
    def test_query_api_error(self, mock_anthropic_class, mock_env_vars, sample_context):
        """Test query when API call fails."""
        mock_client = Mock()
        mock_client.messages.create.side_effect = Exception("API Error")
        mock_anthropic_class.return_value = mock_client
        client = AnthropicClient()
        
        response = client.query("claude-sonnet-4-20250514", sample_context)
        
        assert "Error querying anthropic" in response
        assert "API Error" in response

    @patch('anthropic.Anthropic')
    def test_format_messages_single_context(self, mock_anthropic_class, mock_env_vars, sample_single_context):
        """Test message formatting with single context item."""
        mock_anthropic_class.return_value = Mock()
        client = AnthropicClient()
        
        messages = client._format_messages(sample_single_context)
        
        assert len(messages) == 1
        assert messages[0]["role"] == "user"
        assert messages[0]["content"] == "What is 2 + 2?"

    @patch('anthropic.Anthropic')
    def test_format_messages_multiple_context(self, mock_anthropic_class, mock_env_vars, sample_context):
        """Test message formatting with multiple context items."""
        mock_anthropic_class.return_value = Mock()
        client = AnthropicClient()
        
        messages = client._format_messages(sample_context)
        
        assert len(messages) == 3  # user, assistant, user continuation
        assert messages[0]["role"] == "user"
        assert messages[1]["role"] == "assistant"
        assert messages[2]["role"] == "user"

    @patch('anthropic.Anthropic')
    def test_format_messages_ends_with_user(self, mock_anthropic_class, mock_env_vars):
        """Test message formatting ensures last message is from user."""
        mock_anthropic_class.return_value = Mock()
        client = AnthropicClient()
        context = ["user message", "assistant response", "another assistant message"]
        
        messages = client._format_messages(context)
        
        assert messages[-1]["role"] == "user"
        # The third message is treated as user (index 2), so no continuation needed
        assert messages[-1]["content"] == "another assistant message"