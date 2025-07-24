#!/usr/bin/env python3
"""Test script for file_writer module parsing functionality."""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "lib"))

from client.file_writer import (
    parse_llm_output,
    write_generated_files,
    print_non_file_text,
)

# Mock LLM response for testing
mock_response = """Here's a simple Python function that adds two numbers:

```output/math_utils.py
def add_numbers(a, b):
    \"\"\"Add two numbers and return the result.\"\"\"
    return a + b

if __name__ == "__main__":
    result = add_numbers(5, 3)
    print(f"5 + 3 = {result}")
```

And here's a test file for it:

```output/test_math_utils.py
import unittest
from math_utils import add_numbers

class TestMathUtils(unittest.TestCase):
    def test_add_numbers(self):
        self.assertEqual(add_numbers(2, 3), 5)
        self.assertEqual(add_numbers(-1, 1), 0)
        self.assertEqual(add_numbers(0, 0), 0)

if __name__ == "__main__":
    unittest.main()
```

These files provide a basic mathematical utility and its corresponding test suite.
"""


def test_parsing():
    """Test the parsing functionality."""
    print("Testing file parsing...")

    file_specs, non_file_text = parse_llm_output(mock_response)

    print(f"Found {len(file_specs)} files:")
    for spec in file_specs:
        print(f"  - {spec.filepath}")

    print("\nNon-file text:")
    print(repr(non_file_text))

    print("\nNon-file text formatted:")
    print_non_file_text(non_file_text)


if __name__ == "__main__":
    test_parsing()
