#!/usr/bin/env python3
"""Extract OCR text from images and save it as CSV."""

import argparse
from pathlib import Path

import pandas as pd
import pytesseract
from PIL import Image


def extract_text_from_images(
    download_folder: Path, img_pattern: str = "IMG_*"
) -> list[dict]:
    """Run OCR for each matching image and return structured rows."""
    if not download_folder.is_dir():
        raise FileNotFoundError(
            f"download_folder does not exist or is not a directory: {download_folder}"
        )

    rows: list[dict] = []
    for file in sorted(download_folder.glob(img_pattern)):
        with Image.open(file) as img:
            rows.append(
                {
                    "image_file": file.name,
                    "extracted_text": pytesseract.image_to_string(img),
                }
            )

    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract OCR text from images")
    parser.add_argument(
        "--download-folder",
        type=Path,
        required=True,
        help="Folder containing images to scan",
    )
    parser.add_argument(
        "--output-csv", type=Path, required=True, help="Output CSV for OCR text"
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

    rows = extract_text_from_images(download_folder, img_pattern=args.img_pattern)
    pd.DataFrame(rows, columns=["image_file", "extracted_text"]).to_csv(
        output_csv, index=False
    )


if __name__ == "__main__":
    main()
