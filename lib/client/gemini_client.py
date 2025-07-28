"""Google Gemini client implementation."""

from typing import List
from .client import Client
from .config import get_api_key, validate_model
from .utils import validate_context, clean_response, retry_on_failure, format_error_message
from .exceptions import APICallError


class GeminiClient(Client):
    """Client implementation for Google Gemini models."""
    
    def __init__(self):
        """Initialize the Gemini client."""
        self.provider = "gemini"
        self.api_key = get_api_key(self.provider)
        
        # Import and initialize the Gemini client
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            self.genai = genai
        except ImportError:
            raise APICallError(
                "Google GenAI library not installed. Please install with: pip install google-generativeai"
            )
    
    @retry_on_failure(max_retries=3, delay=1.0, backoff_factor=2.0)
    def query(self, model: str, context: List[str]) -> str:
        """
        Query Gemini with the given model and context.
        
        Args:
            model: The Gemini model to use
            context: List of context strings
            
        Returns:
            str: Response from Gemini or error message
        """
        try:
            # Validate inputs
            validate_model(self.provider, model)
            validate_context(context)
            
            # Create model instance
            model_instance = self.genai.GenerativeModel(model)
            
            # Format context for Gemini
            prompt = self._format_prompt(context)
            
            # Configure generation parameters
            generation_config = self.genai.GenerationConfig(
                max_output_tokens=65535,
                temperature=0.5,
                top_p=0.95,
                top_k=64,
            )
            
            # Configure safety settings (optional - can be restrictive)
            safety_settings = [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH", 
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
                },
            ]
            
            # Make the API call
            response = model_instance.generate_content(
                prompt,
                generation_config=generation_config,
                safety_settings=safety_settings
            )
            
            # Check if response was blocked
            if response.candidates[0].finish_reason.name == "SAFETY":
                return "Response was blocked due to safety filters."
            
            # Extract and clean the response text
            response_text = response.text
            return clean_response(response_text)
            
        except Exception as e:
            error_msg = format_error_message(e, self.provider, model)
            return error_msg
    
    def _format_prompt(self, context: List[str]) -> str:
        """
        Format context strings into a prompt for Gemini.
        
        Args:
            context: List of context strings
            
        Returns:
            str: Formatted prompt for Gemini
        """
        if len(context) == 1:
            return context[0]
        
        # For multiple context items, create a conversational format
        formatted_parts = []
        
        for i, content in enumerate(context):
            if i == 0:
                # First message can be system-like instruction or user query
                if self._looks_like_system_message(content):
                    formatted_parts.append(f"Instructions: {content}")
                else:
                    formatted_parts.append(f"Human: {content}")
            elif i % 2 == 1:
                # Odd indices are assistant responses
                formatted_parts.append(f"Assistant: {content}")
            else:
                # Even indices (after 0) are human messages
                formatted_parts.append(f"Human: {content}")
        
        # Add a prompt for continuation if needed
        if not formatted_parts[-1].startswith("Human:"):
            formatted_parts.append("Human: Please provide your response.")
        
        return "\n\n".join(formatted_parts)
    
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