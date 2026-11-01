# =============================================================
# LESSON 05 - ALL FILE MODES
# Creates: output/modes.txt
# =============================================================
#  mode | what it does                | file missing | file exists
#  -----+-----------------------------+--------------+----------------
#  "r"  | read only                   | ERROR        | read from start
#  "w"  | write only                  | create       | ERASE then write
#  "a"  | append only                 | create       | add at end
#  "x"  | create new only             | create       | ERROR
#  "r+" | read + write                | ERROR        | start at beginning
#  "w+" | write + read                | create       | ERASE first
#  "a+" | append + read               | create       | add at end
#  Add "b" for binary files: "rb", "wb", "ab" (see lesson 14)

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.makedirs("output", exist_ok=True)
path = "output/modes.txt"

if os.path.exists(path):
    os.remove(path)          # start clean every time you run this lesson


print("===== 'x' : create only if it does not exist =====")
with open(path, "x", encoding="utf-8") as f:
    f.write("Created with x mode\n")
print("Created the file.")

try:
    with open(path, "x", encoding="utf-8") as f:
        f.write("This will not happen")
except FileExistsError:
    print("Second time -> FileExistsError (x protects existing files)")


print("\n===== 'r+' : read and write =====")
with open(path, "r+", encoding="utf-8") as f:
    print("Read :", f.read().strip())
    f.write("Added with r+\n")       # cursor was at the end after read()
with open(path, encoding="utf-8") as f:
    print(f.read())


print("===== 'w+' : erase, write, then read back =====")
with open(path, "w+", encoding="utf-8") as f:
    f.write("Fresh content from w+\n")
    f.seek(0)                        # go back to the start before reading
    print("Read back:", f.read().strip())


print("\n===== 'a+' : add at end, and read =====")
with open(path, "a+", encoding="utf-8") as f:
    f.write("Added with a+\n")
    f.seek(0)
    print(f.read())


print("===== 'r' on a missing file =====")
try:
    open("output/does_not_exist.txt", "r")
except FileNotFoundError:
    print("FileNotFoundError: 'r' needs the file to exist")
