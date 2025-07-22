"""Tests for custom exceptions."""

import pytest
from lib.client.exceptions import (
    ClientError, APIKeyMissingError, ModelNotFoundError, 
    APICallError, InvalidContextError
)


class TestExceptions:
    """Test cases for custom exceptions."""

    def test_client_error_inheritance(self):
        """Test that all custom exceptions inherit from ClientError."""
        assert issubclass(APIKeyMissingError, ClientError)
        assert issubclass(ModelNotFoundError, ClientError)
        assert issubclass(APICallError, ClientError)
        assert issubclass(InvalidContextError, ClientError)

    def test_client_error_is_exception(self):
        """Test that ClientError inherits from base Exception."""
        assert issubclass(ClientError, Exception)

    def test_api_key_missing_error(self):
        """Test APIKeyMissingError creation and message."""
        message = "API key not found"
        error = APIKeyMissingError(message)
        
        assert str(error) == message
        assert isinstance(error, ClientError)
        assert isinstance(error, Exception)

    def test_model_not_found_error(self):
        """Test ModelNotFoundError creation and message."""
        message = "Model not supported"
        error = ModelNotFoundError(message)
        
        assert str(error) == message
        assert isinstance(error, ClientError)

    def test_api_call_error(self):
        """Test APICallError creation and message."""
        message = "API call failed"
        error = APICallError(message)
        
        assert str(error) == message
        assert isinstance(error, ClientError)

    def test_invalid_context_error(self):
        """Test InvalidContextError creation and message."""
        message = "Context is invalid"
        error = InvalidContextError(message)
        
        assert str(error) == message
        assert isinstance(error, ClientError)

    def test_exceptions_can_be_raised_and_caught(self):
        """Test that exceptions can be raised and caught properly."""
        # Test raising and catching APIKeyMissingError
        with pytest.raises(APIKeyMissingError):
            raise APIKeyMissingError("Test message")

        # Test catching as ClientError
        with pytest.raises(ClientError):
            raise ModelNotFoundError("Test message")

        # Test catching as base Exception
        with pytest.raises(Exception):
            raise APICallError("Test message")

    def test_exceptions_with_empty_message(self):
        """Test exceptions with empty or no message."""
        error1 = ClientError()
        error2 = APIKeyMissingError("")
        
        assert str(error1) == ""
        assert str(error2) == ""