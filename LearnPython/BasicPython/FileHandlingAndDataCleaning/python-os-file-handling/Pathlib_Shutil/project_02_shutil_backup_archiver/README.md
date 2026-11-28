# Project 2 — Shutil Backup and Archiver

## Goal

Build a small backup utility that copies a controlled source folder, creates a ZIP archive, extracts it into a restore folder, and records what happened.

The project uses:
- `pathlib` to define and inspect paths.
- `shutil.copy2()` to copy individual files.
- `shutil.copytree()` to copy the source directory tree.
- `shutil.make_archive()` to create a ZIP.
- `shutil.unpack_archive()` to extract the ZIP.
- `shutil.disk_usage()` to report disk capacity.

## Folder layout

```text
project_02_shutil_backup_archiver/
├── README.md
├── main.py
├── backup_manager.py
├── data/
│   ├── source/
│   │   ├── report.txt
│   │   └── records.csv
│   └── destination/
├── backups/
├── archives/
└── logs/
```

## Run

From repository root:

```bash
python project_02_shutil_backup_archiver/main.py
```

Or:

```bash
cd project_02_shutil_backup_archiver
python main.py
```

## Expected result

After a successful run:
- `backups/source_snapshot/` contains a directory copy of source data.
- `archives/source_backup.zip` contains a ZIP archive.
- `data/destination/restored/` contains the extracted archive contents.
- `logs/backup.log` contains operation messages.

The source files remain untouched.

## Queries demonstrated

```python
Path(__file__).resolve().parent  # Project root
source.exists()                  # Verify source path
source.is_dir()                  # Verify it is a directory
shutil.copy2(src, dst)           # Copy file with metadata attempt
shutil.copytree(src, dst)        # Copy complete directory tree
shutil.make_archive(...)         # Create archive
shutil.unpack_archive(...)       # Extract archive
shutil.disk_usage(path)          # Inspect disk usage
```

## Student exercises

1. Add a timestamp to each backup folder name.
2. Copy only `.csv` files into a separate backup folder.
3. Skip hidden files.
4. Compare source and backup file counts.
5. Calculate total source size in bytes.
6. Add a dry-run mode that prints intended operations without changing files.
7. Create a second archive with a different supported format.
8. Restore to a new folder and compare the restored file names with the originals.
9. Add a confirmation prompt before replacing any existing backup.
10. Add a checksum comparison for file integrity.

## Safety notes

- This lab never deletes the original source.
- `copytree()` normally expects the destination not to exist.
- `rmtree()` is intentionally not called by the default program.
- Only extract archives you trust.
- A copied folder or ZIP file is not a complete enterprise backup strategy. Production backups need retention, access control, integrity verification, off-site copies, and restore testing.
