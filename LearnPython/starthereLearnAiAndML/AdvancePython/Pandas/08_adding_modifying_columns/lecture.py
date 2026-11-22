"""Lecture 08: Adding & modifying columns: vectorized maths, np.where, cut, map, assign, apply."""
from pathlib import Path
import numpy as np
import pandas as pd

DATA = Path(__file__).resolve().parent.parent / "data"
pd.set_option("display.width", 140)
sales = pd.read_csv(DATA / "sales.csv")

print("=== 1. Vectorized arithmetic ===")
sales["revenue"] = sales["units"] * sales["unit_price"]
sales["with_gst"] = (sales["revenue"] * 1.18).round(2)
print(sales[["product", "units", "unit_price", "revenue", "with_gst"]].head())

print("\n=== 2. Conditional columns ===")
sales["size"] = np.where(sales["units"] >= 4, "bulk", "single")
sales["tier"] = np.select(
    [sales["revenue"] >= 100_000, sales["revenue"] >= 20_000],
    ["gold", "silver"], default="bronze")
sales["band"] = pd.cut(sales["revenue"], bins=[0, 5_000, 50_000, np.inf],
                       labels=["small", "medium", "large"])
sales["units_level"] = pd.cut(sales["units"], bins=[0, 2, 3, 5], labels=["low", "mid", "high"])
print(sales[["revenue", "size", "tier", "band", "units_level"]].head(6))
print(sales["tier"].value_counts())

sales["discount"] = np.where(sales["category"] == "Electronics", sales["revenue"] * 0.1, 0)
sales.loc[sales["region"] == "West", "discount"] += 500      # change only matching rows
print(sales[["category", "region", "revenue", "discount"]].head())

print("\n=== where / mask ===")
capped = sales["revenue"].where(sales["revenue"] <= 100_000, 100_000)   # keep if True
print("max before:", sales["revenue"].max(), "| after cap:", capped.max())

print("\n=== 3. map and replace ===")
codes = {"North": "N", "South": "S", "East": "E"}          # West missing on purpose
sales["region_code"] = sales["region"].map(codes)
print(sales[["region", "region_code"]].drop_duplicates())
print(sales["region"].replace({"North": "Northern"}).unique())

print("\n=== 4. assign in a chain ===")
report = (
    pd.read_csv(DATA / "sales.csv")
    .assign(revenue=lambda d: d["units"] * d["unit_price"],
            gst=lambda d: d["revenue"] * 0.18,
            net=lambda d: d["revenue"] + d["gst"])
    [["order_id", "product", "revenue", "gst", "net"]]
)
print(report.head(3))

print("\n=== 5. apply (works, but is a hidden loop) ===")
sales["code"] = sales["product"].apply(lambda p: p.upper()[:3])
sales["code_fast"] = sales["product"].str.upper().str[:3]     # vectorized equivalent
print(sales[["product", "code", "code_fast"]].drop_duplicates().head())
print("same result?", sales["code"].equals(sales["code_fast"]))

print("\n=== 6. rename, drop, reorder, insert ===")
tidy = (sales.rename(columns={"unit_price": "price"})
             .drop(columns=["code", "code_fast", "region_code"])
             [["order_id", "date", "product", "units", "price", "revenue"]])
tidy.insert(1, "year", 2025)
print(tidy.head(3))
