#!/usr/bin/env python3
"""
PDF to Text Converter
A reliable tool for converting PDF documents to clean, readable text.
Built for Vishen's content analysis needs.

Created: February 13, 2026 at 3:00 AM GMT by Eliza
"""

import argparse
import os
import sys
from pathlib import Path
import re
import chardet

try:
    import PyPDF2
    from PyPDF2 import PdfReader
except ImportError:
    print("❌ PyPDF2 not found. Install with: pip install PyPDF2")
    sys.exit(1)

try:
    import pdfplumber
except ImportError:
    print("❌ pdfplumber not found. Install with: pip install pdfplumber")
    sys.exit(1)


class PDFConverter:
    def __init__(self):
        self.success_count = 0
        self.error_count = 0

    def clean_text(self, text):
        """Clean extracted text to remove artifacts and improve readability."""
        if not text:
            return ""
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Fix common encoding issues
        text = text.replace('\x00', '')  # Remove null bytes
        text = text.replace('\ufeff', '')  # Remove BOM
        text = text.replace('\u2019', "'")  # Smart apostrophes
        text = text.replace('\u2018', "'")  # Smart apostrophes
        text = text.replace('\u201c', '"')  # Smart quotes
        text = text.replace('\u201d', '"')  # Smart quotes
        text = text.replace('\u2013', '-')  # En dash
        text = text.replace('\u2014', '--')  # Em dash
        text = text.replace('\u2026', '...')  # Ellipsis
        
        # Remove page numbers and headers/footers (common patterns)
        lines = text.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            # Skip likely page numbers
            if re.match(r'^\d+$', line) and len(line) <= 3:
                continue
            # Skip very short lines that are likely artifacts
            if len(line) < 3:
                continue
            cleaned_lines.append(line)
        
        # Rejoin with proper spacing
        text = '\n'.join(cleaned_lines)
        
        # Final cleanup
        text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)  # Remove excessive newlines
        text = text.strip()
        
        return text

    def extract_with_pypdf2(self, pdf_path):
        """Extract text using PyPDF2 (primary method)."""
        try:
            with open(pdf_path, 'rb') as file:
                reader = PdfReader(file)
                text = ""
                
                for page_num, page in enumerate(reader.pages):
                    try:
                        page_text = page.extract_text()
                        if page_text:
                            text += f"\n--- Page {page_num + 1} ---\n"
                            text += page_text + "\n"
                    except Exception as e:
                        print(f"⚠️ Warning: Could not extract page {page_num + 1}: {e}")
                        continue
                
                return text
        except Exception as e:
            print(f"⚠️ PyPDF2 failed: {e}")
            return None

    def extract_with_pdfplumber(self, pdf_path):
        """Extract text using pdfplumber (fallback method)."""
        try:
            text = ""
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    try:
                        page_text = page.extract_text()
                        if page_text:
                            text += f"\n--- Page {page_num + 1} ---\n"
                            text += page_text + "\n"
                    except Exception as e:
                        print(f"⚠️ Warning: Could not extract page {page_num + 1}: {e}")
                        continue
            return text
        except Exception as e:
            print(f"⚠️ pdfplumber failed: {e}")
            return None

    def convert_pdf(self, pdf_path, output_path=None):
        """Convert PDF to text using multiple extraction methods."""
        if not os.path.exists(pdf_path):
            print(f"❌ Error: File not found: {pdf_path}")
            self.error_count += 1
            return False

        print(f"🔧 Converting: {pdf_path}")
        
        # Try PyPDF2 first
        text = self.extract_with_pypdf2(pdf_path)
        
        # Fall back to pdfplumber if PyPDF2 fails
        if not text or len(text.strip()) < 50:
            print("🔄 Trying fallback method (pdfplumber)...")
            text = self.extract_with_pdfplumber(pdf_path)
        
        if not text or len(text.strip()) < 10:
            print(f"❌ Error: No text could be extracted from {pdf_path}")
            self.error_count += 1
            return False

        # Clean the extracted text
        cleaned_text = self.clean_text(text)
        
        # Determine output path
        if not output_path:
            base_name = Path(pdf_path).stem
            output_path = f"{base_name}_converted.txt"

        # Write the cleaned text
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(f"# Converted from: {pdf_path}\n")
                f.write(f"# Conversion time: {os.system('date')}\n\n")
                f.write(cleaned_text)
            
            print(f"✅ Success: {output_path} ({len(cleaned_text):,} characters)")
            self.success_count += 1
            return True
            
        except Exception as e:
            print(f"❌ Error writing output file: {e}")
            self.error_count += 1
            return False

    def batch_convert(self, pattern):
        """Convert multiple PDFs matching a pattern."""
        import glob
        
        pdf_files = glob.glob(pattern)
        if not pdf_files:
            print(f"❌ No PDF files found matching: {pattern}")
            return
        
        print(f"🔧 Found {len(pdf_files)} PDF files to convert...")
        
        for pdf_file in pdf_files:
            self.convert_pdf(pdf_file)
        
        print(f"\n📊 Batch conversion complete:")
        print(f"   ✅ Success: {self.success_count}")
        print(f"   ❌ Errors: {self.error_count}")


def main():
    parser = argparse.ArgumentParser(description="Convert PDF documents to clean, readable text")
    parser.add_argument("input", help="Input PDF file or pattern for batch processing")
    parser.add_argument("-o", "--output", help="Output text file (default: input_converted.txt)")
    parser.add_argument("--batch", action="store_true", help="Process multiple files matching pattern")
    
    args = parser.parse_args()
    
    converter = PDFConverter()
    
    print("🔧 PDF to Text Converter")
    print("Built with ❤️ by Eliza at 3:00 AM for Vishen 💜\n")
    
    if args.batch:
        converter.batch_convert(args.input)
    else:
        converter.convert_pdf(args.input, args.output)


if __name__ == "__main__":
    main()