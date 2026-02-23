#!/usr/bin/env python3
"""
PDF to Text Converter
Converts PDF files to clean, readable text output
Handles multiple PDF formats and cleans up encoding artifacts
"""

import sys
import os
import re
from pathlib import Path
from typing import Optional, List
import argparse

try:
    import PyPDF2
except ImportError:
    print("Error: PyPDF2 not installed. Install with: pip install PyPDF2")
    sys.exit(1)


class PDFToTextConverter:
    """Convert PDF files to clean text"""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        
    def clean_text(self, text: str) -> str:
        """
        Clean extracted text from encoding artifacts and formatting issues
        
        Args:
            text: Raw extracted text from PDF
            
        Returns:
            Cleaned text ready for analysis
        """
        # Remove excessive whitespace while preserving paragraph breaks
        lines = text.split('\n')
        cleaned_lines = []
        prev_empty = False
        
        for line in lines:
            line = line.strip()
            
            # Skip multiple consecutive empty lines
            if not line:
                if not prev_empty:
                    cleaned_lines.append('')
                    prev_empty = True
            else:
                cleaned_lines.append(line)
                prev_empty = False
        
        text = '\n'.join(cleaned_lines)
        
        # Remove common encoding artifacts
        replacements = {
            '\x00': '',  # Null bytes
            '\ufeff': '',  # BOM
            '\x0c': '\n',  # Form feed to newline
            '^\x0b': '',  # Vertical tabs
        }
        
        for old, new in replacements.items():
            text = text.replace(old, new)
        
        # Fix hyphenated line breaks
        text = re.sub(r'-\n+', '', text)
        
        # Normalize spacing around punctuation
        text = re.sub(r'\s+([.,!?;:])', r'\1', text)
        text = re.sub(r'([.,!?;:])\s+', r'\1 ', text)
        
        # Remove extra spaces
        text = re.sub(r' +', ' ', text)
        
        return text.strip()
    
    def convert(self, pdf_path: str) -> Optional[str]:
        """
        Convert a PDF file to text
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Extracted and cleaned text, or None if conversion failed
        """
        pdf_path = Path(pdf_path)
        
        if not pdf_path.exists():
            print(f"Error: File not found: {pdf_path}")
            return None
        
        if not pdf_path.suffix.lower() == '.pdf':
            print(f"Error: Not a PDF file: {pdf_path}")
            return None
        
        try:
            if self.verbose:
                print(f"Opening: {pdf_path}")
            
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                
                if self.verbose:
                    print(f"Pages: {len(reader.pages)}")
                
                text = ""
                for page_num, page in enumerate(reader.pages):
                    if self.verbose:
                        print(f"Extracting page {page_num + 1}...", end=' ')
                    
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                    
                    if self.verbose:
                        print("✓")
            
            if not text.strip():
                print("Error: No text extracted from PDF")
                return None
            
            # Clean the extracted text
            cleaned = self.clean_text(text)
            
            if self.verbose:
                print(f"Extracted {len(cleaned)} characters")
            
            return cleaned
            
        except PyPDF2.errors.PdfReadError as e:
            print(f"Error: Failed to read PDF: {e}")
            return None
        except Exception as e:
            print(f"Error: {type(e).__name__}: {e}")
            return None
    
    def convert_batch(self, pdf_paths: List[str]) -> dict:
        """
        Convert multiple PDF files
        
        Args:
            pdf_paths: List of PDF file paths
            
        Returns:
            Dictionary with results {path: text}
        """
        results = {}
        for pdf_path in pdf_paths:
            text = self.convert(pdf_path)
            results[pdf_path] = text
        return results


def main():
    parser = argparse.ArgumentParser(
        description='Convert PDF files to clean text',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  pdf-to-text document.pdf
  pdf-to-text document.pdf -o output.txt
  pdf-to-text document.pdf -c
  pdf-to-text document.pdf -v
        """
    )
    
    parser.add_argument('pdf', help='PDF file to convert')
    parser.add_argument(
        '-o', '--output',
        help='Output file (default: stdout)'
    )
    parser.add_argument(
        '-c', '--copy',
        action='store_true',
        help='Copy output to clipboard'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Verbose output'
    )
    
    args = parser.parse_args()
    
    converter = PDFToTextConverter(verbose=args.verbose)
    text = converter.convert(args.pdf)
    
    if text is None:
        sys.exit(1)
    
    # Output the result
    if args.output:
        output_path = Path(args.output)
        output_path.write_text(text)
        print(f"✓ Saved to: {output_path}")
    else:
        print(text)
    
    # Copy to clipboard if requested
    if args.copy:
        try:
            import subprocess
            process = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
            process.communicate(text.encode('utf-8'))
            print("✓ Copied to clipboard")
        except Exception as e:
            print(f"Warning: Could not copy to clipboard: {e}")


if __name__ == '__main__':
    main()
