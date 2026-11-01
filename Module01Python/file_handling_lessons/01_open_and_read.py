# =============================================================
# LESSON 01 - OPEN, READ AND CLOSE A FILE
# File used: notes.txt
# =============================================================
# A file is data saved on your computer. To use it in Python:
#   1. OPEN the file   -> open()
#   2. READ the data   -> .read()
#   3. CLOSE the file  -> .close()

import os  # Imports the built-in operating system module to work with files and paths

# Changes the current working directory to the directory where this script file is saved
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # look for files in THIS folder


# ---------- Way 1: open -> read -> close ----------
# Prints a header section to the terminal for the first example method
print("===== Way 1: open, read, close =====")

# Opens 'notes.txt' in read-only ("r") mode using UTF-8 character encoding, saving it to a variable
file = open("notes.txt", "r", encoding="utf-8")
#            file name   mode  encoding (always use utf-8)

content = file.read()  # Reads the entire content of the file and stores it as a single string variable
file.close()  # Closes the file object to free up system resources immediately

print(content)  # Prints the full contents of the file that were stored in the content variable
print(
    "Type of content:", type(content)
)  # Displays the data type of the content variable (<class 'str'>)
print(
    "Is the file closed?", file.closed
)  # Checks and prints the boolean status of whether the file object is closed (True)


# ---------- Way 2: the 'with' statement (BEST way) ----------
# Prints a header section to the terminal for the recommended context manager method
print("\n===== Way 2: with statement =====")
# 'with' closes the file for you automatically, even if an error happens.

# Opens 'notes.txt' using a 'with' block, which assigns the open file object to the variable 'file'
with open("notes.txt", "r", encoding="utf-8") as file:
    content = (
        file.read()
    )  # Reads the entire file content into the content variable while inside the block
    print(
        "Inside with -> closed?", file.closed
    )  # Confirms that the file is still open (False) while inside the block

print(
    "Outside with -> closed?", file.closed
)  # Confirms that the file was automatically closed (True) after exiting the block
print(
    "Number of characters:", len(content)
)  # Counts and prints the total number of characters in the content string


# ---------- 'r' is the default mode ----------
# Prints a header section to the terminal demonstrating default parameter values
print("\n===== Mode 'r' is the default =====")
# Opens 'story.txt' without providing a second argument; Python defaults the file mode to read-only ("r")
with open("story.txt", encoding="utf-8") as file:  # no mode = "r"
    # Reads the file text, extracts a slice of the first 80 characters, and prints it with an ellipsis
    print(file.read()[:80], "...")  # first 80 characters only

# REMEMBER:
#   open(name, "r", encoding="utf-8")  -> opens a file for reading
#   file.read()                        -> whole file as a string
#   file.close()                       -> closes it
#   with open(...) as file:            -> opens AND auto-closes (use this!)
