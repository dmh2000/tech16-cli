"""File content handling with robust encoding detection and error handling."""

import os
import mimetypes
from pathlib import Path
from typing import Optional, List

# Binary file extensions to skip
BINARY_EXTENSIONS = {
    '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp',  # Images
    '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',  # Documents
    '.zip', '.tar', '.gz', '.rar', '.7z',  # Archives
    '.exe', '.dll', '.so', '.dylib',  # Executables
    '.mp3', '.mp4', '.avi', '.mov', '.wav',  # Media
    '.bin', '.dat', '.db', '.sqlite'  # Binary data
}

# Text file extensions that are safe to process
TEXT_EXTENSIONS = {
    '.txt', '.md', '.py', '.js', '.html', '.css', '.json', '.xml',
    '.yml', '.yaml', '.toml', '.ini', '.cfg', '.conf', '.log',
    '.sh', '.bash', '.zsh', '.fish', '.ps1', '.bat', '.cmd',
    '.c', '.cpp', '.h', '.hpp', '.java', '.go', '.rs', '.rb',
    '.php', '.pl', '.r', '.sql', '.csv', '.tsv'
}

# Encoding attempts in order of preference
ENCODING_ATTEMPTS = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252', 'iso-8859-1']

# Maximum file size to process (10MB)
MAX_FILE_SIZE = 10 * 1024 * 1024


def is_binary_file(filepath: str) -> bool:
    """Check if a file is likely binary based on extension and MIME type."""
    path = Path(filepath)
    
    # Check extension
    if path.suffix.lower() in BINARY_EXTENSIONS:
        return True
    
    # Check MIME type
    mime_type, _ = mimetypes.guess_type(filepath)
    if mime_type:
        if not mime_type.startswith(('text/', 'application/json', 'application/xml')):
            # Allow some application types that are text-based
            text_app_types = {
                'application/javascript', 'application/x-sh', 'application/x-python',
                'application/x-yaml', 'application/toml'
            }
            if mime_type not in text_app_types:
                return True
    
    return False


def detect_file_encoding(filepath: str) -> Optional[str]:
    """Detect file encoding by trying common encodings."""
    try:
        with open(filepath, 'rb') as f:
            raw_data = f.read(min(8192, MAX_FILE_SIZE))  # Read first 8KB or max size
        
        for encoding in ENCODING_ATTEMPTS:
            try:
                raw_data.decode(encoding)
                return encoding
            except UnicodeDecodeError:
                continue
        
        # If all attempts fail, try chardet if available
        try:
            import chardet
            result = chardet.detect(raw_data)
            if result['encoding'] and result['confidence'] > 0.7:
                return result['encoding']
        except ImportError:
            pass
        
        return None
    except Exception:
        return None


def is_file_too_large(filepath: str) -> bool:
    """Check if file exceeds size limit."""
    try:
        return Path(filepath).stat().st_size > MAX_FILE_SIZE
    except Exception:
        return True


def read_file_content(filepath: str) -> str:
    """
    Read file content with robust encoding handling.
    
    Args:
        filepath: Path to the file to read
        
    Returns:
        str: File content or error message
    """
    try:
        path = Path(filepath)
        
        # Check if file exists
        if not path.exists():
            return f"Error: File not found: {filepath}"
        
        if not path.is_file():
            return f"Error: Path is not a file: {filepath}"
        
        # Check file size
        if is_file_too_large(filepath):
            size_mb = path.stat().st_size / (1024 * 1024)
            return f"Error: File too large ({size_mb:.1f}MB, max {MAX_FILE_SIZE // (1024*1024)}MB): {filepath}"
        
        # Check if it's a binary file
        if is_binary_file(filepath):
            return f"Skipped binary file: {filepath}"
        
        # Detect encoding
        encoding = detect_file_encoding(filepath)
        if not encoding:
            return f"Error: Could not determine encoding for file: {filepath}"
        
        # Read with detected encoding
        with open(path, 'r', encoding=encoding, errors='replace') as f:
            content = f.read()
        
        # Remove BOM if present
        if content.startswith('\ufeff'):
            content = content[1:]
        
        # Basic content validation
        if not content.strip():
            return f"Warning: Empty file: {filepath}"
        
        return f"Content from file {filepath} (encoding: {encoding}):\n{content}"
        
    except PermissionError:
        return f"Error: Permission denied reading file: {filepath}"
    except OSError as e:
        return f"Error: OS error reading file '{filepath}': {e}"
    except Exception as e:
        return f"Error: Failed to read file '{filepath}': {e}"


def validate_file_paths(file_paths: List[str]) -> List[str]:
    """
    Validate a list of file paths and return error messages for invalid ones.
    
    Args:
        file_paths: List of file paths to validate
        
    Returns:
        List[str]: List of validation error messages (empty if all valid)
    """
    errors = []
    
    for filepath in file_paths:
        try:
            path = Path(filepath)
            if not path.exists():
                errors.append(f"File not found: {filepath}")
            elif not path.is_file():
                errors.append(f"Path is not a file: {filepath}")
            elif not os.access(filepath, os.R_OK):
                errors.append(f"File not readable: {filepath}")
        except Exception as e:
            errors.append(f"Invalid file path '{filepath}': {e}")
    
    return errors