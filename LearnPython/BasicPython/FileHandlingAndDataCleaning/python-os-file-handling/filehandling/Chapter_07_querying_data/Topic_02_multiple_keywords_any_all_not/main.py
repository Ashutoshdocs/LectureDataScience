# Import the module or specific tools needed for this lesson.
import re
# Import the module or specific tools needed for this lesson.
from dataset import load

# Assign the calculated or created value to rows for later use.
rows = load()

# Define a reusable function; parameters let the caller provide input.
def word(w):
    # Send this result back to the caller and finish the function.
    return re.compile(rf"\b{re.escape(w)}\b", re.IGNORECASE)

# Define a reusable function; parameters let the caller provide input.
def query(rows, any_of=(), all_of=(), none_of=(), column="review"):
    # Assign the calculated or created value to any_p for later use.
    any_p = [word(w) for w in any_of]
    # Assign the calculated or created value to all_p for later use.
    all_p = [word(w) for w in all_of]
    # Assign the calculated or created value to none_p for later use.
    none_p = [word(w) for w in none_of]
    # Assign the calculated or created value to result for later use.
    result = []
    # Loop through each item so the same operation is applied repeatedly.
    for r in rows:
        # Assign the calculated or created value to text for later use.
        text = r[column]
        # Check this condition; the indented block runs only when it is true.
        if any_p and not any(p.search(text) for p in any_p):
            # Skip to the next iteration of the loop.
            continue
        # Check this condition; the indented block runs only when it is true.
        if not all(p.search(text) for p in all_p):
            # Skip to the next iteration of the loop.
            continue
        # Check this condition; the indented block runs only when it is true.
        if any(p.search(text) for p in none_p):
            # Skip to the next iteration of the loop.
            continue
        # Perform this operation; the expression or method shown determines the exact action.
        result.append(r)
    # Send this result back to the caller and finish the function.
    return result

# Define a reusable function; parameters let the caller provide input.
def show(label, result):
    # Display this value so we can inspect the program's result.
    print(f"{label:<32} -> {[r['id'] for r in result]}")

# Perform this operation; the expression or method shown determines the exact action.
show("ANY late / slow / delay", query(rows, any_of=["late", "slow", "delay"]))
# Perform this operation; the expression or method shown determines the exact action.
show("ALL battery + delivery", query(rows, all_of=["battery", "delivery"]))
# Perform this operation; the expression or method shown determines the exact action.
show("ANY quality, NOT poor", query(rows, any_of=["quality"], none_of=["poor"]))
# Perform this operation; the expression or method shown determines the exact action.
show("ANY great/good, NOT but", query(rows, any_of=["great", "good"], none_of=["but"]))
# Perform this operation; the expression or method shown determines the exact action.
show("substring 'late' (wrong!)", [r for r in rows if "late" in r["review"].lower()])
