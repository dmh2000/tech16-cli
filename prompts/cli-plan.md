# CLI Implementation Plan - tech16-cli

## Overview
Building a Python CLI tool that queries LLMs with custom prompts and context from files/URLs.

## Current State Analysis
- **Existing Infrastructure**: 
  - Client library with abstract base class and provider implementations
  - Configuration system with supported models
  - Exception handling framework
  - Test infrastructure in place
- **Entry Point**: Use existing `src/tech16-cli/main.py` (to be renamed to `tech16-cli`)
- **Dependencies**: Client library already implements the query interface needed

## Step-by-Step Implementation Plan

### Phase 1: Core Infrastructure Setup

#### Step 1: Rename and Setup Main Entry Point
- Rename `src/tech16-cli/main.py` to `src/tech16-cli/tech16-cli`
- Make it executable with shebang line
- Update project structure documentation

#### Step 2: ~~Create System Prompts Module~~ (REMOVED)
- ~~Create `lib/client/system_prompts.py`~~ - No longer needed
- ~~Define four prompt variables~~ - Replaced with file-based prompts
- System prompts are now provided via `--prompt filename` argument

#### Step 3: Add Required Dependencies
- Update `requirements.txt` with:
  - `requests` (for URL fetching)
  - `beautifulsoup4` (for HTML parsing)
  - `argparse` (likely already available in stdlib)

### Phase 2: Argument Parsing and Validation

#### Step 4: Implement Command Line Argument Parser
- Create argument parser with:
  - Optional `--prompt filename` argument to specify prompt file
  - Optional `--model` argument (default: `o4-mini`)
  - Positional arguments for filenames and URLs
- Add prompt file reading and validation
- Add model validation using existing `get_provider_for_model()` function

#### Step 5: Implement stdin Reading
- Add function to check and read from stdin if available
- Handle case where stdin is empty vs. has content
- Integrate stdin content into context processing

#### Step 6: Error Handling Framework
- Create centralized error handler function
- Map specific exceptions to user-friendly error messages:
  - `ModelNotFoundError` → "Invalid model specified"
  - `APIKeyMissingError` → "API key missing for provider"
  - File not found → "File not found"
  - URL fetch errors → "Failed to fetch URL"
- Ensure all errors exit with appropriate exit codes
- **Add auto-help detection**: Check for no-input condition (no stdin, no prompt file, no input files) and display helpful usage message

### Phase 3: Context Processing

#### Step 7: File Reading Module
- Create function to read file contents
- Handle different file types (text files, basic error handling for binary)
- Add file existence validation
- Handle encoding issues gracefully

#### Step 8: URL Scraping Module
- Implement URL validation and fetching using `requests`
- Add BeautifulSoup integration for HTML parsing
- Implement depth-2 scraping:
  - Parse initial URL
  - Extract links from the page
  - Follow links one level deep
  - Aggregate all content into single string
- Add error handling for:
  - Network timeouts
  - Invalid URLs
  - HTTP errors (404, 403, etc.)
  - Parsing failures

#### Step 9: Context Array Builder
- Create function to compile context array in correct order:
  1. stdin content (if available) (first)
  2. File contents (in order specified)
  3. URL content (in order specified)
  4. Prompt file content (last, if --prompt specified)
- Ensure proper string formatting and separation

### Phase 4: Client Integration and Query Execution

#### Step 10: Client Factory Integration
- Use existing `get_provider_for_model()` to determine provider
- Import and instantiate appropriate client class:
  - `AnthropicClient` for Anthropic models
  - `OpenAIClient` for OpenAI models  
  - `GeminiClient` for Gemini models
- Handle client instantiation errors

#### Step 11: Query Execution
- Call client's `query()` method with model and context array
- Handle API-related exceptions gracefully
- Stream or buffer output appropriately for stdout

#### Step 12: Output Formatting
- Print LLM response directly to stdout
- Ensure proper encoding for terminal output
- Handle potential Unicode/encoding issues

### Phase 5: Integration and Testing

#### Step 13: End-to-End Integration
- Combine all modules in main execution flow
- Add comprehensive error handling throughout
- Test argument parsing edge cases
- Verify proper cleanup on exit

#### Step 14: Create Integration Tests
- Test with and without `--prompt` argument
- Test with different models from each provider
- Test file reading functionality
- Test URL scraping functionality
- Test error conditions and proper exit codes

#### Step 15: Performance and Reliability
- Add timeout handling for URL requests
- Implement reasonable limits on:
  - File sizes that can be read
  - URL content length
  - Context array total size
- Add progress indicators for long operations (URL scraping)

### Phase 6: Polish and Documentation

#### Step 16: Help and Usage
- Add comprehensive `--help` output
- Include examples of common usage patterns
- Document supported models and file types
- **Auto-help feature**: When no stdin, no prompt, and no input files are provided, automatically display usage message with:
  - Usage examples
  - List of all providers and their supported models
  - Basic CLI argument descriptions

#### Step 17: Configuration Options
- Consider adding config file support for default models
- Add environment variable support for common settings
- Document configuration options

#### Step 18: Error Messages and User Experience
- Polish all error messages for clarity
- Add verbose mode for debugging
- Ensure consistent output formatting

## Implementation Notes

### Architecture Decisions
- **Modularity**: Each major function (arg parsing, file reading, URL scraping, client management) should be in separate functions for testability
- **Error Handling**: Use existing exception framework, add new exceptions as needed
- **Dependencies**: Leverage existing client library infrastructure
- **Testing**: Build on existing test framework

### Key Integration Points
- `lib/client/config.py:get_provider_for_model()` for model-to-provider mapping
- `lib/client/client.py:Client.query()` interface for LLM interactions
- Existing exception classes in `lib/client/exceptions.py`

### Potential Challenges
- **URL Scraping Complexity**: Depth-2 scraping may be slow/complex - consider implementing basic version first
- **Context Size Limits**: Large files + URLs + stdin may exceed model context limits
- **Rate Limiting**: Multiple URL requests may hit rate limits
- **Encoding Issues**: File/URL content encoding may cause problems

### Success Criteria
- CLI accepts all specified arguments correctly
- Successfully queries all three provider types
- Handles files and URLs as context
- Proper error handling with informative messages
- Clean stdout output suitable for piping