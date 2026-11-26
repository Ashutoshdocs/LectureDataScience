# Import the module or specific tools needed for this lesson.
from dataset import load

# Assign the calculated or created value to rows for later use.
rows = load()

# Define a reusable function; parameters let the caller provide input.
def select(rows, *conditions):
    # Send this result back to the caller and finish the function.
    return [r for r in rows if all(cond(r) for cond in conditions)]

# Assign the calculated or created value to cheap for later use.
cheap = lambda r: r["price"] < 2000
# Perform this operation; the expression or method shown determines the exact action.
liked = lambda r: r["rating"] >= 4
# Define a reusable function; parameters let the caller provide input.
def in_city(*cities):
    # Assign the calculated or created value to wanted for later use.
    wanted = {c.lower() for c in cities}
    # Send this result back to the caller and finish the function.
    return lambda r: r["city"].lower() in wanted
# Define a reusable function; parameters let the caller provide input.
def mentions(word):
    # Send this result back to the caller and finish the function.
    return lambda r: word in r["review"].lower()

# Display this value so we can inspect the program's result.
print("cheap & liked:", [r["id"] for r in select(rows, cheap, liked)])
# Display this value so we can inspect the program's result.
print("Pune or Delhi, rating <= 2:", [r["id"] for r in select(rows, in_city("pune", "delhi"), lambda r: r["rating"] <= 2)])
# Display this value so we can inspect the program's result.
print("Electronics mentioning battery:", [r["id"] for r in select(rows, lambda r: r["category"] == "Electronics", mentions("battery"))])

# Assign the calculated or created value to result for later use.
result = select(rows, lambda r: r["category"] in ("Fashion", "Home"))
# Assign the calculated or created value to result for later use.
result = sorted(result, key=lambda r: (-r["rating"], r["price"]))[:3]

# Display this value so we can inspect the program's result.
print(f"\n{'product':<14}{'rating':>7}{'price':>8}")
# Loop through each item so the same operation is applied repeatedly.
for r in result:
    # Display this value so we can inspect the program's result.
    print(f"{r['product']:<14}{r['rating']:>7}{r['price']:>8.0f}")
