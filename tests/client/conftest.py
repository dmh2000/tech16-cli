"""Shared fixtures and configuration for client tests."""

import pytest
from unittest.mock import Mock, patch
from lib.client.exceptions import APIKeyMissingError, APICallError


@pytest.fixture
def mock_env_vars():
    """Mock environment variables for testing."""
    with patch.dict('os.environ', {
        'ANTHROPIC_API_KEY': 'test-anthropic-key',
        'OPENAI_API_KEY': 'test-openai-key',
        'GOOGLE_API_KEY': 'test-google-key'
    }):
        yield


@pytest.fixture
def sample_context():
    """Sample context for testing queries."""
    return [
        "You are a helpful assistant.",
        "What is the capital of France?"
    ]


@pytest.fixture
def sample_single_context():
    """Sample single message context."""
    return ["What is 2 + 2?"]


@pytest.fixture
def sample_response():
    """Sample API response text."""
    return "The capital of France is Paris."


@pytest.fixture
def mock_anthropic_client():
    """Mock Anthropic client."""
    mock_client = Mock()
    mock_response = Mock()
    mock_response.content = [Mock(text="The capital of France is Paris.")]
    mock_client.messages.create.return_value = mock_response
    return mock_client


@pytest.fixture
def mock_openai_client():
    """Mock OpenAI client."""
    mock_client = Mock()
    mock_response = Mock()
    mock_response.choices = [Mock(message=Mock(content="The capital of France is Paris."))]
    mock_client.chat.completions.create.return_value = mock_response
    return mock_client


@pytest.fixture 
def mock_gemini_response():
    """Mock Gemini response."""
    mock_response = Mock()
    mock_response.text = "The capital of France is Paris."
    mock_response.candidates = [Mock(finish_reason=Mock(name="STOP"))]
    return mock_response