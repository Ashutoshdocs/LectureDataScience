"""Lecture 04: Exploring a dataset: glimpse, describe, null_count, value_counts."""
from pathlib import Path
import polars as pl

DATA = Path(__file__).resolve().parent.parent / "data"
pl.Config.set_tbl_width_chars(120)

sales = pl.read_csv(DATA / "sales.csv", try_parse_dates=True)
students = pl.read_csv(DATA / "students.csv")

print("=== head / tail / sample ===")
print(sales.head(3))
print(sales.tail(2))
print(sales.sample(3, seed=1))

print("\n=== shape / schema / glimpse ===")
print("shape:", sales.shape)
print(sales.schema)
sales.glimpse()

print("\n=== describe ===")
print(sales.describe())

print("\n=== value_counts ===")
print(sales["region"].value_counts(sort=True))
print(sales["category"].value_counts(normalize=True))
print("busiest region:", sales["region"].value_counts(sort=True).row(0)[0])

print("\n=== unique ===")
print("products :", sorted(sales["product"].unique().to_list()))
print("customers:", sales["customer_id"].n_unique())

print("\n=== missing values ===")
print(sales.null_count())
print(students.null_count())

print("\n=== duplicates, size, ranges ===")
print("duplicate rows:", sales.is_duplicated().sum())
print(f"memory: {sales.estimated_size('kb'):.1f} KB")
print(sales.select(pl.col("date").min().alias("first"), pl.col("date").max().alias("last"),
                   pl.col("unit_price").min().alias("min_price"), pl.col("unit_price").max().alias("max_price")))

print("\n=== correlation ===")
print(students.select(pl.corr("maths", "science").alias("maths~science"),
                      pl.corr("maths", "cs").alias("maths~cs")))

print("\n=== Show more rows temporarily ===")
with pl.Config(tbl_rows=12):
    print(students)
