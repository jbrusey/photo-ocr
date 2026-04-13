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
    r"/(?:19|20)\\d{2}/[^\\s]+?\\.(?:heic|jpe?g)",
    re.IGNORECASE,
)
TRAILING_ALPHA_BEFORE_EXT_RE = re.compile(
    r"(?<=\\d)[A-Za-z](?=\\.(?:heic|jpe?g)$)",
    re.IGNORECASE,
)


def _normalize_extracted_path(path: str) -> str:
    """Normalize OCR path artifacts while preserving expected server format."""
    normalized = TRAILING_ALPHA_BEFORE_EXT_RE.sub("", path)
    return normalized


def extract_server_paths(
    download_folder: Path, img_pattern: str = "IMG_*"
) -> list[str]:
    if not download_folder.is_dir():
        raise FileNotFoundError(
            f"download_folder does not exist or is not a directory: {download_folder}"
        )

    server_paths: list[str] = []
    seen_paths: set[str] = set()

    for file in sorted(download_folder.glob(img_pattern)):
        text = pytesseract.image_to_string(Image.open(file))

        # Extract canonical server paths from noisy OCR output.
        for match in PATH_RE.finditer(text):
            path = _normalize_extracted_path(match.group(0))
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
