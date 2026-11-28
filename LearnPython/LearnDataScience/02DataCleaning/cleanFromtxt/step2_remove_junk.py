"""
STEP 2 - Remove unwanted Instagram button text.

Input:
    outputs/step1_stripped.txt

Output:
    outputs/step2_no_junk.txt

The copied profile text contains button labels such as Follow and Message.
This step removes those lines without changing the other profile data.
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "outputs" / "step1_stripped.txt"
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

# Read the cleaned lines created by Step 1.
with open(INPUT_FILE, encoding="utf-8") as file:
    lines = file.read().split("\n")

# A set makes it easy to check whether a line is unwanted.
junk_lines = {"Follow", "Message"}

# Count the unwanted lines before removing them.
junk_count = sum(1 for line in lines if line in junk_lines)
print("Junk lines found:", junk_count)

# Keep only lines that are not in the junk_lines set.
clean_lines = [line for line in lines if line not in junk_lines]

# Write the remaining lines to a new file.
output_file = OUTPUT_DIR / "step2_no_junk.txt"

with open(output_file, "w", encoding="utf-8") as file:
    file.write("\n".join(clean_lines))

print(f"Saved: {output_file}")
