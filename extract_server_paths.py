#!/usr/bin/env python3
"""Backward-compatible wrapper that runs OCR + path extraction in one command."""

import argparse
from pathlib import Path

import pandas as pd

from extract_image_text import extract_text_from_images
from text_to_server_path import extract_server_paths_from_rows, extract_paths_from_text


def extract_server_paths(
    download_folder: Path, img_pattern: str = "IMG_*"
) -> list[str]:
    rows = extract_text_from_images(download_folder, img_pattern=img_pattern)
    return extract_server_paths_from_rows(rows)


def main() -> None:
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

__all__ = ["extract_paths_from_text", "extract_server_paths"]
