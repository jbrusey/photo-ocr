#!/usr/bin/env python3
"""Extract server paths from images in Downloads folder.

Usage:
    python extract_server_paths.py --download-folder ~/Downloads/images-to-delete --output-csv server_paths.csv
"""

import argparse
import cv2
import pandas as pd
import pytesseract
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Extract server paths from images")
    parser.add_argument(
        "--download-folder",
        type=Path,
        required=True,
        help="Folder containing images to scan (default: ~/Downloads/images-to-delete)"
    )
    parser.add_argument(
        "--output-csv",
        type=Path,
        required=True,
        help="Output CSV file path"
    )
    parser.add_argument(
        "--img-pattern",
        type=str,
        default="IMG_*",
        help="Glob pattern for image files (default: IMG_*)"
    )

    args = parser.parse_args()

    server_paths = []
    image_files = list(args.download_folder.glob(args.img_pattern))

    for file in image_files:
        img = cv2.imread(str(file))
        if img is None:
            continue

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

        text = pytesseract.image_to_string(thresh)

        # Extract paths: look for lines that look like server paths
        # Server paths have format like: /YYYY/YYYY-MM-DD-HASH.ext
        lines = text.splitlines()
        seen_paths = set()

        # Metadata words to skip
        metadata_words = ["Taken", "Camera", "Original", "Compressed", "Location", "Offline", "Download", "Downloaded", "Path", "size", "x", "PM", "AM", "Unknown", "Full", "West", "Midlands", "England", "United", "Kingdom", "Photograph", "Apple", "NIKON", "OLYMPUS", "Canon", "PNG"]

        # Valid file extensions
        valid_extensions = {".heic", ".jpeg", ".jpg", ".JPG", ".HEIC", ".JPEG"}

        current_path = None  # Buffer for collecting a path

        for line in lines:
            line_stripped = line.strip()

            # Skip empty lines - flush buffered path if valid
            if not line_stripped:
                if current_path and any(ext in current_path for ext in valid_extensions):
                    if current_path not in seen_paths:
                        print(current_path)
                        server_paths.append(current_path)
                        seen_paths.add(current_path)
                    current_path = None
                continue

            # Reject metadata words
            if any(word in line_stripped for word in metadata_words):
                continue

            # Check if this line ends with a valid file extension
            has_valid_ext = any(ext in line_stripped for ext in valid_extensions)

            # Check if this line looks like a server path (has date pattern or starts with /)
            has_date = any(date_pat in line_stripped for date_pat in ["/YYYY/", "-01-", "-02-", "-03-", "-04-", "-05-", "-06-", "-07-", "-08-", "-09-", "-10-", "-11-", "-12-", "/20", "/201"])
            starts_with_slash = line_stripped.startswith("/")

            # Line is a candidate if it has valid extension, starts with /, or has date pattern
            is_candidate = has_valid_ext or starts_with_slash or has_date

            if is_candidate:
                if current_path:
                    # We have a buffered path - combine if this line is clean
                    if " " not in line_stripped:
                        current_path = current_path.rstrip() + " " + line_stripped
                    else:
                        # Flush current path and start new one
                        if current_path not in seen_paths:
                            print(current_path)
                            server_paths.append(current_path)
                            seen_paths.add(current_path)
                        current_path = line_stripped
                else:
                    current_path = line_stripped

        # Flush any remaining buffered path
        if current_path:
            if any(ext in current_path for ext in valid_extensions):
                if current_path not in seen_paths:
                    print(current_path)
                    server_paths.append(current_path)
                    seen_paths.add(current_path)

    pd.DataFrame(server_paths, columns=["server_path"]).to_csv(args.output_csv, index=False)


if __name__ == "__main__":
    main()
