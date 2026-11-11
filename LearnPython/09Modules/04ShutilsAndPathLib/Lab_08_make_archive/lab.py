import shutil
from pathlib import Path

# Prepare a small project directory.
project = Path("project")
project.mkdir(exist_ok=True)
(project / "app.txt").write_text("Application file", encoding="utf-8")
(project / "notes.txt").write_text("Project notes", encoding="utf-8")

# Creates project_backup.zip in the current folder.
archive_path = shutil.make_archive(
    "project_backup",
    "zip",
    root_dir=".",
    base_dir="project"
)

print("Created:", archive_path)
print("ZIP exists:", Path(archive_path).exists())
