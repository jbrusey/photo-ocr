#!/usr/bin/env python3
"""Thin compatibility wrapper for server path extraction from OCR text."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from photo_ocr.cli import extract_paths_main
from photo_ocr.match_paths import (
    extract_paths_from_text,
    extract_server_paths_from_csv,
    extract_server_paths_from_rows,
)


if __name__ == "__main__":
    extract_paths_main()


__all__ = [
    "extract_paths_from_text",
    "extract_server_paths_from_rows",
    "extract_server_paths_from_csv",
]
