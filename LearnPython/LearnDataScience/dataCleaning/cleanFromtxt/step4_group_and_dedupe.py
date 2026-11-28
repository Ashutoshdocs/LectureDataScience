"""
STEP 4 - Group lines into profiles and remove duplicate profiles.

Input:
    outputs/step3_fixed_words.txt

Output:
    outputs/step4_cleaned.txt

Rules:
- A blank line marks the end of one profile.
- The first line of a profile is its username.
- A set tracks usernames that have already been included.
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "outputs" / "step3_fixed_words.txt"
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

# Read the standardised lines from Step 3.
with open(INPUT_FILE, encoding="utf-8") as file:
    lines = file.read().split("\n")

# ---------------------------------------------------------
# 1. Group lines into separate profile lists
# ---------------------------------------------------------
profiles = []
current_profile = []

for line in lines:
    if line == "":
        # A blank line means the current profile has ended.
        if current_profile:
            profiles.append(current_profile)
        current_profile = []
    else:
        # Add the current line to the profile being built.
        current_profile.append(line)

# Add the final profile if the file does not end with a blank line.
if current_profile:
    profiles.append(current_profile)

print("Profiles found:", len(profiles))

# ---------------------------------------------------------
# 2. Remove duplicate usernames
# ---------------------------------------------------------
seen_usernames = set()
unique_profiles = []

for profile in profiles:
    username = profile[0]  # The first line stores the username.

    if username in seen_usernames:
        print("Duplicate removed:", username)
        continue

    # Remember this username so a later duplicate can be detected.
    seen_usernames.add(username)
    unique_profiles.append(profile)

print("Unique profiles:", len(unique_profiles))

# ---------------------------------------------------------
# 3. Save unique profiles with one blank line between them
# ---------------------------------------------------------
# Join lines within a profile, then separate profiles with two newlines.
cleaned_text = "\n\n".join(
    "\n".join(profile)
    for profile in unique_profiles
) + "\n"

output_file = OUTPUT_DIR / "step4_cleaned.txt"

with open(output_file, "w", encoding="utf-8") as file:
    file.write(cleaned_text)

print(f"Saved: {output_file}")
