"""
STEP 0 - Learn Python file reading and writing.

Input:
    raw_data.txt

Output:
    outputs/step0_report.txt

This step demonstrates:
- open() and close()
- with open(...)
- read(), readline(), and readlines()
- looping through a file
- write mode ("w") and append mode ("a")
- creating an output directory
"""

import os
from pathlib import Path

# Use the folder containing this script as the project directory.
BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "raw_data.txt"
OUTPUT_DIR = BASE_DIR / "outputs"

# ---------------------------------------------------------
# 1. Open, read, and close a file manually
# ---------------------------------------------------------
# The default mode is "r" (read).
file = open(INPUT_FILE, encoding="utf-8")
text = file.read()  # read() returns the complete file as one string.
file.close()        # Close the file after reading.

print(type(text))
print(len(text), "characters")

# ---------------------------------------------------------
# 2. Use with open() - recommended approach
# ---------------------------------------------------------
# The file is closed automatically when the with block ends.
with open(INPUT_FILE, encoding="utf-8") as file:
    text = file.read()

print("First 120 characters:")
print(text[:120])

# ---------------------------------------------------------
# 3. Read one line at a time
# ---------------------------------------------------------
with open(INPUT_FILE, encoding="utf-8") as file:
    first = file.readline()   # Reads only the first line.
    second = file.readline()  # Reads the next line.

# repr() makes spaces and newline characters visible.
print("First line:", repr(first))
print("Second line:", repr(second))

# ---------------------------------------------------------
# 4. Read all lines into a list
# ---------------------------------------------------------
with open(INPUT_FILE, encoding="utf-8") as file:
    lines = file.readlines()

print("Total lines:", len(lines))
print("First five lines:", lines[:5])

# ---------------------------------------------------------
# 5. Loop over a file line by line
# ---------------------------------------------------------
blank_line_count = 0

with open(INPUT_FILE, encoding="utf-8") as file:
    for line in file:
        # strip() removes surrounding spaces, tabs, and newline characters.
        if line.strip() == "":
            blank_line_count += 1

print("Blank lines:", blank_line_count)

# ---------------------------------------------------------
# 6. Create the output folder
# ---------------------------------------------------------
# exist_ok=True prevents an error if the folder already exists.
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ---------------------------------------------------------
# 7. Write a report using mode "w"
# ---------------------------------------------------------
# "w" creates a new file or overwrites an existing file.
report_file = OUTPUT_DIR / "step0_report.txt"

with open(report_file, "w", encoding="utf-8") as file:
    file.write("Raw data report\n")
    file.write(f"Characters: {len(text)}\n")
    file.write(f"Lines: {len(lines)}\n")
    file.write(f"Blank lines: {blank_line_count}\n")

# ---------------------------------------------------------
# 8. Append more content using mode "a"
# ---------------------------------------------------------
# "a" adds content to the end without replacing existing content.
with open(report_file, "a", encoding="utf-8") as file:
    file.write("First line: " + lines[0].strip() + "\n")

# Read the report back to verify that it was created.
print(report_file.read_text(encoding="utf-8"))
print(f"Saved: {report_file}")
