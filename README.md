# Tech16 Final Project

- author : david howard

## tech16-coder

### Usage

```text
tech16-coder - Code generation assistant

USAGE:
  tech16-coder --model MODEL_NAME [FILES_AND_URLS...]

ARGUMENTS:
  --model MODEL_NAME   Model to use (required, must be first argument)
  FILES_AND_URLS       Any number of files and URLs to analyze

EXAMPLES:
  tech16-coder --model claude-sonnet-4 requirements.md
  tech16-coder --model o4-mini file1.txt file2.py https://example.com/docs
  tech16-coder --model gemini-2.5-pro spec.txt https://docs.api.com

SUPPORTED PROVIDERS AND MODELS:

  ANTHROPIC:
    - claude-3-5-haiku-20241022
    - claude-sonnet-4-20250514

  GEMINI:
    - gemini-2.5-flash
    - gemini-2.5-pro

  OPENAI:
    - gpt-4o-mini
    - o3-mini
    - o4-mini

Total models available: 7

NOTE: Requires appropriate API keys set as environment variables:
  - ANTHROPIC_API_KEY for Anthropic models
  - OPENAI_API_KEY for OpenAI models
  - GOOGLE_API_KEY for Gemini models
```

## tech16-planner

### Usage

```text

tech16-planner - General purpose lanning assistant CLI tool

USAGE:
  tech16-planner --model MODEL_NAME [FILES_AND_URLS...]

ARGUMENTS:
  --model MODEL_NAME   Model to use (required, must be first argument)
  FILES_AND_URLS       Any number of files and URLs to analyze

EXAMPLES:
  tech16-planner --model claude-sonnet-4 project-docs.md
  tech16-planner --model o4-mini file1.txt file2.py https://example.com/docs
  tech16-planner --model gemini-2.5-pro requirements.txt https://docs.api.com

SUPPORTED PROVIDERS AND MODELS:

  ANTHROPIC:
    - claude-3-5-haiku-20241022
    - claude-sonnet-4-20250514

  GEMINI:
    - gemini-2.5-flash
    - gemini-2.5-pro

  OPENAI:
    - gpt-4o-mini
    - o3-mini
    - o4-mini

Total models available: 7

NOTE: Requires appropriate API keys set as environment variables:
  - ANTHROPIC_API_KEY for Anthropic models
  - OPENAI_API_KEY for OpenAI models
  - GOOGLE_API_KEY for Gemini models

```

## tech16-cli

This tool is a more general purpose tool that does not have a specific system prompt. It has an optional command line argument to specify a system prompt.

### Usage

tech16-cli - Query LLMs with custom prompts and context

USAGE:
tech16-cli [OPTIONS] [FILES_AND_URLS...]

OPTIONS:
--prompt FILENAME File containing the prompt to use
--model MODEL_NAME Model to use (default: o4-mini)
--help Show this help message

EXAMPLES:
tech16-cli file.txt
tech16-cli --model claude-sonnet-4 file.txt
tech16-cli --prompt system.txt --model o4-mini https://example.com/docs
echo "analyze this" | tech16-cli --prompt review.txt
tech16-cli --prompt plan.txt file1.py file2.py https://docs.example.com

SUPPORTED PROVIDERS AND MODELS:

ANTHROPIC: - claude-3-5-haiku-20241022 - claude-sonnet-4-20250514

GEMINI: - gemini-2.5-flash - gemini-2.5-pro

OPENAI: - gpt-4o-mini - o3-mini - o4-mini (default)

Total models available: 7

NOTE: Requires appropriate API keys set as environment variables:

- ANTHROPIC_API_KEY for Anthropic models
- OPENAI_API_KEY for OpenAI models
- GOOGLE_API_KEY for Gemini models
