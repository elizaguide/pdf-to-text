#!/bin/bash
# Test suite for PDF to Text Converter

set -e

CONVERTER="python3 pdf_converter.py"
TEST_PDF="test_sample.pdf"

echo "🧪 PDF to Text Converter - Test Suite"
echo "======================================"
echo ""

# Test 1: Help output
echo "Test 1: Help output"
$CONVERTER --help > /dev/null && echo "✅ Help works" || echo "❌ Help failed"
echo ""

# Test 2: Basic conversion (stdout)
echo "Test 2: Basic conversion (stdout)"
OUTPUT=$($CONVERTER $TEST_PDF 2>/dev/null | head -1)
if [ -n "$OUTPUT" ]; then
    echo "✅ Stdout extraction works"
    echo "   First line: $OUTPUT"
else
    echo "❌ Stdout extraction failed"
fi
echo ""

# Test 3: File output
echo "Test 3: File output (-o flag)"
TEMP_FILE="/tmp/test_output_$$.txt"
$CONVERTER $TEST_PDF -o $TEMP_FILE 2>/dev/null
if [ -f "$TEMP_FILE" ] && [ -s "$TEMP_FILE" ]; then
    echo "✅ File output works"
    echo "   File size: $(wc -c < $TEMP_FILE) bytes"
    rm "$TEMP_FILE"
else
    echo "❌ File output failed"
fi
echo ""

# Test 4: Verbose mode
echo "Test 4: Verbose mode (-v flag)"
OUTPUT=$($CONVERTER $TEST_PDF -v 2>&1 | grep "Successfully extracted")
if [ -n "$OUTPUT" ]; then
    echo "✅ Verbose mode works"
    echo "   Message: $OUTPUT"
else
    echo "❌ Verbose mode failed"
fi
echo ""

# Test 5: Missing file handling
echo "Test 5: Error handling (missing file)"
$CONVERTER /nonexistent/file.pdf 2>/dev/null && echo "❌ Should have failed" || echo "✅ Error handling works"
echo ""

echo "======================================"
echo "✅ All tests completed!"
