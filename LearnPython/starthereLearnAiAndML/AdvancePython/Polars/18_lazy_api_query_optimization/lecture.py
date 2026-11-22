"""Lecture 18: The lazy API: plans, pushdown optimisations, streaming, sink."""
import time
from pathlib import Path
import numpy as np
import polars as pl

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data"
OUT = HERE / "output"
OUT.mkdir(exist_ok=True)
BIG = OUT / "big_sales.parquet"
N = 5_000_000


def make_big_file():
    """5M synthetic orders, written once and reused."""
    rng = np.random.default_rng(42)
    products = ["Laptop", "Phone", "Tablet", "Headphones", "Charger", "Desk", "Chair", "Lamp"]
    prices = np.array([55000, 25000, 18000, 3500, 900, 12000, 7500, 1500])
    idx = rng.integers(0, len(products), N)
    pl.DataFrame({
        "order_id": np.arange(N),
        "day": rng.integers(0, 365, N),
        "region": rng.choice(["North", "South", "East", "West"], N),
        "product": np.array(products)[idx],
        "units": rng.integers(1, 6, N),
        "unit_price": prices[idx],
        "customer_id": rng.integers(1, 50_000, N),
        "notes": rng.choice(["", "gift", "express", "fragile"], N),
    }).with_columns(date=pl.date(2025, 1, 1) + pl.duration(days=pl.col("day"))).drop("day") \
      .write_parquet(BIG, row_group_size=250_000)


if not BIG.exists():
    print(f"Creating {N:,}-row Parquet file (one-time)...")
    make_big_file()
print(f"{BIG.name}: {BIG.stat().st_size / 1e6:.0f} MB on disk\n")

print("=== 1. A LazyFrame is a plan ===")
lf = pl.scan_parquet(BIG)
print(type(lf).__name__)
print("schema without reading data:", lf.collect_schema())

query = (lf.filter(pl.col("region") == "North")
           .with_columns(revenue=pl.col("units") * pl.col("unit_price"))
           .group_by("product")
           .agg(pl.col("revenue").sum())
           .sort("revenue", descending=True))

print("\n=== 2. Plan as written (unoptimised) ===")
print(query.explain(optimized=False))
print("\n=== 3. Optimised plan: note PROJECT and SELECTION at the scan ===")
print(query.explain())

print("\n=== 4. Eager vs lazy timing ===")
t = time.perf_counter()
eager = (pl.read_parquet(BIG)                                   # reads ALL 8 columns, ALL rows
           .filter(pl.col("region") == "North")
           .with_columns(revenue=pl.col("units") * pl.col("unit_price"))
           .group_by("product").agg(pl.col("revenue").sum())
           .sort("revenue", descending=True))
eager_t = time.perf_counter() - t

t = time.perf_counter()
lazy = query.collect()
lazy_t = time.perf_counter() - t
print(lazy)
print(f"eager: {eager_t * 1000:7.0f} ms | lazy: {lazy_t * 1000:7.0f} ms | same result: {eager.equals(lazy)}")

print("\n=== 5. Slice pushdown: instant preview ===")
t = time.perf_counter()
print(pl.scan_parquet(BIG).head(3).collect())
print(f"took {(time.perf_counter() - t) * 1000:.1f} ms for a {N:,}-row file")

print("\n=== 6. Projection: how much data is actually read ===")
full_mb = pl.read_parquet(BIG).estimated_size("mb")
needed_mb = pl.scan_parquet(BIG).select("region", "product", "units", "unit_price").collect().estimated_size("mb")
print(f"all columns in memory: {full_mb:.0f} MB | only the 4 needed: {needed_mb:.0f} MB")

print("\n=== 7. Streaming engine ===")
t = time.perf_counter()
streamed = query.collect(engine="streaming")
print(f"streaming collect: {(time.perf_counter() - t) * 1000:.0f} ms | same result: {streamed.equals(lazy)}")

print("\n=== 8. sink: write a result without collecting ===")
(pl.scan_parquet(BIG)
   .filter(pl.col("product").is_in(["Desk", "Chair", "Lamp"]))
   .sink_parquet(OUT / "furniture_only.parquet"))
print("furniture rows written:", pl.scan_parquet(OUT / "furniture_only.parquet").select(pl.len()).collect().item())

print("\n=== 9. collect_all: several results from one plan run ===")
base = pl.scan_parquet(BIG).with_columns(revenue=pl.col("units") * pl.col("unit_price"))
by_region, by_month = pl.collect_all([
    base.group_by("region").agg(pl.col("revenue").sum()).sort("region"),
    base.group_by(pl.col("date").dt.month().alias("month")).agg(pl.len()).sort("month").head(3),
])
print(by_region)
print(by_month)

print("\n=== 10. Small data: .lazy() works on any DataFrame ===")
small = pl.read_csv(DATA / "sales.csv").lazy()
print(small.filter(pl.col("units") == 5).select(pl.len()).collect())
