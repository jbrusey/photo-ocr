import csv
import shutil
from pathlib import Path

photo = Path("/Volumes/photo")
trash = photo / "trash"

csv_file = Path("~/Downloads/images-to-delete/server_paths_corrected.csv").expanduser()

with open(csv_file) as f:
    reader = csv.DictReader(f)
    for row in reader:
        p = row["corrected_server_path"]
        clean_p = p.lstrip("/")
        src = photo / clean_p
        dest = trash / Path(clean_p).name

        if dest.exists():
            print(f"Already moved to trash: {dest}")
            continue

        if src.exists():
            shutil.move(str(src), str(dest))
            print(f"Moved to trash: {dest}")
        else:
            print(f"Source path does not exist: {src}")
