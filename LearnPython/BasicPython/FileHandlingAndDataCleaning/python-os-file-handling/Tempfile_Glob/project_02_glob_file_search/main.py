import csv
from pathlib import Path

from search_tools import find_by_pattern, find_recursively_with_iterator

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"
REPORT_PATH = OUTPUT_DIR / "file_inventory.csv"


def build_inventory(paths):
    inventory = []

    for path_string in paths:
        path = Path(path_string)

        if path.is_file():
            inventory.append({
                "relative_path": str(path.relative_to(BASE_DIR)),
                "filename": path.name,
                "extension": path.suffix,
                "size_bytes": path.stat().st_size,
            })

    return inventory


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Project data directory:", DATA_DIR)

    print("\nCSV files found recursively:")
    csv_matches = find_by_pattern(DATA_DIR, "**/*.csv", recursive=True)
    for match in csv_matches:
        print("-", Path(match).relative_to(BASE_DIR))

    print("\nLog files using iglob:")
    for match in find_recursively_with_iterator(DATA_DIR, "**/*.log"):
        print("-", Path(match).relative_to(BASE_DIR))

    print("\nText files directly under incoming:")
    text_matches = find_by_pattern(DATA_DIR / "incoming", "*.txt")
    for match in text_matches:
        print("-", Path(match).name)

    all_matches = find_by_pattern(DATA_DIR, "**/*", recursive=True)
    inventory = build_inventory(all_matches)

    with REPORT_PATH.open("w", encoding="utf-8", newline="") as report_file:
        fieldnames = ["relative_path", "filename", "extension", "size_bytes"]
        writer = csv.DictWriter(report_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(inventory)

    print("\nTotal files inventoried:", len(inventory))
    print("Report saved to:", REPORT_PATH)


if __name__ == "__main__":
    main()
