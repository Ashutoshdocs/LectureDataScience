import glob
from pathlib import Path


def find_by_pattern(search_root: Path, pattern: str, recursive: bool = False):
    """Return sorted matching path strings beneath the given search root."""
    search_pattern = str(search_root / pattern)
    return sorted(glob.glob(search_pattern, recursive=recursive))


def find_recursively_with_iterator(search_root: Path, pattern: str):
    """Yield matches lazily using glob.iglob()."""
    search_pattern = str(search_root / pattern)
    yield from glob.iglob(search_pattern, recursive=True)


def find_csv_files(search_root: Path):
    """Find CSV files at any depth."""
    return find_by_pattern(search_root, "**/*.csv", recursive=True)
