"""
Approach 2: NumPy.
NumPy is excellent for numerical calculations. Here we create arrays
for numeric columns. Text columns are still handled separately.
"""
import csv
from pathlib import Path
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CSV_FILE = PROJECT_ROOT / "data" / "sales.csv"

quantities = []
unit_prices = []
regions = []
products = []

with CSV_FILE.open("r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        quantities.append(int(row["quantity"]))
        unit_prices.append(float(row["unit_price"]))
        regions.append(row["region"])
        products.append(row["product"])

# Convert numeric Python lists into NumPy arrays.
quantity_array = np.array(quantities)
price_array = np.array(unit_prices)

# Vectorized multiplication: no explicit Python loop needed.
sales_array = quantity_array * price_array

print("\n--- NUMPY ---")
print("Sales for each order:", sales_array)
print("Total sales:", np.sum(sales_array))
print("Average order value:", np.mean(sales_array))
print("Largest order:", np.max(sales_array))
print("Total quantity:", np.sum(quantity_array))

# Boolean masking works well for numeric arrays.
high_value_mask = sales_array > 10000
print("\nHigh-value order sales:", sales_array[high_value_mask])

# We can filter a separate text list with the same mask,
# but we must remember to keep all arrays aligned.
product_array = np.array(products)
print("Products in high-value orders:", product_array[high_value_mask])

# Grouping by a text category takes additional steps.
region_array = np.array(regions)
print("\nSales by region (manual NumPy approach):")
for region in np.unique(region_array):
    region_total = np.sum(sales_array[region_array == region])
    print(region, region_total)
