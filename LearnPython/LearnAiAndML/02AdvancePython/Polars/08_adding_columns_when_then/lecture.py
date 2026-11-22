"""Lecture 08: with_columns, when/then/otherwise, binning, replace, horizontal ops."""
from pathlib import Path
import polars as pl

DATA = Path(__file__).resolve().parent.parent / "data"
sales = pl.read_csv(DATA / "sales.csv", try_parse_dates=True)
students = pl.read_csv(DATA / "students.csv")

print("=== with_columns ===")
sales = sales.with_columns(
    revenue=pl.col("units") * pl.col("unit_price"),
    with_gst=(pl.col("units") * pl.col("unit_price") * 1.18).round(2),
)
print(sales.select("product", "units", "unit_price", "revenue", "with_gst").head(4))

print("\n=== when / then / otherwise ===")
sales = sales.with_columns(
    size=pl.when(pl.col("units") >= 4).then(pl.lit("bulk")).otherwise(pl.lit("single")),
    tier=pl.when(pl.col("revenue") >= 100_000).then(pl.lit("gold"))
           .when(pl.col("revenue") >= 20_000).then(pl.lit("silver"))
           .otherwise(pl.lit("bronze")),
    level=pl.when(pl.col("units") <= 2).then(pl.lit("low"))
            .when(pl.col("units") == 3).then(pl.lit("mid"))
            .otherwise(pl.lit("high")),
    discount=pl.when(pl.col("category") == "Electronics")
               .then(pl.col("revenue") * 0.1).otherwise(0),
)
print(sales.select("units", "revenue", "size", "tier", "level", "discount").head(6))
print(sales["tier"].value_counts(sort=True))

print("\nWithout otherwise -> null:")
print(sales.select(pl.when(pl.col("units") == 5).then(pl.lit("max")).alias("flag")).head(4))

print("\n=== Change only some rows ===")
sales = sales.with_columns(
    discount=pl.when(pl.col("region") == "West").then(pl.col("discount") + 500)
               .otherwise(pl.col("discount")))
print(sales.select("region", "category", "revenue", "discount").head(4))

print("\n=== Binning with bin_intervals (Polars 2) ===")
print(sales.select("revenue", band=pl.col("revenue").bin_intervals(
    [5_000, 50_000], labels=["small", "medium", "large"])).head(5))

print("\n=== replace vs replace_strict ===")
codes = {"North": "N", "South": "S", "East": "E"}          # West missing on purpose
print(sales.select(
    "region",
    replaced=pl.col("region").replace(codes),
    strict=pl.col("region").replace_strict(codes, default=None),
).unique().sort("region"))

print("\n=== Horizontal (across columns) ===")
marks = ["maths", "science", "english", "cs"]
print(students.with_columns(
    total=pl.sum_horizontal(marks),
    best=pl.max_horizontal(marks),
    avg=pl.mean_horizontal(marks).round(1),
).select("name", *marks, "total", "best", "avg").head(5))

print("\n=== Text from several columns, clipping ===")
print(sales.select(
    label=pl.concat_str(["product", "region"], separator=" - "),
    capped=pl.col("revenue").clip(upper_bound=100_000),
).head(3))
