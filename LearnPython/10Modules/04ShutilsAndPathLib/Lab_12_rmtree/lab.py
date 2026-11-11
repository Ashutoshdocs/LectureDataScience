import shutil
from pathlib import Path

# Create a clearly named practice directory and a file inside it.
target = Path("project_backup")
target.mkdir(exist_ok=True)
(target / "app.txt").write_text("Temporary practice file", encoding="utf-8")

print("Exists before deletion:", target.exists())

# Safety: delete only the practice directory created above.
shutil.rmtree(target)

print("Exists after deletion:", target.exists())
