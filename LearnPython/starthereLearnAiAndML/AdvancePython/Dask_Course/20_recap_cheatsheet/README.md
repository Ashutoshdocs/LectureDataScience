# Lecture 20: Recap, pandas → Dask translation & cheat sheet

Run: `python lecture.py` (a self-test: predict each answer first)

## Dask in one picture

```
 Your code (pandas / NumPy / plain-Python style)
        │  builds
        ▼
 Task graph  ──►  Optimiser  ──►  Scheduler  ──►  Workers (cores / machines)
 (lazy)           (drop columns,   (threads,        process partitions/chunks
                  push filters,    processes,       in parallel, within memory)
                  fuse steps)      distributed)
        ▲
        └──── .compute() / .persist() / dask.compute(...) / .to_parquet()
```

## The five collections

| Collection | Use for | Made of |
|------------|---------|---------|
| `dask.dataframe` | big tables | pandas partitions |
| `dask.array` | big N-dimensional arrays | NumPy chunks |
| `dask.bag` | messy JSON / text / logs | Python lists |
| `dask.delayed` | your own functions → a graph | function calls |
| futures (`client.submit/map`) | real-time, dynamic task submission | function calls |

## pandas → Dask DataFrame

| Task | pandas | Dask |
|------|--------|------|
| Import | `import pandas as pd` | `import dask.dataframe as dd` |
| Read many CSVs | loop + `pd.concat` | `dd.read_csv("data/*.csv", dtype={...})` |
| Read Parquet | `pd.read_parquet(f)` | `dd.read_parquet(folder, columns=..., filters=...)` |
| From pandas | n/a | `dd.from_pandas(pdf, npartitions=8)` |
| Get the result | it's already there | `.compute()` |
| Several results | n/a | `dask.compute(a, b, c)` |
| Keep in memory | n/a | `.persist()` |
| Preview | `df.head()` | `ddf.head()` (first partition only) |
| Row count | `len(df)` | `len(ddf)` (full pass!) |
| Filter / new column / groupby / merge | same | same (lazy) |
| `df.iloc[5]` | ✅ | ❌ filter by a column instead |
| `df.loc[label]` | ✅ | ✅ fast only with a sorted index (`set_index`) |
| `apply(axis=1)` | slow | slower; use vectorized code or `map_partitions(meta=...)` |
| Custom pandas per chunk | n/a | `ddf.map_partitions(func, meta=...)` |
| Neighbouring rows | `shift`, `rolling` | `map_overlap(func, before=, after=)` |
| Median / quantile | exact | approximate (`median_approximate`, `quantile`) |
| Sort everything | cheap | expensive (shuffle); prefer `nlargest` |
| `resample` | any freq | needs a sorted datetime index; mind partition edges (`"MS"`) |
| Write | `df.to_csv(f)` | `ddf.to_parquet(folder)` (one file per partition) |

## Cheat sheet

```python
import dask, dask.dataframe as dd, dask.array as da, dask.bag as db
from dask.distributed import Client, LocalCluster

if __name__ == "__main__":
    client = Client(LocalCluster(n_workers=4, threads_per_worker=2))   # dashboard: client.dashboard_link

    ddf = dd.read_csv("raw/*.csv", dtype={"units": "float64"}, parse_dates=["ts"])
    ddf = ddf.assign(revenue=ddf.units * ddf.price).dropna(subset=["units"])
    ddf.to_parquet("clean/", partition_on=["region"])                  # convert once

    ddf = dd.read_parquet("clean/")
    total, by_region = dask.compute(ddf.revenue.sum(), ddf.groupby("region").revenue.sum())
    ddf = ddf.set_index("ts", sorted=True)                             # time index, known divisions
    monthly = ddf.revenue.resample("MS").sum().compute()
    ddf.map_partitions(my_pandas_func, meta=ddf._meta.assign(new=0.0))

    x = da.random.default_rng(0).random((50_000, 50_000), chunks=(5_000, 5_000))
    x.mean(axis=0).compute()

    results = dask.compute(*[dask.delayed(process)(f) for f in files])
    futures = client.map(simulate, range(100), pure=False)

    with dask.config.set(scheduler="synchronous"):                     # debugging
        ddf.head()
```

## Top 12 Dask mistakes

| Mistake | Fix |
|---------|-----|
| `.compute()` inside a loop | one `dask.compute(*many)` or a groupby |
| `ddf.compute()` on huge data | reduce first (filter / aggregate) |
| Using Dask on small data | pandas is faster below ~1/5 of your RAM |
| CSV for repeated analysis | convert to Parquet once |
| Tiny partitions / tiny tasks | ~100 MB partitions, ≥100 ms tasks |
| Not declaring CSV dtypes | `dtype={...}`, or Parquet |
| No `meta` in `map_partitions` | pass `meta=` |
| Per-partition logic for global values (mean, rank) | compute the global value first; shuffle if needed |
| Shuffle joins with a small table | keep the small table in pandas (broadcast) |
| `set_index` again and again | once, `sorted=True` if possible, save to Parquet |
| Missing `if __name__ == "__main__":` | add it whenever processes / clusters are involved |
| Processes scheduler with a few big tasks | `chunksize=1`, or use a LocalCluster |

## When to use what

| Situation | Tool |
|-----------|------|
| Data fits in memory, pandas speed is fine | **pandas** |
| Fits in memory, need more speed, single machine | **Polars** (or DuckDB) |
| Bigger than memory, or many files, pandas-style code | **Dask DataFrame** |
| Large arrays, scientific data | **Dask Array** (+ Xarray) |
| Custom Python functions in parallel | **dask.delayed** / futures |
| Must scale to a cluster | **Dask** (or Spark) |

## Where to go next

- Docs and best practices: https://docs.dask.org/en/stable/best-practices.html
- Dask tutorial: https://tutorial.dask.org/
- **Xarray**: labelled N-D arrays on top of Dask (climate, satellite data)
- **dask-ml** / XGBoost / LightGBM: distributed machine learning
- **Coiled**, `dask-jobqueue`, `dask-kubernetes`: running on real clusters
