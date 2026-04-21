"""Move photo files to trash."""

import argparse
import csv
import shutil
from pathlib import Path


def validate_folder_name(name: str) -> str:
    """Validate that name is a simple folder name without path separators."""
    if "/" in name or "\\" in name:
        raise argparse.ArgumentTypeError(
            f"'{name}' must be a simple folder name, not a path"
        )
    return name


def move_paths_to_trash(photo_folder: Path, trash: Path, csv_file: Path) -> None:
    """Move paths listed in CSV from photo_folder to trash folder."""
    if not trash.exists():
        trash.mkdir(parents=True)

    with csv_file.open() as f:
        reader = csv.DictReader(f)
        for row in reader:
            path_value = row["corrected_server_path"]
            clean_path = path_value.lstrip("/")
            src = photo_folder / clean_path
            dest = trash / Path(clean_path).name

            if dest.exists():
                if src.exists():
                    print(f"Destination already exists, removing source: {src}")
                    src.unlink()
                else:
                    print(f"Already moved to trash: {dest}")
                continue

            if src.exists():
                shutil.move(str(src), str(dest))
                print(f"Moved to trash: {dest}")
            else:
                print(f"Source path does not exist: {src}")
