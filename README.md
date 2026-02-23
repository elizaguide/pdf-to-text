# PDF to Text Converter

A simple, reliable Python tool for converting PDF files to clean, readable text. Handles encoding artifacts, formatting issues, and multiple PDF formats.

## Features

✅ **Clean Text Extraction** - Removes encoding artifacts and formatting noise
✅ **Multiple Output Modes** - stdout, file, or clipboard
✅ **Batch Processing** - Convert multiple PDFs programmatically  
✅ **Verbose Mode** - Track conversion progress with detailed output
✅ **Error Handling** - Graceful handling of corrupted PDFs and edge cases
✅ **Simple API** - Easy to use from command line or Python code

## Installation

```bash
# Clone the repository
git clone https://github.com/vishen/pdf-to-text.git
cd pdf-to-text

# Install dependencies
pip install -r requirements.txt

# Make CLI executable
chmod +x pdf-to-text
```

## Quick Start

### Command Line

```bash
# Extract text to stdout
python pdf_to_text.py document.pdf

# Save to file
python pdf_to_text.py document.pdf -o output.txt

# Copy to clipboard
python pdf_to_text.py document.pdf -c

# Verbose mode (show progress)
python pdf_to_text.py document.pdf -v

# Using the CLI wrapper
./pdf-to-text document.pdf -o output.txt
```

### Python Code

```python
from pdf_to_text import PDFToTextConverter

# Create converter
converter = PDFToTextConverter(verbose=True)

# Convert single PDF
text = converter.convert('document.pdf')
print(text)

# Convert multiple PDFs
results = converter.convert_batch(['doc1.pdf', 'doc2.pdf', 'doc3.pdf'])
for path, text in results.items():
    print(f"{path}: {len(text)} characters extracted")
```

## Command Line Options

| Option | Short | Description |
|--------|-------|-------------|
| `pdf` | - | PDF file to convert (required) |
| `--output` | `-o` | Save output to file instead of stdout |
| `--copy` | `-c` | Copy output text to clipboard |
| `--verbose` | `-v` | Show detailed conversion progress |

## Examples

```bash
# Extract and display
python pdf_to_text.py research.pdf

# Save to specific location
python pdf_to_text.py report.pdf -o data/extracted.txt

# Quick clipboard copy for analysis
python pdf_to_text.py analysis.pdf -c

# See detailed extraction progress
python pdf_to_text.py document.pdf -v -o output.txt
```

## How It Works

1. **Reads the PDF** using PyPDF2
2. **Extracts text** from each page
3. **Cleans the text**:
   - Removes encoding artifacts (null bytes, BOM, etc.)
   - Fixes hyphenated line breaks
   - Normalizes whitespace
   - Removes excessive blank lines
   - Fixes spacing around punctuation
4. **Outputs result** in your requested format

## Supported PDF Formats

- Standard PDF documents
- PDFs with text layers (not image-only scans)
- Multi-page documents
- PDFs with different encodings

## Limitations

- **Image-only PDFs**: Cannot extract text from scanned PDFs without OCR
- **Encrypted PDFs**: Requires password (not yet implemented)
- **Complex layouts**: May not preserve exact formatting

## Error Handling

The tool gracefully handles:
- Missing files
- Non-PDF files
- Corrupted PDF files
- PDFs with no extractable text
- Permission errors

All errors are reported clearly with helpful messages.

## Requirements

- Python 3.7+
- PyPDF2 3.0.0+

## Development

### Running Tests

```bash
python -m pytest tests/
```

### Adding Features

The `PDFToTextConverter` class is designed for extension:

```python
class CustomConverter(PDFToTextConverter):
    def clean_text(self, text: str) -> str:
        # Override cleaning logic
        return super().clean_text(text)
```

## License

MIT License - See LICENSE file for details

## Support

For issues, feature requests, or questions:
- Open an issue on GitHub
- Check existing issues for solutions

## Changelog

### v1.0.0 (Feb 23, 2026)
- Initial release
- PDF extraction with text cleaning
- CLI interface with multiple output modes
- Batch processing support
- Encoding artifact removal
