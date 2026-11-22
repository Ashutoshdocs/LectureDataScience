"""Lecture 05: Expressions: recipes for columns, used in four contexts."""
from pathlib import Path
import polars as pl

DATA = Path(__file__).resolve().parent.parent / "data"
sales = pl.read_csv(DATA / "sales.csv", try_parse_dates=True)

print("=== An expression is just a recipe ===")
rev = pl.col("units") * pl.col("unit_price")
print("type :", type(rev).__name__)
print("value:", rev)                               # shows the recipe, no data

print("\n=== The same expression in four contexts ===")
print("select:")
print(sales.select(rev.alias("revenue")).head(3))

print("with_columns:")
print(sales.with_columns(rev.alias("revenue")).head(3))

print("filter:")
print(sales.filter(rev > 150_000).select("order_id", "product", "units"))

print("group_by().agg():")
print(sales.group_by("region").agg(rev.sum().alias("revenue")).sort("region"))

print("\n=== Building blocks ===")
print(sales.select(
    pl.col("units").sum().alias("total_units"),
    pl.col("unit_price").mean().round(1).alias("avg_price"),
    pl.col("product").n_unique().alias("products"),
    pl.lit("2025").alias("year"),
    (pl.col("units") >= 4).mean().round(3).alias("share_bulk"),
))

print("\n=== Keyword naming instead of alias ===")
print(sales.with_columns(revenue=rev, with_gst=rev * 1.18).head(3))

print("\n=== Expressions in one context run in parallel ===")
try:
    sales.with_columns(revenue=rev, gst=pl.col("revenue") * 0.18)
except pl.exceptions.ColumnNotFoundError as e:
    print("error:", str(e).splitlines()[0])
fixed = (sales.with_columns(revenue=rev)
              .with_columns(gst=pl.col("revenue") * 0.18))
print(fixed.select("order_id", "revenue", "gst").head(3))

print("\n=== Several columns at once ===")
students = pl.read_csv(DATA / "students.csv")
print(students.select(pl.col("maths", "science", "english", "cs").mean().round(1)))
print(students.select(pl.col(pl.Float64).max()))
print(students.select("name", (pl.col("maths", "science") / 10).name.suffix("_out_of_10")).head(3))

print("\n=== Reusable expressions ===")
def pct_of_total(column: str) -> pl.Expr:
    return (pl.col(column) / pl.col(column).sum() * 100).round(2).alias(f"{column}_pct")

by_region = (sales.with_columns(revenue=rev)
                  .group_by("region").agg(pl.col("revenue").sum())
                  .with_columns(pct_of_total("revenue"))
                  .sort("revenue", descending=True))
print(by_region)
