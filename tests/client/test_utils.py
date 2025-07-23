"""Tests for the utils module."""

import pytest
from unittest.mock import Mock, patch
from lib.client.utils import (
    validate_context, clean_response, retry_on_failure, format_error_message
)
from lib.client.exceptions import InvalidContextError, APICallError


class TestUtils:
    """Test cases for utils module."""

    def test_validate_context_success(self):
        """Test successful context validation."""
        context = ["Hello", "How are you?"]
        validate_context(context)  # Should not raise

    def test_validate_context_not_list(self):
        """Test context validation with non-list input."""
        with pytest.raises(InvalidContextError, match="Context must be a list"):
            validate_context("not a list")

    def test_validate_context_empty(self):
        """Test context validation with empty list."""
        with pytest.raises(InvalidContextError, match="Context cannot be empty"):
            validate_context([])

    def test_validate_context_non_string_item(self):
        """Test context validation with non-string item."""
        with pytest.raises(InvalidContextError, match="must be a string"):
            validate_context(["Hello", 123])

    def test_validate_context_empty_string(self):
        """Test context validation with empty string item."""
        with pytest.raises(InvalidContextError, match="cannot be empty or whitespace"):
            validate_context(["Hello", ""])
        
        with pytest.raises(InvalidContextError, match="cannot be empty or whitespace"):
            validate_context(["Hello", "   "])

    def test_clean_response_success(self):
        """Test successful response cleaning."""
        response = "  Hello world!  \r\n\r  "
        cleaned = clean_response(response)
        assert cleaned == "Hello world!"

    def test_clean_response_non_string(self):
        """Test response cleaning with non-string input."""
        response = 123
        cleaned = clean_response(response)
        assert cleaned == "123"

    def test_clean_response_line_endings(self):
        """Test response cleaning normalizes line endings."""
        response = "Line 1\r\nLine 2\rLine 3\nLine 4"
        cleaned = clean_response(response)
        assert cleaned == "Line 1\nLine 2\nLine 3\nLine 4"

    def test_retry_on_failure_success(self):
        """Test retry decorator with successful function."""
        @retry_on_failure(max_retries=2, delay=0.1)
        def success_func():
            return "success"
        
        result = success_func()
        assert result == "success"

    def test_retry_on_failure_eventual_success(self):
        """Test retry decorator with eventual success."""
        call_count = 0
        
        @retry_on_failure(max_retries=2, delay=0.1)
        def eventually_succeeds():
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise Exception("Temporary error")
            return "success"
        
        result = eventually_succeeds()
        assert result == "success"
        assert call_count == 2

    def test_retry_on_failure_max_retries_exceeded(self):
        """Test retry decorator when max retries is exceeded."""
        @retry_on_failure(max_retries=2, delay=0.1)
        def always_fails():
            raise Exception("Always fails")
        
        with pytest.raises(APICallError, match="failed after 3 attempts"):
            always_fails()

    def test_retry_on_failure_no_retry_on_invalid_context(self):
        """Test retry decorator doesn't retry on InvalidContextError."""
        call_count = 0
        
        @retry_on_failure(max_retries=2, delay=0.1)
        def raises_invalid_context():
            nonlocal call_count
            call_count += 1
            raise InvalidContextError("Invalid context")
        
        with pytest.raises(InvalidContextError):
            raises_invalid_context()
        
        assert call_count == 1  # Should not retry

    def test_format_error_message(self):
        """Test error message formatting."""
        error = Exception("Something went wrong")
        formatted = format_error_message(error, "anthropic", "claude-3-5-sonnet-20241022")
        
        expected = "Error querying anthropic model 'claude-3-5-sonnet-20241022': Exception - Something went wrong"
        assert formatted == expected

    def test_format_error_message_with_different_error_types(self):
        """Test error message formatting with different error types."""
        # Test with ValueError
        error = ValueError("Invalid value")
        formatted = format_error_message(error, "openai", "gpt-4")
        assert "ValueError - Invalid value" in formatted
        
        # Test with custom exception
        error = InvalidContextError("Context issue")
        formatted = format_error_message(error, "gemini", "gemini-1.5-pro")
        assert "InvalidContextError - Context issue" in formatted