# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2026-02-24

### Added
- Initial release of PDF to Text Converter
- Core text extraction using pdfplumber
- Intelligent text cleaning (removes encoding artifacts, normalizes whitespace)
- CLI interface with single and batch processing
- Verbose mode for progress tracking
- Comprehensive documentation and usage guide
- Virtual environment setup with requirements.txt
- Python package configuration (setup.py)
- Error handling for corrupted pages and invalid PDFs
- Support for wildcard file patterns (*.pdf)
- Output to stdout or file
- Batch output to directory

### Features
- ✨ Clean text extraction from PDFs
- 🎯 Smart formatting and whitespace normalization
- 📦 Batch processing for multiple files
- 🛠️ Easy CLI interface
- ⚡ Robust error handling
- 📊 Verbose progress reporting

### Documentation
- README.md - Quick start and overview
- USAGE_GUIDE.md - Detailed workflows and examples
- setup.py - Package configuration
- requirements.txt - Dependency management

---

## Future Enhancements

Planned for future releases:

- [ ] OCR support for image-based PDFs
- [ ] Preserve complex formatting (tables, columns)
- [ ] Custom regex patterns for domain-specific cleaning
- [ ] Performance optimizations for batch jobs
- [ ] Progress bar for large conversions
- [ ] JSON output format option
- [ ] Streaming output for very large PDFs
- [ ] Configuration file support (.pdf2txt.conf)
- [ ] Parallel processing for multiple files
- [ ] Integration with cloud storage (S3, GCS)

---

**v1.0.0 released:** Tuesday, February 24th, 2026 @ 3:00 AM (Europe/London)
