#!/usr/bin/env python3
"""Move files from photo folder to trash based on CSV list of paths to delete.

Usage:
    python move_to_trash.py --photo-folder /Volumes/photo --trash-folder /Volumes/photo/trash --csv-file ~/Downloads/images-to-delete/server_paths_corrected.csv
"""

import csv
import shutil
import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Move files to trash based on CSV list")
    parser.add_argument(
        "--photo-folder",
        type=Path,
        required=True,
        help="Base photo server path (e.g., /Volumes/photo)"
    )
    parser.add_argument(
        "--trash-folder",
        type=Path,
        required=True,
        help="Trash folder within photo folder (default: <photo-folder>/trash)"
    )
    parser.add_argument(
        "--csv-file",
        type=Path,
        required=True,
        help="CSV file with list of paths to move to trash"
    )
    parser.add_argument(
        "--trash-folder-name",
        type=Path,
        default=Path("trash"),
        help="Name of the trash folder (default: trash)"
    )

    args = parser.parse_args()

    trash = args.trash_folder / args.trash_folder_name
    if not trash.exists():
        trash.mkdir(parents=True)

    with open(args.csv_file) as f:
        reader = csv.DictReader(f)
        for row in reader:
            p = row["corrected_server_path"]
            clean_p = p.lstrip("/")
            src = args.photo_folder / clean_p
            dest = trash / Path(clean_p).name

            if dest.exists():
                if src.exists():
                    print(f"Destination already exists, removing source: {dest}")
                    src.unlink()
                else:
                    print(f"Already moved to trash: {dest}")
                continue

            if src.exists():
                shutil.move(str(src), str(dest))
                print(f"Moved to trash: {dest}")
            else:
                print(f"Source path does not exist: {src}")


if __name__ == "__main__":
    main()
