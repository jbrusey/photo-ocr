import csv
import shutil
from pathlib import Path

photo = Path("~/Downloads/images-to-delete").expanduser()
csv_file = photo / "server_paths.csv"

with open(csv_file) as f:
    reader = csv.DictReader(f)
    for row in reader:
        p = row["server_path"]
        clean_p = p.lstrip("/")
        src = photo / clean_p

        if not src.exists():
            print(f"Source path does not exist: {src}")
