#!/usr/bin/env python3
"""Thin compatibility wrapper for moving files to trash."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from photo_ocr.cli import move_to_trash_main
from photo_ocr.trash import move_paths_to_trash, validate_folder_name


if __name__ == "__main__":
    move_to_trash_main()


__all__ = ["move_paths_to_trash", "validate_folder_name"]
