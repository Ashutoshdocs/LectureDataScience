"""Lecture 15: joins (incl. semi/anti/cross/asof) and concat."""
from datetime import date
from pathlib import Path
import polars as pl

DATA = Path(__file__).resolve().parent.parent / "data"
pl.Config.set_tbl_width_chars(160)
pl.Config.set_tbl_cols(12)

sales = (pl.read_csv(DATA / "sales.csv", try_parse_dates=True)
           .with_columns(revenue=pl.col("units") * pl.col("unit_price")))
customers = pl.read_csv(DATA / "customers.csv", try_parse_dates=True)

print("=== Join types on a tiny example ===")
left = pl.DataFrame({"id": [1, 2, 3], "order": ["pen", "book", "lamp"]})
right = pl.DataFrame({"id": [2, 3, 4], "name": ["Ravi", "Meena", "John"]})
for how in ["inner", "left", "right", "full", "semi", "anti"]:
    print(f"\nhow='{how}'")
    print(left.join(right, on="id", how=how, coalesce=True).sort("id"))

print("\n=== Enrich sales with customers ===")
full = sales.join(customers, on="customer_id", how="left", validate="m:1")
print("rows before:", sales.height, "| after:", full.height)
print(full.select("order_id", "product", "revenue", "name", "city", "segment").head(4))

print("\n=== Analyse the joined table ===")
print(full.group_by("city").agg(pl.col("revenue").sum()).sort("revenue", descending=True))
print(full.group_by("segment").agg(pl.col("revenue").sum(), pl.col("revenue").mean().round(0).alias("avg"))
          .sort("segment"))

print("\n=== semi / anti: who did / didn't order ===")
print("ordered      :", customers.join(sales, on="customer_id", how="semi").height, "customers")
print(customers.join(sales, on="customer_id", how="anti").select("customer_id", "name"))

print("\n=== Different key names + suffix ===")
targets = pl.DataFrame({"area": ["North", "South", "East", "West"], "revenue": [2_500_000] * 4})
actual = sales.group_by("region").agg(pl.col("revenue").sum())
print(actual.join(targets, left_on="region", right_on="area", suffix="_target")
            .with_columns(hit=pl.col("revenue") >= pl.col("revenue_target")).sort("region"))

print("\n=== The duplicate-key trap ===")
dup = pl.concat([customers, customers.head(1)])
bad = sales.join(dup, on="customer_id")
print("rows:", sales.height, "->", bad.height, "| revenue:", sales["revenue"].sum(), "->", bad["revenue"].sum())
try:
    sales.join(dup, on="customer_id", validate="m:1")
except pl.exceptions.ComputeError as e:
    print("validate caught it:", str(e).splitlines()[0])

print("\n=== cross join: a complete grid ===")
regions = sales.select("region").unique()
categories = sales.select("category").unique()
rev = sales.group_by("region", "category").agg(pl.col("revenue").sum())
grid = (regions.join(categories, how="cross")
               .join(rev, on=["region", "category"], how="left")
               .with_columns(pl.col("revenue").fill_null(0))
               .sort("region", "category"))
print(grid)

print("\n=== join_asof: price valid on the order date ===")
price_list = pl.DataFrame({
    "product": ["Phone", "Phone", "Phone"],
    "valid_from": [date(2025, 1, 1), date(2025, 5, 1), date(2025, 10, 1)],   # Python dates, not pl.date (an expression)
    "list_price": [26000, 24500, 23000],
})
phones = sales.filter(pl.col("product") == "Phone").select("order_id", "date", "product").sort("date")
priced = phones.join_asof(price_list.sort("valid_from"), left_on="date", right_on="valid_from", by="product",
                      check_sortedness=False)   # we sorted both sides ourselves
print(priced.gather_every(8))

print("\n=== concat ===")
q1 = sales.filter(pl.col("date").dt.quarter() == 1)
q2 = sales.filter(pl.col("date").dt.quarter() == 2)
print("vertical  :", pl.concat([q1, q2]).height, "rows")
a = pl.DataFrame({"x": [1], "y": ["a"]})
b = pl.DataFrame({"x": [2], "z": [True]})
print(pl.concat([a, b], how="diagonal"))
print(pl.concat([pl.DataFrame({"n": [1, 2]}), pl.DataFrame({"m": ["a", "b"]})], how="horizontal"))
