#!/usr/bin/env python3
"""
PDF to Text Converter
Simple, reliable tool for converting PDFs to readable text
"""

import sys
import os
import re
import argparse
from pathlib import Path
from typing import Optional

try:
    import pdfplumber
except ImportError:
    print("Error: pdfplumber not installed. Run: pip install pdfplumber")
    sys.exit(1)


class PDFToTextConverter:
    """Convert PDF files to clean text output"""
    
    def __init__(self, verbose=False):
        self.verbose = verbose
    
    def _clean_text(self, text: str) -> str:
        """Clean extracted text: remove artifacts, normalize whitespace"""
        # Remove encoding artifacts and control characters
        text = re.sub(r'[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F]', '', text)
        
        # Normalize multiple spaces to single space
        text = re.sub(r'[ \t]+', ' ', text)
        
        # Normalize multiple newlines to max 2
        text = re.sub(r'\n\n\n+', '\n\n', text)
        
        # Remove trailing whitespace on each line
        lines = [line.rstrip() for line in text.split('\n')]
        text = '\n'.join(lines)
        
        # Strip leading/trailing whitespace
        text = text.strip()
        
        return text
    
    def convert(self, pdf_path: str, output_path: Optional[str] = None) -> str:
        """
        Convert PDF to text
        
        Args:
            pdf_path: Path to PDF file
            output_path: Optional path to save output (if not provided, returns text)
            
        Returns:
            Extracted and cleaned text
        """
        pdf_path = Path(pdf_path)
        
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        if not pdf_path.suffix.lower() == '.pdf':
            raise ValueError(f"File is not a PDF: {pdf_path}")
        
        if self.verbose:
            print(f"📄 Processing: {pdf_path.name}")
        
        extracted_text = ""
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                if self.verbose:
                    print(f"   Pages: {len(pdf.pages)}")
                
                for i, page in enumerate(pdf.pages, 1):
                    if self.verbose:
                        print(f"   • Extracting page {i}...", end=' ', flush=True)
                    
                    try:
                        page_text = page.extract_text()
                        if page_text:
                            extracted_text += page_text + "\n\n"
                            if self.verbose:
                                print("✓")
                        else:
                            if self.verbose:
                                print("(empty)")
                    except Exception as e:
                        if self.verbose:
                            print(f"(error: {e})")
                        # Continue with next page even if one fails
                        continue
        
        except Exception as e:
            raise RuntimeError(f"Failed to read PDF: {e}")
        
        # Clean the extracted text
        cleaned_text = self._clean_text(extracted_text)
        
        if self.verbose:
            print(f"✨ Text extracted: {len(cleaned_text)} characters")
        
        # Save to file if output path provided
        if output_path:
            output_path = Path(output_path)
            output_path.write_text(cleaned_text, encoding='utf-8')
            if self.verbose:
                print(f"💾 Saved to: {output_path}")
        
        return cleaned_text


def main():
    """CLI interface"""
    parser = argparse.ArgumentParser(
        description='Convert PDF files to clean text',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  %(prog)s document.pdf                    # Output to stdout
  %(prog)s document.pdf -o output.txt      # Save to file
  %(prog)s document.pdf -o output.txt -v   # Verbose mode
  %(prog)s *.pdf -d output_folder          # Convert all PDFs in folder
        '''.strip()
    )
    
    parser.add_argument('pdf_files', nargs='+', help='PDF file(s) to convert')
    parser.add_argument('-o', '--output', help='Output text file (for single PDF)')
    parser.add_argument('-d', '--directory', help='Output directory (for multiple PDFs)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    converter = PDFToTextConverter(verbose=args.verbose)
    
    # Expand wildcards if present
    pdf_files = []
    for pattern in args.pdf_files:
        pdf_files.extend(Path('.').glob(pattern) if '*' in pattern else [Path(pattern)])
    
    pdf_files = list(set(pdf_files))  # Remove duplicates
    
    if not pdf_files:
        print("Error: No PDF files found")
        sys.exit(1)
    
    if len(pdf_files) > 1 and args.output:
        print("Error: Cannot use -o with multiple PDFs. Use -d for directory output instead.")
        sys.exit(1)
    
    failed = []
    succeeded = []
    
    for pdf_file in pdf_files:
        try:
            # Determine output file
            if args.directory:
                os.makedirs(args.directory, exist_ok=True)
                output_file = Path(args.directory) / f"{pdf_file.stem}.txt"
            elif args.output:
                output_file = args.output
            else:
                output_file = None
            
            text = converter.convert(str(pdf_file), str(output_file) if output_file else None)
            
            # If no output file specified, print to stdout
            if not output_file:
                print(text)
            
            succeeded.append(pdf_file.name)
        
        except Exception as e:
            print(f"❌ Error processing {pdf_file.name}: {e}", file=sys.stderr)
            failed.append((pdf_file.name, str(e)))
    
    # Summary
    if args.verbose and len(pdf_files) > 1:
        print(f"\n📊 Summary: {len(succeeded)} succeeded, {len(failed)} failed")
        if failed:
            for name, error in failed:
                print(f"   ❌ {name}: {error}")
    
    sys.exit(0 if not failed else 1)


if __name__ == '__main__':
    main()
