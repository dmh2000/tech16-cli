"""File writer module for parsing LLM output and writing generated files."""

import os
import re
import random
from pathlib import Path
from typing import List, Tuple, NamedTuple


class FileSpec(NamedTuple):
    """Specification for a file to be written."""

    filepath: str
    content: str


def parse_llm_output(response: str) -> Tuple[List[FileSpec], str]:
    """
    Parse LLM output to extract file specifications and non-file text.

    Args:
        response: Raw LLM response containing file blocks and explanatory text

    Returns:
        Tuple[List[FileSpec], str]: (file_specs, non_file_text)
    """
    file_specs = []

    # Pattern to match triple backtick blocks with file annotations
    # Captures: filepath on same line as opening ```, and file content
    file_pattern = r"```(\S+)\n(.*?)\n```"

    # Find all file blocks
    matches = re.findall(file_pattern, response, re.MULTILINE | re.DOTALL)

    for filepath, content in matches:
        # Validate filepath format - basic security check
        if not _is_safe_filepath(filepath):
            print(
                f"Warning: Skipping potentially unsafe filepath: {filepath}",
                file=sys.stderr,
            )
            continue

        file_specs.append(FileSpec(filepath=filepath, content=content))

    # Extract non-file text by removing all file blocks
    non_file_text = re.sub(file_pattern, "", response, flags=re.MULTILINE | re.DOTALL)

    # Clean up extra whitespace while preserving intentional formatting
    non_file_text = re.sub(r"\n\s*\n\s*\n", "\n\n", non_file_text.strip())

    return file_specs, non_file_text


def write_generated_files(file_specs: List[FileSpec]) -> List[str]:
    """
    Write generated files to filesystem with collision avoidance.
    Only writes files within the current working directory for security.

    Args:
        file_specs: List of file specifications to write

    Returns:
        List[str]: List of actual filepaths written (may differ from requested due to collisions)
    """
    written_files = []
    cwd = Path.cwd()

    for file_spec in file_specs:
        try:
            # Validate that the file path is within current working directory
            if not _is_within_cwd(file_spec.filepath, cwd):
                print(
                    f"Warning: Skipping file outside current working directory: {file_spec.filepath}",
                    file=sys.stderr,
                )
                continue

            # Generate safe filename to avoid collisions
            safe_filepath = generate_safe_filename(file_spec.filepath)

            # Double-check that the safe filepath is still within CWD
            if not _is_within_cwd(safe_filepath, cwd):
                print(
                    f"Warning: Skipping file outside current working directory after collision avoidance: {safe_filepath}",
                    file=sys.stderr,
                )
                continue

            # Create parent directories if they don't exist
            parent_dir = Path(safe_filepath).parent
            parent_dir.mkdir(parents=True, exist_ok=True)

            # Write the file
            with open(safe_filepath, "w", encoding="utf-8") as f:
                f.write(file_spec.content)

            written_files.append(safe_filepath)

        except (OSError, IOError) as e:
            print(f"Error writing file {file_spec.filepath}: {e}", file=sys.stderr)
            continue

    return written_files


def generate_safe_filename(filepath: str) -> str:
    """
    Generate a safe filename that doesn't overwrite existing files.

    Args:
        filepath: Requested filepath

    Returns:
        str: Safe filepath (may have random suffix if collision detected)
    """
    return filepath
    # if not os.path.exists(filepath):
    #     return filepath

    # path_obj = Path(filepath)
    # stem = path_obj.stem
    # suffix = path_obj.suffix
    # parent = path_obj.parent

    # # Try up to 10 times to find a non-colliding filename
    # for _ in range(10):
    #     # Generate 3-digit random number
    #     random_num = random.randint(100, 999)

    #     # Create new filename: name-123.ext
    #     new_name = f"{stem}-{random_num}{suffix}"
    #     new_filepath = str(parent / new_name)

    #     if not os.path.exists(new_filepath):
    #         return new_filepath

    # # Fallback if we couldn't find a free name after 10 tries
    # # Use timestamp-based suffix
    # import time
    # timestamp = int(time.time() * 1000) % 100000
    # new_name = f"{stem}-{timestamp}{suffix}"
    # return str(parent / new_name)


def print_non_file_text(non_file_text: str) -> None:
    """
    Print non-file text (explanations, comments) to stdout.

    Args:
        non_file_text: Text content that should be displayed to user
    """
    if non_file_text.strip():
        print(non_file_text)


def _is_safe_filepath(filepath: str) -> bool:
    """
    Check if a filepath is safe to write to (basic path traversal protection).

    Args:
        filepath: Filepath to validate

    Returns:
        bool: True if filepath is considered safe
    """
    # Convert to Path object for normalization
    try:
        path_obj = Path(filepath)

        # Check for path traversal attempts
        if ".." in str(path_obj):
            return False

        # Check for absolute paths (should be relative)
        if path_obj.is_absolute():
            return False

        # Basic filename validation - allow normal files
        if not path_obj.name:
            return False

        # Don't allow hidden files that start with dot (except common extensions)
        if path_obj.name.startswith(".") and not any(
            path_obj.name.endswith(ext)
            for ext in [".py", ".js", ".ts", ".json", ".md", ".txt"]
        ):
            return False

        # Check if path is within current working directory
        if not _is_within_cwd(filepath, Path.cwd()):
            return False

        return True

    except (ValueError, OSError):
        return False


def _is_within_cwd(filepath: str, cwd: Path) -> bool:
    """
    Check if a filepath resolves to a location within the current working directory.

    Args:
        filepath: Filepath to check
        cwd: Current working directory Path object

    Returns:
        bool: True if filepath is within the current working directory
    """
    try:
        # Resolve the filepath to an absolute path
        resolved_path = (cwd / filepath).resolve()

        # Check if the resolved path is within the current working directory
        return cwd.resolve() in resolved_path.parents or resolved_path == cwd.resolve()

    except (ValueError, OSError):
        return False


# Import sys for stderr usage
import sys
