"""Lecture 00: Prerequisites: your resources, and chunked processing by hand (no Dask yet)."""
import os
import time
from pathlib import Path
import numpy as np
import pandas as pd
import psutil

DATA = Path(__file__).resolve().parent.parent / "data"

print("=== 1. Your machine ===")
print("logical CPU cores:", os.cpu_count())
print(f"RAM: {psutil.virtual_memory().total / 1e9:.1f} GB total, "
      f"{psutil.virtual_memory().available / 1e9:.1f} GB available")

print("\n=== 2. pandas needs several times the file size in memory ===")
f = DATA / "sales.csv"
df = pd.read_csv(f)
print(f"file: {f.stat().st_size / 1024:.1f} KB | in memory: {df.memory_usage(deep=True).sum() / 1024:.1f} KB")

print("\n=== 3. pandas uses one core ===")
x = np.random.default_rng(0).random(5_000_000)
t = time.perf_counter()
s = pd.Series(x).rolling(50).mean().sum()
print(f"one rolling mean over 5M values: {(time.perf_counter() - t) * 1000:.0f} ms on a single core")

print("\n=== 4. Chunked processing by hand ===")
total_revenue = 0
rows = 0
for chunk in pd.read_csv(f, chunksize=50):           # only 50 rows in memory at a time
    total_revenue += (chunk["units"] * chunk["unit_price"]).sum()
    rows += len(chunk)
print(f"processed {rows} rows in chunks of 50 -> total revenue {total_revenue:,}")
print("check (whole file):", f"{(df['units'] * df['unit_price']).sum():,}")

print("\n=== 5. Combining partial results ===")
chunks = [c for c in pd.read_csv(f, chunksize=60)]
partial_sums = [int(c["units"].sum()) for c in chunks]
partial_counts = [len(c) for c in chunks]
print("partial sums  :", partial_sums, "-> total", sum(partial_sums))
print("mean from parts:", sum(partial_sums) / sum(partial_counts), "| true mean:", df["units"].mean())
medians = [c["unit_price"].median() for c in chunks]
print("median of medians:", np.median(medians), "| true median:", df["unit_price"].median(), "<- not the same!")

print("\nDask automates step 4 (chunks), runs the chunks in parallel, and knows how to")
print("combine partial results correctly (step 5). Next: Lecture 01.")
