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


def test_extract_server_paths_parses_noisy_ocr_text(monkeypatch: pytest.MonkeyPatch):
    test_data_dir = Path("test_data")

    sample_ocr_text = """
    2022-12-14-3327BA8B-I/2022/2022-12-14-3327BA8B-D47F-4EDC-9C41-EFBBDC4B5D64.heic
    Ld /2019/2019-06-04-DSC_9083a.JPG
    """

    monkeypatch.setattr(pytesseract, "image_to_string", lambda _img: sample_ocr_text)

    actual_paths = extract_server_paths(test_data_dir, img_pattern="IMG_0871.PNG")

    assert actual_paths == [
        "/2022/2022-12-14-3327BA8B-D47F-4EDC-9C41-EFBBDC4B5D64.heic",
        "/2019/2019-06-04-DSC_9083.JPG",
    ]
