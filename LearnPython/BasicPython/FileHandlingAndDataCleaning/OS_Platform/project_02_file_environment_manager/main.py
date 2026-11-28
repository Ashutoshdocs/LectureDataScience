import csv
import logging
import os
import platform
from datetime import datetime

from file_manager import (
    list_files,
    find_files_by_extension,
    read_text_file,
    read_csv_file,
    copy_to_archive,
)


# Keep every project path anchored to this file.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.path.join(BASE_DIR, "data", "input")
ARCHIVE_DIR = os.path.join(BASE_DIR, "data", "archive")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
LOG_DIR = os.path.join(BASE_DIR, "logs")


def configure_logging():
    os.makedirs(LOG_DIR, exist_ok=True)
    log_path = os.path.join(LOG_DIR, "file_manager.log")

    logging.basicConfig(
        filename=log_path,
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )


def main():
    # Ensure expected folders exist before the application uses them.
    for folder in [INPUT_DIR, ARCHIVE_DIR, OUTPUT_DIR, LOG_DIR]:
        os.makedirs(folder, exist_ok=True)

    configure_logging()

    # Environment variables are useful for non-secret configuration.
    app_environment = os.getenv("APP_ENV", "development")
    logging.info("Application started in %s environment", app_environment)

    print("OS:", platform.system())
    print("APP_ENV:", app_environment)
    print("\nFiles in input folder:")

    filenames = list_files(INPUT_DIR)
    for filename in filenames:
        print("-", filename)

    csv_files = find_files_by_extension(INPUT_DIR, ".csv")
    print("\nCSV files found:", len(csv_files))

    # Read the sample text file when present.
    notes_path = os.path.join(INPUT_DIR, "notes.txt")
    if os.path.isfile(notes_path):
        print("\nText preview:")
        print(read_text_file(notes_path))

    # Read CSV data and write a small summary report.
    report_rows = []
    for csv_path in csv_files:
        rows = read_csv_file(csv_path)
        report_rows.append({
            "file": os.path.basename(csv_path),
            "row_count": len(rows),
            "columns": ", ".join(rows[0].keys()) if rows else "",
        })

    report_path = os.path.join(OUTPUT_DIR, "file_inventory_report.csv")
    with open(report_path, "w", encoding="utf-8", newline="") as report_file:
        fieldnames = ["file", "row_count", "columns"]
        writer = csv.DictWriter(report_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(report_rows)

    # Archive copies of input files. Original inputs remain untouched.
    for filename in filenames:
        source_path = os.path.join(INPUT_DIR, filename)
        try:
            archived_path = copy_to_archive(source_path, ARCHIVE_DIR)
            logging.info("Copied %s to %s", source_path, archived_path)
        except FileExistsError:
            logging.warning("Archive copy already exists for %s", filename)

    print("\nReport saved to:", report_path)
    print("Log saved to:", os.path.join(LOG_DIR, "file_manager.log"))
    print("Completed at:", datetime.now().isoformat(timespec="seconds"))


if __name__ == "__main__":
    main()
