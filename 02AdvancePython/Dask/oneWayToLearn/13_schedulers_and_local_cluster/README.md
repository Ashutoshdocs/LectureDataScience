# Lecture 13: Schedulers & LocalCluster

Run: `python lecture.py`. It starts a local cluster and prints a **dashboard link**. Open it in your browser while the script runs.

## What is a scheduler?

The task graph says *what* to run. The **scheduler** decides *where and when*: which worker runs which task, in what order, while keeping memory low.

| Scheduler | How to use | Workers | Best for |
|-----------|-----------|---------|----------|
| `"threads"` | default for DataFrame & Array | threads in your process | NumPy/pandas work (they release the GIL) |
| `"processes"` | default for Bag | separate Python processes | pure-Python code (strings, dicts, loops) |
| `"synchronous"` (`"sync"`) | debugging | none: runs in your thread, one task at a time | **debugging** (normal tracebacks, `pdb`) |
| **distributed** | `Client()` / `LocalCluster()` | processes × threads, with a dashboard | **recommended** for real work, even on a laptop |

Choosing a local scheduler:

```python
x.compute(scheduler="processes")                 # one call
with dask.config.set(scheduler="synchronous"):   # a block of code
    x.compute()
```

### Measured in `lecture.py` (2 cores)

| Work | synchronous | threads | processes | LocalCluster 2×1 |
|------|-------------|---------|-----------|------------------|
| pandas-style groupby on 2.4M rows | 0.27 s | **0.21 s** | 3.94 s ❌ | 0.24 s |
| 4 pure-Python CPU tasks | 0.55 s | 0.64 s | 1.50 s | **0.33 s** |

Lessons:
- **Threads** suit pandas/NumPy work. The `"processes"` scheduler was ~19× slower there, because it starts new processes and copies data to them on every call.
- For pure Python, threads don't help (the GIL). The one-shot `"processes"` scheduler pays startup costs each time, while a **LocalCluster keeps its worker processes warm**, so it wins.

## The distributed scheduler (recommended)

```python
from dask.distributed import Client, LocalCluster

if __name__ == "__main__":
    cluster = LocalCluster(n_workers=2, threads_per_worker=2, memory_limit="2GB")
    client = Client(cluster)
    print(client.dashboard_link)        # http://127.0.0.1:8787/status
    result = ddf.groupby("region").revenue.sum().compute()   # uses the cluster automatically
    client.close(); cluster.close()
```

Once a `Client` exists, **every** `.compute()` uses it automatically.

### Why use it even on one machine?

| Feature | Local schedulers | Distributed |
|---------|------------------|-------------|
| Live **dashboard** (task stream, memory, progress) | ❌ | ✅ |
| Memory limits per worker, **spilling to disk** | ❌ | ✅ |
| Smarter scheduling (data locality, work stealing) | basic | ✅ |
| Futures API (Lecture 14) | ❌ | ✅ |
| Same code scales to a real cluster | ❌ | ✅ |

### Workers, threads and memory

```
 LocalCluster(n_workers=2, threads_per_worker=2, memory_limit="2GB")

 ┌── worker 1 (process) ──┐   ┌── worker 2 (process) ──┐
 │ thread  thread   2 GB  │   │ thread  thread   2 GB  │
 └────────────────────────┘   └────────────────────────┘
```

- NumPy/pandas-heavy work: **fewer workers, more threads** (shared memory, no copying)
- Pure-Python work: **more workers, 1 thread each** (avoids the GIL)
- When a worker passes ~60% of its memory limit, it **spills** data to disk; at ~95% it's restarted.

### The dashboard

| Page | Shows |
|------|-------|
| **Status → Task Stream** | every task as a coloured bar: busy cores, idle gaps |
| **Progress** | tasks done / remaining per operation |
| **Memory** | per-worker memory; orange/grey means spilling |
| **Graph** | the live task graph |
| **Workers** | CPU, memory, network per worker |

## Scaling beyond your laptop

The **same code** runs on a real cluster. Only the cluster object changes:

| Where | Cluster object |
|-------|----------------|
| Laptop | `LocalCluster()` |
| HPC (SLURM, PBS) | `dask_jobqueue.SLURMCluster(...)` |
| Kubernetes | `dask_kubernetes.KubeCluster(...)` |
| Cloud | Coiled, Saturn Cloud, `dask_cloudprovider` |
| An existing scheduler | `Client("tcp://scheduler-address:8786")` |

## ⚠️ The `__main__` guard

`LocalCluster` starts worker **processes**. On Windows and macOS, and on Linux with recent Python versions, those processes re-import your script, so without the guard each worker would try to start its own cluster:

```python
def main():
    with LocalCluster() as cluster, Client(cluster) as client:
        ...

if __name__ == "__main__":
    main()
```

In **Jupyter notebooks** the guard isn't needed.

## Exercises

1. Run the lecture and watch the Task Stream while the groupby runs.
2. Compare `n_workers=1, threads_per_worker=2` vs `n_workers=2, threads_per_worker=1` for the pure-Python task in `lecture.py`.
3. Use `client.run(os.getpid)` to see each worker's process id.
4. Set `memory_limit="300MB"` and watch the dashboard as data spills.

<details><summary>Solutions</summary>

2. Pure Python: 2 processes × 1 thread is faster (no GIL contention). NumPy/pandas: about the same or slightly in favour of threads.
</details>

**Next →** [Lecture 14: Futures & Bag](../14_futures_and_bag/)
