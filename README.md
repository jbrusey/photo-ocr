# photo-ocr

Utility scripts for OCR-ing image metadata and moving files to trash.

## install (uv)

```sh
# install uv if needed: https://docs.astral.sh/uv/getting-started/installation/
uv python install 3.13
uv venv --python 3.13
source .venv/bin/activate
uv sync --all-groups
```

## Usage

All scripts now accept paths via CLI arguments. See `--help` for each script:

### extract_server_paths.py

Extract server paths from images in a Downloads folder.

```sh
# Basic usage
uv run python extract_server_paths.py \
    --download-folder ~/Downloads/images-to-delete \
    --output-csv ~/Downloads/images-to-delete/server_paths.csv

# Custom image pattern
uv run python extract_server_paths.py \
    --download-folder /Volumes/photo/imports \
    --output-csv /Volumes/photo/imports/parsed_paths.csv \
    --img-pattern "PHOTO_*"
```

**Args:**
- `--download-folder`: Folder containing images to scan (required)
- `--output-csv`: Output CSV file path (required)
- `--img-pattern`: Glob pattern for image files (default: `IMG_*`)

### check_filenames.py

Check file paths against available files in the photo folder and suggest corrections for missing files.

```sh
# Basic usage
uv run python check_filenames.py \
    --photo-folder /Volumes/photo \
    --base-folder ~/Downloads/images-to-delete \
    --input-csv server_paths.csv

# Custom output filename
uv run python check_filenames.py \
    --photo-folder /Volumes/photo \
    --base-folder ~/Downloads \
    --input-csv my_paths.csv \
    --output-csv my_paths_corrected.csv

# Adjust fuzzy match cutoff (0.0-1.0, higher = stricter)
uv run python check_filenames.py \
    --photo-folder /Volumes/photo \
    --base-folder ~/Downloads/images-to-delete \
    --input-csv server_paths.csv \
    --cutoff 0.8
```

**Args:**
- `--photo-folder`: Base photo server path (e.g., `/Volumes/photo`)
- `--base-folder`: Base folder for CSV files (default: `~/Downloads/images-to-delete`)
- `--input-csv`: Input CSV file name (e.g., `server_paths.csv`)
- `--output-csv`: Output CSV file name (default: `<input-stem>_corrected<ext>`, e.g. `server_paths_corrected.csv`)
- `--cutoff`: Fuzzy matching cutoff (default: `0.75`)

### move_to_trash.py

Move files from the photo folder to trash based on a CSV list of paths.

```sh
# Basic usage (trash directory is <photo-folder>/trash by default)
uv run python move_to_trash.py \
    --photo-folder /Volumes/photo \
    --csv-file ~/Downloads/images-to-delete/server_paths_corrected.csv

# Explicit trash directory
uv run python move_to_trash.py \
    --photo-folder /Volumes/photo \
    --trash-folder /Volumes/photo/trash \
    --csv-file ~/Downloads/images-to-delete/server_paths_corrected.csv

# Custom trash folder name (derived from photo-folder)
uv run python move_to_trash.py \
    --photo-folder /Volumes/photo \
    --trash-folder-name recycle \
    --csv-file ~/Downloads/server_paths_corrected.csv
```

**Args:**
- `--photo-folder`: Base photo server path (e.g., `/Volumes/photo`)
- `--trash-folder`: Trash directory to move files into (default: `<photo-folder>/<trash-folder-name>`)
- `--csv-file`: CSV file with list of paths to move to trash (required)
- `--trash-folder-name`: Name of the trash folder when `--trash-folder` is not specified (default: `trash`)

## Workflow

1. **Extract paths** from unprocessed images:
   ```sh
   uv run python extract_server_paths.py \
       --download-folder ~/Downloads/images-to-delete \
       --output-csv ~/Downloads/images-to-delete/server_paths.csv
   ```

2. **Check and correct** paths for missing files:
   ```sh
   uv run python check_filenames.py \
       --photo-folder /Volumes/photo \
       --base-folder ~/Downloads/images-to-delete \
       --input-csv server_paths.csv
   ```

3. **Move to trash** once paths are verified:
   ```sh
   uv run python move_to_trash.py \
       --photo-folder /Volumes/photo \
       --trash-folder /Volumes/photo/trash \
       --csv-file ~/Downloads/images-to-delete/server_paths_corrected.csv
   ```


## Development

Run linting and formatting with Ruff:

```sh
uv run ruff check .
uv run ruff format .
```

## Notes

- Scripts are now **portable** - paths are provided via CLI arguments
- All paths support `~` expansion (e.g. `~/Downloads`)
- The `--cutoff` parameter controls fuzzy matching strictness (lower = more lenient)

## Configuration reference

`.config.example.json` documents the available configuration values for reference when constructing CLI commands. It is not loaded by any script directly.