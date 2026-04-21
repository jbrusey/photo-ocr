"""Path extraction and path matching logic."""

import re
from difflib import get_close_matches
from pathlib import Path

import pandas as pd

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


def extract_paths_from_text(text: str) -> list[str]:
    """Extract canonical server paths from a single OCR text blob."""
    candidates: list[str] = []

    candidates.extend(match.group(0) for match in PATH_RE.finditer(text))

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


def extract_server_paths_from_rows(rows: list[dict]) -> list[str]:
    """Extract unique server paths from OCR rows produced by extract_image_text."""
    server_paths: list[str] = []
    seen_paths: set[str] = set()

    for row in rows:
        text = str(row.get("extracted_text", ""))
        for path in extract_paths_from_text(text):
            if path not in seen_paths:
                server_paths.append(path)
                seen_paths.add(path)

    return server_paths


def extract_server_paths_from_csv(input_csv: Path) -> list[str]:
    """Load OCR text CSV and extract unique server paths."""
    rows = pd.read_csv(input_csv).to_dict(orient="records")
    return extract_server_paths_from_rows(rows)


def build_available_paths(base_dir: Path) -> list[str]:
    """Return all file paths under ``base_dir`` relative to ``base_dir``."""
    return [
        str(candidate.relative_to(base_dir))
        for candidate in base_dir.rglob("*")
        if candidate.is_file()
    ]


def find_fuzzy_match(
    candidate: str, available_paths: list[str], *, cutoff: float = 0.75
) -> str | None:
    """Return the closest available path to ``candidate`` if it is similar enough."""
    matches = get_close_matches(candidate, available_paths, n=1, cutoff=cutoff)
    return matches[0] if matches else None
