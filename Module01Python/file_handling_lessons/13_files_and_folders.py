# =============================================================
# LESSON 13 - FILES AND FOLDERS (os, shutil, pathlib)
# Creates and then cleans up: output/practice/
# =============================================================

import os
import shutil
from pathlib import Path
os.chdir(os.path.dirname(os.path.abspath(__file__)))


print("===== 1. Where am I? =====")
print("Current folder:", os.getcwd())


print("\n===== 2. List files in a folder =====")
for name in sorted(os.listdir(".")):
    if name.endswith((".txt", ".csv", ".json")):
        size = os.path.getsize(name)
        print(f"  {name:<15} {size:>5} bytes")


print("\n===== 3. Check a path =====")
print("exists  :", os.path.exists("notes.txt"))
print("is file :", os.path.isfile("notes.txt"))
print("is folder:", os.path.isdir("output"))


print("\n===== 4. Make folders =====")
os.makedirs("output/practice/inner", exist_ok=True)
# makedirs creates all folders in the path.
# exist_ok=True means: don't complain if it already exists.
print("Created output/practice/inner")


print("\n===== 5. Copy, rename, delete files =====")
shutil.copy("notes.txt", "output/practice/notes_copy.txt")   # copy
os.rename("output/practice/notes_copy.txt",
          "output/practice/renamed.txt")                     # rename
print("Files now:", os.listdir("output/practice"))
os.remove("output/practice/renamed.txt")                     # delete
print("After delete:", os.listdir("output/practice"))


print("\n===== 6. Split a path into parts =====")
path = "output/practice/report.final.txt"
print("folder   :", os.path.dirname(path))
print("file name:", os.path.basename(path))
print("name+ext :", os.path.splitext(path))
print("joined   :", os.path.join("output", "practice", "a.txt"))


print("\n===== 7. pathlib: the modern way =====")
p = Path("students.csv")
print("name  :", p.name)
print("stem  :", p.stem)       # name without extension
print("suffix:", p.suffix)     # extension
print("exists:", p.exists())
new = Path("output") / "practice" / "hello.txt"   # the / operator joins paths
new.write_text("Hi from pathlib!\n", encoding="utf-8")
print("read  :", new.read_text(encoding="utf-8").strip())
print("all .txt files:", sorted(f.name for f in Path(".").glob("*.txt")))


print("\n===== 8. Walk through every folder =====")
for folder, subfolders, files in os.walk("output"):
    print(folder, "->", files)


print("\n===== 9. Delete a whole folder =====")
shutil.rmtree("output/practice")     # careful: deletes everything inside!
print("practice folder exists?", os.path.exists("output/practice"))
