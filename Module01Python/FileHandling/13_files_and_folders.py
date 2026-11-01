# =============================================================
# LESSON 13 - FILES AND FOLDERS (os, shutil, pathlib)
# Creates and then cleans up: output/practice/
# =============================================================

import os
import shutil
from pathlib import Path

# Changes the working directory to the folder containing this script to avoid path errors.
os.chdir(os.path.dirname(os.path.abspath(__file__)))


print("===== 1. Where am I? =====")
# os.getcwd() (Get Current Working Directory) prints out the absolute terminal folder path path where Python is executing.
print("Current folder:", os.getcwd())


print("\n===== 2. List files in a folder =====")
# os.listdir(".") grabs all filesystem contents in the current directory, and sorts them alphabetically.
for name in sorted(os.listdir(".")):
    # Checks if the file name ends with any of the valid extension strings within the matching tuple.
    if name.endswith((".txt", ".csv", ".json")):
        # Returns the total physical size layout of the matching filename item measured directly in bytes.
        size = os.path.getsize(name)
        # Formats the string: pushes the name left by 15 spaces and aligns the size to the right by 5 spaces.
        print(f"  {name:<15} {size:>5} bytes")


print("\n===== 3. Check a path =====")
# Returns True if the specified route exists as either a file or a folder directory.
print("exists  :", os.path.exists("notes.txt"))
# Returns True if the specified location maps directly to a literal file entity.
print("is file :", os.path.isfile("notes.txt"))
# Returns True if the specified path points explicitly to an operational folder container directory.
print("is folder:", os.path.isdir("output"))


print("\n===== 4. Make folders =====")
# Creates the entire target tree pathway. 
# exist_ok=True prevents code crashes if the directories are already present on disk.
os.makedirs("output/practice/inner", exist_ok=True)
# makedirs creates all folders in the path.
# exist_ok=True means: don't complain if it already exists.
print("Created output/practice/inner")


print("\n===== 5. Copy, rename, delete files =====")
# shutil.copy(source, destination) duplicates the target file content stream and attributes over to the destination path.
shutil.copy("notes.txt", "output/practice/notes_copy.txt")   # copy
# os.rename(old, new) modifies the file pointer location tag or changes its name directly on the storage disk.
os.rename("output/practice/notes_copy.txt",
          "output/practice/renamed.txt")                     # rename
print("Files now:", os.listdir("output/practice"))
# os.remove(path) deletes an individual target file structure directly off the hard drive.
os.remove("output/practice/renamed.txt")                     # delete
print("After delete:", os.listdir("output/practice"))


print("\n===== 6. Split a path into parts =====")
# Sample complex directory string path path assignment.
path = "output/practice/report.final.txt"
# Returns the upper folder directory routing section of the string, dropping the base filename.
print("folder   :", os.path.dirname(path))
# Returns the bottom base file name element of the path string, dropping the folder routes.
print("file name:", os.path.basename(path))
# Splitting structure that isolates the absolute root path map away from its final extension trailing tag.
print("name+ext :", os.path.splitext(path))
# Intelligently concatenates directory tokens together using the target OS specific line separator tag (\ or /).
print("joined   :", os.path.join("output", "practice", "a.txt"))


print("\n===== 7. pathlib: the modern way =====")
# Instantiates an objective Path tracking wrapper module object targeting students.csv.
p = Path("students.csv")
# Returns the absolute complete file descriptor text value string including extension matching.
print("name  :", p.name)
# Returns the base file item name text string value without its trailing file type suffix.
print("stem  :", p.stem)       # name without extension
# Returns the specific dot notation extension classification metadata characters of the item.
print("suffix:", p.suffix)     # extension
# Performs a contextual object lookup query to check if the route entity is online on the system.
print("exists:", p.exists())
# Uses the custom forward slash operator syntax logic of pathlib to build paths safely across operating systems.
new = Path("output") / "practice" / "hello.txt"   # the / operator joins paths
# A short path method that automatically manages opening, writing a string block, and closing the target file resource.
new.write_text("Hi from pathlib!\n", encoding="utf-8")
# A simple path method that automatically opens, pulls down all inner file text data, and safely closes the resource.
print("read  :", new.read_text(encoding="utf-8").strip())
# Uses glob matching to search the location path and pull a list of names for all entries containing the .txt suffix.
print("all .txt files:", sorted(f.name for f in Path(".").glob("*.txt")))


print("\n===== 8. Walk through every folder =====")
# Recalls a top-down tree generation loop iterator returning the current root path, subfolders lists, and files.
for folder, subfolders, files in os.walk("output"):
    print(folder, "->", files)


print("\n===== 9. Delete a whole folder =====")
# shutil.rmtree (Remove Tree) completely obliterates the entire target directory along with all its nested contents.
shutil.rmtree("output/practice")     # careful: deletes everything inside!
# Re-checks path locations to verify the absolute removal state of the targeted test folder asset.
print("practice folder exists?", os.path.exists("output/practice"))
