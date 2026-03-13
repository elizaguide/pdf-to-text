# PDF to Text Converter

Simple, reliable tool for converting PDFs to clean, readable text. Perfect for document analysis, content extraction, and preparing PDFs for LLM processing.

## Features

- ✅ **Dual-engine extraction** - Uses pdfplumber (preferred) with PyPDF2 fallback
- ✅ **Clean output** - Removes encoding artifacts, extra whitespace, and control characters
- ✅ **Error handling** - Graceful failures with helpful error messages
- ✅ **Verbose mode** - See extraction progress and methods used
- ✅ **Flexible output** - Write to file or stdout
- ✅ **Cross-platform** - Works on macOS, Linux, Windows

## Installation

### 1. Install dependencies

```bash
pip install pdfplumber PyPDF2
```

### 2. Make the script executable

```bash
chmod +x pdf_converter.py
```

## Usage

### Basic usage (output to stdout)

```bash
python pdf_converter.py document.pdf
```

### Save to file

```bash
python pdf_converter.py input.pdf -o output.txt
```

### Verbose mode (see processing details)

```bash
python pdf_converter.py report.pdf -v
python pdf_converter.py report.pdf -o output.txt -v
```

## Examples

### Extract PDF and view in terminal
```bash
python pdf_converter.py /path/to/file.pdf | less
```

### Convert batch of PDFs
```bash
for pdf in *.pdf; do
  python pdf_converter.py "$pdf" -o "${pdf%.pdf}.txt"
done
```

### Use with analysis tools
```bash
# Extract text and pipe to other commands
python pdf_converter.py document.pdf | grep "keyword" | head -20

# Get word count of extracted text
python pdf_converter.py document.pdf | wc -w
```

## How It Works

1. **Detection** - Checks for available PDF libraries
2. **Extraction** - Uses pdfplumber (better) or PyPDF2 (fallback)
3. **Cleaning** - Removes encoding artifacts and normalizes whitespace
4. **Output** - Writes to file or stdout

### Text Cleaning Steps

- Removes form feeds and control characters
- Strips encoding artifacts (Â, â, etc.)
- Normalizes whitespace while preserving structure
- Removes multiple consecutive blank lines
- Preserves indentation and formatting intent

## Supported PDF Types

- ✅ Text-based PDFs (extraction-friendly)
- ✅ Scanned PDFs with OCR text layer
- ⚠️ Image-only PDFs (no text layer) - Cannot extract without OCR

## Troubleshooting

### "No PDF library available"
```bash
pip install pdfplumber PyPDF2
```

### Garbled output
- Try with `-v` flag to see which extraction method was used
- Some PDFs may have encoding issues; check the source PDF
- For scanned PDFs, you may need OCR (use `pytesseract` + tesseract)

### Incomplete text extraction
- Some PDFs use special encoding that's hard to extract
- Try both methods: `pdfplumber` typically works better
- For complex layouts, consider PDFMiner or other specialized tools

## Technical Details

### Extraction Methods

**pdfplumber** (preferred)
- Better text layout preservation
- Handles complex PDFs well
- Accurate page-by-page extraction

**PyPDF2** (fallback)
- Simpler, more lightweight
- Used if pdfplumber is unavailable
- Good for straightforward text PDFs

## License

MIT - Feel free to use, modify, and distribute.

## Author

Built with ❤️ for Vishen | March 2026
