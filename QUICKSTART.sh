#!/bin/bash
# Quick Start Script for PDF to Text Converter
# Run this script for one-command setup

set -e

echo "🚀 PDF to Text Converter - Quick Setup"
echo "======================================"

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $PYTHON_VERSION"

# Create virtual environment
echo ""
echo "Setting up virtual environment..."
if [ -d "venv" ]; then
    echo "✓ Virtual environment already exists"
else
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
source venv/bin/activate
echo "✓ Virtual environment activated"

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo "✓ Dependencies installed"

# Test the installation
echo ""
echo "Testing installation..."
python3 pdf_to_text.py --help > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✓ Installation successful!"
else
    echo "✗ Installation test failed"
    exit 1
fi

echo ""
echo "✨ Setup Complete!"
echo ""
echo "Next steps:"
echo "1. Activate the environment: source venv/bin/activate"
echo "2. Convert a PDF: python3 pdf_to_text.py document.pdf -o output.txt"
echo "3. View help: python3 pdf_to_text.py --help"
echo ""
echo "For detailed usage, see USAGE_GUIDE.md"
