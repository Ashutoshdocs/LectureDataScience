import shutil
from pathlib import Path

Path("source.txt").write_text("Hello Python", encoding="utf-8")

# copyfile() copies the contents only.
shutil.copyfile("source.txt", "backup3.txt")

print(Path("backup3.txt").read_text(encoding="utf-8"))
