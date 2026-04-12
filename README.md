# photo-ocr

## install (uv)

```sh
# install uv if needed: https://docs.astral.sh/uv/getting-started/installation/
uv python install 3.13
uv venv --python 3.13
source .venv/bin/activate
uv sync --all-groups
```

## run scripts

```sh
uv run python extract_server_paths.py
uv run python check_filenames.py
uv run python move_to_trash.py
```
