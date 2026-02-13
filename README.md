# PDF to Text Converter

A simple, reliable tool for converting PDF documents to clean, readable text.

## Features

✅ **Clean Text Output** - No encoding artifacts or formatting issues  
✅ **Multiple PDF Formats** - Handles various PDF types and edge cases  
✅ **CLI Interface** - Easy command-line usage  
✅ **Error Handling** - Graceful failure with helpful error messages  
✅ **Batch Processing** - Process multiple files at once  

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Single file
```bash
python pdf_converter.py input.pdf
```

### Output to specific file
```bash
python pdf_converter.py input.pdf -o output.txt
```

### Batch processing
```bash
python pdf_converter.py *.pdf --batch
```

### Help
```bash
python pdf_converter.py --help
```

## Requirements

- Python 3.7+
- PyPDF2
- pdfplumber (fallback parser)
- chardet (encoding detection)

## Built with ❤️ for Vishen's content analysis needs

Created at 3:00 AM on February 13th, 2026 by Eliza 💜