# Import the module or specific tools needed for this lesson.
import csv
# Import the module or specific tools needed for this lesson.
import json

# Open/use the resource in a context manager so it is closed automatically.
with open("orders.json", encoding="utf-8") as f:
    # Assign the calculated or created value to orders for later use.
    orders = json.load(f)

# Assign the calculated or created value to rows for later use.
rows = []
# Loop through each item so the same operation is applied repeatedly.
for order in orders:
    # Loop through each item so the same operation is applied repeatedly.
    for item in order["items"]:
        # Perform this operation; the expression or method shown determines the exact action.
        rows.append({
            # Perform this operation; the expression or method shown determines the exact action.
            "order_id": order["id"],
            # Perform this operation; the expression or method shown determines the exact action.
            "customer": order["customer"]["name"],
            # Perform this operation; the expression or method shown determines the exact action.
            "city": order["customer"].get("city", "unknown"),
            # Perform this operation; the expression or method shown determines the exact action.
            "product": item["product"],
            # Perform this operation; the expression or method shown determines the exact action.
            "qty": item["qty"],
            # Perform this operation; the expression or method shown determines the exact action.
            "amount": item["qty"] * item["price"],
        # Perform this operation; the expression or method shown determines the exact action.
        })

# Loop through each item so the same operation is applied repeatedly.
for r in rows:
    # Display this value so we can inspect the program's result.
    print(r)

# Open/use the resource in a context manager so it is closed automatically.
with open("order_items.csv", "w", newline="", encoding="utf-8") as f:
    # Assign the calculated or created value to writer for later use.
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    # Perform this operation; the expression or method shown determines the exact action.
    writer.writeheader()
    # Perform this operation; the expression or method shown determines the exact action.
    writer.writerows(rows)
# Display this value so we can inspect the program's result.
print("rows written:", len(rows))
