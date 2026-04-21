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

Use package entrypoints via `uv run <command>`. Legacy root-level scripts are kept as thin compatibility wrappers.

### photo-ocr-extract-text

Extract OCR text from images and write an intermediate CSV.

```sh
uv run photo-ocr-extract-text \
    --download-folder ~/Downloads/images-to-delete \
    --output-csv ~/Downloads/images-to-delete/extracted_text.csv \
    --img-pattern "IMG_*"
```

**Args:**
- `--download-folder`: Folder containing images to scan (required)
- `--output-csv`: Output CSV file path for OCR text (required)
- `--img-pattern`: Glob pattern for image files (default: `IMG_*`)

### photo-ocr-extract-paths

Parse OCR text CSV and extract canonical server paths.

```sh
uv run photo-ocr-extract-paths \
    --input-csv ~/Downloads/images-to-delete/extracted_text.csv \
    --output-csv ~/Downloads/images-to-delete/server_paths.csv
```

**Args:**
- `--input-csv`: OCR text CSV from `photo-ocr-extract-text` (required)
- `--output-csv`: Output CSV file path for parsed server paths (required)

### photo-ocr-extract-server-paths (compatibility workflow wrapper)

Runs both steps above in one command.

```sh
uv run photo-ocr-extract-server-paths \
    --download-folder ~/Downloads/images-to-delete \
    --output-csv ~/Downloads/images-to-delete/server_paths.csv
```

### photo-ocr-check-filenames

Check file paths against available files in the photo folder and suggest corrections for missing files.

```sh
uv run photo-ocr-check-filenames \
    --photo-folder /Volumes/photo \
    --base-folder ~/Downloads/images-to-delete \
    --input-csv server_paths.csv
```

### photo-ocr-move-to-trash

Move files from the photo folder to trash based on a CSV list of paths.

```sh
uv run photo-ocr-move-to-trash \
    --photo-folder /Volumes/photo \
    --csv-file ~/Downloads/images-to-delete/server_paths_corrected.csv
```

## Workflow

1. **Extract OCR text** from images:
   ```sh
   uv run photo-ocr-extract-text \
       --download-folder ~/Downloads/images-to-delete \
       --output-csv ~/Downloads/images-to-delete/extracted_text.csv
   ```
2. **Parse server paths** from OCR text:
   ```sh
   uv run photo-ocr-extract-paths \
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
