"""URL content handling with robust encoding detection and error handling."""

import urllib.parse
from typing import Optional, Set

import requests
from bs4 import BeautifulSoup

# Content types we can safely process
ALLOWED_CONTENT_TYPES = {
    'text/html', 'text/plain', 'text/xml', 'text/css', 'text/javascript',
    'application/json', 'application/xml', 'application/xhtml+xml',
    'application/javascript', 'application/x-javascript'
}

# Maximum content size to process (5MB)
MAX_CONTENT_SIZE = 5 * 1024 * 1024

# Request timeout in seconds
REQUEST_TIMEOUT = 15


def is_valid_url(url_string: str) -> bool:
    """Check if a string is a valid URL."""
    try:
        result = urllib.parse.urlparse(url_string)
        return bool(result.scheme and result.netloc)
    except Exception:
        return False


def is_processable_content_type(content_type: str) -> bool:
    """Check if content type is safe to process as text."""
    if not content_type:
        return False
    
    # Extract main content type (ignore charset, etc.)
    main_type = content_type.split(';')[0].strip().lower()
    return main_type in ALLOWED_CONTENT_TYPES


def detect_response_encoding(response: requests.Response) -> str:
    """Detect the best encoding for the response."""
    # First, try the response's apparent encoding (from headers)
    if response.encoding and response.encoding.lower() != 'iso-8859-1':
        # requests defaults to ISO-8859-1 if no charset is specified, which is often wrong
        return response.encoding
    
    # Try to detect from content
    try:
        import chardet
        detected = chardet.detect(response.content[:8192])  # Check first 8KB
        if detected['encoding'] and detected['confidence'] > 0.7:
            return detected['encoding']
    except ImportError:
        pass
    
    # Fallback to UTF-8
    return 'utf-8'


def clean_html_content(html_content: str) -> str:
    """Extract and clean text content from HTML."""
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove script and style elements
        for element in soup(['script', 'style', 'nav', 'header', 'footer', 'aside']):
            element.decompose()
        
        # Remove comments
        from bs4 import Comment
        for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
            comment.extract()
        
        # Get text content
        text = soup.get_text()
        
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text
        
    except Exception as e:
        return f"Error parsing HTML content: {e}"


def scrape_url_content(url: str) -> str:
    """
    Scrape content from a single URL with robust encoding handling.
    
    Args:
        url: URL to scrape
        
    Returns:
        str: Scraped content or error message
    """
    if not is_valid_url(url):
        return f"Error: Invalid URL format: {url}"
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; tech16-cli/1.0)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,text/plain;q=0.8,*/*;q=0.1',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
        }
        
        # Make request with timeout
        response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT, stream=True)
        response.raise_for_status()
        
        # Check content type before downloading
        content_type = response.headers.get('content-type', '').lower()
        if not is_processable_content_type(content_type):
            return f"Skipped non-text content (type: {content_type}): {url}"
        
        # Check content length
        content_length = response.headers.get('content-length')
        if content_length and int(content_length) > MAX_CONTENT_SIZE:
            size_mb = int(content_length) / (1024 * 1024)
            return f"Error: Content too large ({size_mb:.1f}MB, max {MAX_CONTENT_SIZE // (1024*1024)}MB): {url}"
        
        # Download content with size limit
        content_bytes = b''
        downloaded = 0
        
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                downloaded += len(chunk)
                if downloaded > MAX_CONTENT_SIZE:
                    return f"Error: Content exceeded size limit during download: {url}"
                content_bytes += chunk
        
        # Detect and decode with proper encoding
        if 'html' in content_type:
            # For HTML, use requests' text property but with our encoding detection
            try:
                encoding = detect_response_encoding(response)
                text_content = content_bytes.decode(encoding, errors='replace')
                cleaned_content = clean_html_content(text_content)
            except Exception as e:
                return f"Error decoding HTML content from {url}: {e}"
        else:
            # For plain text and other formats
            try:
                encoding = detect_response_encoding(response)
                cleaned_content = content_bytes.decode(encoding, errors='replace')
            except Exception as e:
                return f"Error decoding content from {url}: {e}"
        
        # Basic content validation
        if not cleaned_content.strip():
            return f"Warning: No text content found at {url}"
        
        # Truncate very long content
        if len(cleaned_content) > 50000:  # 50KB of text
            cleaned_content = cleaned_content[:50000] + "\n... [Content truncated]"
        
        return f"Content from {url} (type: {content_type}, encoding: {encoding}):\n{cleaned_content}"
        
    except requests.exceptions.Timeout:
        return f"Error: Request timeout ({REQUEST_TIMEOUT}s) for URL: {url}"
    except requests.exceptions.ConnectionError:
        return f"Error: Connection failed for URL: {url}"
    except requests.exceptions.HTTPError as e:
        return f"Error: HTTP {e.response.status_code} for URL: {url}"
    except requests.exceptions.RequestException as e:
        return f"Error: Request failed for URL {url}: {e}"
    except Exception as e:
        return f"Error: Unexpected error processing URL {url}: {e}"


def validate_urls(urls: list[str]) -> list[str]:
    """
    Validate a list of URLs and return error messages for invalid ones.
    
    Args:
        urls: List of URLs to validate
        
    Returns:
        List[str]: List of validation error messages (empty if all valid)
    """
    errors = []
    
    for url in urls:
        if not is_valid_url(url):
            errors.append(f"Invalid URL format: {url}")
        else:
            # Check for obviously problematic URLs
            parsed = urllib.parse.urlparse(url)
            if parsed.scheme not in ['http', 'https']:
                errors.append(f"Unsupported URL scheme '{parsed.scheme}': {url}")
    
    return errors