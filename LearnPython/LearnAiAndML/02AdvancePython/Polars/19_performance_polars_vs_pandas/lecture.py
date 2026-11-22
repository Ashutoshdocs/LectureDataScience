"""Lecture 19: Polars vs pandas speed race on 5M rows, plus Polars anti-patterns."""
import time
import warnings
from pathlib import Path
import numpy as np
import pandas as pd
import polars as pl

HERE = Path(__file__).resolve().parent
OUT = HERE / "output"
OUT.mkdir(exist_ok=True)
N = 5_000_000
print(f"Polars {pl.__version__} ({pl.thread_pool_size()} threads) vs pandas {pd.__version__}, {N:,} rows\n")

rng = np.random.default_rng(0)
products = np.array(["Laptop", "Phone", "Tablet", "Headphones", "Charger", "Desk", "Chair", "Lamp"])
data = {
    "region": rng.choice(["North", "South", "East", "West"], N),
    "product": products[rng.integers(0, 8, N)],
    "units": rng.integers(1, 6, N),
    "unit_price": rng.choice([900, 1500, 3500, 7500, 12000, 18000, 25000, 55000], N),
    "customer_id": rng.integers(0, 50_000, N),
}
pdf = pd.DataFrame(data)
pldf = pl.DataFrame(data)
cust_pd = pd.DataFrame({"customer_id": np.arange(50_000), "segment": rng.choice(["Retail", "Business"], 50_000)})
cust_pl = pl.from_pandas(cust_pd)

csv_path = OUT / "race_1m.csv"
if not csv_path.exists():
    pldf.head(1_000_000).write_csv(csv_path)


def best_of(fn, repeat=3):
    times = []
    for _ in range(repeat):
        t = time.perf_counter()
        fn()
        times.append(time.perf_counter() - t)
    return min(times) * 1000


tasks = {
    "read CSV (1M rows)": (lambda: pd.read_csv(csv_path),
                           lambda: pl.read_csv(csv_path)),
    "filter": (lambda: pdf[(pdf["region"] == "North") & (pdf["units"] >= 3)],
               lambda: pldf.filter((pl.col("region") == "North") & (pl.col("units") >= 3))),
    "new column": (lambda: pdf.assign(revenue=pdf["units"] * pdf["unit_price"]),
                   lambda: pldf.with_columns(revenue=pl.col("units") * pl.col("unit_price"))),
    "group by (sum, mean)": (lambda: pdf.groupby(["region", "product"])["units"].agg(["sum", "mean"]),
                             lambda: pldf.group_by("region", "product").agg(
                                 pl.col("units").sum().alias("sum"), pl.col("units").mean().alias("mean"))),
    "join 50k customers": (lambda: pdf.merge(cust_pd, on="customer_id", how="left"),
                           lambda: pldf.join(cust_pl, on="customer_id", how="left")),
    "sort by 2 columns": (lambda: pdf.sort_values(["product", "unit_price"]),
                          lambda: pldf.sort("product", "unit_price")),
    "string upper+contains": (lambda: pdf["product"].str.upper().str.contains("PHONE"),
                              lambda: pldf.select(pl.col("product").str.to_uppercase().str.contains("PHONE"))),
    "pipeline (lazy in Polars)": (
        lambda: (pdf[pdf["units"] >= 2]
                 .assign(revenue=lambda d: d["units"] * d["unit_price"])
                 .groupby("region")["revenue"].sum().sort_values()),
        lambda: (pldf.lazy().filter(pl.col("units") >= 2)
                 .with_columns(revenue=pl.col("units") * pl.col("unit_price"))
                 .group_by("region").agg(pl.col("revenue").sum()).sort("revenue").collect())),
}

print(f"{'task':<28}{'pandas ms':>11}{'polars ms':>11}{'speed-up':>10}")
print("-" * 60)
rows = []
for name, (pd_fn, pl_fn) in tasks.items():
    p, q = best_of(pd_fn), best_of(pl_fn)
    rows.append({"task": name, "pandas_ms": round(p, 1), "polars_ms": round(q, 1), "speedup": round(p / q, 1)})
    print(f"{name:<28}{p:>11.1f}{q:>11.1f}{p / q:>9.1f}x")

results = pl.DataFrame(rows)
results.write_csv(OUT / "race_results.csv")
print(f"\nmedian speed-up: {results['speedup'].median():.1f}x  (saved output/race_results.csv)")

print("\n=== Same answers? ===")
a = pdf.groupby("region")["units"].sum().sort_index()
b = pldf.group_by("region").agg(pl.col("units").sum()).sort("region")
print("group-by totals equal:", a.to_list() == b["units"].to_list())

print("\n=== Anti-pattern: map_elements (Python per value) ===")
small = pldf.head(500_000)
with warnings.catch_warnings(record=True) as caught:
    warnings.simplefilter("always")
    t = time.perf_counter()
    slow = small.with_columns(size=pl.col("units").map_elements(
        lambda u: "bulk" if u >= 4 else "single", return_dtype=pl.String))
    slow_ms = (time.perf_counter() - t) * 1000
if caught:
    print("Polars warned:", type(caught[0].message).__name__)
t = time.perf_counter()
fast = small.with_columns(size=pl.when(pl.col("units") >= 4).then(pl.lit("bulk")).otherwise(pl.lit("single")))
fast_ms = (time.perf_counter() - t) * 1000
print(f"map_elements: {slow_ms:7.1f} ms | when/then: {fast_ms:6.1f} ms | {slow_ms / fast_ms:.0f}x faster | equal: {slow.equals(fast)}")

print("\n=== Anti-pattern: many with_columns vs one ===")
def many():
    d = pldf
    for i in range(8):
        d = d.with_columns((pl.col("units") * (i + 1)).alias(f"c{i}"))
    return d
def one():
    return pldf.with_columns([(pl.col("units") * (i + 1)).alias(f"c{i}") for i in range(8)])
print(f"8 separate with_columns: {best_of(many):6.1f} ms | one with_columns: {best_of(one):6.1f} ms")
