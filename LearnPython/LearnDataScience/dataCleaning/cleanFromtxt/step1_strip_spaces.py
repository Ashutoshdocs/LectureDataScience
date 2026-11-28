"""
STEP 1 - Remove extra spaces and tabs from every line.

Input:
    raw_data.txt

Output:
    outputs/step1_stripped.txt

Concepts:
    split(), strip(), list comprehension, and join()
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "raw_data.txt"
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

# Read the complete raw file and split it into individual lines.
with open(INPUT_FILE, encoding="utf-8") as file:
    lines = file.read().split("\n")

print("BEFORE cleaning:")
print(lines[:6])

# strip() removes spaces and tabs from the beginning and end of each line.
# The list comprehension applies strip() to every line.
lines = [line.strip() for line in lines]

print("\nAFTER cleaning:")
print(lines[:6])

# join() combines the list back into one string with newline separators.
output_file = OUTPUT_DIR / "step1_stripped.txt"

with open(output_file, "w", encoding="utf-8") as file:
    file.write("\n".join(lines))

print(f"\nSaved: {output_file}")
