import csv
import importlib.util
from pathlib import Path

TRASH_MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "photo_ocr" / "trash.py"
spec = importlib.util.spec_from_file_location("photo_ocr_trash", TRASH_MODULE_PATH)
trash_module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(trash_module)
move_paths_to_trash = trash_module.move_paths_to_trash
unique_destination = trash_module._unique_destination


def _write_csv(path: Path, values: list[str]) -> None:
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["corrected_server_path"])
        writer.writeheader()
        for value in values:
            writer.writerow({"corrected_server_path": value})


def test_move_paths_to_trash_preserves_relative_structure(tmp_path: Path) -> None:
    photo_folder = tmp_path / "photos"
    trash = tmp_path / "trash"
    csv_file = tmp_path / "paths.csv"

    first = photo_folder / "album-a" / "IMG_0001.jpg"
    second = photo_folder / "album-b" / "IMG_0001.jpg"
    first.parent.mkdir(parents=True)
    second.parent.mkdir(parents=True)
    first.write_text("first")
    second.write_text("second")

    _write_csv(
        csv_file,
        ["/album-a/IMG_0001.jpg", "/album-b/IMG_0001.jpg"],
    )

    move_paths_to_trash(photo_folder=photo_folder, trash=trash, csv_file=csv_file)

    assert not first.exists()
    assert not second.exists()
    assert (trash / "album-a" / "IMG_0001.jpg").read_text() == "first"
    assert (trash / "album-b" / "IMG_0001.jpg").read_text() == "second"


def test_move_paths_to_trash_uses_unique_name_on_collision(tmp_path: Path) -> None:
    photo_folder = tmp_path / "photos"
    trash = tmp_path / "trash"
    csv_file = tmp_path / "paths.csv"

    src = photo_folder / "album-a" / "IMG_0001.jpg"
    src.parent.mkdir(parents=True)
    src.write_text("new source")

    existing = trash / "album-a" / "IMG_0001.jpg"
    existing.parent.mkdir(parents=True)
    existing.write_text("already in trash")

    _write_csv(csv_file, ["/album-a/IMG_0001.jpg"])

    move_paths_to_trash(photo_folder=photo_folder, trash=trash, csv_file=csv_file)

    assert not src.exists()
    assert existing.read_text() == "already in trash"
    assert (trash / "album-a" / "IMG_0001__dup1.jpg").read_text() == "new source"


def test_unique_destination_skips_existing_candidates(tmp_path: Path) -> None:
    dest = tmp_path / "album-a" / "IMG_0001.jpg"
    dest.parent.mkdir(parents=True)
    dest.write_text("existing")
    (tmp_path / "album-a" / "IMG_0001__dup1.jpg").write_text("existing dup")

    next_dest = unique_destination(dest)

    assert next_dest == tmp_path / "album-a" / "IMG_0001__dup2.jpg"
    assert not next_dest.exists()
