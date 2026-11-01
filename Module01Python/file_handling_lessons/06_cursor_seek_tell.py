# =============================================================
# LESSON 06 - THE FILE CURSOR: tell(), seek(), truncate()
# File used: shopping.txt   Creates: output/cut.txt
# =============================================================
# An open file has an invisible CURSOR (like the blinking line in Notepad).
# Every read moves it forward.
#   tell()      -> where is the cursor now? (a number)
#   seek(n)     -> move the cursor to position n
#   seek(0)     -> go back to the start
#   truncate(n) -> cut the file to n characters

import os

# Changes the working directory to the script's folder to ensure reliable file paths.
os.chdir(os.path.dirname(os.path.abspath(__file__)))
# Creates an 'output' directory if it doesn't already exist.
os.makedirs("output", exist_ok=True)


print("===== tell() =====")
with open("shopping.txt", encoding="utf-8") as f:
    # f.tell() returns the current position of the file pointer (0 at the start of a fresh file)
    print("At start:", f.tell())
    # Reads the first line, moving the internal pointer forward by the length of that line
    print("Read    :", f.readline().strip())
    # Prints the updated byte position where the next read operation will begin
    print("Now at  :", f.tell())
    # Reads the second line, advancing the pointer even further
    print("Read    :", f.readline().strip())
    # Prints the byte position after reading the second line
    print("Now at  :", f.tell())


print("\n===== seek(0): read the file twice =====")
with open("shopping.txt", encoding="utf-8") as f:
    # Reads the entire file, which leaves the pointer sitting at the absolute end (EOF)
    first_time = f.read()
    # Attempting to read again without moving the pointer results in an empty string ''
    print("Second read without seek:", repr(f.read()))  # '' empty - at the end!
    # Explicitly resets the pointer back to index 0 (the beginning of the file)
    f.seek(0)
    # Reads the whole file a second time starting from the newly reset position
    second_time = f.read()
    # Confirms that the two reads produced identical content strings
    print("Same after seek(0)?", first_time == second_time)


print("\n===== Save a position and come back to it =====")
with open("shopping.txt", encoding="utf-8") as f:
    # Reads and discards the first line to advance the pointer past it
    f.readline()
    # Saves the exact numeric position of the pointer right before line 2 starts
    saved = f.tell()              # remember this spot
    # Reads and prints line 2, moving the pointer past it
    print("Line 2:", f.readline().strip())
    # Reads and prints line 3, moving the pointer past it
    print("Line 3:", f.readline().strip())
    # Jumps the pointer back to the exact byte offset saved earlier
    f.seek(saved)                 # jump back
    # Reads line 2 again because the pointer was reset to the start of line 2
    print("Again line 2:", f.readline().strip())


print("\n===== seek from the END (binary mode) =====")
# In binary mode you can seek(offset, whence):
#   whence 0 = from start, 1 = from current place, 2 = from end
# Opens the file in "rb" (Read Binary) mode, which allows seeking relative to the end of the file
with open("shopping.txt", "rb") as f:
    # Moves the pointer 0 bytes relative to the end of the file (whence=2 means from the end)
    f.seek(0, 2)                  # jump to the end
    # Because the pointer is at the absolute end, tell() returns the total size of the file in bytes
    print("File size in bytes:", f.tell())
    # Moves the pointer 10 bytes backward (-10) relative to the end of the file (whence=2)
    f.seek(-10, 2)                # 10 bytes before the end
    # Reads and prints the remaining 10 bytes of binary data from the file
    print("Last 10 bytes:", f.read())


print("\n===== truncate(): cut a file =====")
# Opens a clean test file in write mode to populate it with a simple test string
with open("output/cut.txt", "w", encoding="utf-8") as f:
    f.write("ABCDEFGHIJKLMNOP")
# Opens the file in "r+" (Read/Write) mode so we can perform modification actions like truncate
with open("output/cut.txt", "r+", encoding="utf-8") as f:
    # Slices the file on the hard drive, dropping everything after the first 5 characters
    f.truncate(5)                 # keep only first 5 characters
# Opens the truncated file in regular read mode to verify the content reduction
with open("output/cut.txt", encoding="utf-8") as f:
    # Prints the remaining contents, which will just be "ABCDE"
    print("After truncate(5):", f.read())
