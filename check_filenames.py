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


photo = Path("/Volumes/photo")
downloads = Path("~/Downloads/images-to-delete/").expanduser()
csv_file = downloads / "server_paths.csv"

df = pd.read_csv(csv_file)
df["corrected_server_path"] = df["server_path"].astype(str)

available_paths = build_available_paths(photo)
corrected = []

for index, server_path in enumerate(df["server_path"].astype(str)):
    clean_p = server_path.lstrip("/")
    src = photo / clean_p

    if src.exists():
        corrected.append(server_path)
        continue

    print(f"Source path does not exist: {src}")

    match = find_fuzzy_match(clean_p, available_paths)

    if match:
        corrected_path = f"/{match}"
        print(f"  -> Suggested correction: {corrected_path}")
        corrected.append(corrected_path)
    else:
        corrected.append(server_path)

df["corrected_server_path"] = corrected
corrected_csv = csv_file.with_name("server_paths_corrected.csv")
df.to_csv(corrected_csv, index=False)

print(f"Wrote corrected paths to {corrected_csv}")
