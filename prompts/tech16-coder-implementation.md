# tech16-coder Implementation Plan

## Overview

This document outlines the comprehensive implementation plan for `tech16-coder`, a CLI tool for generating code using LLM services. The program will be similar to `tech16-planner` but focused on code generation rather than planning, with additional functionality to parse LLM output and write generated files to the filesystem.

## Requirements Analysis

### Core Requirements
1. **CLI Interface**: Named argument `--model (model_name)` as first argument, followed by any number of filenames and URLs
2. **Input Processing**: 
   - File reading (reuse existing file_handler.py)
   - URL scraping using BeautifulSoup (reuse existing url_handler.py)
3. **LLM Integration**: Built-in system prompt for coding, context building, and model querying
4. **Output Processing**: Parse LLM output for file delimiters, extract files, and write to filesystem with collision avoidance
5. **Non-file Text Output**: Print any LLM response text that is not wrapped in triple backticks to stdout

### Technical Feasibility Assessment
- ✅ **Existing Infrastructure**: Can reuse client library, file handlers, URL handlers from tech16-planner
- ✅ **File Parsing**: Standard regex-based parsing for triple backtick delimited files
- ✅ **Collision Avoidance**: Simple filename modification with dash and 3-digit random number
- ✅ **No Conflicts**: No technical or architectural conflicts identified

## Project Structure

```
src/tech16-coder/
├── tech16-coder                # Main CLI executable
├── __init__.py                 # Package initialization
├── file_writer.py              # New module for parsing output and writing files
└── scripts/                    # Test scripts and examples
    └── (test files as needed)
```

## Implementation Plan

### Phase 1: Core CLI Framework (High Priority)

#### Task 1.1: Create Main CLI Program
- **File**: `src/tech16-coder/tech16-coder`
- **Dependencies**: Reuse imports from tech16-planner
- **Key Components**:
  - Argument parsing with required `--model` as first arg
  - Input validation and categorization (files vs URLs)
  - Error handling and usage display
  - Main execution flow

#### Task 1.2: System Prompt Definition
- **Location**: String constant in main file
- **Content**: Placeholder system prompt optimized for code generation
- **Requirements**: 
  - Focus on code generation vs planning
  - Include instructions for file output format
  - Specify triple backtick delimiter requirements

#### Task 1.3: Context Building Integration
- **Reuse**: `build_context()` function pattern from tech16-planner
- **Modifications**: Adapt for coding-specific system prompt
- **Integration**: Combine system prompt with file/URL content

### Phase 2: LLM Integration (High Priority)

#### Task 2.1: Client Creation and Model Support
- **Reuse**: `create_client()` function from tech16-planner
- **Dependencies**: 
  - `lib/client/config.py` for model-to-provider mapping
  - `lib/client/{anthropic,openai,gemini}_client.py` for API clients
- **Validation**: Ensure all existing supported models work

#### Task 2.2: Query Execution
- **Pattern**: Follow tech16-planner query execution
- **Input**: Context string built from system prompt + input sources
- **Output**: Raw LLM response for parsing

### Phase 3: Output Processing (High Priority)

#### Task 3.1: Create File Writer Module
- **File**: `src/tech16-coder/file_writer.py`
- **Core Functions**:
  - `parse_llm_output(response: str) -> Tuple[List[FileSpec], str]` - Returns file specs and non-file text
  - `write_generated_files(file_specs: List[FileSpec]) -> List[str]`
  - `generate_safe_filename(filepath: str) -> str`
  - `print_non_file_text(non_file_text: str) -> None` - Print explanatory text to stdout

#### Task 3.2: File Parsing Logic
- **Pattern Detection**: Regex for triple backtick blocks with file annotations
- **Expected Format**: 
  ```
  ```filepath/filename.ext
  file content here
  ```
  ```
- **Edge Cases**: Handle multiple files, nested directories, various file types

#### Task 3.3: File Writing with Collision Avoidance
- **Collision Detection**: Check if target file exists
- **Naming Strategy**: Append `-{3-digit-random}` before file extension
- **Directory Creation**: Auto-create parent directories if needed
- **Error Handling**: File permission issues, disk space, invalid paths

### Phase 4: Integration and Testing (Medium Priority)

#### Task 4.1: End-to-End Integration
- **Main Function**: Integrate all components into main execution flow
- **Error Propagation**: Ensure proper error handling throughout pipeline
- **Output Handling**: 
  - Print non-file text to stdout immediately
  - Report created files to stderr for status updates
  - Separate explanatory text from file creation notifications

#### Task 4.2: Package Initialization
- **File**: `src/tech16-coder/__init__.py`
- **Content**: Basic package marker, version info if needed

#### Task 4.3: Script Testing Framework
- **Directory**: `src/tech16-coder/scripts/`
- **Test Files**: Create sample input files and expected outputs
- **Validation**: Manual testing with different models and input types

### Phase 5: Documentation and Polish (Low Priority)

#### Task 5.1: Usage Documentation
- **Help Text**: Comprehensive usage examples in CLI help
- **Model Listing**: Display supported models and providers
- **Error Messages**: Clear, actionable error messages

#### Task 5.2: Code Quality
- **Code Style**: Follow existing project conventions
- **Documentation**: Docstrings for all functions
- **Type Hints**: Consistent typing throughout

## Technical Implementation Details

### File Output Parsing

#### Expected LLM Output Format
```
Here's the generated code:

```src/components/Button.py
import React from 'react';

const Button = ({ children, onClick }) => {
  return (
    <button onClick={onClick}>
      {children}
    </button>
  );
};

export default Button;
```

```src/components/Button.test.py
import { render, fireEvent } from '@testing-library/react';
import Button from './Button';

test('calls onClick when clicked', () => {
  const onClick = jest.fn();
  const { getByRole } = render(<Button onClick={onClick}>Click me</Button>);
  fireEvent.click(getByRole('button'));
  expect(onClick).toHaveBeenCalled();
});
```
```

#### Parsing Algorithm
1. **Regex Pattern**: `r'```(\S+)\n(.*?)\n```'` (multiline, dotall)
2. **Extraction**: Capture filename and content groups for file blocks
3. **Non-file Text Extraction**: Remove all triple backtick blocks and extract remaining text
4. **Validation**: Ensure valid filepath format
5. **Content Processing**: Preserve original formatting and whitespace for both files and text
6. **Output Handling**: Print non-file text to stdout, write files to filesystem

### Collision Avoidance Strategy

#### Filename Generation Logic
```python
def generate_safe_filename(filepath: str) -> str:
    if not os.path.exists(filepath):
        return filepath
    
    path_obj = Path(filepath)
    stem = path_obj.stem
    suffix = path_obj.suffix
    parent = path_obj.parent
    
    # Generate 3-digit random number
    random_num = random.randint(100, 999)
    
    # Create new filename: name-123.ext
    new_name = f"{stem}-{random_num}{suffix}"
    return str(parent / new_name)
```

### System Prompt Design

#### Core Elements
1. **Role Definition**: Senior software engineer and code generator
2. **Output Format**: Specify triple backtick file delimiter requirements
3. **Code Quality**: Emphasis on clean, production-ready code
4. **File Organization**: Guidelines for proper file structure and naming
5. **Best Practices**: Security, performance, maintainability considerations

#### Placeholder Content
```python
SYSTEM_PROMPT = """
# System Prompt for Code Generation Assistant

You are an expert software engineer specializing in generating high-quality, production-ready code. Your role is to analyze requirements and create clean, well-structured code files that follow industry best practices.

## Output Format Requirements

When generating code files, you MUST use the following format:

```filepath/filename.ext
[file content here]
```

- Use triple backticks to delimit each file
- Include the full relative filepath on the same line as opening backticks
- Preserve all code formatting and indentation
- Generate multiple files as needed

## Code Quality Standards

- Write clean, readable, and maintainable code
- Follow language-specific conventions and best practices
- Include appropriate error handling
- Add comments only where necessary for clarity
- Ensure code is production-ready and follows security best practices

[Additional coding guidelines to be expanded based on specific needs]
"""
```

## Dependencies and Reuse

### Existing Components to Reuse
1. **Client Library**: `lib/client/` - All LLM client implementations
2. **File Handling**: `src/tech16-cli/file_handler.py` - File reading and validation
3. **URL Handling**: `src/tech16-cli/url_handler.py` - URL scraping with BeautifulSoup
4. **Configuration**: `lib/client/config.py` - Model-to-provider mapping

### New Dependencies
- **Standard Library**: `random` for collision avoidance, `pathlib` for path handling
- **Regex**: For parsing LLM output file delimiters
- **OS Operations**: File system operations for writing and directory creation

## Risk Assessment and Mitigation

### Identified Risks

#### High Risk
1. **File Overwrite**: Accidentally overwriting existing files
   - **Mitigation**: Robust collision detection and filename modification
   - **Validation**: Test with existing files in target directories

2. **Path Traversal**: LLM generating dangerous file paths (../../../etc/passwd)
   - **Mitigation**: Path validation and sanitization
   - **Security**: Restrict output to project directory or below

#### Medium Risk
1. **Parsing Failures**: LLM not following expected output format
   - **Mitigation**: Robust regex patterns and error handling
   - **Fallback**: Clear error messages for manual file extraction

2. **Permission Issues**: Writing to restricted directories
   - **Mitigation**: Proper error handling and user feedback
   - **Documentation**: Clear guidance on file permissions

#### Low Risk
1. **Large File Output**: LLM generating extremely large files
   - **Mitigation**: Basic size checks and user confirmation
   - **Monitoring**: Log file sizes for awareness

## Testing Strategy

### Unit Testing Focus Areas
1. **File Parsing**: Various LLM output formats and edge cases
2. **Collision Avoidance**: Filename generation under different scenarios
3. **Path Validation**: Security and safety checks
4. **Integration**: End-to-end workflow with mock LLM responses

### Integration Testing
1. **Multiple Models**: Test with different LLM providers
2. **Mixed Input**: Files and URLs together
3. **Real Scenarios**: Actual code generation tasks
4. **Error Conditions**: Network failures, permission issues, malformed input

## Success Criteria

### Functional Requirements
- ✅ CLI accepts `--model` as first argument
- ✅ Processes multiple files and URLs as input
- ✅ Combines inputs with system prompt for LLM context
- ✅ Parses LLM output for file delimiters
- ✅ Writes generated files to specified paths
- ✅ Avoids overwriting existing files with collision detection
- ✅ Prints non-file text (explanations, comments) to stdout

### Quality Requirements
- ✅ Reuses existing project infrastructure
- ✅ Follows established code patterns and conventions
- ✅ Includes comprehensive error handling
- ✅ Provides clear user feedback and progress indication
- ✅ Maintains security best practices

### Performance Requirements
- ✅ Efficient file I/O operations
- ✅ Reasonable memory usage for large LLM responses
- ✅ Fast file collision detection

## Timeline Estimation

### Development Phases
- **Phase 1** (Core CLI): 2-3 hours
- **Phase 2** (LLM Integration): 1-2 hours  
- **Phase 3** (Output Processing): 3-4 hours
- **Phase 4** (Integration/Testing): 2-3 hours
- **Phase 5** (Documentation/Polish): 1-2 hours

**Total Estimated Time**: 9-14 hours

### Critical Path
1. File parsing and writing logic (Phase 3) - Most complex component
2. End-to-end integration (Phase 4) - Dependency on all other phases
3. Security validation - Cross-cutting concern affecting multiple phases

## Future Enhancements (Out of Scope)

### Potential Extensions
1. **Configuration Files**: Support for custom system prompts
2. **Template System**: Pre-defined coding templates
3. **Interactive Mode**: Prompt for overwrite confirmation
4. **Diff Preview**: Show changes before writing files
5. **Batch Processing**: Process multiple model queries in sequence
6. **Output Validation**: Syntax checking for generated code

### Integration Opportunities
1. **Version Control**: Automatic git integration for generated files
2. **IDE Integration**: Plugin support for popular editors
3. **CI/CD**: Integration with build and deployment pipelines
4. **Code Review**: Automated code quality analysis

## Conclusion

This implementation plan provides a comprehensive roadmap for developing `tech16-coder` while maximizing reuse of existing infrastructure. The phased approach ensures systematic development with early validation of core functionality. The risk mitigation strategies address key security and reliability concerns, while the modular design supports future enhancements and maintenance.

The plan builds directly on the proven patterns from `tech16-planner`, ensuring consistency and reliability while adding the new file generation capabilities required for the coding use case.