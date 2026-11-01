# =============================================================
# LESSON 02 - ALL THE WAYS TO READ A FILE
# File used: story.txt
# =============================================================
#   read()       -> whole file as ONE string
#   read(n)      -> only n characters
#   readline()   -> ONE line
#   readlines()  -> ALL lines as a LIST
#   for line in file -> one line at a time (best for big files)

import os

# Changes the working directory to the folder where this specific script is saved.
# This prevents "File Not Found" errors, regardless of where you run the script from.
os.chdir(os.path.dirname(os.path.abspath(__file__)))


print("===== 1. read(n): read only some characters =====")
# Opens the file in default 'read' mode using UTF-8 text encoding
with open("story.txt", encoding="utf-8") as f:
    # Reads and prints the first 10 characters from the file
    print(repr(f.read(10)))   
    # Reads and prints the NEXT 10 characters. Python remembers where it left off!
    print(repr(f.read(10)))   
# repr() shows hidden characters like \n (new line) precisely as they are stored


print("\n===== 2. readline(): one line at a time =====")
with open("story.txt", encoding="utf-8") as f:
    # Reads up until it hits a newline character (\n) and grabs the 1st line
    line1 = f.readline()
    # Reads from the cursor position up to the next \n and grabs the 2nd line
    line2 = f.readline()
    
    print("Line 1:", repr(line1))
    print("Line 2:", repr(line2))
# Notice every line ends with '\n'


print("\n===== 3. readlines(): all lines in a list =====")
with open("story.txt", encoding="utf-8") as f:
    # Reads the entire file at once and splits it into a Python list of strings
    lines = f.readlines()

# Prints the variable type, which will be <class 'list'>
print("Type:", type(lines))
# Counts the number of items (lines) inside the list
print("How many lines:", len(lines))
# Accesses index 0 (the first line) and removes trailing whitespace/\n
print("First line:", lines[0].strip())   # strip() removes the '\n'
# Accesses index -1 (the last line) and removes trailing whitespace/\n
print("Last line :", lines[-1].strip())  # -1 means the last item


print("\n===== 4. for loop: the most common way =====")
with open("story.txt", encoding="utf-8") as f:
    # Iterates over the file object directly, loading only one line into memory at a time
    for line in f:
        # Prints the current line without its default trailing newline character
        print(line.strip())
        # Checks if the substring "box" exists anywhere in the current line
        if "box" in line:                # stop when we reach 'box'
            print("...found the word 'box', stopping.")
            # Exits the loop immediately, closing the file loop early
            break


print("\n===== 5. enumerate(): add line numbers =====")
with open("story.txt", encoding="utf-8") as f:
    # Wraps the file iterator to track line counts automatically, starting the count at 1
    for number, line in enumerate(f, start=1):
        # Checks if we have processed more than 5 lines
        if number > 5:
            # Breaks the loop if we pass line 5
            break
        # Prints the line number formatted to take 2 spaces ':2' next to the stripped text
        print(f"{number:2}: {line.strip()}")


print("\n===== 6. read().splitlines(): list WITHOUT \\n =====")
with open("shopping.txt", encoding="utf-8") as f:
    # f.read() reads everything as one huge string; .splitlines() splits it by newlines
    # while automatically throwing away the '\n' tags entirely.
    items = f.read().splitlines()

# Slices and prints just the first 5 elements of the clean items list
print(items[:5])

# Note: When the file ends (EOF), read() and readline() return "" (an empty string).
