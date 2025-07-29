# Tech16 Final Project

- author : david howard
- linkedin : https://www.linkedin.com/in/david-howard-95482a1/
- github : https://github.com/dmh2000/tech16-cli

Because I am an old school terminal guy, I decided to cobble some command line AI tools for use in shell scripts. I initially started on a do-everything cli tool (see src/tech16-cli) but I decided to add a couple of special purpose cli tools that do one thing only:

- src/tech-cli : tries to cover all bases. not fully tested
- src/tech-planner : has a system prompt that configures it as a planning assistant. it can try to plan just about anything, such as a code project or a trip.
- src/tech-coder : has a system prompt that configures it as a coding assistant.

The intent is providing cli tools that could be combined in a shell script to create an 'agent'.

<img src="o0hr3le7b6a71.png" width="240px"/>

## tech16-coder

[tech16-coder](src/tech16-coder/) is reasonably easy to use. You specify a model (or accept the default of o4-mini) and a file containing a description of what you want, prompt plus (optional) files and urls as context, and it will attempt to write the requestd code. This app will write the file or files it generates based on the paths and filenames the LLM called for. It's not a smart agent like Claude, Cline, Cursor etc, so right now its best for simple requests, like "write me a single file python program that does X'.

### System Prompt

Uses a [system prompt for a coder](src/tech16-coder/system.py). This system prompt was created in steps:

- asked Perplexity what a system prompt for a coder assistant should have
- had anthropic claude generate the system prompt, following the recommendations from Perplexity
- hard coded this prompt in the application

### Implementation

98% of the code in tech16-coder is generated using Claude Code and the claude-4-sonnet model. I didn't use Opus because its really expensive. The code was created step by step:

1. I wrote a [rough description](prompts/tech16-coder.md) of what I wanted this app to do.
2. Gave the description to Claude and asked it to create a [comprehensive implementation plan](prompts/tech16-coder-implementation.md).
3. Gave that implementation plan to Claude and told it to implement the app.
4. I tweaked some of the code by hand because sometimes its easier to do that than come up with a specific enought prompt.

## Examples

Bash scripts that use tech16-coder

examples
├── coder-hello.sh
├── coder.sh
├── mlb (Major League Basball)
│   ├── coder-mlb-api.sh
│   ├── coder-mlb-csv.sh
│   ├── coder-mlb-prompt.md
│   ├── coder-mlb.sh
│   ├── coder-mlb-web.sh
│   ├── mlb
└── web (simple web app)
└── coder-web.sh

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

[tech16-planner](src/tech16-planner/) is an assistant that will generate a plan for just about anything you ask for that could be planned. Again, pretty easy to use.

### System Prompt

Uses a [system prompt for a coder](src/tech16-planner/system.py). This system prompt was created in steps:

- asked Perplexity what a system prompt for a planner assistant should have
- had anthropic claude generate the system prompt, following the recommendations from Perplexity
- hard coded this prompt in the application

### Implementation

98% of the code in tech16-coder is generated using Claude Code and the claude-4-sonnet model. I didn't use Opus because its really expensive. The code was created step by step:

1. I wrote a [rough description](prompts/tech16-planner.md) of what I wanted this app to do.
2. Gave the description to Claude and asked it to create a [comprehensive implementation plan](prompts/tech16-planner-implementation.md).
3. Gave that implementation plan to Claude and told it to implement the app.
4. I tweaked some of the code by hand because sometimes its easier to do that than come up with a specific enought prompt.

## Examples

./examples
├── all.sh
├── hello.md
├── hello-plan.md
├── hello.sh
├── output
│   ├── hello-plan.md
│   ├── space-plan.md
│   └── trip-plan.md
├── space.md
├── space-plan.md
├── space.sh
├── trip.md
├── trip-plan.md
└── trip.sh

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
