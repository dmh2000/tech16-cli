# Client Library Implementation Plan

## Overview
This document outlines the detailed implementation plan for the client library that provides a unified interface for querying multiple LLM providers (Anthropic, Google Gemini, and OpenAI).

## Library Structure

```
lib/client/
├── __init__.py              # Package initialization and public API exports
├── client.py                # Abstract Client interface definition
├── anthropic_client.py      # Anthropic implementation
├── gemini_client.py         # Google Gemini implementation
├── openai_client.py         # OpenAI implementation
├── exceptions.py            # Custom exception classes
├── utils.py                 # Shared utility functions
└── config.py                # Configuration and environment handling
```

## Core Components

### 1. Client Interface (`client.py`)

**Purpose**: Define the abstract base class that all client implementations must follow.

**Implementation Details**:
- Use Python's `abc` module to create an abstract base class
- Define the abstract `query` method signature
- Include type hints using `typing` module
- Add docstrings for interface documentation

**Key Methods**:
```python
from abc import ABC, abstractmethod
from typing import List

class Client(ABC):
    @abstractmethod
    def query(self, model: str, context: List[str]) -> str:
        """Query the LLM with the given model and context."""
        pass
```

### 2. Exception Handling (`exceptions.py`)

**Purpose**: Define custom exceptions for better error handling and debugging.

**Exception Classes**:
- `ClientError`: Base exception for all client-related errors
- `APIKeyMissingError`: When required API key is not found in environment
- `ModelNotFoundError`: When specified model is not available
- `APICallError`: When the underlying API call fails
- `InvalidContextError`: When context format is invalid

### 3. Configuration Management (`config.py`)

**Purpose**: Handle environment variables and configuration validation.

**Responsibilities**:
- Environment variable retrieval with validation
- Default model configurations for each provider
- API endpoint configurations (if needed for custom endpoints)
- Timeout and retry configurations

**Key Functions**:
```python
def get_api_key(provider: str) -> str:
    """Get API key from environment with proper error handling."""
    pass

def validate_model(provider: str, model: str) -> bool:
    """Validate if model is supported by provider."""
    pass
```

### 4. Utility Functions (`utils.py`)

**Purpose**: Shared functionality across all client implementations.

**Functions**:
- Context preprocessing and validation
- Response parsing and cleaning
- Logging utilities
- Retry logic decorators

### 5. Provider Implementations

#### Anthropic Client (`anthropic_client.py`)

**Dependencies**: `anthropic` Python library

**Environment Variables**:
- `ANTHROPIC_API_KEY`: Required API key

**Supported Models** (examples):
- `claude-3-5-sonnet-20241022`
- `claude-3-5-haiku-20241022`
- `claude-3-opus-20240229`

**Implementation Details**:
- Initialize Anthropic client in constructor
- Handle message formatting for Claude's expected structure
- Implement proper error handling and retries
- Support system messages vs user messages distinction

#### Google Gemini Client (`gemini_client.py`)

**Dependencies**: `google-genai` Python library

**Environment Variables**:
- `GOOGLE_API_KEY`: Required API key

**Supported Models** (examples):
- `gemini-1.5-pro`
- `gemini-1.5-flash`
- `gemini-1.0-pro`

**Implementation Details**:
- Initialize Google GenAI client
- Handle content formatting for Gemini API
- Implement safety settings if needed
- Handle streaming vs non-streaming responses

#### OpenAI Client (`openai_client.py`)

**Dependencies**: `openai` Python library

**Environment Variables**:
- `OPENAI_API_KEY`: Required API key

**Supported Models** (examples):
- `gpt-4o`
- `gpt-4o-mini`
- `gpt-3.5-turbo`

**Implementation Details**:
- Initialize OpenAI client
- Handle chat completion message formatting
- Implement token usage tracking
- Support for different OpenAI endpoints

### 6. Factory Functions

**Purpose**: Provide simple factory functions for creating client instances.

**Location**: In `__init__.py` or separate `factories.py`

**Functions**:
```python
def new_anthropic() -> AnthropicClient:
    """Create and return a new Anthropic client instance."""
    pass

def new_gemini() -> GeminiClient:
    """Create and return a new Gemini client instance."""
    pass

def new_openai() -> OpenAIClient:
    """Create and return a new OpenAI client instance."""
    pass
```

## Implementation Phases

### Phase 1: Core Infrastructure
1. Create abstract Client interface
2. Implement custom exception classes
3. Create configuration management module
4. Set up utility functions

### Phase 2: Provider Implementations
1. Implement Anthropic client
2. Implement OpenAI client
3. Implement Gemini client
4. Create factory functions

### Phase 3: Testing and Validation
1. Create unit tests for each client implementation
2. Create integration tests with mock API responses
3. Add configuration validation tests
4. Performance and reliability testing

### Phase 4: Documentation and Packaging
1. Add comprehensive docstrings
2. Create usage examples
3. Set up package configuration
4. Add logging and debugging support

## Error Handling Strategy

### Graceful Degradation
- Return error messages as strings when API calls fail
- Log errors for debugging while maintaining user-friendly responses
- Implement exponential backoff for transient failures

### Input Validation
- Validate model names against known supported models
- Check context array for empty or invalid strings
- Verify API keys exist before making calls

### API-Specific Error Handling
- Handle rate limiting (429 errors) with appropriate delays
- Manage authentication errors (401/403)
- Process model availability errors (404)
- Handle timeout and network errors

## Configuration Examples

### Environment Variables Required
```bash
# Required for respective clients
ANTHROPIC_API_KEY=your_anthropic_key_here
GOOGLE_API_KEY=your_google_key_here
OPENAI_API_KEY=your_openai_key_here
```

### Model Configuration
Each client should maintain a list of supported models and validate against them before making API calls.

## Usage Pattern

```python
from lib.client import new_anthropic, new_openai, new_gemini

# Create clients
anthropic_client = new_anthropic()
openai_client = new_openai()
gemini_client = new_gemini()

# Query examples
context = ["You are a helpful assistant.", "What is the capital of France?"]

response1 = anthropic_client.query("claude-3-5-sonnet-20241022", context)
response2 = openai_client.query("gpt-4o", context)
response3 = gemini_client.query("gemini-1.5-pro", context)
```

## Dependencies

### Required Python Packages
- `anthropic`: For Anthropic Claude API
- `google-genai`: For Google Gemini API
- `openai`: For OpenAI API
- `typing`: For type hints (built-in)
- `abc`: For abstract base classes (built-in)
- `os`: For environment variables (built-in)

### Development Dependencies
- `pytest`: For testing
- `pytest-mock`: For mocking API calls
- `mypy`: For type checking
- `black`: For code formatting
- `ruff`: For linting

## Quality Assurance

### Code Standards
- Use type hints throughout
- Follow PEP 8 style guidelines
- Maintain >90% test coverage
- Use descriptive variable and function names

### Testing Strategy
- Unit tests for each client implementation
- Integration tests with mocked API responses
- Error handling tests for various failure scenarios
- Performance tests for response times

### Security Considerations
- Never log API keys
- Validate all inputs to prevent injection attacks
- Use secure methods for environment variable access
- Implement proper timeout handling to prevent hanging

## Future Enhancements

### Potential Features
- Async/await support for concurrent queries
- Response caching mechanisms
- Streaming response support
- Custom model endpoints
- Usage analytics and monitoring
- Plugin architecture for additional providers

This plan provides a comprehensive foundation for implementing the client library with proper architecture, error handling, and extensibility.