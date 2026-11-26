# Import the module or specific tools needed for this lesson.
import json
# Import the module or specific tools needed for this lesson.
from pathlib import Path

# Assign the calculated or created value to path for later use.
path = Path("tasks.json")

# Define a reusable function; parameters let the caller provide input.
def load_tasks():
    # Check this condition; the indented block runs only when it is true.
    if not path.exists():
        # Send this result back to the caller and finish the function.
        return {"tasks": []}
    # Open/use the resource in a context manager so it is closed automatically.
    with open(path, encoding="utf-8") as f:
        # Send this result back to the caller and finish the function.
        return json.load(f)

# Define a reusable function; parameters let the caller provide input.
def save_tasks(data):
    # Open/use the resource in a context manager so it is closed automatically.
    with open(path, "w", encoding="utf-8") as f:
        # Call the relevant Python function/method to perform this file or data operation.
        json.dump(data, f, indent=2)

# Assign the calculated or created value to data for later use.
data = load_tasks()
# Assign the calculated or created value to next_id for later use.
next_id = max((t["id"] for t in data["tasks"]), default=0) + 1
# Perform this operation; the expression or method shown determines the exact action.
data["tasks"].append({"id": next_id, "title": "Clean the CSV", "done": False})

# Loop through each item so the same operation is applied repeatedly.
for t in data["tasks"]:
    # Check this condition; the indented block runs only when it is true.
    if t["title"] == "Buy milk":
        # Assign the calculated or created value to t["done"] for later use.
        t["done"] = True

# Perform this operation; the expression or method shown determines the exact action.
save_tasks(data)

# Loop through each item so the same operation is applied repeatedly.
for t in load_tasks()["tasks"]:
    # Display this value so we can inspect the program's result.
    print(("[x] " if t["done"] else "[ ] ") + t["title"])
