#!/usr/bin/env python3
"""
PDF to Text Converter
A robust PDF parser that handles encoding artifacts and multiple PDF formats.
Created by Eliza for Vishen Lakhiani - February 14th, 2026
"""

import sys
import argparse
import re
from pathlib import Path
from typing import Optional, List

try:
    import PyPDF2
    import pdfplumber
except ImportError as e:
    print(f"Error: Missing required libraries. Please run: pip install -r requirements.txt")
    print(f"Details: {e}")
    sys.exit(1)


class PDFConverter:
    """Robust PDF to text converter with multiple parsing strategies."""
    
    def __init__(self, encoding_cleanup: bool = True, verbose: bool = False):
        self.encoding_cleanup = encoding_cleanup
        self.verbose = verbose
    
    def log(self, message: str):
        """Print message if verbose mode is enabled."""
        if self.verbose:
            print(f"[PDF Converter] {message}")
    
    def clean_encoding_artifacts(self, text: str) -> str:
        """Remove common PDF encoding artifacts and normalize text."""
        if not self.encoding_cleanup:
            return text
        
        # Remove null bytes and other control characters
        text = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F-\x9F]', '', text)
        
        # Fix common encoding issues
        replacements = {
            # Common PDF artifacts
            'ï¿½': '',  # Replacement character
            'â€™': "'",  # Smart apostrophe
            'â€œ': '"',  # Smart quote left
            'â€': '"',   # Smart quote right  
            'â€"': '—',  # Em dash
            'â€"': '–',  # En dash
            'â€¦': '...',  # Ellipsis
            'Â': '',     # Non-breaking space artifact
            'Ã©': 'é',   # e with acute
            'Ã¡': 'á',   # a with acute
            'Ã­': 'í',   # i with acute
            'Ã³': 'ó',   # o with acute
            'Ãº': 'ú',   # u with acute
            'Ã±': 'ñ',   # n with tilde
        }
        
        for artifact, replacement in replacements.items():
            text = text.replace(artifact, replacement)
        
        # Normalize whitespace
        text = re.sub(r'\n\s*\n\s*\n', '\n\n', text)  # Max double newlines
        text = re.sub(r'[ \t]+', ' ', text)  # Normalize spaces
        text = text.strip()
        
        return text
    
    def extract_with_pypdf2(self, pdf_path: Path) -> Optional[str]:
        """Extract text using PyPDF2 library."""
        try:
            self.log("Attempting extraction with PyPDF2...")
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page_num, page in enumerate(reader.pages):
                    try:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
                            self.log(f"Extracted page {page_num + 1}")
                    except Exception as e:
                        self.log(f"Error on page {page_num + 1}: {e}")
                        continue
                return text.strip()
        except Exception as e:
            self.log(f"PyPDF2 extraction failed: {e}")
            return None
    
    def extract_with_pdfplumber(self, pdf_path: Path) -> Optional[str]:
        """Extract text using pdfplumber library."""
        try:
            self.log("Attempting extraction with pdfplumber...")
            with pdfplumber.open(pdf_path) as pdf:
                text = ""
                for page_num, page in enumerate(pdf.pages):
                    try:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
                            self.log(f"Extracted page {page_num + 1}")
                    except Exception as e:
                        self.log(f"Error on page {page_num + 1}: {e}")
                        continue
                return text.strip()
        except Exception as e:
            self.log(f"pdfplumber extraction failed: {e}")
            return None
    
    def convert_pdf(self, pdf_path: Path) -> Optional[str]:
        """
        Convert PDF to text using best available method.
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Extracted text or None if extraction fails
        """
        if not pdf_path.exists():
            print(f"Error: File not found: {pdf_path}")
            return None
        
        if not pdf_path.suffix.lower() == '.pdf':
            print(f"Error: File is not a PDF: {pdf_path}")
            return None
        
        self.log(f"Processing: {pdf_path}")
        
        # Try pdfplumber first (generally more reliable for complex layouts)
        text = self.extract_with_pdfplumber(pdf_path)
        
        # Fallback to PyPDF2 if pdfplumber fails
        if not text or len(text.strip()) < 50:
            self.log("pdfplumber result insufficient, trying PyPDF2...")
            text = self.extract_with_pypdf2(pdf_path)
        
        # Clean encoding artifacts if extraction succeeded
        if text:
            original_length = len(text)
            text = self.clean_encoding_artifacts(text)
            self.log(f"Text extracted: {original_length} -> {len(text)} characters after cleanup")
            return text
        else:
            print(f"Error: Unable to extract text from {pdf_path}")
            return None


def main():
    """Command line interface for PDF conversion."""
    parser = argparse.ArgumentParser(
        description="Convert PDF files to clean text",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 pdf_converter.py document.pdf
  python3 pdf_converter.py document.pdf -o output.txt
  python3 pdf_converter.py *.pdf --batch
  python3 pdf_converter.py document.pdf --no-cleanup --verbose
        """
    )
    
    parser.add_argument('input', nargs='+', help='PDF file(s) to convert')
    parser.add_argument('-o', '--output', help='Output file (default: stdout or auto-generated)')
    parser.add_argument('--no-cleanup', action='store_true', 
                       help='Skip encoding artifact cleanup')
    parser.add_argument('--batch', action='store_true',
                       help='Process multiple files, auto-generate output names')
    parser.add_argument('--verbose', action='store_true',
                       help='Enable verbose output')
    
    args = parser.parse_args()
    
    # Initialize converter
    converter = PDFConverter(
        encoding_cleanup=not args.no_cleanup,
        verbose=args.verbose
    )
    
    # Process files
    for input_path_str in args.input:
        input_path = Path(input_path_str)
        
        # Handle wildcards if shell didn't expand them
        if '*' in input_path_str and not input_path.exists():
            matching_files = list(input_path.parent.glob(input_path.name))
            if not matching_files:
                print(f"No files found matching: {input_path_str}")
                continue
        else:
            matching_files = [input_path]
        
        for pdf_path in matching_files:
            # Convert PDF
            text = converter.convert_pdf(pdf_path)
            if not text:
                continue
            
            # Determine output
            if args.batch or len(args.input) > 1:
                # Auto-generate output filename
                output_path = pdf_path.with_suffix('.txt')
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(text)
                print(f"✅ Converted: {pdf_path} -> {output_path}")
            elif args.output:
                # Specific output file
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(text)
                print(f"✅ Converted: {pdf_path} -> {args.output}")
            else:
                # Output to stdout
                print(text)


if __name__ == "__main__":
    main()