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

# Changes the working directory to the folder containing this script to avoid path issues.
os.chdir(os.path.dirname(os.path.abspath(__file__)))
# Creates an 'output' directory if it doesn't already exist.
os.makedirs("output", exist_ok=True)
# Saves the path to the target text file in a variable for clean re-use.
path = "output/modes.txt"

# Checks if the file already exists from a previous script execution.
if os.path.exists(path):
    # Deletes the file entirely to ensure a consistent, clean test environment.
    os.remove(path)          # start clean every time you run this lesson


print("===== 'x' : create only if it does not exist =====")
# Opens in "x" (Exclusive Creation) mode. Creates a fresh file since we just deleted it.
with open(path, "x", encoding="utf-8") as f:
    # Writes initial text into the newly created file.
    f.write("Created with x mode\n")
print("Created the file.")

# Sets up a safety block to catch predictable runtime issues.
try:
    # Attempts to open the same file in "x" mode again, which is now an invalid operation.
    with open(path, "x", encoding="utf-8") as f:
        f.write("This will not happen")
# Catches the specific exception raised when an "x" mode target already exists.
except FileExistsError:
    # Executes this safety message instead of letting the program crash.
    print("Second time -> FileExistsError (x protects existing files)")


print("\n===== 'r+' : read and write =====")
# Opens in "r+" (Read and Write) mode. The file pointer starts at index 0.
with open(path, "r+", encoding="utf-8") as f:
    # Reads the entire file, which moves the internal pointer to the very end.
    print("Read :", f.read().strip())
    # Appends text right where the pointer is resting (at the end).
    f.write("Added with r+\n")       # cursor was at the end after read()

# Reopens the file in standard read mode to confirm both lines exist.
with open(path, encoding="utf-8") as f:
    print(f.read())


print("===== 'w+' : erase, write, then read back =====")
# Opens in "w+" (Write and Read) mode. Wipes out all text currently inside the file.
with open(path, "w+", encoding="utf-8") as f:
    # Writes new text into the empty file. The file pointer is now at the end of this sentence.
    f.write("Fresh content from w+\n")
    # Resets the file pointer back to index 0 so we can read from the beginning.
    f.seek(0)                        # go back to the start before reading
    # Reads and prints the content we just wrote.
    print("Read back:", f.read().strip())


print("\n===== 'a+' : add at end, and read =====")
# Opens in "a+" (Append and Read) mode. The write pointer forces new content to the absolute end.
with open(path, "a+", encoding="utf-8") as f:
    # Appends text to the end of the file.
    f.write("Added with a+\n")
    # Moves the read pointer back to index 0 (otherwise read() would see nothing but empty space).
    f.seek(0)
    # Reads and displays everything inside the file.
    print(f.read())


print("===== 'r' on a missing file =====")
try:
    # Attempts to open a non-existent file in default "r" (Read) mode.
    open("output/does_not_exist.txt", "r")
# Catches the standard error raised when a requested file cannot be located.
except FileNotFoundError:
    # Prints a confirmation that the file was missing.
    print("FileNotFoundError: 'r' needs the file to exist")
