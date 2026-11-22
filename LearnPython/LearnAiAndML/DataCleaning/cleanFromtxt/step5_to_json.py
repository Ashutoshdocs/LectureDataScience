"""
STEP 5 - Convert cleaned text profiles into structured JSON.

Input:
    outputs/step4_cleaned.txt

Output:
    outputs/step5_clean_data.json

This step:
- Converts comma-separated, K, and M count values into integers.
- Creates one dictionary for each profile.
- Saves all profile dictionaries as JSON.
"""

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "outputs" / "step4_cleaned.txt"
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)


def to_number(value):
    """
    Convert profile counts into integers.

    Examples:
        "2,300" -> 2300
        "18.6K" -> 18600
        "1.2M"  -> 1200000
    """
    # Remove commas before converting the value.
    value = value.replace(",", "")

    if value.endswith("K"):
        # K means thousand.
        return int(float(value[:-1]) * 1_000)

    if value.endswith("M"):
        # M means million.
        return int(float(value[:-1]) * 1_000_000)

    # If there is no K or M suffix, convert directly.
    return int(value)


def parse_profile(chunk):
    """
    Convert one profile's block of text into a dictionary.

    The profile lines are expected in this order:
    username, posts, followers, following, name, category, bio.
    """
    lines = chunk.split("\n")

    return {
        "username": lines[0],
        "posts": to_number(lines[1].split(" ")[0]),
        "followers": to_number(lines[2].split(" ")[0]),
        "following": to_number(lines[3].split(" ")[0]),
        "name": lines[4],
        # Some profiles do not have a category line.
        "category": lines[5] if len(lines) > 5 else "Unknown",
        # Remaining lines are combined into the profile bio.
        "bio": "\n".join(lines[6:]),
    }


# Read the cleaned text file created by Step 4.
with open(INPUT_FILE, encoding="utf-8") as file:
    cleaned_text = file.read().strip()

# Each profile is separated by one blank line (two newline characters).
profile_chunks = cleaned_text.split("\n\n")

# Convert every profile block into a Python dictionary.
data = [parse_profile(chunk) for chunk in profile_chunks]

# Save the list of dictionaries as JSON.
output_file = OUTPUT_DIR / "step5_clean_data.json"

with open(output_file, "w", encoding="utf-8") as file:
    # ensure_ascii=False keeps emojis and accented characters readable.
    json.dump(data, file, indent=4, ensure_ascii=False)

print("Saved", len(data), "profiles")
print("First profile:")
print(json.dumps(data[0], indent=4, ensure_ascii=False))
print(f"Saved: {output_file}")
