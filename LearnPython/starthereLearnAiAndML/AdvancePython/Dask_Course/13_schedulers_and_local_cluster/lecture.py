"""Lecture 13: Schedulers (threads / processes / sync / distributed) and LocalCluster."""
import os
import sys
import time
from pathlib import Path
import dask
import dask.bag as db
import dask.dataframe as dd
from dask.distributed import Client, LocalCluster

DATA = Path(__file__).resolve().parent.parent / "data"
sys.path.insert(0, str(DATA))
from make_big_data import ensure_big_parquet       # noqa: E402


def python_heavy(n):
    """Pure-Python CPU work: holds the GIL."""
    total = 0
    for i in range(n):
        total += (i * i) % 7
    return total


def timed(label, fn):
    t = time.perf_counter()
    out = fn()
    print(f"  {label:<44} {time.perf_counter() - t:6.2f} s")
    return out


def main():
    pq = ensure_big_parquet()
    ddf = dd.read_parquet(pq)
    ddf = ddf.assign(revenue=ddf.units * ddf.unit_price)
    query = ddf.groupby("region").revenue.sum()
    py_tasks = [dask.delayed(python_heavy)(3_000_000) for _ in range(4)]
    print("cores:", os.cpu_count())

    print("\n=== 1. Local schedulers ===")
    print("pandas-style groupby (releases the GIL):")
    for name in ["synchronous", "threads", "processes"]:
        timed(name, lambda: query.compute(scheduler=name))
    print("pure-Python tasks (hold the GIL):")
    for name in ["synchronous", "threads"]:
        timed(name, lambda: dask.compute(*py_tasks, scheduler=name))
    timed("processes (chunksize=1, see Lecture 03)",
          lambda: dask.compute(*py_tasks, scheduler="processes", chunksize=1))

    print("\n=== 2. A config block ===")
    with dask.config.set(scheduler="synchronous"):
        print("  inside the block, scheduler =", dask.config.get("scheduler"), "->", f"{ddf.units.sum().compute():,.0f}")

    print("\n=== 3. LocalCluster + Client (distributed) ===")
    with LocalCluster(n_workers=2, threads_per_worker=1, memory_limit="2GB",
                      dashboard_address=":8787") as cluster, Client(cluster) as client:
        print(" ", client)
        print("  dashboard:", client.dashboard_link, "(open it now!)")
        print("  worker pids:", list(client.run(os.getpid).values()))

        result = timed("groupby on the cluster", lambda: query.compute())
        print("  ", result.round(0).to_dict())
        timed("pure-Python tasks on 2 worker processes", lambda: dask.compute(*py_tasks))

        print("  bag on the cluster:",
              db.from_sequence(range(1, 11), npartitions=2).map(lambda x: x * x).sum().compute())

        info = client.scheduler_info()
        for addr, w in info["workers"].items():
            print(f"  worker {addr}: {w['nthreads']} thread(s), memory limit {w['memory_limit'] / 1e9:.1f} GB")

    print("\n=== 4. Threads vs processes inside a cluster ===")
    for workers, threads in [(1, 2), (2, 1)]:
        with LocalCluster(n_workers=workers, threads_per_worker=threads, dashboard_address=":0") as c, Client(c):
            timed(f"{workers} worker(s) x {threads} thread(s): pure Python", lambda: dask.compute(*py_tasks))
            timed(f"{workers} worker(s) x {threads} thread(s): pandas groupby", lambda: query.compute())


if __name__ == "__main__":       # REQUIRED: LocalCluster starts worker processes
    main()
