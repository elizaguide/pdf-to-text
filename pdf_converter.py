#!/usr/bin/env python3
"""
PDF to Text Converter
Extracts clean text from PDF files with error handling and formatting cleanup.
"""

import sys
import argparse
import os
from pathlib import Path

try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except ImportError:
    PDFPLUMBER_AVAILABLE = False

try:
    from PyPDF2 import PdfReader
    PYPDF2_AVAILABLE = True
except ImportError:
    PYPDF2_AVAILABLE = False


class PDFConverter:
    """Clean, simple PDF to text converter."""
    
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.method_used = None
    
    def _log(self, message):
        """Print verbose output if enabled."""
        if self.verbose:
            print(f"[*] {message}", file=sys.stderr)
    
    def _clean_text(self, text):
        """Clean extracted text of common encoding artifacts."""
        import re
        
        # Remove multiple consecutive newlines
        text = '\n'.join([line.rstrip() for line in text.split('\n')])
        
        # Remove form feeds and other control characters
        text = text.replace('\f', '\n')
        text = text.replace('\x00', '')
        
        # Clean up common encoding artifacts
        text = text.replace('Â', '')
        text = text.replace('â', '')
        
        # Remove CID (character ID) encoding artifacts like (cid:XXXX)
        text = re.sub(r'\(cid:\d+\)', '•', text)
        
        # Normalize whitespace
        lines = []
        for line in text.split('\n'):
            # Strip trailing whitespace but preserve indentation
            line = line.rstrip()
            if line:  # Skip completely empty lines
                lines.append(line)
            elif lines and lines[-1]:  # Keep single blank lines between content
                lines.append('')
        
        # Remove trailing empty lines
        while lines and not lines[-1]:
            lines.pop()
        
        return '\n'.join(lines)
    
    def convert_with_pdfplumber(self, pdf_path):
        """Extract text using pdfplumber (preferred method)."""
        try:
            text = ""
            with pdfplumber.open(pdf_path) as pdf:
                self._log(f"PDF has {len(pdf.pages)} pages")
                for i, page in enumerate(pdf.pages, 1):
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                    self._log(f"Extracted page {i}/{len(pdf.pages)}")
            
            self.method_used = "pdfplumber"
            return self._clean_text(text)
        except Exception as e:
            self._log(f"pdfplumber failed: {e}")
            return None
    
    def convert_with_pypdf2(self, pdf_path):
        """Fallback: Extract text using PyPDF2."""
        try:
            text = ""
            with open(pdf_path, 'rb') as f:
                reader = PdfReader(f)
                self._log(f"PDF has {len(reader.pages)} pages")
                for i, page in enumerate(reader.pages, 1):
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                    self._log(f"Extracted page {i}/{len(reader.pages)}")
            
            self.method_used = "PyPDF2"
            return self._clean_text(text)
        except Exception as e:
            self._log(f"PyPDF2 failed: {e}")
            return None
    
    def convert(self, pdf_path):
        """Convert PDF to text, trying best method first."""
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        self._log(f"Converting: {pdf_path}")
        
        # Try pdfplumber first (better text extraction)
        if PDFPLUMBER_AVAILABLE:
            result = self.convert_with_pdfplumber(pdf_path)
            if result:
                self._log(f"Successfully extracted with {self.method_used}")
                return result
        
        # Fallback to PyPDF2
        if PYPDF2_AVAILABLE:
            result = self.convert_with_pypdf2(pdf_path)
            if result:
                self._log(f"Successfully extracted with {self.method_used}")
                return result
        
        # No working method available
        raise RuntimeError(
            "No PDF library available. Install with:\n"
            "  pip install pdfplumber PyPDF2"
        )


def main():
    """CLI interface."""
    parser = argparse.ArgumentParser(
        description='Convert PDF files to clean text',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python pdf_converter.py document.pdf
  python pdf_converter.py input.pdf -o output.txt
  python pdf_converter.py report.pdf -v
        """
    )
    
    parser.add_argument(
        'pdf_file',
        help='PDF file to convert'
    )
    parser.add_argument(
        '-o', '--output',
        help='Output text file (default: stdout)'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Show detailed processing info'
    )
    
    args = parser.parse_args()
    
    try:
        converter = PDFConverter(verbose=args.verbose)
        text = converter.convert(args.pdf_file)
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(text)
            print(f"✅ Converted to: {args.output}")
        else:
            print(text)
        
        return 0
    
    except FileNotFoundError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1
    except RuntimeError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"❌ Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
