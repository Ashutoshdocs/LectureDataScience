# =============================================================
# LESSON 01 - OPEN, READ AND CLOSE A FILE
# File used: notes.txt
# =============================================================
# A file is data saved on your computer. To use it in Python:
#   1. OPEN the file   -> open()
#   2. READ the data   -> .read()
#   3. CLOSE the file  -> .close()

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # look for files in THIS folder


# ---------- Way 1: open -> read -> close ----------
print("===== Way 1: open, read, close =====")

file = open("notes.txt", "r", encoding="utf-8")
#            file name   mode  encoding (always use utf-8)

content = file.read()      # reads the WHOLE file into one string
file.close()               # always close the file when finished

print(content)
print("Type of content:", type(content))   # <class 'str'>
print("Is the file closed?", file.closed)  # True


# ---------- Way 2: the 'with' statement (BEST way) ----------
print("\n===== Way 2: with statement =====")
# 'with' closes the file for you automatically, even if an error happens.

with open("notes.txt", "r", encoding="utf-8") as file:
    content = file.read()
    print("Inside with -> closed?", file.closed)   # False

print("Outside with -> closed?", file.closed)      # True
print("Number of characters:", len(content))


# ---------- 'r' is the default mode ----------
print("\n===== Mode 'r' is the default =====")
with open("story.txt", encoding="utf-8") as file:   # no mode = "r"
    print(file.read()[:80], "...")                  # first 80 characters only

# REMEMBER:
#   open(name, "r", encoding="utf-8")  -> opens a file for reading
#   file.read()                        -> whole file as a string
#   file.close()                       -> closes it
#   with open(...) as file:            -> opens AND auto-closes (use this!)
