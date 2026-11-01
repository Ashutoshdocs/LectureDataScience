# =============================================================
# LESSON 04 - APPENDING (mode "a") AND print() TO A FILE
# Creates: output/diary.txt
# =============================================================
# Mode "a" = append. It ADDS to the END of the file.
# Old content is KEPT. If the file is missing, it is created.

import os

# Changes the working directory to the folder containing this script to avoid path issues.
os.chdir(os.path.dirname(os.path.abspath(__file__)))
# Creates an 'output' directory if it doesn't already exist.
os.makedirs("output", exist_ok=True)


# Start with a fresh file
# Opens the file in "w" (Write) mode to clean out any old records and start fresh.
with open("output/diary.txt", "w", encoding="utf-8") as f:
    # Writes the first entry into the newly cleared file.
    f.write("Day 1: Learned to read files.\n")

print("===== 1. Append new lines =====")
# Opens the file in "a" (Append) mode. The file pointer is automatically placed at the very end.
with open("output/diary.txt", "a", encoding="utf-8") as f:
    # Adds Day 2 text right below Day 1 without erasing it.
    f.write("Day 2: Learned to write files.\n")
    # Adds Day 3 text straight after Day 2.
    f.write("Day 3: Learned to append.\n")

# Reopens the file in default read mode to print out the combined content.
with open("output/diary.txt", encoding="utf-8") as f:
    print(f.read())


print("===== 2. Append in a loop =====")
# Loops through numbers 4, 5, and 6 (range stops right before 7).
for day in range(4, 7):
    # Opens, appends to, and safely closes the file on every single loop iteration.
    with open("output/diary.txt", "a", encoding="utf-8") as f:
        # Appends a formatted f-string tracking the current loop number.
        f.write(f"Day {day}: Practised more.\n")

# Reopens the file to inspect the loop's output.
with open("output/diary.txt", encoding="utf-8") as f:
    print(f.read())


print("===== 3. print() can write to a file =====")
# print adds '\n' automatically and accepts numbers too.
# Opens the file in append mode once again.
with open("output/diary.txt", "a", encoding="utf-8") as f:
    # Uses print() instead of write(). The 'file=f' argument redirects output from the console into the file.
    print("Day 7:", "Used print with file=", file=f)
    # Automatically handles integer conversion (7) to text and adds a newline at the end.
    print("Total days:", 7, file=f)
    # The 'sep="-"' argument replaces the default space between arguments with a hyphen.
    print("A", "B", "C", sep="-", file=f)    # sep = what goes between items

# Reopens the file to print all contents including the new print()-generated rows.
with open("output/diary.txt", encoding="utf-8") as f:
    print(f.read())


print("===== 4. Copy shopping.txt items to a new file, adding a tick =====")
# Uses a backslash (\) to open two files at once: 'src' for reading and 'dst' for appending.
with open("shopping.txt", encoding="utf-8") as src, \
     open("output/diary.txt", "a", encoding="utf-8") as dst:
    # Reads through 'shopping.txt' line by line.
    for line in src:
        # Prepend a checkbox prefix to the raw line text and streams it straight into the diary file.
        dst.write("[x] " + line)
print("Done. Open output/diary.txt to see it.")

# SUMMARY:  "w" = erase and write    "a" = keep and add to end
