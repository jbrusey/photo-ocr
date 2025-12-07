from pathlib import Path

import pandas as pd

photo = Path("~/Downloads/images-to-delete").expanduser()
csv_file = photo / "server_paths.csv"

df = pd.read_csv(csv_file)

for server_path in df["server_path"].astype(str):
    clean_p = server_path.lstrip("/")
    src = photo / clean_p

    if not src.exists():
        print(f"Source path does not exist: {src}")
