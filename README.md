# PDF to Text Converter

Simple, reliable tool for extracting clean text from PDF files. Handles multiple PDF formats, removes encoding artifacts, and produces formatted text output.

## Features

✅ **Clean Text Extraction** - Removes encoding artifacts, control characters, and formatting junk  
✅ **Multi-Page Support** - Handles PDFs with any number of pages  
✅ **Error Handling** - Graceful handling of corrupted or problematic PDFs  
✅ **CLI Interface** - Easy command-line use with flexible output options  
✅ **Verbose Mode** - Progress tracking for large PDF files  

## Installation

```bash
# Clone/download the tool
cd ~/.openclaw/tools/pdf-to-text

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Basic Usage

**Print extracted text to console:**
```bash
python pdf_to_text.py document.pdf
```

**Save to specific output file:**
```bash
python pdf_to_text.py document.pdf -o output.txt
```

**Auto-generate output filename (converts .pdf → .txt):**
```bash
python pdf_to_text.py document.pdf --auto-save
```

### Advanced Options

**Verbose mode with progress tracking:**
```bash
python pdf_to_text.py document.pdf -v
python pdf_to_text.py document.pdf -v -o output.txt
```

### Examples

```bash
# Extract and display (good for quick previews)
python pdf_to_text.py ~/Downloads/report.pdf

# Extract large PDF with progress tracking
python pdf_to_text.py ~/Documents/analysis.pdf -v --auto-save

# Save to specific location
python pdf_to_text.py research.pdf -o ~/Dropbox/research-text.txt

# Chain with other tools
python pdf_to_text.py document.pdf | grep "keyword"
```

## Text Cleaning

The converter automatically:

1. **Removes encoding artifacts** - Control characters, binary junk
2. **Normalizes whitespace** - Removes excessive blank lines while preserving paragraph structure
3. **Cleans formatting** - Strips extra spaces, fixes common OCR issues
4. **Preserves readability** - Maintains logical structure and paragraph breaks

## Output Format

- UTF-8 text encoding
- Paragraphs separated by blank lines
- No trailing whitespace
- Clean, readable formatting

## Error Handling

- ✅ Handles corrupted or malformed PDFs gracefully
- ✅ Skips problematic pages and continues
- ✅ Provides clear error messages
- ✅ Non-zero exit codes for failures

## API Usage (Python)

```python
from pdf_to_text import PDFToTextConverter

# Create converter
converter = PDFToTextConverter(verbose=True)

# Extract text (returns string)
text = converter.extract_text('document.pdf')

# Convert and save to file
output_path = converter.convert('document.pdf', 'output.txt')

# Or just print the text
print(converter.extract_text('document.pdf'))
```

## Command-Line Reference

```
usage: pdf_to_text.py [-h] [-o OUTPUT] [-v] [--auto-save] pdf_file

positional arguments:
  pdf_file              Path to PDF file

optional arguments:
  -h, --help            Show this help message
  -o, --output OUTPUT   Output text file path
  -v, --verbose         Verbose output with progress
  --auto-save           Auto-generate output filename (pdf → txt)
```

## Troubleshooting

**PyPDF2 not found:**
```bash
pip install PyPDF2
```

**Permission denied on output:**
```bash
# Check file permissions or try different location
chmod u+w ~/path/to/output/
```

**PDF won't extract:**
- Try verbose mode to see which pages fail: `python pdf_to_text.py -v`
- Some encrypted PDFs may not extract; consider using `pdfrw` or other tools
- Scanned PDFs (image-based) won't work with text extraction; use OCR tool instead

## Performance

- **Small PDFs (< 10 pages):** Instant
- **Medium PDFs (10-100 pages):** < 1 second
- **Large PDFs (> 100 pages):** 1-5 seconds depending on content density

Use `--verbose` mode to monitor progress on large files.

## License

Public tool for Eliza's document analysis pipeline.

---

**Built:** March 1, 2026 | **For:** PDF analysis and text extraction  
**Tested with:** PyPDF2 4.0+  
**Python version:** 3.8+
