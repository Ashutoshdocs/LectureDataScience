# Import the module or specific tools needed for this lesson.
from dataset import load

# Assign the calculated or created value to rows for later use.
rows = load()
# Display this value so we can inspect the program's result.
print(len(rows), "reviews loaded")

# Define a reusable function; parameters let the caller provide input.
def search(rows, keyword, column="review"):
    # Assign the calculated or created value to kw for later use.
    kw = keyword.lower()
    # Send this result back to the caller and finish the function.
    return [r for r in rows if kw in r[column].lower()]

# Loop through each item so the same operation is applied repeatedly.
for r in search(rows, "delivery"):
    # Display this value so we can inspect the program's result.
    print(f"#{r['id']:<3} {r['product']:<14} {r['review']}")

# Display this value so we can inspect the program's result.
print("BATTERY  :", [r["id"] for r in search(rows, "BATTERY")])
# Display this value so we can inspect the program's result.
print("product  :", [r["id"] for r in search(rows, "phone", column="product")])

# Define a reusable function; parameters let the caller provide input.
def search_all_columns(rows, keyword, columns=("product", "category", "city", "review")):
    # Assign the calculated or created value to kw for later use.
    kw = keyword.lower()
    # Send this result back to the caller and finish the function.
    return [r for r in rows if any(kw in r[c].lower() for c in columns)]

# Display this value so we can inspect the program's result.
print("anywhere 'home':", [r["id"] for r in search_all_columns(rows, "home")])
