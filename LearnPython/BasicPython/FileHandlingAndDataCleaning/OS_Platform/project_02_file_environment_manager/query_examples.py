"""Small demonstrations of common os queries used in this project."""

import os


def show_folder_queries(folder):
    print("Folder exists:", os.path.exists(folder))
    print("Is directory:", os.path.isdir(folder))
    print("Absolute path:", os.path.abspath(folder))

    if os.path.isdir(folder):
        print("Direct entries:", os.listdir(folder))


def show_file_queries(file_path):
    print("Path exists:", os.path.exists(file_path))
    print("Is regular file:", os.path.isfile(file_path))

    if os.path.isfile(file_path):
        print("Base name:", os.path.basename(file_path))
        print("Parent folder:", os.path.dirname(file_path))
        print("Extension:", os.path.splitext(file_path)[1])
        print("Size in bytes:", os.stat(file_path).st_size)


if __name__ == "__main__":
    # Paths are relative to this script's project folder.
    project_dir = os.path.dirname(os.path.abspath(__file__))
    input_dir = os.path.join(project_dir, "data", "input")
    sample_file = os.path.join(input_dir, "notes.txt")

    print("--- Folder queries ---")
    show_folder_queries(input_dir)

    print("\n--- File queries ---")
    show_file_queries(sample_file)
