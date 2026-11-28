"""
Approach 1: Built-in file handling + csv module.
Notice how much work we do manually for conversions, calculations,
filtering, and grouping.
"""
import csv
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CSV_FILE = PROJECT_ROOT / "data" / "sales.csv"

orders = []

# Read the CSV file. CSV values initially arrive as strings.
with CSV_FILE.open("r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        # Convert numeric text into Python numbers.
        row["quantity"] = int(row["quantity"])
        row["unit_price"] = float(row["unit_price"])

        # Calculate a new value manually for every row.
        row["sales"] = row["quantity"] * row["unit_price"]
        orders.append(row)

print("\n--- FILE HANDLING + CSV ---")
print("Number of orders:", len(orders))

# Calculate total sales using a loop.
total_sales = 0
for order in orders:
    total_sales += order["sales"]
print("Total sales:", total_sales)

# Filter orders from East using a loop.
print("\nOrders from East:")
for order in orders:
    if order["region"] == "East":
        print(order["order_id"], order["product"], order["sales"])

# Group sales by region manually using a dictionary.
sales_by_region = {}
for order in orders:
    region = order["region"]
    sales_by_region[region] = sales_by_region.get(region, 0) + order["sales"]

print("\nSales by region (manual grouping):")
for region, amount in sales_by_region.items():
    print(region, amount)

# Missing salesperson values need explicit handling.
missing_count = 0
for order in orders:
    if not order["salesperson"]:
        missing_count += 1
print("\nMissing salesperson values:", missing_count)
