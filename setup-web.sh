#!/bin/bash

# PDF to Text Converter - Web Server Setup
# Simple one-command setup for the web interface

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

echo "🚀 Setting up PDF to Text Web Server..."
echo ""

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first:"
    echo "   https://nodejs.org/"
    exit 1
fi

echo "✅ Node.js found: $(node --version)"

# Install Node dependencies
echo ""
echo "📦 Installing Node.js dependencies..."
npm install

# Check Python environment
echo ""
echo "🐍 Checking Python environment..."
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -q -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 To start the web server, run:"
echo "   npm start"
echo ""
echo "Then open your browser to:"
echo "   http://localhost:3000"
echo ""
