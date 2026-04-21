"""OCR extraction logic."""

from pathlib import Path

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
