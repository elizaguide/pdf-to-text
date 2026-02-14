# PDF to Text Converter

A robust, reliable PDF parser that handles encoding artifacts and multiple PDF formats. Built specifically to solve PDF parsing issues encountered with complex documents.

## ✨ Features

- **Dual parsing engines**: Uses both pdfplumber and PyPDF2 for maximum compatibility
- **Encoding artifact cleanup**: Automatically removes common PDF encoding issues
- **Batch processing**: Handle multiple files at once
- **Flexible output**: Save to file or output to stdout
- **Error handling**: Graceful fallbacks when one parsing method fails
- **CLI interface**: Simple command-line usage

## 🚀 Quick Start

```bash
# Convert PDF to text (output to console)
./convert-pdf your-document.pdf

# Save to file
./convert-pdf your-document.pdf -o output.txt

# Process multiple files
./convert-pdf *.pdf --batch

# Verbose mode for debugging
./convert-pdf document.pdf --verbose
```

## 📦 Installation

The project comes with a virtual environment already set up:

```bash
cd /Users/vishen/clawd/pdf-to-text
source venv/bin/activate
pip install -r requirements.txt
```

## 💡 Usage Examples

### Basic Usage
```bash
# Simple conversion
./convert-pdf report.pdf

# Save to specific file
./convert-pdf analysis.pdf -o clean_analysis.txt
```

### Batch Processing
```bash
# Convert all PDFs in current directory
./convert-pdf *.pdf --batch

# This creates .txt files for each PDF:
# document1.pdf -> document1.txt
# report.pdf -> report.txt
```

### Advanced Options
```bash
# Keep original encoding (skip cleanup)
./convert-pdf document.pdf --no-cleanup

# Verbose output for debugging
./convert-pdf problematic.pdf --verbose

# Combine options
./convert-pdf *.pdf --batch --verbose
```

## 🔧 How It Works

The converter uses a two-stage approach:

1. **Primary extraction**: Attempts extraction with `pdfplumber` (excellent for complex layouts)
2. **Fallback extraction**: If primary fails, uses `PyPDF2` as backup
3. **Encoding cleanup**: Removes common PDF artifacts like:
   - Replacement characters (ï¿½)
   - Smart quotes (â€œ, â€)
   - Encoding artifacts (Â, Ã©)
   - Control characters
   - Normalized whitespace

## 📋 Command Line Reference

```
python3 pdf_converter.py [-h] [-o OUTPUT] [--no-cleanup] [--batch] [--verbose] input [input ...]

Options:
  input               PDF file(s) to convert
  -o OUTPUT          Output file (default: stdout or auto-generated)
  --no-cleanup       Skip encoding artifact cleanup
  --batch            Process multiple files, auto-generate output names
  --verbose          Enable verbose output
  -h, --help         Show help message
```

## 🛠 Technical Details

### Dependencies
- **PyPDF2**: Fast, lightweight PDF parsing
- **pdfplumber**: Advanced text extraction with layout awareness
- **Python 3.7+**: Modern Python features

### Error Handling
- Graceful fallbacks between parsing engines
- Page-level error recovery (skips problematic pages)
- Clear error messages for debugging

### Performance
- Efficient memory usage for large documents
- Parallel processing ready (for future enhancement)
- Minimal external dependencies

## 🎯 Use Cases

Perfect for:
- **Document analysis**: Clean text extraction for AI processing
- **Content migration**: Converting PDF archives to searchable text
- **Data extraction**: Pulling content from PDF reports
- **Accessibility**: Creating text versions of PDF documents

## 🔍 Troubleshooting

### Common Issues

**No text extracted:**
- PDF might be image-based (scanned document)
- Try `--verbose` flag to see detailed error messages
- Consider using OCR for scanned PDFs

**Encoding artifacts remain:**
- Some artifacts might be document-specific
- Try `--no-cleanup` to see original text
- Report specific artifacts for improvement

**File not found:**
- Check file path and permissions
- Ensure file has .pdf extension

### Getting Help
```bash
./convert-pdf --help
python3 pdf_converter.py --help
```

## 📈 Examples Output

**Before (with artifacts):**
```
This is a test documentÂ with encodingÂ issues. Itâ€™s importantÂ to clean these up.
```

**After (cleaned):**
```
This is a test document with encoding issues. It's important to clean these up.
```

## 🚨 Known Limitations

- **Scanned PDFs**: Cannot extract text from image-based PDFs (requires OCR)
- **Complex layouts**: Some advanced formatting might be lost
- **Encrypted PDFs**: Password-protected files need manual unlock
- **Large files**: Memory usage scales with document size

## 📊 Development Notes

Built by Eliza for Vishen Lakhiani on February 14th, 2026 at 3:00 AM GMT.

**Design goals:**
- Solve encoding artifact issues encountered in PDF analysis
- Simple, reliable tool for daily use
- Robust error handling for production use
- Extensible architecture for future enhancements

---

## 📝 License

Built for Vishen Lakhiani's personal use. Modify and distribute as needed.