"""
TASK 1 - Clean and structure the social-network data.

Input:
    social_data.json

Outputs:
    outputs/clean_social_data.json
    outputs/users.csv
    outputs/friendships.csv
    outputs/likes.csv
    outputs/popular_pages.csv

This script handles messy IDs, names, duplicate records, invalid
relationships, invalid page likes, and inactive users.
"""

import json
from pathlib import Path
from collections import Counter

import pandas as pd

# Use paths relative to this script so it works from any terminal folder.
BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "social_data.json"
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

# ---------------------------------------------------------
# 1. Load the raw JSON data
# ---------------------------------------------------------
with INPUT_FILE.open(encoding="utf-8") as file:
    data = json.load(file)

users = data["users"]
pages = data["pages"]

print(f"{len(users)} raw user records and {len(pages)} page records loaded.")

# ---------------------------------------------------------
# 2. Inspect common data-quality problems
# ---------------------------------------------------------
user_ids = [str(user["id"]) for user in users]

duplicate_user_ids = [
    user_id
    for user_id, count in Counter(user_ids).items()
    if count > 1
]

users_without_name = [
    user["id"]
    for user in users
    if not user["name"].strip()
]

users_without_activity = [
    user["id"]
    for user in users
    if not user["friends"] and not user["liked_pages"]
]

duplicate_page_ids = [
    page_id
    for page_id, count in Counter(page["id"] for page in pages).items()
    if count > 1
]

print("\nDATA QUALITY REPORT")
print("Duplicate user IDs:", duplicate_user_ids)
print("Users without names:", users_without_name)
print("Users without activity:", users_without_activity)
print("IDs stored as text:", [u["id"] for u in users if isinstance(u["id"], str)])
print("Duplicate page IDs:", duplicate_page_ids)

# ---------------------------------------------------------
# 3. Clean users and merge duplicate user records
# ---------------------------------------------------------
clean_users = {}

for user in users:
    # Convert IDs and relationship IDs to integers.
    user_id = int(user["id"])

    # Remove extra spaces and standardise the person's name.
    name = user["name"].strip().title()

    # Do not keep records that have no usable name.
    if not name:
        continue

    # Sets automatically remove repeated friend and page IDs.
    friends = {int(friend_id) for friend_id in user["friends"]}
    liked_pages = {int(page_id) for page_id in user["liked_pages"]}

    if user_id in clean_users:
        # Merge relationships when the same user ID appears more than once.
        clean_users[user_id]["friends"].update(friends)
        clean_users[user_id]["liked_pages"].update(liked_pages)
    else:
        clean_users[user_id] = {
            "id": user_id,
            "name": name,
            "friends": friends,
            "liked_pages": liked_pages,
        }

print(f"\n{len(clean_users)} users after merging duplicate IDs.")

# ---------------------------------------------------------
# 4. Clean page records
# ---------------------------------------------------------
clean_pages = {}

for page in pages:
    page_id = int(page["id"])
    name = page["name"].strip()

    # Skip blank page names and keep the first valid name for each ID.
    if name and page_id not in clean_pages:
        if name.isupper() or name.islower():
            name = name.title()
        clean_pages[page_id] = name

print(f"{len(clean_pages)} pages after cleaning.")

# ---------------------------------------------------------
# 5. Remove invalid relationships and page likes
# ---------------------------------------------------------
for user_id, user in clean_users.items():
    # Remove self-friendships and references to missing users.
    user["friends"] = {
        friend_id
        for friend_id in user["friends"]
        if friend_id != user_id and friend_id in clean_users
    }

    # Remove likes that point to pages that do not exist.
    user["liked_pages"] = {
        page_id
        for page_id in user["liked_pages"]
        if page_id in clean_pages
    }

# Make all friendships mutual:
# if A lists B as a friend, B will also list A.
for user_id, user in clean_users.items():
    for friend_id in list(user["friends"]):
        clean_users[friend_id]["friends"].add(user_id)

# Remove users who have no friends and have not liked any page.
inactive_users = [
    user_id
    for user_id, user in clean_users.items()
    if not user["friends"] and not user["liked_pages"]
]

for user_id in inactive_users:
    del clean_users[user_id]

print("Removed inactive users:", inactive_users)
print(f"Final cleaned user count: {len(clean_users)}")

# ---------------------------------------------------------
# 6. Create lookup dictionaries for recommendation tasks
# ---------------------------------------------------------
friends_of = {
    user_id: user["friends"]
    for user_id, user in clean_users.items()
}

likes_of = {
    user_id: user["liked_pages"]
    for user_id, user in clean_users.items()
}

name_of = {
    user_id: user["name"]
    for user_id, user in clean_users.items()
}

# ---------------------------------------------------------
# 7. Create tidy pandas tables
# ---------------------------------------------------------
users_df = pd.DataFrame([
    {
        "id": user_id,
        "name": user["name"],
        "num_friends": len(user["friends"]),
        "num_pages_liked": len(user["liked_pages"]),
    }
    for user_id, user in sorted(clean_users.items())
])

# Store each friendship only once (A-B, not both A-B and B-A).
friendship_pairs = sorted({
    tuple(sorted((user_id, friend_id)))
    for user_id, friend_ids in friends_of.items()
    for friend_id in friend_ids
})

friendships_df = pd.DataFrame(
    friendship_pairs,
    columns=["user_1", "user_2"],
)

likes_df = pd.DataFrame([
    (user_id, page_id, clean_pages[page_id])
    for user_id, page_ids in likes_of.items()
    for page_id in sorted(page_ids)
], columns=["user_id", "page_id", "page_name"])

popular_pages_df = (
    likes_df["page_name"]
    .value_counts()
    .rename("likes")
    .rename_axis("page_name")
    .reset_index()
)

print(f"\nCreated {len(friendships_df)} unique friendships and {len(likes_df)} likes.")
print("\nUsers table:")
print(users_df.head(10))
print("\nMost popular pages:")
print(popular_pages_df.head(10))

# ---------------------------------------------------------
# 8. Save cleaned JSON and CSV tables for later tasks
# ---------------------------------------------------------
clean_json = {
    "users": [
        {
            **user,
            "friends": sorted(user["friends"]),
            "liked_pages": sorted(user["liked_pages"]),
        }
        for user in clean_users.values()
    ],
    "pages": [
        {"id": page_id, "name": page_name}
        for page_id, page_name in clean_pages.items()
    ],
}

with (OUTPUT_DIR / "clean_social_data.json").open("w", encoding="utf-8") as file:
    json.dump(clean_json, file, indent=2, ensure_ascii=False)

users_df.to_csv(OUTPUT_DIR / "users.csv", index=False)
friendships_df.to_csv(OUTPUT_DIR / "friendships.csv", index=False)
likes_df.to_csv(OUTPUT_DIR / "likes.csv", index=False)
popular_pages_df.to_csv(OUTPUT_DIR / "popular_pages.csv", index=False)

print("\nTask 1 completed.")
print("Cleaned data and tables saved inside the outputs folder.")
