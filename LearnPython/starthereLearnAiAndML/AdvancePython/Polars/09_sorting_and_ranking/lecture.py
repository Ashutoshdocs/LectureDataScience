"""Lecture 09: Sorting & ranking."""
from pathlib import Path
import polars as pl

DATA = Path(__file__).resolve().parent.parent / "data"
sales = (pl.read_csv(DATA / "sales.csv", try_parse_dates=True)
           .with_columns(revenue=pl.col("units") * pl.col("unit_price")))
students = (pl.read_csv(DATA / "students.csv")
              .with_columns(total=pl.sum_horizontal("maths", "science", "english", "cs")))
cols = ["order_id", "region", "product", "revenue"]

print("=== sort ===")
print(sales.sort("revenue").select(cols).head(3))
print(sales.sort("revenue", descending=True).select(cols).head(3))
print(sales.sort("region", "revenue", descending=[False, True]).select(cols).head(6))

print("\n=== nulls first (default) vs nulls_last ===")
print(students.sort("maths").select("name", "maths").head(3))
print(students.sort("maths", nulls_last=True).select("name", "maths").head(3))

print("\n=== Sort by an expression ===")
names = pl.DataFrame({"name": ["bob", "Alice", "carol", "Dave"]})
print("default        :", names.sort("name")["name"].to_list())
print("case-insensitive:", names.sort(pl.col("name").str.to_lowercase())["name"].to_list())
print("by length      :", names.sort(pl.col("name").str.len_chars(), "name")["name"].to_list())

print("\n=== top_k / bottom_k ===")
print(sales.top_k(5, by="revenue").select(cols))
print(students.bottom_k(3, by="cs").select("name", "cs"))

print("\n=== Sorting inside expressions ===")
print(students.group_by("class", maintain_order=True).agg(
    pl.col("name").sort_by("maths", descending=True, nulls_last=True).alias("best_to_worst_maths")))

print("\n=== rank methods on ties ===")
s = pl.DataFrame({"player": ["A", "B", "C", "D"], "score": [90, 85, 85, 70]})
print(s.with_columns(
    average=pl.col("score").rank("average", descending=True),
    min=pl.col("score").rank("min", descending=True),
    dense=pl.col("score").rank("dense", descending=True),
    ordinal=pl.col("score").rank("ordinal", descending=True),
))

print("\n=== Ranking students overall and within class ===")
print(students.with_columns(
    rank=pl.col("total").rank("min", descending=True),
    class_rank=pl.col("total").rank("min", descending=True).over("class"),
).sort("rank").select("name", "class", "total", "rank", "class_rank"))
