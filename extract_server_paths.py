#!/usr/bin/env python3
"""Thin compatibility wrapper that runs OCR + path extraction in one command."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from photo_ocr.cli import extract_server_paths_main
from photo_ocr.extract import extract_text_from_images
from photo_ocr.match_paths import extract_paths_from_text, extract_server_paths_from_rows


def extract_server_paths(
    download_folder: Path, img_pattern: str = "IMG_*"
) -> list[str]:
    rows = extract_text_from_images(download_folder, img_pattern=img_pattern)
    return extract_server_paths_from_rows(rows)


if __name__ == "__main__":
    extract_server_paths_main()


__all__ = ["extract_paths_from_text", "extract_server_paths"]
