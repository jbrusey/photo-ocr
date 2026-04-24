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
            dest = trash / clean_path

            if dest.exists():
                if src.exists():
                    dest = _unique_destination(dest)
                    _move_with_parent_dirs(src, dest)
                    print(
                        "Destination already exists, moved source to unique path: "
                        f"{dest}"
                    )
                else:
                    print(f"Already moved to trash: {dest}")
                continue

            if src.exists():
                _move_with_parent_dirs(src, dest)
                print(f"Moved to trash: {dest}")
            else:
                print(f"Source path does not exist: {src}")


def _move_with_parent_dirs(src: Path, dest: Path) -> None:
    """Move src to dest, creating destination parent folders as needed."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(src), str(dest))


def _unique_destination(dest: Path) -> Path:
    """Return a unique destination path based on dest."""
    suffixes = "".join(dest.suffixes)
    stem = dest.name[: -len(suffixes)] if suffixes else dest.name

    counter = 1
    while True:
        candidate = dest.with_name(f"{stem}__dup{counter}{suffixes}")
        if not candidate.exists():
            return candidate
        counter += 1
