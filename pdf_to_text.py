#!/usr/bin/env python3
"""
PDF to Text Converter - Clean, simple text extraction from PDF files
Handles multiple PDF formats and cleans output formatting
"""

import sys
import os
import re
import argparse
from pathlib import Path

try:
    import PyPDF2
except ImportError:
    print("Error: PyPDF2 not installed. Install with: pip install PyPDF2")
    sys.exit(1)


class PDFToTextConverter:
    """Convert PDF files to clean text output"""

    def __init__(self, verbose=False):
        self.verbose = verbose

    def clean_text(self, text):
        """Clean extracted text: remove encoding artifacts, extra whitespace"""
        # Remove control characters and encoding artifacts
        text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', text)
        
        # Remove excessive whitespace while preserving paragraph structure
        lines = text.split('\n')
        cleaned_lines = []
        
        for line in lines:
            # Strip leading/trailing whitespace from each line
            cleaned_line = line.strip()
            
            # Skip completely empty lines, but preserve single empty lines as paragraph breaks
            if cleaned_line or (cleaned_lines and cleaned_lines[-1] != ''):
                cleaned_lines.append(cleaned_line)
        
        # Join with single newlines
        text = '\n'.join(cleaned_lines)
        
        # Remove multiple consecutive blank lines (reduce to max 2)
        text = re.sub(r'\n\n\n+', '\n\n', text)
        
        # Fix common OCR artifacts
        text = re.sub(r'([a-z])\s+([a-z])\s+([a-z])', r'\1 \2 \3', text)
        
        return text.strip()

    def extract_text(self, pdf_path):
        """Extract text from PDF file"""
        try:
            if self.verbose:
                print(f"📖 Opening PDF: {pdf_path}")
            
            pdf_path = Path(pdf_path)
            if not pdf_path.exists():
                raise FileNotFoundError(f"PDF file not found: {pdf_path}")
            
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                num_pages = len(pdf_reader.pages)
                
                if self.verbose:
                    print(f"📄 Found {num_pages} page(s)")
                
                full_text = []
                
                for page_num, page in enumerate(pdf_reader.pages, 1):
                    try:
                        if self.verbose:
                            print(f"   Extracting page {page_num}/{num_pages}...", end='\r')
                        
                        text = page.extract_text()
                        if text:
                            full_text.append(text)
                    except Exception as e:
                        if self.verbose:
                            print(f"   ⚠️  Warning on page {page_num}: {str(e)}")
                        continue
                
                if self.verbose:
                    print(f"\n✅ Successfully extracted {num_pages} page(s)")
                
                # Combine all text
                combined_text = '\n\n'.join(full_text)
                
                # Clean the output
                cleaned_text = self.clean_text(combined_text)
                
                return cleaned_text
        
        except Exception as e:
            raise Exception(f"Error processing PDF: {str(e)}")

    def convert(self, pdf_path, output_path=None):
        """Convert PDF to text and optionally save to file"""
        try:
            text = self.extract_text(pdf_path)
            
            if output_path:
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(text)
                if self.verbose:
                    print(f"💾 Saved to: {output_path}")
                return output_path
            else:
                return text
        
        except Exception as e:
            print(f"❌ Error: {str(e)}", file=sys.stderr)
            sys.exit(1)


def main():
    """CLI interface"""
    parser = argparse.ArgumentParser(
        description='Convert PDF files to clean text',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Extract and print to console
  python pdf_to_text.py document.pdf
  
  # Extract and save to file
  python pdf_to_text.py document.pdf -o document.txt
  
  # Verbose mode with progress
  python pdf_to_text.py document.pdf -v
  
  # Save with auto-generated filename
  python pdf_to_text.py document.pdf --auto-save
        '''
    )
    
    parser.add_argument('pdf_file', help='Path to PDF file')
    parser.add_argument('-o', '--output', help='Output text file path')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output with progress')
    parser.add_argument('--auto-save', action='store_true', help='Auto-generate output filename (pdf → txt)')
    
    args = parser.parse_args()
    
    # Determine output path
    output_path = None
    if args.auto_save:
        pdf_path = Path(args.pdf_file)
        output_path = pdf_path.with_suffix('.txt')
    elif args.output:
        output_path = args.output
    
    # Convert
    converter = PDFToTextConverter(verbose=args.verbose)
    result = converter.convert(args.pdf_file, output_path)
    
    # Print result if no output file specified
    if not output_path:
        print(result)


if __name__ == '__main__':
    main()
