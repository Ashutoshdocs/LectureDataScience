"""Lecture 03: dask.delayed: build task graphs from ordinary Python functions."""
import os
import time
from pathlib import Path
import dask
import pandas as pd

DATA = Path(__file__).resolve().parent.parent / "data"


# ---------- 1. A slow function, sequential vs delayed ----------
def slow_square(x):
    time.sleep(0.5)          # pretend this is a file download or an API call
    return x * x


@dask.delayed
def slow_square_d(x):
    time.sleep(0.5)
    return x * x


# ---------- 2. A small pipeline ----------
@dask.delayed
def load(path):
    return pd.read_csv(path)


@dask.delayed
def summarise(df, name):
    return {"file": name, "rows": len(df), "columns": df.shape[1],
            "numeric_cols": len(df.select_dtypes("number").columns)}


@dask.delayed
def combine(parts):
    return pd.DataFrame(parts)


# ---------- 3. Pure-Python CPU work ----------
def count_primes(limit):
    count = 0
    for n in range(2, limit):
        if all(n % d for d in range(2, int(n ** 0.5) + 1)):
            count += 1
    return count


def main():
    print("cores:", os.cpu_count())

    print("\n=== 1. Sequential vs delayed ===")
    t = time.perf_counter()
    seq = [slow_square(i) for i in range(8)]
    seq_t = time.perf_counter() - t

    lazy = [slow_square_d(i) for i in range(8)]
    print("lazy objects:", lazy[:2], "...")
    t = time.perf_counter()
    par = dask.compute(*lazy)                      # threads by default
    par_t = time.perf_counter() - t
    t = time.perf_counter()
    dask.compute(*lazy, num_workers=8)             # more threads than cores: fine for waiting tasks
    wide_t = time.perf_counter() - t
    print(f"sequential: {seq_t:.2f} s | delayed (threads = cores): {par_t:.2f} s | "
          f"delayed (8 threads): {wide_t:.2f} s | same: {list(par) == seq}")
    print("Waiting tasks (I/O, sleep) can use more threads than cores; CPU tasks can't.")

    total = dask.delayed(sum)(lazy)                # depend on all eight
    print("sum of squares:", total.compute())

    print("\n=== 2. A pipeline across files ===")
    files = ["sales.csv", "customers.csv", "students.csv"]
    parts = [summarise(load(DATA / f), f) for f in files]
    report = combine(parts)
    print("tasks in graph:", len(report.__dask_graph__()))
    print(report.compute())

    print("\n=== 3. Wrapping an existing function ===")
    lazy_read = dask.delayed(pd.read_csv)
    sizes = [dask.delayed(len)(lazy_read(DATA / f)) for f in files]
    print(dict(zip(files, dask.compute(*sizes))))

    print("\n=== 4. Threads vs processes for pure-Python CPU work ===")
    work = [dask.delayed(count_primes)(500_000) for _ in range(4)]
    t = time.perf_counter(); [count_primes(500_000) for _ in range(4)]; base = time.perf_counter() - t
    t = time.perf_counter(); dask.compute(*work, scheduler="threads"); thr = time.perf_counter() - t
    t = time.perf_counter(); dask.compute(*work, scheduler="processes"); prc = time.perf_counter() - t
    t = time.perf_counter(); dask.compute(*work, scheduler="processes", chunksize=1); prc1 = time.perf_counter() - t
    print(f"plain loop: {base:.2f} s | threads: {thr:.2f} s | processes: {prc:.2f} s | "
          f"processes, chunksize=1: {prc1:.2f} s")
    print("Threads don't help pure-Python code (the GIL).")
    print("The processes scheduler sends tasks in batches of 6 by default, so 4 big tasks all")
    print("went to ONE worker. chunksize=1 spreads them out and every core gets used.")

    print("\n=== 5. Splitting a returned tuple: nout ===")
    pair = dask.delayed(lambda x: (x, -x), nout=2)(5)
    a, b = pair
    print("a, b =", dask.compute(a, b))

    print("\n=== 6. Anti-pattern: tasks that are too small ===")
    tiny = [dask.delayed(lambda v: v + 1)(i) for i in range(2_000)]
    t = time.perf_counter(); dask.compute(*tiny); tiny_t = time.perf_counter() - t
    t = time.perf_counter(); [i + 1 for i in range(2_000)]; plain_t = time.perf_counter() - t
    print(f"2,000 tiny delayed tasks: {tiny_t * 1000:.0f} ms | plain Python: {plain_t * 1000:.2f} ms")
    print("Each task costs scheduling overhead, so make tasks do real work.")


if __name__ == "__main__":        # required because section 4 starts worker processes
    main()
