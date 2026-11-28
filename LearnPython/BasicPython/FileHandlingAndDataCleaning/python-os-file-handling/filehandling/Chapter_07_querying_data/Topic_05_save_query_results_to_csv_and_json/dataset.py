# Import the module or specific tools needed for this lesson.
import csv

# Define a reusable function; parameters let the caller provide input.
def load(path="reviews.csv"):
    # Perform this operation; the expression or method shown determines the exact action.
    """Load reviews.csv with numeric columns converted."""
    # Open/use the resource in a context manager so it is closed automatically.
    with open(path, newline="", encoding="utf-8") as f:
        # Assign the calculated or created value to rows for later use.
        rows = list(csv.DictReader(f))
    # Loop through each item so the same operation is applied repeatedly.
    for r in rows:
        # Assign the calculated or created value to r["id"] for later use.
        r["id"] = int(r["id"])
        # Assign the calculated or created value to r["rating"] for later use.
        r["rating"] = int(r["rating"])
        # Assign the calculated or created value to r["price"] for later use.
        r["price"] = float(r["price"])
    # Send this result back to the caller and finish the function.
    return rows
