# Import the module or specific tools needed for this lesson.
import csv
# Import the module or specific tools needed for this lesson.
import json
# Import the module or specific tools needed for this lesson.
from dataset import load

# Define a reusable function; parameters let the caller provide input.
def save_csv(rows, path, columns):
    # Open/use the resource in a context manager so it is closed automatically.
    with open(path, "w", newline="", encoding="utf-8") as f:
        # Assign the calculated or created value to writer for later use.
        writer = csv.DictWriter(f, fieldnames=columns, extrasaction="ignore")
        # Perform this operation; the expression or method shown determines the exact action.
        writer.writeheader()
        # Perform this operation; the expression or method shown determines the exact action.
        writer.writerows(rows)

# Define a reusable function; parameters let the caller provide input.
def save_json(data, path):
    # Open/use the resource in a context manager so it is closed automatically.
    with open(path, "w", encoding="utf-8") as f:
        # Call the relevant Python function/method to perform this file or data operation.
        json.dump(data, f, indent=2, ensure_ascii=False)

# Assign the calculated or created value to rows for later use.
rows = load()
# Assign the calculated or created value to keyword for later use.
keyword = "delivery"
# Assign the calculated or created value to hits for later use.
hits = [r for r in rows if keyword in r["review"].lower()]

# Perform this operation; the expression or method shown determines the exact action.
save_csv(hits, f"{keyword}_reviews.csv", ["id", "product", "rating", "review"])

# Assign the calculated or created value to summary for later use.
summary = {
    # Perform this operation; the expression or method shown determines the exact action.
    "keyword": keyword,
    # Perform this operation; the expression or method shown determines the exact action.
    "matches": len(hits),
    # Perform this operation; the expression or method shown determines the exact action.
    "share_of_reviews": round(len(hits) / len(rows), 2),
    # Perform this operation; the expression or method shown determines the exact action.
    "avg_rating": round(sum(r["rating"] for r in hits) / len(hits), 2),
    # Perform this operation; the expression or method shown determines the exact action.
    "unhappy_ids": [r["id"] for r in hits if r["rating"] <= 2],
# Perform this operation; the expression or method shown determines the exact action.
}
# Perform this operation; the expression or method shown determines the exact action.
save_json(summary, f"{keyword}_summary.json")

# Display this value so we can inspect the program's result.
print(open(f"{keyword}_reviews.csv", encoding="utf-8").read().strip())
# Display this value so we can inspect the program's result.
print(open(f"{keyword}_summary.json", encoding="utf-8").read())
