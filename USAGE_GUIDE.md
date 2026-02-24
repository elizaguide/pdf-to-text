# PDF to Text Converter - Usage Guide

Complete guide to using the PDF to Text Converter for various scenarios.

## Quick Start

### 1. Installation (First Time)

```bash
# Clone the repository
git clone https://github.com/elizaguide/pdf-to-text.git
cd pdf-to-text

# Set up virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Basic Conversion

```bash
# Activate virtual environment (if not already active)
source venv/bin/activate

# Convert single PDF and view on terminal
python3 pdf_to_text.py document.pdf

# Convert and save to file
python3 pdf_to_text.py document.pdf -o document.txt

# Convert with progress info
python3 pdf_to_text.py document.pdf -o document.txt -v
```

## Common Workflows

### Workflow 1: Convert Report and Analyze

```bash
# Extract text from report
python3 pdf_to_text.py quarterly_report.pdf -o report.txt -v

# Search for specific terms
grep "revenue" report.txt

# Count pages by blank lines
wc -l report.txt
```

### Workflow 2: Batch Convert Multiple Documents

```bash
# Create output directory
mkdir -p extracted_texts

# Convert all PDFs
python3 pdf_to_text.py *.pdf -d extracted_texts -v

# Verify results
ls -la extracted_texts/
wc -l extracted_texts/*.txt
```

### Workflow 3: Extract and Process with Python

```python
#!/usr/bin/env python3
import subprocess
import sys

# Convert PDF using the tool
result = subprocess.run([
    sys.executable, 'pdf_to_text.py',
    'data.pdf', '-o', 'data.txt'
], capture_output=True, text=True)

if result.returncode == 0:
    # Read the extracted text
    with open('data.txt', 'r') as f:
        text = f.read()
    
    # Process the text
    lines = text.split('\n')
    print(f"Document has {len(lines)} lines")
else:
    print("Conversion failed:", result.stderr)
```

### Workflow 4: Extract Text for AI/LLM Processing

```bash
# Convert PDF
python3 pdf_to_text.py document.pdf -o document.txt

# Now use with your AI pipeline
# Example: Feed to Claude API via file
cat document.txt | wc -c  # Check token count roughly
```

### Workflow 5: Archive Multiple PDFs as Text

```bash
# Create archive directory
mkdir -p ~/pdf_archive/extracted

# Convert everything with timestamps
python3 pdf_to_text.py ~/pdf_archive/*.pdf -d ~/pdf_archive/extracted -v

# Create index
ls -la ~/pdf_archive/extracted/ > ~/pdf_archive/INDEX.txt
echo "Archive created at $(date)" >> ~/pdf_archive/INDEX.txt
```

## Advanced Usage

### Custom Cleaning Pipeline

Extend the converter for domain-specific cleaning:

```python
from pdf_to_text import PDFToTextConverter

class CustomConverter(PDFToTextConverter):
    def _clean_text(self, text):
        # First apply standard cleaning
        text = super()._clean_text(text)
        
        # Add custom cleaning for your domain
        # Example: Remove URLs
        import re
        text = re.sub(r'https?://\S+', '', text)
        
        return text

# Use custom converter
converter = CustomConverter(verbose=True)
result = converter.convert('document.pdf', 'output.txt')
```

### Batch Processing with Status Tracking

```bash
#!/bin/bash
# Convert PDFs with detailed logging

source venv/bin/activate

LOG_FILE="conversion_log.txt"
echo "PDF Conversion Log - $(date)" > $LOG_FILE

for pdf in *.pdf; do
    echo "Processing: $pdf" | tee -a $LOG_FILE
    python3 pdf_to_text.py "$pdf" -o "${pdf%.pdf}.txt" -v >> $LOG_FILE 2>&1
    
    if [ $? -eq 0 ]; then
        echo "✓ Success: $pdf" >> $LOG_FILE
    else
        echo "✗ Failed: $pdf" >> $LOG_FILE
    fi
done

echo "Conversion complete. See $LOG_FILE for details"
```

### Pipeline: Convert → Search → Extract

```bash
#!/bin/bash
# Find all PDFs containing "executive summary", extract only those sections

SEARCH_TERM="executive summary"
OUTPUT_DIR="executive_summaries"
mkdir -p $OUTPUT_DIR

source venv/bin/activate

for pdf in *.pdf; do
    # Convert to text
    TEMP_TEXT=$(mktemp)
    python3 pdf_to_text.py "$pdf" -o "$TEMP_TEXT"
    
    # Check if contains search term
    if grep -qi "$SEARCH_TERM" "$TEMP_TEXT"; then
        # Extract section (example: 5 lines after match)
        grep -i -A5 "$SEARCH_TERM" "$TEMP_TEXT" > "$OUTPUT_DIR/${pdf%.pdf}_summary.txt"
        echo "✓ Extracted from: $pdf"
    fi
    
    rm "$TEMP_TEXT"
done
```

## Troubleshooting Guide

### Issue: "PDFs with scanned images don't extract text"

**Solution:** These are image-based PDFs. You need OCR:
```bash
# Install tesseract for OCR
brew install tesseract

# Use pytesseract with OCR
# (Not built into this tool, but available as extension)
```

### Issue: "Special characters look corrupted"

**Solution:** Check what's happening:
```bash
# Run with verbose to see details
python3 pdf_to_text.py document.pdf -v

# Check file encoding
file document.txt
hexdump -C document.txt | head -20
```

### Issue: "Conversion is very slow"

**Solution:** Large PDFs take time. Monitor progress:
```bash
# Use verbose to watch progress
python3 pdf_to_text.py large_document.pdf -o output.txt -v

# Or check in background
python3 pdf_to_text.py large_document.pdf -o output.txt &
watch -n 1 'wc -c output.txt'
```

### Issue: "Getting 'Cannot use -o with multiple PDFs' error"

**Solution:** Use directory output instead:
```bash
# ✗ Wrong - will error
python3 pdf_to_text.py *.pdf -o output.txt

# ✓ Correct - use directory
python3 pdf_to_text.py *.pdf -d output_folder
```

## Performance Tips

### For Large Batches

```bash
# Process in parallel (macOS/Linux)
ls *.pdf | xargs -P 4 -I {} python3 pdf_to_text.py {} -d output/

# Track progress
pv *.pdf | parallel python3 pdf_to_text.py
```

### For Memory Efficiency

The converter processes one page at a time, so even huge PDFs won't consume much RAM.

```bash
# Monitor memory while running
python3 pdf_to_text.py huge_document.pdf -o output.txt &
PID=$!
while kill -0 $PID 2>/dev/null; do
    ps aux | grep $PID | grep -v grep | awk '{print $6 " KB"}'
    sleep 1
done
```

## Integration Examples

### With Other Tools

```bash
# Extract and count words
python3 pdf_to_text.py document.pdf | wc -w

# Extract and find statistics
python3 pdf_to_text.py document.pdf | grep -o '\b\w\+\b' | sort | uniq -c | sort -rn | head -20

# Extract and send to analysis
python3 pdf_to_text.py document.pdf | your_analysis_script.py

# Extract to clipboard (macOS)
python3 pdf_to_text.py document.pdf | pbcopy
```

### In Shell Scripts

```bash
#!/bin/bash
# Automatic workflow

convert_pdf() {
    local pdf=$1
    local output=${pdf%.pdf}.txt
    
    echo "Converting $pdf..."
    python3 pdf_to_text.py "$pdf" -o "$output"
    
    if [ $? -eq 0 ]; then
        echo "✓ Converted to $output"
        return 0
    else
        echo "✗ Failed to convert $pdf"
        return 1
    fi
}

# Process all PDFs
for pdf in documents/*.pdf; do
    convert_pdf "$pdf"
done
```

## Getting Help

```bash
# View full help
python3 pdf_to_text.py --help

# Check version
python3 pdf_to_text.py --version 2>/dev/null || echo "Version: 1.0.0"

# Run a test
echo "Testing converter..."
python3 pdf_to_text.py -h > /dev/null && echo "✓ Tool is working"
```

---

**Questions?** Check the README.md or open an issue on GitHub.
