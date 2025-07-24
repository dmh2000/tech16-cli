"""Tests for the OpenAI client."""

import pytest
from unittest.mock import patch, Mock
from lib.client.openai_client import OpenAIClient
from lib.client.exceptions import APIKeyMissingError, APICallError, ModelNotFoundError


class TestOpenAIClient:
    """Test cases for OpenAIClient."""

    @patch('openai.OpenAI')
    def test_init_success(self, mock_openai_class, mock_env_vars):
        """Test successful client initialization."""
        mock_openai_class.return_value = Mock()
        client = OpenAIClient()
        
        assert client.provider == "openai"
        assert client.api_key == "test-openai-key"
        mock_openai_class.assert_called_once_with(api_key="test-openai-key")

    def test_init_missing_api_key(self):
        """Test initialization fails when API key is missing."""
        with patch.dict('os.environ', {}, clear=True):
            with pytest.raises(APIKeyMissingError):
                OpenAIClient()

    @patch('openai.OpenAI')
    def test_init_missing_library(self, mock_openai_class, mock_env_vars):
        """Test initialization fails when OpenAI library is not installed."""
        with patch.dict('sys.modules', {'openai': None}):
            with pytest.raises(APICallError, match="OpenAI library not installed"):
                OpenAIClient()

    @patch('openai.OpenAI')
    def test_query_success(self, mock_openai_class, mock_env_vars, sample_context, mock_openai_client):
        """Test successful query."""
        mock_openai_class.return_value = mock_openai_client
        client = OpenAIClient()
        
        response = client.query("gpt-4o-mini", sample_context)
        
        assert response == "The capital of France is Paris."
        mock_openai_client.chat.completions.create.assert_called_once()

    @patch('openai.OpenAI')
    def test_query_invalid_model(self, mock_openai_class, mock_env_vars, sample_context):
        """Test query with invalid model."""
        mock_openai_class.return_value = Mock()
        client = OpenAIClient()
        
        response = client.query("invalid-model", sample_context)
        
        assert "Model 'invalid-model' not supported" in response

    @patch('openai.OpenAI')
    def test_query_empty_context(self, mock_openai_class, mock_env_vars):
        """Test query with empty context."""
        mock_openai_class.return_value = Mock()
        client = OpenAIClient()
        
        response = client.query("gpt-4o-mini", [])
        
        assert "Context cannot be empty" in response

    @patch('openai.OpenAI')
    def test_query_api_error(self, mock_openai_class, mock_env_vars, sample_context):
        """Test query when API call fails."""
        mock_client = Mock()
        mock_client.chat.completions.create.side_effect = Exception("API Error")
        mock_openai_class.return_value = mock_client
        client = OpenAIClient()
        
        response = client.query("gpt-4o-mini", sample_context)
        
        assert "Error querying openai" in response
        assert "API Error" in response

    @patch('openai.OpenAI')
    def test_format_messages_single_context(self, mock_openai_class, mock_env_vars, sample_single_context):
        """Test message formatting with single context item."""
        mock_openai_class.return_value = Mock()
        client = OpenAIClient()
        
        messages = client._format_messages(sample_single_context)
        
        assert len(messages) == 1
        assert messages[0]["role"] == "user"
        assert messages[0]["content"] == "What is 2 + 2?"

    @patch('openai.OpenAI')
    def test_format_messages_system_message(self, mock_openai_class, mock_env_vars):
        """Test message formatting with system-like first message."""
        mock_openai_class.return_value = Mock()
        client = OpenAIClient()
        context = ["You are a helpful assistant.", "What is 2 + 2?"]
        
        messages = client._format_messages(context)
        
        assert len(messages) == 3  # system, assistant, user continuation
        assert messages[0]["role"] == "system"
        assert messages[1]["role"] == "assistant"
        assert messages[2]["role"] == "user"

    @patch('openai.OpenAI')
    def test_format_messages_multiple_context(self, mock_openai_class, mock_env_vars):
        """Test message formatting with multiple context items."""
        mock_openai_class.return_value = Mock()
        client = OpenAIClient()
        context = ["Hello", "Hi there", "How are you?"]
        
        messages = client._format_messages(context)
        
        assert len(messages) == 3
        assert messages[0]["role"] == "user"  # First message treated as user
        assert messages[1]["role"] == "assistant"
        assert messages[2]["role"] == "user"

    @patch('openai.OpenAI')
    def test_looks_like_system_message(self, mock_openai_class, mock_env_vars):
        """Test system message detection."""
        mock_openai_class.return_value = Mock()
        client = OpenAIClient()
        
        assert client._looks_like_system_message("You are a helpful assistant.")
        assert client._looks_like_system_message("Your role is to help users.")
        assert client._looks_like_system_message("Act as a translator.")
        assert not client._looks_like_system_message("What is the weather?")
        assert not client._looks_like_system_message("Hello there!")

    @patch('openai.OpenAI')
    def test_format_messages_ends_with_user(self, mock_openai_class, mock_env_vars):
        """Test message formatting ensures last message is from user."""
        mock_openai_class.return_value = Mock()
        client = OpenAIClient()
        context = ["user message", "assistant response"]
        
        messages = client._format_messages(context)
        
        assert messages[-1]["role"] == "user"
        assert "Please continue" in messages[-1]["content"]