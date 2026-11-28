import shutil
from pathlib import Path


def copy_directory_tree(source_dir: Path, backup_dir: Path) -> Path:
    """Copy a complete directory tree to a new backup destination."""
    if not source_dir.exists() or not source_dir.is_dir():
        raise NotADirectoryError(f"Source directory does not exist: {source_dir}")

    if backup_dir.exists():
        raise FileExistsError(f"Backup destination already exists: {backup_dir}")

    backup_dir.parent.mkdir(parents=True, exist_ok=True)
    return Path(shutil.copytree(source_dir, backup_dir))


def create_zip_archive(source_dir: Path, archive_base: Path) -> Path:
    """Create a ZIP archive containing the source directory contents."""
    if not source_dir.exists() or not source_dir.is_dir():
        raise NotADirectoryError(f"Source directory does not exist: {source_dir}")

    archive_base.parent.mkdir(parents=True, exist_ok=True)

    # root_dir makes the contents of source_dir the root of the ZIP.
    archive_name = shutil.make_archive(
        str(archive_base),
        "zip",
        root_dir=str(source_dir),
    )
    return Path(archive_name)


def extract_zip_archive(archive_path: Path, destination_dir: Path) -> Path:
    """Extract a trusted archive to a new destination folder."""
    if not archive_path.exists() or not archive_path.is_file():
        raise FileNotFoundError(f"Archive does not exist: {archive_path}")

    if destination_dir.exists():
        raise FileExistsError(f"Extraction destination already exists: {destination_dir}")

    destination_dir.mkdir(parents=True, exist_ok=True)
    shutil.unpack_archive(str(archive_path), str(destination_dir))
    return destination_dir
