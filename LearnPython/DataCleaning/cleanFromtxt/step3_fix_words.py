"""
STEP 3 - Standardise count words.

Input:
    outputs/step2_no_junk.txt

Output:
    outputs/step3_fixed_words.txt

Example:
    1,240 POSTS     -> 1,240 posts
    18.6K Followers -> 18.6K followers

Only the final count label is changed. The number is preserved.
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "outputs" / "step2_no_junk.txt"
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

# Read the lines created by Step 2.
with open(INPUT_FILE, encoding="utf-8") as file:
    lines = file.read().split("\n")

# These are the count labels that should be lowercase.
count_words = ("post", "posts", "follower", "followers", "following")

fixed_lines = []

for line in lines:
    # rsplit(" ", 1) splits at the final space, starting from the right.
    # For "18.6K Followers", the result is ["18.6K", "Followers"].
    parts = line.rsplit(" ", 1)

    # Continue only when the line has a number part and a final word.
    if len(parts) == 2 and parts[1].lower() in count_words:
        # Lowercase the label, but leave the number such as 18.6K unchanged.
        new_line = parts[0] + " " + parts[1].lower()

        # Print only lines that were actually modified.
        if new_line != line:
            print(f"{line!r:24} -> {new_line}")

        line = new_line

    fixed_lines.append(line)

# Save the standardised text.
output_file = OUTPUT_DIR / "step3_fixed_words.txt"

with open(output_file, "w", encoding="utf-8") as file:
    file.write("\n".join(fixed_lines))

print(f"Saved: {output_file}")
