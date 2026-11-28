import csv
import os
import shutil


def list_files(folder):
    """List regular files directly inside a folder."""
    if not os.path.isdir(folder):
        raise NotADirectoryError(f"Folder does not exist: {folder}")

    return [
        name for name in os.listdir(folder)
        if os.path.isfile(os.path.join(folder, name))
    ]


def find_files_by_extension(folder, extension):
    """Find files with an extension, including in nested folders."""
    normalized_extension = extension.lower()
    if not normalized_extension.startswith("."):
        normalized_extension = "." + normalized_extension

    matches = []
    for root, directories, filenames in os.walk(folder):
        for filename in filenames:
            if os.path.splitext(filename)[1].lower() == normalized_extension:
                matches.append(os.path.join(root, filename))

    return matches


def read_text_file(path):
    """Read a UTF-8 text file and return its contents."""
    with open(path, "r", encoding="utf-8") as input_file:
        return input_file.read()


def read_csv_file(path):
    """Read CSV rows as dictionaries, using the header row as keys."""
    with open(path, "r", encoding="utf-8", newline="") as input_file:
        return list(csv.DictReader(input_file))


def copy_to_archive(source_path, archive_folder):
    """Copy a file into the archive folder without deleting the original."""
    os.makedirs(archive_folder, exist_ok=True)
    destination_path = os.path.join(archive_folder, os.path.basename(source_path))

    if os.path.exists(destination_path):
        raise FileExistsError(
            f"Archive already contains {os.path.basename(source_path)}"
        )

    shutil.copy2(source_path, destination_path)
    return destination_path
