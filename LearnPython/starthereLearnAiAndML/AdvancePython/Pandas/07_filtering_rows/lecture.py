"""Lecture 07: Filtering rows with masks, isin, between, str, query."""
from pathlib import Path
import pandas as pd

DATA = Path(__file__).resolve().parent.parent / "data"
sales = pd.read_csv(DATA / "sales.csv")
students = pd.read_csv(DATA / "students.csv")

print("=== A mask is a True/False Series ===")
mask = sales["units"] >= 4
print(mask.head())
print("rows with units >= 4:", mask.sum(), "of", len(sales), f"({mask.mean():.0%})")
print(sales[mask].head(3))

print("\n=== & | ~ ===")
south_big = sales[(sales["region"] == "South") & (sales["units"] > 3)]
print("South & units>3:", len(south_big))
desk_or_chair = sales[(sales["product"] == "Desk") | (sales["product"] == "Chair")]
print("Desk | Chair   :", len(desk_or_chair))
not_furniture = sales[~(sales["category"] == "Furniture")]
print("~Furniture     :", len(not_furniture))

try:
    sales[(sales["units"] > 3) and (sales["region"] == "North")]
except ValueError as e:
    print("using 'and' ->", str(e)[:45], "...")

print("\n=== Helpers ===")
print("isin     :", len(sales[sales["product"].isin(["Laptop", "Tablet"])]))
print("between  :", len(sales[sales["unit_price"].between(1000, 20000)]))
print("contains :", sales.loc[sales["product"].str.contains("one"), "product"].unique())
print("March    :", len(sales[sales["date"].str.startswith("2025-03")]))
print("missing maths:\n", students.loc[students["maths"].isna(), ["name", "maths"]])

print("\n=== query ===")
print(sales.query("region == 'South' and units > 3").head(3))
limit = 20000
print("unit_price > @limit:", len(sales.query("unit_price > @limit")))
print("in list:", len(sales.query("region in ['North', 'East'] and units >= 4")))

print("\n=== Filter then pick columns ===")
print(sales.loc[sales["region"] == "West", ["date", "product", "units"]].head())

print("\n=== nlargest ===")
print(sales.nlargest(3, "unit_price")[["order_id", "product", "unit_price"]])
