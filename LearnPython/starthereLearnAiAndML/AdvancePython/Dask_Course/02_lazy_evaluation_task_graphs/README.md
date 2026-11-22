# Lecture 02: Lazy evaluation & task graphs

Run: `python lecture.py`

## Lazy by default

Every Dask operation returns a **lazy** object, a *description* of work:

```python
filtered = ddf[ddf.units >= 4]        # instant: nothing read or computed
total = filtered.units.sum()          # instant
total.compute()                       # runs everything now
```

| Trigger | Does |
|---------|------|
| `x.compute()` | run and return a **pandas/NumPy/Python** result (must fit in memory!) |
| `dask.compute(a, b, c)` | run several results **together**, sharing common work |
| `x.persist()` | run and keep the result **in memory as Dask** (Lecture 15) |
| `x.head()` | compute just enough partitions for a preview |
| `len(ddf)` | counts rows (runs a computation) |
| `ddf.to_parquet(...)` | runs and writes to disk |

## The task graph

Dask turns your code into a **directed acyclic graph** (DAG):

```
 read part 0 ─► filter ─► sum ─┐
 read part 1 ─► filter ─► sum ─┼─► total sum ─► result
 read part 2 ─► filter ─► sum ─┘
```

- **Nodes** = tasks (small Python function calls on one partition/chunk)
- **Edges** = dependencies
- Tasks without dependencies between them run **in parallel**

Inspect it:

```python
len(total.__dask_graph__())     # number of tasks
total.dask                      # the graph itself (a mapping)
total.visualize("graph.png")    # picture (needs Graphviz installed)
ddf.pprint()                    # DataFrame expression tree, as text
ddf.optimize().pprint()         # after the optimiser
```

## The optimiser (Dask DataFrame)

Before running, Dask DataFrame rewrites the expression tree:

| Optimisation | Example |
|--------------|---------|
| **Column projection** | you use 2 of 8 columns, so only those are read from Parquet |
| **Predicate pushdown** | filters applied while reading Parquet |
| **Combining steps** | `assign` + `filter` + `sum` fused into one task per partition |
| **Lowering** | picks the right algorithm (e.g. broadcast vs shuffle join) from partition counts |

## Why lazy?

1. **Larger-than-memory**: Dask can stream: read a piece, process it, free it.
2. **Optimisation**: seeing the whole plan lets Dask skip work.
3. **Sharing**: `dask.compute(a, b)` reads the data once for both.

## ⚠️ The #1 beginner mistake: calling `compute()` too often

```python
for region in regions:                                        # ❌ reads ALL files 4 times
    print(ddf[ddf.region == region].units.sum().compute())

results = dask.compute(*[ddf[ddf.region == r].units.sum() for r in regions])   # ✅ once
print(ddf.groupby("region").units.sum().compute())                            # ✅ even better
```

Measured in `lecture.py` on the 2.4M-row dataset (2-core machine): **4 separate `compute()` calls took 10.3 s**, while one `dask.compute(...)` or one `groupby` took **2.6 s**.

## Exercises

1. Build a three-step pipeline and count its tasks before and after `.optimize()`.
2. Time two separate `.compute()` calls against one `dask.compute(a, b)`.
3. If Graphviz is installed, `.visualize()` a small graph.

<details><summary>Solution hints</summary>

Use `len(x.__dask_graph__())` for task counts. `lecture.py` sections 3 and 5 show the timing pattern.
</details>

**Next →** [Lecture 03: `dask.delayed`](../03_dask_delayed/)
