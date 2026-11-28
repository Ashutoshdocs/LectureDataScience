# Import the module or specific tools needed for this lesson.
import csv
# Import the module or specific tools needed for this lesson.
from pathlib import Path

# Assign the calculated or created value to FIELDS for later use.
FIELDS = ["item", "qty", "price"]

# Define a reusable function; parameters let the caller provide input.
def add_sale(item, qty, price):
    # Assign the calculated or created value to path for later use.
    path = Path("sales.csv")
    # Perform this operation; the expression or method shown determines the exact action.
    is_new = not path.exists() or path.stat().st_size == 0
    # Open/use the resource in a context manager so it is closed automatically.
    with open(path, "a", newline="", encoding="utf-8") as f:
        # Assign the calculated or created value to writer for later use.
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        # Check this condition; the indented block runs only when it is true.
        if is_new:
            # Perform this operation; the expression or method shown determines the exact action.
            writer.writeheader()
        # Perform this operation; the expression or method shown determines the exact action.
        writer.writerow({"item": item, "qty": qty, "price": price})

# Perform this operation; the expression or method shown determines the exact action.
add_sale("pen", 10, 5.0)
# Perform this operation; the expression or method shown determines the exact action.
add_sale("notebook", 3, 45.5)
# Perform this operation; the expression or method shown determines the exact action.
add_sale("bag", 1, 799)

# Assign the calculated or created value to total for later use.
total = 0
# Open/use the resource in a context manager so it is closed automatically.
with open("sales.csv", newline="", encoding="utf-8") as f:
    # Loop through each item so the same operation is applied repeatedly.
    for row in csv.DictReader(f):
        # Assign the calculated or created value to amount for later use.
        amount = int(row["qty"]) * float(row["price"])
        # Perform this operation; the expression or method shown determines the exact action.
        total += amount
        # Display this value so we can inspect the program's result.
        print(f"{row['item']:<9} {amount:>7.2f}")
# Display this value so we can inspect the program's result.
print(f"{'TOTAL':<9} {total:>7.2f}")
