import csv
from pathlib import Path
from datetime import datetime

# Resolve this project directory from the current script file.
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"
REPORT_PATH = OUTPUT_DIR / "file_inventory.csv"


def collect_file_inventory(root_folder):
    """Return metadata for all regular files found recursively."""
    inventory = []

    for file_path in root_folder.rglob("*"):
        if file_path.is_file():
            details = file_path.stat()
            inventory.append({
                "name": file_path.name,
                "suffix": file_path.suffix,
                "parent": str(file_path.parent.relative_to(BASE_DIR)),
                "relative_path": str(file_path.relative_to(BASE_DIR)),
                "size_bytes": details.st_size,
            })

    return inventory


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Current working directory:", Path.cwd())
    print("Project directory:", BASE_DIR)
    print("\nDirect items inside data/input:")

    input_folder = DATA_DIR / "input"
    for item in input_folder.iterdir():
        print("-", item.name, "| file:", item.is_file(), "| folder:", item.is_dir())

    print("\nRecursive CSV search:")
    for csv_path in DATA_DIR.rglob("*.csv"):
        print(csv_path.relative_to(BASE_DIR))

    inventory = collect_file_inventory(DATA_DIR)

    with REPORT_PATH.open("w", encoding="utf-8", newline="") as report_file:
        fieldnames = ["name", "suffix", "parent", "relative_path", "size_bytes"]
        writer = csv.DictWriter(report_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(inventory)

    notes_file = input_folder / "notes.txt"
    if notes_file.is_file():
        print("\nNotes preview:")
        print(notes_file.read_text(encoding="utf-8"))

    print("\nFiles inventoried:", len(inventory))
    print("Report:", REPORT_PATH)
    print("Completed:", datetime.now().isoformat(timespec="seconds"))


if __name__ == "__main__":
    main()
