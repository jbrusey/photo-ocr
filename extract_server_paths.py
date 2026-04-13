#!/usr/bin/env python3
"""Extract server paths from images in Downloads folder.

Usage:
    python extract_server_paths.py --download-folder \
        ~/Downloads/images-to-delete --output-csv server_paths.csv
"""

import argparse
import re
from pathlib import Path

import pytesseract
from PIL import Image

PATH_RE = re.compile(
    r"/(?:19|20)\d{2}/[A-Za-z0-9._/-]*?\.(?:heic|jpe?g)",
    re.IGNORECASE,
)
TRAILING_ALPHA_BEFORE_EXT_RE = re.compile(
    r"(?<=\d)[A-Za-z](?=\.(?:heic|jpe?g)$)",
    re.IGNORECASE,
)


def _normalize_extracted_path(path: str) -> str:
    """Normalize OCR path artifacts while preserving expected server format."""
    return TRAILING_ALPHA_BEFORE_EXT_RE.sub("", path)


def extract_text_from_images(
    download_folder: Path, img_pattern: str = "IMG_*"
) -> list[str]:
    """Run OCR for each matching image and return raw text blobs."""
    if not download_folder.is_dir():
        raise FileNotFoundError(
            f"download_folder does not exist or is not a directory: {download_folder}"
        )

    texts: list[str] = []
    for file in sorted(download_folder.glob(img_pattern)):
        with Image.open(file) as img:
            texts.append(pytesseract.image_to_string(img))

    return texts


def extract_paths_from_text(text: str) -> list[str]:
    """Extract canonical server paths from a single OCR text blob."""
    candidates: list[str] = []

    # Pass 1: normal OCR text (works when path appears on one line).
    candidates.extend(match.group(0) for match in PATH_RE.finditer(text))

    # Pass 2: collapsed whitespace for OCR that splits paths across lines/spaces.
    compact_text = "".join(text.split())
    candidates.extend(match.group(0) for match in PATH_RE.finditer(compact_text))

    normalized_paths: list[str] = []
    seen_paths: set[str] = set()
    for candidate in candidates:
        normalized = _normalize_extracted_path(candidate)
        if normalized not in seen_paths:
            normalized_paths.append(normalized)
            seen_paths.add(normalized)

    return normalized_paths


def extract_server_paths(
    download_folder: Path, img_pattern: str = "IMG_*"
) -> list[str]:
    texts = extract_text_from_images(download_folder, img_pattern=img_pattern)

    server_paths: list[str] = []
    seen_paths: set[str] = set()
    for text in texts:
        for path in extract_paths_from_text(text):
            if path not in seen_paths:
                server_paths.append(path)
                seen_paths.add(path)

    return server_paths


def main():
    import pandas as pd

    parser = argparse.ArgumentParser(description="Extract server paths from images")
    parser.add_argument(
        "--download-folder",
        type=Path,
        required=True,
        help="Folder containing images to scan (default: ~/Downloads/images-to-delete)",
    )
    parser.add_argument(
        "--output-csv", type=Path, required=True, help="Output CSV file path"
    )
    parser.add_argument(
        "--img-pattern",
        type=str,
        default="IMG_*",
        help="Glob pattern for image files (default: IMG_*)",
    )

    args = parser.parse_args()

    download_folder = args.download_folder.expanduser().resolve()
    output_csv = args.output_csv.expanduser().resolve()

    server_paths = extract_server_paths(download_folder, img_pattern=args.img_pattern)

    for path in server_paths:
        print(path)

    pd.DataFrame(server_paths, columns=["server_path"]).to_csv(output_csv, index=False)


if __name__ == "__main__":
    main()
