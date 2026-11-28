"""
Approach 3: Pandas.
A DataFrame keeps mixed columns together and provides convenient
operations for inspection, cleaning, filtering, grouping, and sorting.
"""
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CSV_FILE = PROJECT_ROOT / "data" / "sales.csv"

# Read the CSV directly into a labeled table.
df = pd.read_csv(CSV_FILE)

print("\n--- PANDAS ---")
print("\nComplete table:")
print(df)

print("\nTable information:")
df.info()

print("\nMissing values per column:")
print(df.isna().sum())

# Create a new column for calculated sales.
df["sales"] = df["quantity"] * df["unit_price"]

print("\nOrders from East:")
print(df.loc[df["region"] == "East", ["order_id", "product", "sales"]])

print("\nSales by region:")
print(df.groupby("region")["sales"].sum().sort_values(ascending=False))

print("\nAverage, minimum, and maximum sales:")
print(df["sales"].agg(["mean", "min", "max"]))

print("\nTop 3 orders:")
print(df.nlargest(3, "sales")[["order_id", "product", "region", "sales"]])

# Replace missing salesperson values without writing a manual loop.
df["salesperson"] = df["salesperson"].fillna("Unknown")

# Save the transformed table to a new CSV file.
output_file = PROJECT_ROOT / "data" / "sales_with_analysis.csv"
df.to_csv(output_file, index=False)
print(f"\nCleaned and calculated data saved to: {output_file}")
