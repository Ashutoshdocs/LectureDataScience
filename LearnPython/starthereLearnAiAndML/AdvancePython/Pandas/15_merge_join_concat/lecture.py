"""Lecture 15: Merge, join & concat."""
from pathlib import Path
import pandas as pd

DATA = Path(__file__).resolve().parent.parent / "data"
pd.set_option("display.width", 140)

sales = pd.read_csv(DATA / "sales.csv")
sales["revenue"] = sales["units"] * sales["unit_price"]
customers = pd.read_csv(DATA / "customers.csv")

print("=== Four join types on a tiny example ===")
left = pd.DataFrame({"id": [1, 2, 3], "order": ["pen", "book", "lamp"]})
right = pd.DataFrame({"id": [2, 3, 4], "name": ["Ravi", "Meena", "John"]})
for how in ["inner", "left", "right", "outer"]:
    print(f"\nhow='{how}'")
    print(left.merge(right, on="id", how=how))

print("\n=== Enrich sales with customer info ===")
full = sales.merge(customers, on="customer_id", how="left", validate="many_to_one")
print("rows before:", len(sales), "| after:", len(full))
print(full[["order_id", "product", "revenue", "name", "city", "segment"]].head())

print("\n=== Analyse the merged table ===")
print(full.groupby("city")["revenue"].sum().sort_values(ascending=False))
print(full.groupby("segment")["revenue"].agg(["sum", "mean"]).round(0))

print("\n=== Who never ordered? indicator=True ===")
check = customers.merge(sales[["customer_id"]].drop_duplicates(), on="customer_id",
                        how="left", indicator=True)
print(check["_merge"].value_counts())
print(check.loc[check["_merge"] == "left_only", ["customer_id", "name"]])

print("\n=== Different key names + suffixes ===")
targets = pd.DataFrame({"area": ["North", "South", "East", "West"],
                        "revenue": [2_500_000, 2_500_000, 2_500_000, 2_500_000]})
actual = sales.groupby("region", as_index=False)["revenue"].sum()
vs = actual.merge(targets, left_on="region", right_on="area", suffixes=("_actual", "_target"))
vs["hit"] = vs["revenue_actual"] >= vs["revenue_target"]
print(vs.drop(columns="area"))

print("\n=== The duplicate-key trap ===")
dup_customers = pd.concat([customers, customers.iloc[[0]]])     # customer 1 twice
bad = sales.merge(dup_customers, on="customer_id")
print("rows:", len(sales), "->", len(bad), "| revenue:", sales["revenue"].sum(), "->", bad["revenue"].sum())
try:
    sales.merge(dup_customers, on="customer_id", validate="many_to_one")
except pd.errors.MergeError as e:
    print("validate caught it:", e)

print("\n=== concat: stacking ===")
q1 = sales[sales["date"] < "2025-04-01"]
q2 = sales[(sales["date"] >= "2025-04-01") & (sales["date"] < "2025-07-01")]
h1 = pd.concat([q1, q2], ignore_index=True)
print("q1", len(q1), "+ q2", len(q2), "=", len(h1))
labelled = pd.concat({"Q1": q1, "Q2": q2}, names=["quarter"]).reset_index(level=0)
print(labelled.groupby("quarter")["revenue"].sum())

print("\n=== concat side by side ===")
a = sales.groupby("region")["units"].sum()
b = sales.groupby("region")["revenue"].sum()
print(pd.concat([a, b], axis=1))

print("\n=== join on the index & map lookup ===")
joined = sales.set_index("customer_id").join(customers.set_index("customer_id")[["name"]])
print(joined[["product", "name"]].head(3))
city_of = customers.set_index("customer_id")["city"]
sales["city"] = sales["customer_id"].map(city_of)
print(sales[["customer_id", "city"]].head(3))
