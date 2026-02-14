#!/usr/bin/env python3
"""
Test script to verify PDF converter is working
"""

import tempfile
from pathlib import Path
import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pdf_converter import PDFConverter

def create_test_content():
    """Create a sample text for testing encoding cleanup."""
    test_text = """
This is a test documentÂ with encodingÂ issues.
Itâ€™s important to clean these up properly.
Here are some examples:
- Smart quotes: â€œHelloâ€ and â€˜worldâ€™
- Dashes: â€" and â€"
- Special chars: Ã©, Ã±, Ãº
- Artifacts: ï¿½ replacement characters
    """
    return test_text

def test_encoding_cleanup():
    """Test the encoding cleanup functionality."""
    print("🧪 Testing encoding cleanup...")
    
    converter = PDFConverter(encoding_cleanup=True, verbose=True)
    test_text = create_test_content()
    
    print("\n📥 Original text with artifacts:")
    print(repr(test_text))
    
    cleaned_text = converter.clean_encoding_artifacts(test_text)
    
    print("\n✨ Cleaned text:")
    print(repr(cleaned_text))
    print("\n📄 Readable output:")
    print(cleaned_text)
    
    # Basic validation
    assert 'Â' not in cleaned_text, "Non-breaking space artifacts remain"
    assert 'â€™' not in cleaned_text, "Smart quote artifacts remain" 
    assert 'ï¿½' not in cleaned_text, "Replacement characters remain"
    
    print("\n✅ Encoding cleanup test passed!")

if __name__ == "__main__":
    test_encoding_cleanup()
    print("\n🎉 All tests completed successfully!")