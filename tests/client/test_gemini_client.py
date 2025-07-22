"""Tests for the Gemini client."""

import pytest
from unittest.mock import patch, Mock
from lib.client.gemini_client import GeminiClient
from lib.client.exceptions import APIKeyMissingError, APICallError, ModelNotFoundError


class TestGeminiClient:
    """Test cases for GeminiClient."""

    @patch('lib.client.gemini_client.genai')
    def test_init_success(self, mock_genai, mock_env_vars):
        """Test successful client initialization."""
        client = GeminiClient()
        
        assert client.provider == "gemini"
        assert client.api_key == "test-google-key"
        mock_genai.configure.assert_called_once_with(api_key="test-google-key")

    def test_init_missing_api_key(self):
        """Test initialization fails when API key is missing."""
        with pytest.raises(APIKeyMissingError):
            GeminiClient()

    @patch('lib.client.gemini_client.genai')
    def test_init_missing_library(self, mock_genai, mock_env_vars):
        """Test initialization fails when Google GenAI library is not installed."""
        with patch.dict('sys.modules', {'google.generativeai': None}):
            with pytest.raises(APICallError, match="Google GenAI library not installed"):
                GeminiClient()

    @patch('lib.client.gemini_client.genai')
    def test_query_success(self, mock_genai, mock_env_vars, sample_context, mock_gemini_response):
        """Test successful query."""
        mock_model = Mock()
        mock_model.generate_content.return_value = mock_gemini_response
        mock_genai.GenerativeModel.return_value = mock_model
        
        client = GeminiClient()
        response = client.query("gemini-1.5-pro", sample_context)
        
        assert response == "The capital of France is Paris."
        mock_model.generate_content.assert_called_once()

    @patch('lib.client.gemini_client.genai')
    def test_query_invalid_model(self, mock_genai, mock_env_vars, sample_context):
        """Test query with invalid model."""
        client = GeminiClient()
        
        response = client.query("invalid-model", sample_context)
        
        assert "Model 'invalid-model' not supported" in response

    @patch('lib.client.gemini_client.genai')
    def test_query_empty_context(self, mock_genai, mock_env_vars):
        """Test query with empty context."""
        client = GeminiClient()
        
        response = client.query("gemini-1.5-pro", [])
        
        assert "Context cannot be empty" in response

    @patch('lib.client.gemini_client.genai')
    def test_query_safety_blocked(self, mock_genai, mock_env_vars, sample_context):
        """Test query when response is blocked by safety filters."""
        mock_model = Mock()
        mock_response = Mock()
        mock_response.candidates = [Mock(finish_reason=Mock(name="SAFETY"))]
        mock_model.generate_content.return_value = mock_response
        mock_genai.GenerativeModel.return_value = mock_model
        
        client = GeminiClient()
        response = client.query("gemini-1.5-pro", sample_context)
        
        assert "Response was blocked due to safety filters" in response

    @patch('lib.client.gemini_client.genai')
    def test_query_api_error(self, mock_genai, mock_env_vars, sample_context):
        """Test query when API call fails."""
        mock_model = Mock()
        mock_model.generate_content.side_effect = Exception("API Error")
        mock_genai.GenerativeModel.return_value = mock_model
        
        client = GeminiClient()
        response = client.query("gemini-1.5-pro", sample_context)
        
        assert "Error querying gemini" in response
        assert "API Error" in response

    @patch('lib.client.gemini_client.genai')
    def test_format_prompt_single_context(self, mock_genai, mock_env_vars, sample_single_context):
        """Test prompt formatting with single context item."""
        client = GeminiClient()
        
        prompt = client._format_prompt(sample_single_context)
        
        assert prompt == "What is 2 + 2?"

    @patch('lib.client.gemini_client.genai')
    def test_format_prompt_system_message(self, mock_genai, mock_env_vars):
        """Test prompt formatting with system-like first message."""
        client = GeminiClient()
        context = ["You are a helpful assistant.", "What is 2 + 2?"]
        
        prompt = client._format_prompt(context)
        
        assert "Instructions: You are a helpful assistant." in prompt
        assert "Human: What is 2 + 2?" in prompt

    @patch('lib.client.gemini_client.genai')
    def test_format_prompt_conversation(self, mock_genai, mock_env_vars):
        """Test prompt formatting with conversation format."""
        client = GeminiClient()
        context = ["Hello", "Hi there", "How are you?"]
        
        prompt = client._format_prompt(context)
        
        assert "Human: Hello" in prompt
        assert "Assistant: Hi there" in prompt
        assert "Human: How are you?" in prompt

    @patch('lib.client.gemini_client.genai')
    def test_format_prompt_ends_with_human(self, mock_genai, mock_env_vars):
        """Test prompt formatting ensures it ends with human message."""
        client = GeminiClient()
        context = ["user message", "assistant response"]
        
        prompt = client._format_prompt(context)
        
        assert prompt.endswith("Human: Please provide your response.")

    @patch('lib.client.gemini_client.genai')
    def test_looks_like_system_message(self, mock_genai, mock_env_vars):
        """Test system message detection."""
        client = GeminiClient()
        
        assert client._looks_like_system_message("You are a helpful assistant.")
        assert client._looks_like_system_message("Your role is to help users.")
        assert client._looks_like_system_message("Act as a translator.")
        assert not client._looks_like_system_message("What is the weather?")
        assert not client._looks_like_system_message("Hello there!")