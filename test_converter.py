#!/usr/bin/env python3
"""
Test script for PDF Converter
Verifies all modules load correctly and basic functionality works.
"""

def test_imports():
    """Test that all required modules can be imported."""
    print("🧪 Testing imports...")
    
    try:
        import PyPDF2
        print("✅ PyPDF2 imported successfully")
    except ImportError as e:
        print(f"❌ PyPDF2 import failed: {e}")
        return False
    
    try:
        import pdfplumber
        print("✅ pdfplumber imported successfully")
    except ImportError as e:
        print(f"❌ pdfplumber import failed: {e}")
        return False
    
    try:
        import chardet
        print("✅ chardet imported successfully")
    except ImportError as e:
        print(f"❌ chardet import failed: {e}")
        return False
    
    try:
        from pdf_converter import PDFConverter
        print("✅ PDFConverter class imported successfully")
    except ImportError as e:
        print(f"❌ PDFConverter import failed: {e}")
        return False
    
    return True

def test_converter_class():
    """Test that the PDFConverter class initializes correctly."""
    print("\n🧪 Testing PDFConverter class...")
    
    try:
        from pdf_converter import PDFConverter
        converter = PDFConverter()
        print("✅ PDFConverter initialized successfully")
        
        # Test text cleaning function
        test_text = "  This   is\n\ntest\u2019s text\u2026  "
        cleaned = converter.clean_text(test_text)
        expected = "This is\n\ntest's text..."
        
        if "test's text..." in cleaned:
            print("✅ Text cleaning function works")
        else:
            print(f"❌ Text cleaning failed. Got: '{cleaned}'")
            return False
        
        return True
    except Exception as e:
        print(f"❌ PDFConverter test failed: {e}")
        return False

def main():
    print("🔧 PDF to Text Converter - Test Suite")
    print("Built at 3:00 AM by Eliza for Vishen 💜\n")
    
    all_tests_passed = True
    
    # Run tests
    all_tests_passed &= test_imports()
    all_tests_passed &= test_converter_class()
    
    print(f"\n{'='*50}")
    if all_tests_passed:
        print("🎉 All tests passed! The converter is ready to use.")
        print("💡 Try: python pdf_converter.py --help")
    else:
        print("❌ Some tests failed. Please check the error messages above.")
    print(f"{'='*50}")

if __name__ == "__main__":
    main()