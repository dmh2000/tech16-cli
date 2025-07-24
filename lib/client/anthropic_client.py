"""Anthropic Claude client implementation."""

from typing import List
from .client import Client
from .config import get_api_key, validate_model
from .utils import (
    validate_context,
    clean_response,
    retry_on_failure,
    format_error_message,
)
from .exceptions import APICallError


class AnthropicClient(Client):
    """Client implementation for Anthropic Claude models."""

    def __init__(self):
        """Initialize the Anthropic client."""
        self.provider = "anthropic"
        self.api_key = get_api_key(self.provider)

        # Import and initialize the Anthropic client
        try:
            from anthropic import Anthropic

            self.client = Anthropic(api_key=self.api_key)
        except ImportError:
            raise APICallError(
                "Anthropic library not installed. Please install with: pip install anthropic"
            )

    @retry_on_failure(max_retries=3, delay=1.0, backoff_factor=2.0)
    def query(self, model: str, context: List[str]) -> str:
        """
        Query Claude with the given model and context.

        Args:
            model: The Claude model to use
            context: List of context strings

        Returns:
            str: Response from Claude or error message
        """
        try:
            # Validate inputs
            validate_model(self.provider, model)
            validate_context(context)

            # Format messages for Anthropic API
            messages = self._format_messages(context)

            # Make the API call
            response = self.client.messages.create(
                model=model, max_tokens=4096, messages=messages
            )

            # Extract and clean the response text
            response_text = response.content[0].text
            return clean_response(response_text)

        except Exception as e:
            error_msg = format_error_message(e, self.provider, model)
            return error_msg

    def _format_messages(self, context: List[str]) -> List[dict]:
        """
        Format context strings into Anthropic message format.

        Args:
            context: List of context strings

        Returns:
            List[dict]: Formatted messages for Anthropic API
        """
        messages = []

        # If we have an odd number of context items, treat the first as system message
        # and alternate user/assistant for the rest
        if len(context) == 1:
            # Single message - treat as user message
            messages.append({"role": "user", "content": context[0]})
        else:
            # Multiple messages - alternate user/assistant
            for i, content in enumerate(context):
                role = "user" if i % 2 == 0 else "assistant"
                messages.append({"role": role, "content": content})

            # Ensure we end with a user message for Claude to respond to
            if messages[-1]["role"] == "assistant":
                messages.append(
                    {
                        "role": "user",
                        "content": "Please continue or provide your response.",
                    }
                )

        return messages
