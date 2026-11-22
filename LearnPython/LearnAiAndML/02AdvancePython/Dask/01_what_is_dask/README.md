# Lecture 01: What is Dask, and why use it?

Run: `python lecture.py`

## Definition

**Dask** is a free, open-source Python library for **parallel and larger-than-memory computing**. It splits big work into many small tasks, runs them across all your CPU cores (or many machines), and handles data that doesn't fit in RAM by working on one piece at a time.

Its key design choice: **it mimics libraries you already know.**

| Dask collection | Mimics | Made of |
|-----------------|--------|---------|
| `dask.dataframe` | pandas | many pandas DataFrames (**partitions**) |
| `dask.array` | NumPy | many NumPy arrays (**chunks**) |
| `dask.bag` | lists / iterators | many Python lists (for JSON, logs, text) |
| `dask.delayed` | your own functions | any Python function calls |
| `dask.distributed` futures | `concurrent.futures` | tasks submitted in real time |

```
         one big Dask DataFrame (what you see)
 ┌────────────────────────────────────────────────┐
 │ partition 0 │ partition 1 │ partition 2 │ ...  │   each partition = a normal pandas DataFrame
 └────────────────────────────────────────────────┘
       ↓              ↓              ↓
    core 1         core 2         core 3            processed in parallel
```

## Why use Dask?

| Problem | What Dask does |
|---------|----------------|
| Data is **bigger than RAM** (e.g. 50 GB of CSVs on a 16 GB laptop) | streams it partition by partition |
| pandas uses **one core** | uses all of them |
| Data is in **many files** | `dd.read_csv("logs/*.csv")` treats them as one table |
| A slow Python loop over independent items | `dask.delayed` / futures run them in parallel |
| Outgrowing one machine | the same code runs on a **cluster** (Kubernetes, HPC, cloud) |

## How it works: lazy task graphs

```python
total = ddf["units"].sum()      # nothing computed yet: a task graph is built
total.compute()                 # NOW the scheduler runs the graph in parallel
```

1. You write pandas/NumPy-style code. Dask records it as a **task graph** (tasks + dependencies).
2. An **optimiser** simplifies the graph: drop unused columns, push filters early, merge steps.
3. A **scheduler** executes the tasks in parallel, keeping memory low.

Lecture 02 is all about this.

## Dask vs pandas vs Polars vs Spark

| | pandas | Polars | **Dask** | Spark |
|---|---|---|---|---|
| Larger than RAM | ❌ | ✅ streaming | ✅ | ✅ |
| Multi-core | ❌ | ✅ | ✅ | ✅ |
| Multi-machine cluster | ❌ | limited | ✅ | ✅ |
| API | pandas | its own | **pandas / NumPy** | its own (PySpark) |
| Parallelise *any* Python code | ❌ | ❌ | ✅ `delayed`, futures | limited |
| Arrays / ML / science | via NumPy | ❌ | ✅ Dask Array, Xarray, ML | MLlib |
| Overhead on small data | none | tiny | noticeable | large |

**When to choose Dask:** your team knows pandas/NumPy, data is too big for one pandas DataFrame or spread across many files, you need custom Python parallelism, or you'll scale to a cluster.

**When not to:** data fits comfortably in memory. Then plain pandas (or Polars) is simpler and often faster. Dask's own docs say this too.

## Exercises

1. Run `lecture.py`. How many partitions does the Dask DataFrame have, and how big is each?
2. What type is `ddf["units"].sum()` before and after `.compute()`?
3. Change `npartitions` in `from_pandas`. Does the answer change?

<details><summary>Solutions</summary>

2. A lazy Dask `Scalar` before; a plain number after.
3. No. Partitioning changes *how* the work is split, never the result.
</details>

**Next →** [Lecture 02: Lazy evaluation & task graphs](../02_lazy_evaluation_task_graphs/)
