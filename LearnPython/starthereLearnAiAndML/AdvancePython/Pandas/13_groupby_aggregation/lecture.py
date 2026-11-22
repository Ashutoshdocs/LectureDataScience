"""Lecture 13: GroupBy: split, apply, combine. agg, transform, filter."""
from pathlib import Path
import pandas as pd

DATA = Path(__file__).resolve().parent.parent / "data"
pd.set_option("display.width", 140)
pd.set_option("display.float_format", "{:,.1f}".format)

sales = pd.read_csv(DATA / "sales.csv")
sales["revenue"] = sales["units"] * sales["unit_price"]

print("=== The basic pattern ===")
print(sales.groupby("region")["revenue"].sum())

print("\n=== Under the hood: split ===")
for region, part in sales.groupby("region"):
    print(f"{region:6} {len(part):3} rows, revenue {part['revenue'].sum():>12,}")

print("\n=== Several columns / several keys ===")
print(sales.groupby("region")[["units", "revenue"]].sum())
by_two = sales.groupby(["category", "region"])["revenue"].sum()
print(by_two)
print(by_two.unstack())
print(sales.groupby("region", as_index=False)["revenue"].sum())

print("\n=== Ranking groups ===")
print(sales.groupby("product")["units"].sum().sort_values(ascending=False))

print("\n=== agg: several statistics ===")
print(sales.groupby("region")["revenue"].agg(["sum", "mean", "count", "max"]))
summary = sales.groupby("region").agg(
    orders=("order_id", "count"),
    revenue=("revenue", "sum"),
    biggest=("revenue", "max"),
    avg_units=("units", "mean"),
    customers=("customer_id", "nunique"),
).sort_values("revenue", ascending=False)
print(summary)

print("\n=== size vs count ===")
students = pd.read_csv(DATA / "students.csv")
print(pd.DataFrame({"size": students.groupby("class").size(),
                    "count_maths": students.groupby("class")["maths"].count()}))

print("\n=== transform: group value on every row ===")
sales["region_avg"] = sales.groupby("region")["revenue"].transform("mean")
sales["vs_region_avg"] = sales["revenue"] - sales["region_avg"]
sales["pct_of_category"] = (sales["revenue"]
                            / sales.groupby("category")["revenue"].transform("sum") * 100)
print(sales[["region", "revenue", "region_avg", "vs_region_avg", "pct_of_category"]].head())

print("\n=== filter: keep whole groups ===")
loyal = sales.groupby("customer_id").filter(lambda g: len(g) >= 9)
print("customers with 9+ orders:", sorted(loyal["customer_id"].unique().tolist()))

spend = sales.groupby("customer_id")["revenue"].sum()
print("spent > 3,00,000:", spend[spend > 300_000].sort_values(ascending=False).round(0).to_dict())

print("\n=== Top row per group ===")
print(sales.loc[sales.groupby("region")["revenue"].idxmax(), ["region", "product", "revenue"]])

print("\n=== Running total within each customer ===")
sales["cust_running"] = sales.groupby("customer_id")["revenue"].cumsum()
print(sales.loc[sales["customer_id"] == 1, ["date", "revenue", "cust_running"]])
