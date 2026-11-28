import logging
import shutil
from datetime import datetime
from pathlib import Path

from backup_manager import (
    copy_directory_tree,
    create_zip_archive,
    extract_zip_archive,
)

BASE_DIR = Path(__file__).resolve().parent
SOURCE_DIR = BASE_DIR / "data" / "source"
DESTINATION_DIR = BASE_DIR / "data" / "destination"
BACKUPS_DIR = BASE_DIR / "backups"
ARCHIVES_DIR = BASE_DIR / "archives"
LOGS_DIR = BASE_DIR / "logs"


def configure_logging():
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    log_file = LOGS_DIR / "backup.log"

    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )


def main():
    # Ensure project output locations exist.
    for folder in [DESTINATION_DIR, BACKUPS_DIR, ARCHIVES_DIR, LOGS_DIR]:
        folder.mkdir(parents=True, exist_ok=True)

    configure_logging()

    if not SOURCE_DIR.is_dir():
        raise NotADirectoryError(f"Source folder missing: {SOURCE_DIR}")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = BACKUPS_DIR / f"source_snapshot_{timestamp}"
    archive_base = ARCHIVES_DIR / f"source_backup_{timestamp}"
    archive_path = archive_base.with_suffix(".zip")
    restore_dir = DESTINATION_DIR / f"restored_{timestamp}"

    print("Source folder:", SOURCE_DIR)
    print("Source file count:", sum(1 for item in SOURCE_DIR.rglob("*") if item.is_file()))

    # Step 1: Copy the directory tree.
    copied_folder = copy_directory_tree(SOURCE_DIR, backup_dir)
    logging.info("Directory tree copied to %s", copied_folder)
    print("Directory backup:", copied_folder)

    # Step 2: Create ZIP archive.
    created_archive = create_zip_archive(SOURCE_DIR, archive_base)
    logging.info("ZIP archive created at %s", created_archive)
    print("ZIP archive:", created_archive)

    # Step 3: Extract the archive to a separate restore location.
    restored_folder = extract_zip_archive(created_archive, restore_dir)
    logging.info("Archive extracted to %s", restored_folder)
    print("Restored to:", restored_folder)

    # Step 4: Report disk usage.
    usage = shutil.disk_usage(BASE_DIR)
    gib = 1024 ** 3
    print("Disk total GiB:", round(usage.total / gib, 2))
    print("Disk used GiB:", round(usage.used / gib, 2))
    print("Disk free GiB:", round(usage.free / gib, 2))

    logging.info("Backup lab completed successfully")
    print("Log file:", LOGS_DIR / "backup.log")


if __name__ == "__main__":
    main()
