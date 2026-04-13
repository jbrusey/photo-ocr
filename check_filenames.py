#!/usr/bin/env python3
"""Check and correct file paths against available files in photo folder.

Usage:
    python check_filenames.py --photo-folder /Volumes/photo \
        --base-folder ~/Downloads/images-to-delete \
        --input-csv server_paths.csv
"""

import argparse
from difflib import get_close_matches
from pathlib import Path

import pandas as pd


def build_available_paths(base_dir: Path) -> list[str]:
    """Return all file paths under ``base_dir`` relative to ``base_dir``."""
    return [
        str(candidate.relative_to(base_dir))
        for candidate in base_dir.rglob("*")
        if candidate.is_file()
    ]


def find_fuzzy_match(
    candidate: str, available_paths: list[str], *, cutoff: float = 0.75
):
    """Return the closest available path to ``candidate`` if it is similar enough."""
    matches = get_close_matches(candidate, available_paths, n=1, cutoff=cutoff)
    return matches[0] if matches else None


def main():
    parser = argparse.ArgumentParser(description="Check and correct file paths")
    parser.add_argument(
        "--photo-folder",
        type=Path,
        required=True,
        help="Base photo server path (e.g., /Volumes/photo)",
    )
    parser.add_argument(
        "--base-folder",
        type=Path,
        required=True,
        help="Base folder for CSV files (default: ~/Downloads/images-to-delete)",
    )
    parser.add_argument(
        "--input-csv",
        type=str,
        required=True,
        help="Input CSV file name (e.g., server_paths.csv)",
    )
    parser.add_argument(
        "--output-csv",
        type=str,
        default=None,
        help="Output CSV file name (default: input-csv -> input-csv_corrected.csv)",
    )
    parser.add_argument(
        "--cutoff",
        type=float,
        default=0.75,
        help="Fuzzy matching cutoff (default: 0.75)",
    )

    args = parser.parse_args()

    base_dir = args.base_folder.expanduser().resolve()
    photo_folder = args.photo_folder.expanduser().resolve()
    csv_file = base_dir / args.input_csv
    input_path = Path(args.input_csv)
    default_output = f"{input_path.stem}_corrected{input_path.suffix}"
    output_csv = csv_file.with_name(args.output_csv or default_output)

    df = pd.read_csv(csv_file)
    df["corrected_server_path"] = df["server_path"].astype(str)

    available_paths = build_available_paths(photo_folder)
    corrected = []

    for server_path in df["server_path"].astype(str):
        clean_p = server_path.lstrip("/")
        src = photo_folder / clean_p

        if src.exists():
            corrected.append(server_path)
            continue

        print(f"Source path does not exist: {src}")

        match = find_fuzzy_match(clean_p, available_paths, cutoff=args.cutoff)

        if match:
            corrected_path = f"/{match}"
            print(f"  -> Suggested correction: {corrected_path}")
            corrected.append(corrected_path)
        else:
            corrected.append(server_path)

    df["corrected_server_path"] = corrected
    df.to_csv(output_csv, index=False)

    print(f"Wrote corrected paths to {output_csv}")


if __name__ == "__main__":
    main()
