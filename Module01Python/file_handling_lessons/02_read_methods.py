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
os.chdir(os.path.dirname(os.path.abspath(__file__)))


print("===== 1. read(n): read only some characters =====")
with open("story.txt", encoding="utf-8") as f:
    print(repr(f.read(10)))   # first 10 characters
    print(repr(f.read(10)))   # NEXT 10 characters (it continues!)
# repr() shows hidden characters like \n (new line)


print("\n===== 2. readline(): one line at a time =====")
with open("story.txt", encoding="utf-8") as f:
    line1 = f.readline()
    line2 = f.readline()
    print("Line 1:", repr(line1))
    print("Line 2:", repr(line2))
# Notice every line ends with '\n'


print("\n===== 3. readlines(): all lines in a list =====")
with open("story.txt", encoding="utf-8") as f:
    lines = f.readlines()
print("Type:", type(lines))
print("How many lines:", len(lines))
print("First line:", lines[0].strip())   # strip() removes the '\n'
print("Last line :", lines[-1].strip())  # -1 means the last item


print("\n===== 4. for loop: the most common way =====")
with open("story.txt", encoding="utf-8") as f:
    for line in f:
        print(line.strip())
        if "box" in line:                # stop when we reach 'box'
            print("...found the word 'box', stopping.")
            break


print("\n===== 5. enumerate(): add line numbers =====")
with open("story.txt", encoding="utf-8") as f:
    for number, line in enumerate(f, start=1):
        if number > 5:
            break
        print(f"{number:2}: {line.strip()}")


print("\n===== 6. read().splitlines(): list WITHOUT \\n =====")
with open("shopping.txt", encoding="utf-8") as f:
    items = f.read().splitlines()
print(items[:5])

# When the file ends, read() and readline() return "" (empty string).
