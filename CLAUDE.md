# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

Run all commands from the repository root.

- **Linting**: `uv run ruff check .`
- **Formatting**: `uv run ruff format .`
- **Testing**: `uv run pytest` (Note: Always run from root so `test_data/` paths resolve correctly)

## Project Structure

The core logic of the project has been moved to a Python package in `src/photo_ocr`. The top-level scripts in the repository root are thin compatibility wrappers that interface with this package.

- `src/photo_ocr/`: Contains the core implementation (extraction, matching, and trash logic).
- Top-level scripts: Entry points for users, providing CLI interfaces.

## Development Commands

Run all commands from the repository root.

- **Linting**: `uv run ruff check .`
- **Formatting**: `uv run ruff format .`
- **Testing**: `uv run pytest` (Note: Always run from root so `test_data/` paths resolve correctly)

## Project Overview

This repository contains utility scripts for extracting metadata from images via OCR and managing file deletions. The workflow typically involves:

1.  **Extraction**: Using `extract_image_text.py` to extract OCR text to an intermediate CSV.
2.  **Parsing**: Using `text_to_server_path.py` to parse the OCR text and extract canonical server paths.
3.  **Verification**: Using `check_filenames.py` to compare extracted paths against a target photo server, using fuzzy matching to correct discrepancies.
4.  **Cleanup**: Using `move_to_trash.py` to move the verified files to a trash directory.

(Note: `extract_server_paths.py` is available as a compatibility wrapper that performs steps 1 and 2 in one command.)

## Core Scripts (Wrappers)

- `extract_image_text.py`: Extracts OCR text from images and writes to an intermediate CSV.
- `text_to_server_path.py`: Parses the OCR text CSV to extract canonical server paths.
- `extract_server_paths.py`: A compatibility wrapper that runs both extraction and parsing steps in one command.
- `check_filenames.py`: Validates CSV paths against a real filesystem; uses a `--cutoff` parameter for fuzzy matching.
- `move_to_trash.py`: Performs the actual file movement based on a validated CSV.

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

Run all commands from the repository root.

- **Linting**: `uv run ruff check .`
- **Formatting**: `uv run ruff format .`
- **Testing**: `uv run pytest` (Note: Always run from root so `test_data/` paths resolve correctly)

## Project Overview

This repository contains utility scripts for extracting metadata from images via OCR and managing file deletions. The workflow typically involves:

1.  **Extraction**: Using `extract_image_text.py` to extract OCR text to an intermediate CSV.
2.  **Parsing**: Using `text_to_server_path.py` to parse the OCR text and extract canonical server paths.
3.  **Verification**: Using `check_filenames.py` to compare extracted paths against a target photo server, using fuzzy matching to correct discrepancies.
4.  **Cleanup**: Using `move_to_trash.py` to move the verified files to a trash directory.

(Note: `extract_server_paths.py` is available as a compatibility wrapper that performs steps 1 and 2 in one command.)

## Core Scripts (Wrappers)

- `extract_image_text.py`: Extracts OCR text from images and writes to an intermediate CSV.
- `text_to_server_path.py`: Parses the OCR text CSV to extract canonical server paths.
- `extract_server_paths.py`: A compatibility wrapper that runs both extraction and parsing steps in one command.
- `check_filenames.py`: Validates CSV paths against a real filesystem; uses a `--cutoff` parameter for fuzzy matching.
- `move_to_trash.py`: Performs the actual file movement based on a validated CSV.

All scripts are designed to be portable and accept all necessary paths via CLI arguments.

Extra space for testing.
