# Quick Start Guide

## Installation (1 minute)

```bash
# Install dependencies
pip3 install -r requirements.txt

# Make executable
chmod +x pdf_converter.py
```

## Your First Conversion

```bash
# Convert a PDF to text
python3 pdf_converter.py your_document.pdf

# Save to a file
python3 pdf_converter.py your_document.pdf -o output.txt

# See detailed processing
python3 pdf_converter.py your_document.pdf -v
```

## Common Use Cases

### Batch convert all PDFs in a folder
```bash
for pdf in *.pdf; do
  python3 pdf_converter.py "$pdf" -o "${pdf%.pdf}.txt"
done
```

### Extract specific text from a PDF
```bash
python3 pdf_converter.py report.pdf | grep "keyword"
```

### Get word count of extracted text
```bash
python3 pdf_converter.py document.pdf | wc -w
```

### Pipe to another tool
```bash
python3 pdf_converter.py document.pdf | less
```

## How It Works

1. **Tries pdfplumber first** - Better text layout handling
2. **Falls back to PyPDF2** - If pdfplumber unavailable
3. **Cleans the output** - Removes encoding artifacts and extra whitespace
4. **Saves or prints** - To file with `-o` or to stdout

## Troubleshooting

**Question:** What if some text is missing?
**Answer:** Some PDFs have complex layouts. Try with `-v` flag to see which extraction method worked.

**Question:** Can it handle scanned PDFs?
**Answer:** Only if they have OCR text layer. Image-only PDFs need OCR software (tesseract).

**Question:** How do I know it worked?
**Answer:** Run with `-v` (verbose) to see extraction progress. Check output for text content.

## Next Steps

- Read the full README.md for detailed documentation
- Check the source code in pdf_converter.py
- Review test_sample.pdf and test output
