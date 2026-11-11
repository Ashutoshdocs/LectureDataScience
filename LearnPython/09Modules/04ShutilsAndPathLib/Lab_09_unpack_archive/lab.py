import shutil
from pathlib import Path

# Prepare an archive for this standalone lab.
project = Path("project")
project.mkdir(exist_ok=True)
(project / "app.txt").write_text("Application file", encoding="utf-8")
shutil.make_archive("project_backup", "zip", root_dir=".", base_dir="project")

# Extract into a new destination folder.
shutil.unpack_archive("project_backup.zip", "extracted_project")

print([item.name for item in Path("extracted_project").iterdir()])
print((Path("extracted_project") / "app.txt").read_text(encoding="utf-8"))
