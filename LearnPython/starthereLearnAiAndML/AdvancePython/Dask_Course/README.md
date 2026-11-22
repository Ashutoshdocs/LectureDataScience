# Dask: From Zero to Confident

A hands-on Dask course in 21 short lectures (00–20). It builds on the NumPy and pandas courses. **You should know pandas first**, because Dask DataFrames reuse its API.

Every lecture folder has:

| File | What it is |
|------|------------|
| `README.md` | The lesson: concepts, diagrams, tables, common mistakes, exercises (with solutions) |
| `lecture.py` | Runnable code for the lesson. Read it, run it, change it |

## Data

| File | Rows | Used for |
|------|------|----------|
| `data/sales.csv`, `customers.csv`, `students.csv` | 240 / 41 / 12 | small examples (the same files as the pandas course) |
| `data/big/sales_2025-01.csv … sales_2025-12.csv` | 2.4 million | "bigger than you'd want in pandas" examples |
| `data/big/customers_big.csv` | 20,000 | joins |
| `data/make_big_data.py` | n/a | builds `data/big/` |

**`data/big/` is not in the zip.** It's about 160 MB, so the first lecture that needs it builds it automatically (about 10 seconds). You can also build it yourself: `python data/make_big_data.py`.

## How to use this course

1. **Install Python 3.10+**, then the libraries:
   ```bash
   python -m pip install -r requirements.txt
   ```
2. Work through the folders **in order**: read `README.md`, run `python lecture.py` from inside the folder, then do the exercises.

## Course map

| # | Lecture | Big idea |
|---|---------|----------|
| 00 | [Prerequisites](00_prerequisites/) | pandas + NumPy, CPU cores, memory, processes vs threads |
| 01 | [What is Dask?](01_what_is_dask/) | Parallel, larger-than-memory Python that scales from laptop to cluster |
| 02 | [Lazy evaluation & task graphs](02_lazy_evaluation_task_graphs/) | Build a plan → `.compute()` |
| 03 | [`dask.delayed`](03_dask_delayed/) | Parallelise your own Python functions |
| 04 | [Dask Array](04_dask_array/) | NumPy in chunks |
| 05 | [DataFrame basics & partitions](05_dataframe_basics_partitions/) | Many pandas DataFrames acting as one |
| 06 | [Reading & writing files](06_reading_writing_files/) | Globs, `blocksize`, Parquet |
| 07 | [DataFrame operations](07_dataframe_operations/) | The pandas API, lazily |
| 08 | [GroupBy & aggregation](08_groupby_aggregation/) | Tree reductions, `split_out`, custom aggregations |
| 09 | [Index, divisions & shuffling](09_index_divisions_shuffling/) | Why `set_index` is expensive and when it pays off |
| 10 | [Joins & merge](10_joins_and_merge/) | Broadcast vs shuffle joins |
| 11 | [`map_partitions` & `meta`](11_map_partitions_and_meta/) | Run any pandas code on each partition |
| 12 | [Time series](12_time_series/) | Datetime index, `resample`, `rolling` |
| 13 | [Schedulers & LocalCluster](13_schedulers_and_local_cluster/) | threads / processes / distributed, and the dashboard |
| 14 | [Futures & Bag](14_futures_and_bag/) | Real-time task submission; semi-structured data |
| 15 | [`persist`, `compute` & memory](15_persist_compute_memory/) | Avoid recomputing; compute many things at once |
| 16 | [Performance: when Dask helps](16_performance_when_dask_helps/) | Dask vs pandas, honestly measured |
| 17 | [Debugging & best practices](17_debugging_best_practices/) | The synchronous scheduler, dtype errors, partition sizing |
| 18 | [Project: big sales pipeline](18_project_big_sales_pipeline/) | 12 CSVs → clean Parquet → report |
| 19 | [Project: parallel file processing](19_project_parallel_file_processing/) | `delayed` + futures for custom work |
| 20 | [Recap & cheat sheet](20_recap_cheatsheet/) | pandas → Dask translation, decision guide |

## Run everything at once

```bash
python run_all.py
```

## Version notes

Tested with **Dask 2026.8** and pandas 3.0 on a small 2-core machine.

- Modern Dask DataFrames use a **query optimiser** ("dask-expr"). It's on by default and needs no setup. Older tutorials that mention `dask.config.set({"dataframe.query-planning": False})` are out of date.
- Lectures that start worker **processes** (13, 14, 19) wrap their code in `if __name__ == "__main__":`. That's required on Windows, macOS and recent Python versions. Lecture 13 explains why.
- `.visualize()` draws task graphs only if the **Graphviz** program is installed (`conda install python-graphviz`, or the OS package plus `pip install graphviz`). The lectures skip that step gracefully if it's missing.
