# tech16-planner Implementation Plan

## Overview

This document outlines the comprehensive implementation plan for `tech16-planner`, a new CLI program similar to `tech16-cli` but with specific changes to input arguments and functionality focused on planning and analysis tasks.

## Program Specification

**Command Structure:**
```bash
tech16-planner --model <model_name> [file1] [file2] [url1] [url2] ...
```

**Key Requirements:**
- `--model` argument is required and must be the first argument after program name
- Accepts any number of filenames and URLs as input sources
- URLs are scraped using BeautifulSoup
- Built-in system prompt stored as a string (placeholder for now)
- System prompt and input content combined into LLM context
- Output printed to STDOUT

## 1. CLI Argument Structure Design

**Command Structure:**
```bash
tech16-planner --model <model_name> [file1] [file2] [url1] [url2] ...
```

**Key Differences from tech16-cli:**
- `--model` is required and must be first argument after program name
- No support for stdin input (simplified input model)
- No `--prompt` flag (uses built-in system prompt)
- Mixed file and URL arguments in any order

**Argument Validation:**
- Validate `--model` against existing supported models from lib/client/config.py
- Distinguish between file paths and URLs using URL pattern matching
- Ensure at least one input source (file or URL) is provided

## 2. System Prompt Architecture

**Built-in System Prompt:**
- Store as a module-level constant string
- Design for planning/analysis use cases (based on program name)
- Make it configurable in future iterations
- Placeholder prompt should indicate this is a planning assistant

**Implementation Approach:**
```python
SYSTEM_PROMPT = """
You are a planning assistant. Analyze the provided documents and web content to create comprehensive plans, strategies, or analyses based on the information given.

[Placeholder - this will be expanded with specific planning instructions]
"""
```

## 3. Input Processing Pipeline

**File Processing:**
- Reuse existing file reading logic from tech16-cli
- Maintain encoding detection and binary file filtering
- Keep file size limits (10MB) for safety

**URL Processing:**
- Leverage existing BeautifulSoup scraping implementation
- Maintain content size limits (5MB) and timeout settings
- Use same HTML cleaning and content extraction logic

**Input Categorization:**
- URL detection: Use regex pattern matching (http/https schemes)
- File validation: Check file existence and readability
- Error handling: Collect and report all invalid inputs before processing

**Processing Order:**
1. Parse and validate all arguments
2. Categorize inputs (files vs URLs)
3. Process files first (faster, local)
4. Process URLs second (slower, network dependent)
5. Combine all content for context building

## 4. Context Combination and LLM Integration

**Context Building Strategy:**
```
System Prompt
+
Combined Input Content:
  - File contents (with source labels)
  - URL content (with source URLs)
  - Clear separation between sources
```

**LLM Integration:**
- Reuse existing lib/client architecture
- Use client factory pattern: `get_client_for_model(model_name)`
- Leverage existing error handling and retry logic
- Maintain API key management through environment variables

**Context Structure:**
```
SYSTEM_PROMPT + "\n\n" + 
"=== INPUT SOURCES ===\n" +
"File: filename1\n" + file_content + "\n\n" +
"URL: url1\n" + scraped_content + "\n\n" +
...
```

## 5. Code Structure and Module Organization

**File Structure:**
```
src/tech16-planner/
└── tech16-planner    # Main executable script
```

**Code Organization:**
- Single file implementation (similar to tech16-cli)
- Import and reuse lib/client modules
- Follow same coding patterns and conventions

**Key Functions:**
```python
def parse_arguments()           # Handle CLI argument parsing
def categorize_inputs()         # Separate files from URLs  
def process_files()            # Read and validate file contents
def process_urls()             # Scrape and clean URL content
def build_context()            # Combine all inputs with system prompt
def main()                     # Orchestrate the entire workflow
```

**Module Dependencies:**
- Reuse `lib.client` for LLM integration
- Import same utilities (file reading, URL scraping)
- Maintain same dependency footprint

## 6. Error Handling and Output Formatting

**Error Handling Strategy:**
- Follow tech16-cli patterns for consistency
- Use existing exception types from lib/client
- Validate all inputs before processing any
- Provide clear, actionable error messages

**Output Format:**
- LLM response directly to STDOUT (no additional formatting)
- Errors to STDERR 
- Exit codes: 0 (success), 1 (error)

**Error Categories:**
1. Argument validation errors (missing --model, invalid model)
2. Input processing errors (file not found, URL unreachable)
3. LLM API errors (authentication, rate limits, model errors)
4. System errors (network, file permissions)

## 7. Testing Strategy

**Test Structure:**
```
tests/test_tech16_planner.py  # Main test file
```

**Test Coverage Areas:**
1. **Argument Parsing Tests**
   - Valid model and input combinations
   - Missing --model argument
   - Invalid model names  
   - No input sources provided

2. **Input Processing Tests**
   - File reading with various encodings
   - URL scraping with mocked responses
   - Mixed file and URL inputs
   - Error handling for invalid inputs

3. **Context Building Tests**
   - System prompt integration
   - Proper source labeling
   - Content combination formatting

4. **Integration Tests**
   - End-to-end workflow with mocked LLM
   - Error propagation and handling
   - Output formatting verification

**Testing Approach:**
- Use pytest framework (already configured)
- Mock external dependencies (HTTP requests, LLM APIs)
- Follow existing test patterns from tech16-cli tests
- Include both unit and integration tests

## 8. Implementation Phases

**Phase 1: Core Structure**
- Create `src/tech16-planner/tech16-planner` executable
- Implement argument parsing with required `--model` first
- Add placeholder system prompt

**Phase 2: Input Processing** 
- Implement file and URL categorization
- Reuse existing file reading and URL scraping logic
- Add input validation and error handling

**Phase 3: Context Integration**
- Build context combination logic
- Integrate with lib/client LLM framework
- Implement output formatting

**Phase 4: Testing and Validation**
- Create comprehensive test suite
- Test with various input combinations
- Validate error handling scenarios

## Key Implementation Principles

- **Reuse existing code**: Leverage lib/client and utility functions from tech16-cli
- **Maintain consistency**: Follow same patterns, error handling, and conventions
- **Keep it simple**: Single-file implementation focused on core functionality
- **Robust error handling**: Validate inputs thoroughly and provide clear feedback

## Current Codebase Context

**Existing Architecture:**
- `src/tech16-cli/`: Main CLI application with multi-provider LLM support
- `lib/client/`: Client library with abstract base class and provider implementations
- Supported models: Anthropic Claude, OpenAI GPT, Google Gemini
- Dependencies: anthropic, openai, google-generativeai, requests, beautifulsoup4

**Code Patterns to Follow:**
- Abstract Factory Pattern for client creation
- Strategy Pattern for interchangeable LLM providers
- Comprehensive exception hierarchy
- Type hints and docstrings throughout
- Modular design with clear separation of concerns

This plan provides a solid foundation for implementing tech16-planner while maintaining consistency with the existing codebase architecture and patterns.