"""Lecture 13: group_by().agg() with expressions."""
from pathlib import Path
import polars as pl

DATA = Path(__file__).resolve().parent.parent / "data"
pl.Config.set_tbl_width_chars(160)
pl.Config.set_tbl_cols(12)

sales = (pl.read_csv(DATA / "sales.csv", try_parse_dates=True)
           .with_columns(revenue=pl.col("units") * pl.col("unit_price")))

print("=== The basic pattern ===")
print(sales.group_by("region").agg(pl.col("revenue").sum()).sort("region"))

print("\n=== Order is not guaranteed: sort or maintain_order ===")
print("run 1:", sales.group_by("region").agg(pl.len())["region"].to_list())
print("run 2:", sales.group_by("region").agg(pl.len())["region"].to_list())
print("maintain_order:", sales.group_by("region", maintain_order=True).agg(pl.len())["region"].to_list())

print("\n=== Rich aggregations ===")
summary = sales.group_by("region").agg(
    orders=pl.len(),
    revenue=pl.col("revenue").sum(),
    avg_order=pl.col("revenue").mean().round(0),
    biggest=pl.col("revenue").max(),
    customers=pl.col("customer_id").n_unique(),
    bulk_share=(pl.col("units") >= 4).mean().round(2),
    furniture_rev=pl.col("revenue").filter(pl.col("category") == "Furniture").sum(),
    top_product=pl.col("product").sort_by("revenue").last(),
).sort("revenue", descending=True)
print(summary)

print("\n=== No aggregation -> a list per group ===")
print(sales.group_by("category").agg(pl.col("product").unique().sort()).sort("category"))

print("\n=== Units per product ===")
print(sales.group_by("product").agg(pl.col("units").sum()).sort("units", descending=True))

print("\n=== Several keys ===")
print(sales.group_by("category", "region").agg(pl.col("revenue").mean().round(0))
           .sort("category", "region"))

print("\n=== Group by a computed key ===")
print(sales.group_by(month=pl.col("date").dt.month())
           .agg(orders=pl.len(), revenue=pl.col("revenue").sum()).sort("month").head(4))

print("\n=== Shortcuts ===")
print(sales.group_by("region").len().sort("len", descending=True))

print("\n=== HAVING: filter after aggregating ===")
spend = (sales.group_by("customer_id")
              .agg(orders=pl.len(), spent=pl.col("revenue").sum())
              .filter(pl.col("spent") > 300_000)
              .sort("spent", descending=True))
print(spend)

print("\n=== Iterating (rarely needed) ===")
for (region,), part in sales.group_by("region", maintain_order=True):
    print(f"{region:6} {part.height:3} rows")

print("\n=== Student marks by class ===")
students = pl.read_csv(DATA / "students.csv")
print(students.group_by("class").agg(
    pl.len().alias("students"),
    pl.col("maths").count().alias("maths_present"),          # count skips nulls
    pl.col("maths", "science", "english", "cs").mean().round(1),
).sort("class"))
