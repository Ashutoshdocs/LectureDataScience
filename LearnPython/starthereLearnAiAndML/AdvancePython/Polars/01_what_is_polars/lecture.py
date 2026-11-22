"""Lecture 01: What is Polars? First DataFrame, eager vs lazy, threads."""
from pathlib import Path
import polars as pl

DATA = Path(__file__).resolve().parent.parent / "data"

print("Polars version:", pl.__version__)
print("Threads Polars will use:", pl.thread_pool_size())

df = pl.DataFrame({
    "name": ["Asha", "Ravi", "Meena", "John"],
    "class": ["10A", "10A", "10B", "10B"],
    "maths": [78, 92, 45, 83],
})
print(df)
print("schema:", df.schema)

print("\n--- The same questions as the pandas course, Polars style ---")
print("average maths:", df["maths"].mean())
print(df.filter(pl.col("maths") > 60).select("name"))
print(df.sort("maths", descending=True))
print(df.group_by("class", maintain_order=True).agg(pl.col("maths").mean().alias("avg_maths")))

print("\n--- Eager vs lazy ---")
eager = pl.read_csv(DATA / "sales.csv")            # reads the whole file now
print("eager:", type(eager).__name__, eager.shape)

lazy = pl.scan_csv(DATA / "sales.csv")             # nothing read yet: just a plan
print("lazy :", type(lazy).__name__)
query = (lazy.filter(pl.col("region") == "North")
             .group_by("product")
             .agg(pl.col("units").sum())
             .sort("units", descending=True))
print("\nThe optimised plan Polars will run:")
print(query.explain())
print(query.collect())                             # now it actually runs
