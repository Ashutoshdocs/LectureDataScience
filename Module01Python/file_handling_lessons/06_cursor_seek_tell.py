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
os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.makedirs("output", exist_ok=True)


print("===== tell() =====")
with open("shopping.txt", encoding="utf-8") as f:
    print("At start:", f.tell())
    print("Read    :", f.readline().strip())
    print("Now at  :", f.tell())
    print("Read    :", f.readline().strip())
    print("Now at  :", f.tell())


print("\n===== seek(0): read the file twice =====")
with open("shopping.txt", encoding="utf-8") as f:
    first_time = f.read()
    print("Second read without seek:", repr(f.read()))  # '' empty - at the end!
    f.seek(0)
    second_time = f.read()
    print("Same after seek(0)?", first_time == second_time)


print("\n===== Save a position and come back to it =====")
with open("shopping.txt", encoding="utf-8") as f:
    f.readline()
    saved = f.tell()              # remember this spot
    print("Line 2:", f.readline().strip())
    print("Line 3:", f.readline().strip())
    f.seek(saved)                 # jump back
    print("Again line 2:", f.readline().strip())


print("\n===== seek from the END (binary mode) =====")
# In binary mode you can seek(offset, whence):
#   whence 0 = from start, 1 = from current place, 2 = from end
with open("shopping.txt", "rb") as f:
    f.seek(0, 2)                  # jump to the end
    print("File size in bytes:", f.tell())
    f.seek(-10, 2)                # 10 bytes before the end
    print("Last 10 bytes:", f.read())


print("\n===== truncate(): cut a file =====")
with open("output/cut.txt", "w", encoding="utf-8") as f:
    f.write("ABCDEFGHIJKLMNOP")
with open("output/cut.txt", "r+", encoding="utf-8") as f:
    f.truncate(5)                 # keep only first 5 characters
with open("output/cut.txt", encoding="utf-8") as f:
    print("After truncate(5):", f.read())
