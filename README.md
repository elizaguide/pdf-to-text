# PDF to Text Converter

Simple, reliable tool for converting PDF files to clean, readable text. Perfect for extracting content from PDFs for analysis, processing, and archival.

## Features

✨ **Clean Text Extraction** - Removes encoding artifacts, normalizes whitespace, handles multiple page formats
🎯 **Smart Formatting** - Preserves document structure while cleaning up PDF encoding noise
📦 **Batch Processing** - Convert single or multiple PDFs efficiently
🛠️ **CLI Interface** - Easy to use from command line or scripts
⚡ **Robust Error Handling** - Gracefully handles corrupted pages and edge cases
📊 **Verbose Mode** - Detailed output for debugging and monitoring

## Installation

```bash
# Clone the repository
git clone https://github.com/elizaguide/pdf-to-text.git
cd pdf-to-text

# Install dependencies
pip install -r requirements.txt

# Make script executable
chmod +x pdf_to_text.py
```

## Usage

### Basic Usage

Convert a single PDF to stdout:
```bash
python3 pdf_to_text.py document.pdf
```

Save to a text file:
```bash
python3 pdf_to_text.py document.pdf -o output.txt
```

### Batch Processing

Convert multiple PDFs to a directory:
```bash
python3 pdf_to_text.py *.pdf -d output_folder
```

Convert specific PDFs:
```bash
python3 pdf_to_text.py file1.pdf file2.pdf file3.pdf -d output_folder
```

### Verbose Mode

Get detailed output during processing:
```bash
python3 pdf_to_text.py document.pdf -o output.txt -v
```

Output example:
```
📄 Processing: document.pdf
   Pages: 12
   • Extracting page 1... ✓
   • Extracting page 2... ✓
   • Extracting page 3... ✓
   ...
✨ Text extracted: 45,823 characters
💾 Saved to: output.txt
```

## Command-line Options

```
usage: pdf_to_text.py [-h] [-o OUTPUT] [-d DIRECTORY] [-v] pdf_files [pdf_files ...]

positional arguments:
  pdf_files             PDF file(s) to convert

options:
  -h, --help            Show help message
  -o, --output FILE     Output text file (for single PDF)
  -d, --directory DIR   Output directory (for multiple PDFs)
  -v, --verbose         Verbose output with progress details
```

## Examples

### Example 1: Simple conversion
```bash
python3 pdf_to_text.py report.pdf
```
Prints extracted text to terminal.

### Example 2: Save to file
```bash
python3 pdf_to_text.py report.pdf -o report.txt
```
Saves cleaned text to `report.txt`.

### Example 3: Batch with progress
```bash
python3 pdf_to_text.py *.pdf -d ./texts -v
```
Converts all PDFs in current folder to individual `.txt` files in `texts/` directory with progress output.

### Example 4: Pipe to other tools
```bash
python3 pdf_to_text.py document.pdf | grep "keyword"
```
Search for specific text in extracted content.

## Text Cleaning

The converter automatically:

1. **Removes encoding artifacts** - Strips control characters and invalid UTF-8 sequences
2. **Normalizes whitespace** - Converts multiple spaces/tabs to single spaces
3. **Fixes line breaks** - Removes excessive blank lines while preserving paragraph structure
4. **Strips trailing spaces** - Cleans up line endings
5. **Preserves structure** - Maintains paragraph breaks and document flow

## Technical Details

### Dependencies

- **pdfplumber** (≥0.9.0) - Advanced PDF text extraction with layout preservation

### Error Handling

- Corrupted or unreadable PDF pages are skipped with a warning (process continues)
- File validation checks for existence and `.pdf` extension
- Detailed error messages for troubleshooting

### Performance

- Single PDF conversion: Typically < 1 second per page
- Batch processing: Efficient sequential processing
- Memory efficient: Processes pages individually, not loading entire PDF into memory

## Use Cases

📄 **Document Analysis** - Extract text from reports for analysis
🔍 **Data Processing** - Prepare PDF content for NLP or text processing
📚 **Archival** - Convert PDF libraries to searchable text archives
🤖 **AI/ML Pipelines** - Generate clean text datasets from PDF sources
📊 **Content Migration** - Extract content for system migration

## Troubleshooting

### "ModuleNotFoundError: No module named 'pdfplumber'"
```bash
pip install pdfplumber
```

### PDF returns empty or little text
- PDFs with image-based text (scanned documents) won't extract text. Consider OCR tools.
- Some PDFs have copy-protection. Try another extraction tool or contact the publisher.

### Special characters appear corrupted
- Run with verbose mode to check: `python3 pdf_to_text.py file.pdf -v`
- The converter should handle most UTF-8 encoding issues automatically
- If issues persist, the PDF may have non-standard encoding

### "Cannot use -o with multiple PDFs"
- Use `-d directory` flag instead of `-o file` when processing multiple PDFs
- Example: `python3 pdf_to_text.py *.pdf -d output/`

## Development

### Running Tests

```bash
python3 pdf_to_text.py test_files/*.pdf -d test_output -v
```

### Code Structure

```
pdf_to_text.py          # Main converter module
├── PDFToTextConverter  # Core converter class
├── _clean_text()       # Text cleaning logic
├── convert()           # Main conversion method
└── main()              # CLI interface
```

### Extending

To add custom cleaning logic, modify the `_clean_text()` method in the `PDFToTextConverter` class.

## Contributing

Contributions welcome! Areas for enhancement:

- OCR support for image-based PDFs
- Preserve more complex formatting (tables, columns)
- Custom regex patterns for domain-specific cleaning
- Performance optimizations for large batch jobs

## License

MIT License - Use freely in personal and commercial projects

## Support

For issues, feature requests, or questions:
- Open an issue on GitHub
- Check the troubleshooting section above

---

**Built with 💜 for Vishen**

Simple tools for complex problems.
