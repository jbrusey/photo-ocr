import csv
from pathlib import Path

import pytesseract
import pytest

from extract_server_paths import extract_server_paths


def test_extract_server_paths_matches_expected_test_data():

    test_data_dir = Path("test_data")
    with (test_data_dir / "expected.csv").open(newline="") as csv_file:
        expected_paths = [row["Path"] for row in csv.DictReader(csv_file)]

    try:
        actual_paths = extract_server_paths(test_data_dir, img_pattern="IMG_*.PNG")
    except pytesseract.pytesseract.TesseractNotFoundError as exc:  # pragma: no cover
        pytest.skip(f"Tesseract is not installed in this environment: {exc}")

    assert actual_paths == expected_paths
