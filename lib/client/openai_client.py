"""OpenAI client implementation."""

from typing import List
from .client import Client
from .config import get_api_key, validate_model
from .utils import validate_context, clean_response, retry_on_failure, format_error_message
from .exceptions import APICallError


class OpenAIClient(Client):
    """Client implementation for OpenAI models."""
    
    def __init__(self):
        """Initialize the OpenAI client."""
        self.provider = "openai"
        self.api_key = get_api_key(self.provider)
        
        # Import and initialize the OpenAI client
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=self.api_key)
        except ImportError:
            raise APICallError(
                "OpenAI library not installed. Please install with: pip install openai"
            )
    
    @retry_on_failure(max_retries=3, delay=1.0, backoff_factor=2.0)
    def query(self, model: str, context: List[str]) -> str:
        """
        Query OpenAI with the given model and context.
        
        Args:
            model: The OpenAI model to use
            context: List of context strings
            
        Returns:
            str: Response from OpenAI or error message
        """
        try:
            # Validate inputs
            validate_model(self.provider, model)
            validate_context(context)
            
            # Format messages for OpenAI Chat API
            messages = self._format_messages(context)
            
            # Make the API call
            # Use max_completion_tokens for newer models (o1, o4 series) and max_tokens for others
            completion_params = {
                "model": model,
                "messages": messages
            }
            
            # Newer models use max_completion_tokens, older models use max_tokens
            if model.startswith(('o1-', 'o3-', 'o4-')):
                completion_params["max_completion_tokens"] = 4096
            else:
                completion_params["max_tokens"] = 4096
            
            response = self.client.chat.completions.create(**completion_params)
            
            # Extract and clean the response text
            response_text = response.choices[0].message.content
            return clean_response(response_text)
            
        except Exception as e:
            error_msg = format_error_message(e, self.provider, model)
            return error_msg
    
    def _format_messages(self, context: List[str]) -> List[dict]:
        """
        Format context strings into OpenAI message format.
        
        Args:
            context: List of context strings
            
        Returns:
            List[dict]: Formatted messages for OpenAI API
        """
        messages = []
        
        if len(context) == 1:
            # Single message - treat as user message
            messages.append({
                "role": "user",
                "content": context[0]
            })
        else:
            # Multiple messages - alternate user/assistant
            # First message is typically system or user
            messages.append({
                "role": "system" if self._looks_like_system_message(context[0]) else "user",
                "content": context[0]
            })
            
            # Alternate user/assistant for remaining messages
            for i in range(1, len(context)):
                role = "assistant" if i % 2 == 1 else "user"
                messages.append({
                    "role": role,
                    "content": context[i]
                })
            
            # Ensure we end with a user message for the model to respond to
            if messages[-1]["role"] == "assistant":
                messages.append({
                    "role": "user",
                    "content": "Please continue or provide your response."
                })
        
        return messages
    
    def _looks_like_system_message(self, message: str) -> bool:
        """
        Heuristic to determine if a message looks like a system message.
        
        Args:
            message: The message to check
            
        Returns:
            bool: True if message appears to be a system message
        """
        system_indicators = [
            "you are", "your role", "instructions:", "system:",
            "behave as", "act as", "your task", "guidelines:"
        ]
        
        message_lower = message.lower().strip()
        return any(indicator in message_lower for indicator in system_indicators)