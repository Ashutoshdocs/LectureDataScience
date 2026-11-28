"""Small, focused examples of common pathlib queries."""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
INPUT_DIR = BASE_DIR / "data" / "input"
SAMPLE_FILE = INPUT_DIR / "notes.txt"


def show_path_information(path):
    print("Path:", path)
    print("Absolute:", path.resolve())
    print("Name:", path.name)
    print("Stem:", path.stem)
    print("Suffix:", path.suffix)
    print("Parent:", path.parent)
    print("Exists:", path.exists())
    print("Is file:", path.is_file())
    print("Is directory:", path.is_dir())

    if path.is_file():
        print("Size:", path.stat().st_size, "bytes")


if __name__ == "__main__":
    show_path_information(SAMPLE_FILE)
