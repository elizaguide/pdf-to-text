#!/usr/bin/env python3
"""Setup configuration for pdf-to-text package"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pdf-to-text",
    version="1.0.0",
    author="Vishen Lakhiani",
    author_email="vishen@mindvalley.com",
    description="Simple, reliable tool for converting PDFs to clean readable text",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/elizaguide/pdf-to-text",
    py_modules=["pdf_to_text"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pdfplumber>=0.9.0",
    ],
    entry_points={
        "console_scripts": [
            "pdf-to-text=pdf_to_text:main",
        ],
    },
)
