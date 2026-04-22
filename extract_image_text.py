#!/usr/bin/env python3
"""Thin compatibility wrapper for OCR text extraction."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from photo_ocr.cli import extract_text_main
from photo_ocr.extract import extract_text_from_images

if __name__ == "__main__":
    extract_text_main()


__all__ = ["extract_text_from_images"]
