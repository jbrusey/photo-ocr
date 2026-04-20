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

All scripts accept paths via CLI arguments. See `--help` for each script.

### extract_image_text.py

Extract OCR text from images and write an intermediate CSV.

```sh
uv run python extract_image_text.py \
    --download-folder ~/Downloads/images-to-delete \
    --output-csv ~/Downloads/images-to-delete/extracted_text.csv \
    --img-pattern "IMG_*"
```

**Args:**
- `--download-folder`: Folder containing images to scan (required)
- `--output-csv`: Output CSV file path for OCR text (required)
- `--img-pattern`: Glob pattern for image files (default: `IMG_*`)

### text_to_server_path.py

Parse OCR text CSV and extract canonical server paths.

```sh
uv run python text_to_server_path.py \
    --input-csv ~/Downloads/images-to-delete/extracted_text.csv \
    --output-csv ~/Downloads/images-to-delete/server_paths.csv
```

**Args:**
- `--input-csv`: OCR text CSV from `extract_image_text.py` (required)
- `--output-csv`: Output CSV file path for parsed server paths (required)

### extract_server_paths.py (compatibility wrapper)

Runs both steps above in one command for backwards compatibility.

```sh
uv run python extract_server_paths.py \
    --download-folder ~/Downloads/images-to-delete \
    --output-csv ~/Downloads/images-to-delete/server_paths.csv
```

### check_filenames.py

Check file paths against available files in the photo folder and suggest corrections for missing files.

```sh
uv run python check_filenames.py \
    --photo-folder /Volumes/photo \
    --base-folder ~/Downloads/images-to-delete \
    --input-csv server_paths.csv
```

### move_to_trash.py

Move files from the photo folder to trash based on a CSV list of paths.

```sh
uv run python move_to_trash.py \
    --photo-folder /Volumes/photo \
    --csv-file ~/Downloads/images-to-delete/server_paths_corrected.csv
```

## Workflow

1. **Extract OCR text** from images:
   ```sh
   uv run python extract_image_text.py \
       --download-folder ~/Downloads/images-to-delete \
       --output-csv ~/Downloads/images-to-delete/extracted_text.csv
   ```
2. **Parse server paths** from OCR text:
   ```sh
   uv run python text_to_server_path.py \
       --input-csv ~/Downloads/images-to-delete/extracted_text.csv \
       --output-csv ~/Downloads/images-to-delete/server_paths.csv
   ```
3. **Check and correct** paths for missing files.
4. **Move to trash** once paths are verified.

## Development

```sh
uv run ruff check .
uv run ruff format .
uv run pytest
```
