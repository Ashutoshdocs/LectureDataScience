import shutil
from pathlib import Path

Path("source.txt").write_text("Hello Python", encoding="utf-8")

# copy2() attempts to preserve metadata such as modification time.
shutil.copy2("source.txt", "backup2.txt")

print(Path("backup2.txt").read_text(encoding="utf-8"))
