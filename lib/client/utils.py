"""Utility functions for the client library."""

import time
import functools
from typing import List, Callable, Any
from .exceptions import InvalidContextError, APICallError


def validate_context(context: List[str]) -> None:
    """
    Validate the context array.
    
    Args:
        context: List of context strings
        
    Raises:
        InvalidContextError: If context is invalid
    """
    if not isinstance(context, list):
        raise InvalidContextError("Context must be a list of strings")
    
    if not context:
        raise InvalidContextError("Context cannot be empty")
    
    for i, item in enumerate(context):
        if not isinstance(item, str):
            raise InvalidContextError(f"Context item at index {i} must be a string, got {type(item)}")
        
        if not item.strip():
            raise InvalidContextError(f"Context item at index {i} cannot be empty or whitespace only")


def clean_response(response: str) -> str:
    """
    Clean and normalize the response text.
    
    Args:
        response: Raw response from the API
        
    Returns:
        str: Cleaned response text
    """
    if not isinstance(response, str):
        return str(response)
    
    # Remove leading/trailing whitespace
    response = response.strip()
    
    # Normalize line endings
    response = response.replace('\r\n', '\n').replace('\r', '\n')
    
    return response


def retry_on_failure(max_retries: int = 3, delay: float = 1.0, backoff_factor: float = 2.0):
    """
    Decorator to retry function calls on failure with exponential backoff.
    
    Args:
        max_retries: Maximum number of retry attempts
        delay: Initial delay between retries in seconds
        backoff_factor: Factor to multiply delay by after each retry
        
    Returns:
        Decorated function
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None
            current_delay = delay
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    
                    # Don't retry on certain types of errors
                    if isinstance(e, (InvalidContextError,)):
                        raise
                    
                    # If this was the last attempt, raise the exception
                    if attempt == max_retries:
                        break
                    
                    # Wait before retrying
                    time.sleep(current_delay)
                    current_delay *= backoff_factor
            
            # If we get here, all retries failed
            raise APICallError(f"Function failed after {max_retries + 1} attempts. Last error: {last_exception}")
        
        return wrapper
    return decorator


def format_error_message(error: Exception, provider: str, model: str) -> str:
    """
    Format a consistent error message for API failures.
    
    Args:
        error: The original exception
        provider: The provider name
        model: The model that was being used
        
    Returns:
        str: Formatted error message
    """
    error_type = type(error).__name__
    error_msg = str(error)
    
    return f"Error querying {provider} model '{model}': {error_type} - {error_msg}"