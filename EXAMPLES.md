# PDF to Text Converter - Usage Examples

## Quick Start

### Basic Usage
```bash
# Convert single PDF
./convert-pdf document.pdf

# Convert with custom output name
./convert-pdf document.pdf -o clean_text.txt

# Batch convert all PDFs in current directory
./convert-pdf "*.pdf" --batch
```

### Advanced Usage
```bash
# Using Python directly (with virtual environment)
source venv/bin/activate
python pdf_converter.py document.pdf

# Help
./convert-pdf --help
```

## What It Handles

✅ **Multiple PDF formats** - Modern and legacy PDFs  
✅ **Encoding issues** - Fixes smart quotes, em dashes, etc.  
✅ **Page markers** - Adds "--- Page X ---" separators  
✅ **Clean output** - Removes artifacts and excessive whitespace  
✅ **Error recovery** - Falls back to alternative parser if needed  
✅ **Batch processing** - Handle multiple files at once  

## Output Format

```
# Converted from: document.pdf
# Conversion time: [timestamp]

--- Page 1 ---
Your clean, readable text starts here...

--- Page 2 ---
Continues with proper formatting...
```

## Common Use Cases

### 1. Content Analysis
```bash
# Convert analysis documents for AI processing
./convert-pdf strategy_analysis.pdf
# Creates: strategy_analysis_converted.txt
```

### 2. Batch Research
```bash
# Convert all research PDFs
./convert-pdf "research_*.pdf" --batch
```

### 3. Clean Archives
```bash
# Convert with descriptive names
./convert-pdf report.pdf -o "2026-02-13_quarterly-report.txt"
```

## Why This Tool?

Built specifically for Vishen's content analysis needs when standard PDF parsing failed. Handles encoding issues that break other tools and provides clean, AI-ready text output.

**Created at 3:00 AM GMT on February 13th, 2026 by Eliza** 💜