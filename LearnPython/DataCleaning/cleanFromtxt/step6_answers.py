"""
STEP 6 - Answer questions using the cleaned JSON profiles.

Input:
    outputs/step5_clean_data.json

Output:
    outputs/step6_answers.txt

Questions:
- Which profile has the most posts?
- Which profile has the most followers?
- Which profile follows the most people?
- How many profiles are in each category?
"""

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "outputs" / "step5_clean_data.json"
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

# Load the JSON file. json.load() converts JSON into Python objects.
with open(INPUT_FILE, encoding="utf-8") as file:
    data = json.load(file)

# ---------------------------------------------------------
# 1. Find the profile with the maximum values
# ---------------------------------------------------------
# max() checks each dictionary using the value specified by key.
most_posts = max(data, key=lambda profile: profile["posts"])
most_followers = max(data, key=lambda profile: profile["followers"])
most_following = max(data, key=lambda profile: profile["following"])

# ---------------------------------------------------------
# 2. Count how many profiles belong to each category
# ---------------------------------------------------------
category_counts = {}

for profile in data:
    category = profile["category"]

    # get(category, 0) returns 0 when the category is not yet present.
    category_counts[category] = category_counts.get(category, 0) + 1

# Sort categories from highest count to lowest count.
sorted_categories = sorted(
    category_counts.items(),
    key=lambda item: item[1],
    reverse=True,
)

# ---------------------------------------------------------
# 3. Write the answers to a text file
# ---------------------------------------------------------
output_file = OUTPUT_DIR / "step6_answers.txt"

with open(output_file, "w", encoding="utf-8") as file:
    file.write(
        f"Maximum posts:     {most_posts['username']} "
        f"({most_posts['posts']:,})\n"
    )
    file.write(
        f"Maximum followers: {most_followers['username']} "
        f"({most_followers['followers']:,})\n"
    )
    file.write(
        f"Follows the most:  {most_following['username']} "
        f"({most_following['following']:,})\n"
    )
    file.write(f"Categories:        {len(category_counts)}\n\n")

    for category, count in sorted_categories:
        file.write(f"  {category:<24}{count}\n")

# Read the answer file and display it in the terminal.
print(output_file.read_text(encoding="utf-8"))
print(f"Saved: {output_file}")
