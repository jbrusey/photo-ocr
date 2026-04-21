#!/usr/bin/env python3
"""Thin compatibility wrapper for filename/path correction."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from photo_ocr.cli import check_filenames_main
from photo_ocr.match_paths import build_available_paths, find_fuzzy_match


if __name__ == "__main__":
    check_filenames_main()


__all__ = ["build_available_paths", "find_fuzzy_match"]
