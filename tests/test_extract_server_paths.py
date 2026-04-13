import csv
from pathlib import Path

import pytesseract
import pytest

from extract_server_paths import extract_paths_from_text, extract_server_paths


def test_extract_server_paths_matches_expected_test_data():

    test_data_dir = Path("test_data")
    with (test_data_dir / "expected.csv").open(newline="") as csv_file:
        expected_paths = [row["Path"] for row in csv.DictReader(csv_file)]

    try:
        actual_paths = extract_server_paths(test_data_dir, img_pattern="IMG_*.PNG")
    except pytesseract.pytesseract.TesseractNotFoundError as exc:  # pragma: no cover
        pytest.skip(f"Tesseract is not installed in this environment: {exc}")

    assert actual_paths == expected_paths


def test_extract_paths_from_text_parses_noisy_ocr_text():
    sample_ocr_text = """
    2022-12-14-3327BA8B-I/2022/2022-12-14-3327BA8B-D47F-4EDC-9C41-EFBBDC4B5D64.heic
    Ld /2019/2019-06-04-DSC_9083a.JPG
    """

    assert extract_paths_from_text(sample_ocr_text) == [
        "/2022/2022-12-14-3327BA8B-D47F-4EDC-9C41-EFBBDC4B5D64.heic",
        "/2019/2019-06-04-DSC_9083.JPG",
    ]


def test_extract_paths_from_text_handles_split_path_fragments():
    split_path_text = """
    /2022/
    2022-12-14-3327BA8B-D47F-4EDC-9C41-EFBBDC4B5D64.heic
    """

    assert extract_paths_from_text(split_path_text) == [
        "/2022/2022-12-14-3327BA8B-D47F-4EDC-9C41-EFBBDC4B5D64.heic"
    ]
