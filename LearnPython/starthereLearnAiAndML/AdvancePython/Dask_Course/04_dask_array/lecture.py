"""Lecture 04: Dask Array: chunked NumPy, lazy operations, chunk sizing."""
import time
import dask
import dask.array as da
import numpy as np
import psutil

print("=== 1. A big array that never fully exists in memory ===")
rng = da.random.default_rng(42)
x = rng.random((20_000, 20_000), chunks=(5_000, 5_000))
print(x)
print(f"total size: {x.nbytes / 1e9:.1f} GB | one chunk: {np.prod(x.chunksize) * 8 / 1e6:.0f} MB | "
      f"chunks: {x.npartitions} | your RAM: {psutil.virtual_memory().total / 1e9:.1f} GB")

t = time.perf_counter()
mean = x.mean().compute()
print(f"mean of 400 million numbers: {mean:.5f} in {time.perf_counter() - t:.1f} s")

print("\n=== 2. The NumPy API ===")
small = rng.random((10_000, 10_000), chunks=(2_500, 2_500))
col_means = small.mean(axis=0)
print("column means: shape", col_means.shape, "->", col_means[:3].compute().round(4))
print("values > 0.99:", (small > 0.99).sum().compute())
y = da.where(small > 0.5, 1, 0)
print("share above 0.5:", y.mean().compute().round(4))
print("slice:", small[:2, :3].compute().round(3))
z = (da.sqrt(small) + small.T * 2).std()
print("sqrt + transpose + std (lazy):", z, "->", round(float(z.compute()), 5))

print("\n=== 3. Computing several things at once ===")
lo, hi, avg = dask.compute(small.min(), small.max(), small.mean())
print(f"min {lo:.6f} | max {hi:.6f} | mean {avg:.6f} (data read once)")

print("\n=== 4. From NumPy and back ===")
np_arr = np.arange(1_000_000).reshape(1000, 1000)
d = da.from_array(np_arr, chunks=(250, 250))
print(d, "->", type(d.sum(axis=1).compute()).__name__)
print("same result as NumPy:", np.array_equal(d.sum(axis=1).compute(), np_arr.sum(axis=1)))

print("\n=== 5. Chunk size matters ===")
for c in [250, 1_000, 2_500, 5_000]:
    arr = rng.random((10_000, 10_000), chunks=(c, c))
    t = time.perf_counter()
    arr.mean().compute()
    print(f"chunks {c:>5} x {c:<5} -> {arr.npartitions:>5} chunks, "
          f"{len(arr.mean().__dask_graph__()):>5} tasks, {time.perf_counter() - t:5.2f} s")
print("auto chunks:", rng.random((20_000, 20_000), chunks="auto").chunksize)

print("\n=== 6. Rechunking ===")
tall = small.rechunk((10_000, 500))           # whole columns in each chunk
print("before:", small.chunksize, "| after:", tall.chunksize, "| chunks:", tall.npartitions)

print("\n=== 7. Linear algebra ===")
a = rng.random((4_000, 2_000), chunks=(1_000, 1_000))
gram = a.T @ a                                 # (2000, 2000)
print("A.T @ A:", gram.shape, "trace =", round(float(da.trace(gram).compute()), 1))
