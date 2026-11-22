from pathlib import Path

# Create a folder and a file.
folder = Path("pathlib_practice")
folder.mkdir(exist_ok=True)

file_path = folder / "notes.txt"
file_path.write_text("Learning pathlib", encoding="utf-8")

print("File exists:", file_path.exists())
print("Is a file:", file_path.is_file())
print("File name:", file_path.name)
print("File suffix:", file_path.suffix)
print("Parent folder:", file_path.parent)
print("File content:", file_path.read_text(encoding="utf-8"))

print("Python files in current folder:", list(Path(".").glob("*.py")))
