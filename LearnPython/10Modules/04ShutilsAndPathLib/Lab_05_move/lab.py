import shutil
from pathlib import Path

# Prepare a source file and destination folder for this standalone lab.
Path("source.txt").write_text("File to move", encoding="utf-8")
Path("backup_folder").mkdir(exist_ok=True)

shutil.move("source.txt", "backup_folder/source.txt")

print(Path("backup_folder/source.txt").exists())
print(Path("source.txt").exists())
