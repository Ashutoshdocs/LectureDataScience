import shutil
from pathlib import Path

project = Path("project")
project.mkdir(exist_ok=True)
(project / "app.txt").write_text("Application file", encoding="utf-8")

# The destination must not already exist.
shutil.copytree("project", "project_backup")

print(list(Path("project_backup").iterdir()))
print((Path("project_backup") / "app.txt").read_text(encoding="utf-8"))
