# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an early-stage Python project for building a command-line tool that performs queries to AI LLMs. The project is currently in the planning phase.

## Project Structure

- `prompts/`: Contains project planning and architecture documents
  - `layout.md`: Discusses preferred Python project layout with main application and library packages
  - `plan.md`: Outlines the vision for building a CLI tool for AI LLM queries
- `sqirvy-mcp.log`: MCP (Model Context Protocol) server interaction logs

## Development Setup

This project uses Python and follows standard Python project conventions as indicated by the `.gitignore` file.

**Note**: No build scripts, package management files, or test frameworks have been configured yet. When implementing:

- Consider using a standard Python project layout with `src/` directory structure
- Set up package management (requirements.txt, pyproject.toml, or Pipfile)
- Configure testing framework (pytest recommended based on gitignore patterns)
- Add linting and formatting tools (mypy, black, ruff, etc.)

## Architecture Notes

Based on planning documents, the intended architecture includes:
- A main CLI application
- One or more library packages in parallel directories
- Integration with AI LLM services
- MCP (Model Context Protocol) server capabilities

## Current Status

Project is in initial planning phase. No code implementation exists yet.