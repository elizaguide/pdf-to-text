# Setup & Deployment Guide

## Local Setup

The tool is ready to use locally. It's been created with all dependencies configured.

### Quick Start

```bash
cd /Users/vishen/tools/pdf-to-text

# Activate virtual environment
source venv/bin/activate

# Test the tool
python3 pdf_to_text.py --help
```

### Usage Examples

```bash
# Extract and display
python3 pdf_to_text.py document.pdf

# Save to file
python3 pdf_to_text.py document.pdf -o output.txt

# Verbose mode
python3 pdf_to_text.py document.pdf -v

# Copy to clipboard
python3 pdf_to_text.py document.pdf -c
```

## Deploying to GitHub

### Prerequisites

1. A GitHub account
2. Git installed locally (already done)
3. SSH key configured with GitHub

### Steps

1. **Create a new repository on GitHub**
   - Go to https://github.com/new
   - Name: `pdf-to-text`
   - Description: "Simple Python tool for converting PDFs to clean text"
   - Public repository (for sharing)
   - Skip initializing with README (we have one)

2. **Add the remote and push**

   ```bash
   cd /Users/vishen/tools/pdf-to-text
   git remote add origin https://github.com/vishen/pdf-to-text.git
   git branch -M main
   git push -u origin main
   ```

   Or with SSH (if configured):
   ```bash
   git remote add origin git@github.com:vishen/pdf-to-text.git
   git push -u origin main
   ```

3. **Verify**
   - Visit https://github.com/vishen/pdf-to-text
   - Should see all files and README

### Alternative: GitHub CLI

```bash
# If gh-cli is installed
cd /Users/vishen/tools/pdf-to-text
gh repo create pdf-to-text --public --source=. --push
```

## Installation for Users

Once on GitHub, users can install with:

```bash
# Clone
git clone https://github.com/vishen/pdf-to-text.git
cd pdf-to-text

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Use the tool
python pdf_to_text.py document.pdf
```

## Local Development

### Running Tests

```bash
# Create test directory
mkdir -p tests

# Add test cases (example)
cat > tests/test_basic.py << 'EOF'
import pytest
from pdf_to_text import PDFToTextConverter

def test_text_cleaning():
    converter = PDFToTextConverter()
    # Test text cleaning functionality
    pass
EOF

# Run tests
pytest tests/
```

### Making Updates

```bash
# Make code changes
# Test locally
python3 pdf_to_text.py test.pdf

# Commit changes
git add .
git commit -m "Description of changes"

# Push to GitHub
git push origin main
```

## Project Structure

```
pdf-to-text/
├── pdf_to_text.py      # Main converter module
├── pdf-to-text         # CLI wrapper script
├── requirements.txt    # Dependencies
├── README.md          # User documentation
├── SETUP.md           # This file
├── LICENSE            # MIT license
├── .gitignore         # Git ignore rules
└── venv/              # Virtual environment (local only)
```

## Troubleshooting

### PyPDF2 Not Found

```bash
source venv/bin/activate
pip install PyPDF2
```

### Git Remote Already Exists

```bash
git remote remove origin
git remote add origin https://github.com/vishen/pdf-to-text.git
```

### Permission Denied on pdf-to-text

```bash
chmod +x pdf-to-text
```

## Next Steps

1. Push to GitHub (see steps above)
2. Share the repository link
3. Consider adding CI/CD workflows (GitHub Actions)
4. Add more test cases
5. Consider adding OCR support for scanned PDFs

## Support

For issues or questions, open an issue on the GitHub repository.
