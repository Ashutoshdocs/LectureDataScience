# Python Dask — From Scratch to Advanced

A beginner-friendly, practical teaching guide to Dask: parallel and distributed computing in Python. Learn why Dask is useful, how it works, how to use Dask DataFrame and Array, how lazy execution and task graphs work, and how to build practical data-processing projects.

> **Core idea:** Dask helps scale familiar Python workflows beyond the limits of a single eager in-memory operation by dividing work into tasks or partitions and scheduling them. Dask can run on a single machine using multiple cores or connect to a distributed cluster.

---

## Repository structure

```text
Python_Dask_Toolkit/
│
├── README.md
├── requirements.txt
│
├── project_01_large_csv_data_analysis/
│   ├── README.md
│   ├── main.py
│   ├── analysis.py
│   ├── data/
│   │   ├── input/
│   │   │   ├── sales_part_1.csv
│   │   │   └── sales_part_2.csv
│   │   └── reference/
│   │       └── regions.csv
│   └── output/
│
└── project_02_dask_parallel_processing/
    ├── README.md
    ├── main.py
    ├── tasks.py
    ├── data/
    │   └── input/
    │       └── numbers.txt
    ├── output/
    └── logs/
```

Input data, reference data, generated output, and logs are kept in separate folders. The code uses paths relative to the script so the projects can be run from the repository root or from inside each project folder.

## Learning outcomes

By the end, learners should be able to:

1. Explain what Dask is and why it is useful.
2. Understand parallel computing, distributed computing, tasks, and partitions.
3. Understand lazy execution and task graphs.
4. Install Dask and start the local dashboard.
5. Use Dask Delayed for task-based parallelism.
6. Use Dask DataFrame to process CSV datasets.
7. Understand partitions and partition sizes.
8. Filter, select, transform, group, aggregate, and join data.
9. Understand when to call `compute()` and when to use `persist()`.
10. Use Dask Array for chunked numerical operations.
11. Use the distributed scheduler and LocalCluster.
12. Inspect task graphs and the dashboard.
13. Write outputs to CSV and Parquet.
14. Understand common performance and memory pitfalls.
15. Build a large CSV analytics project and a parallel task-processing project.

---

# Part 1 — Foundations

## Chapter 1 — What is Dask?

Dask is a Python library for parallel and distributed computing. It provides tools to scale computations across:
- Multiple CPU cores on one machine.
- Multiple machines in a cluster.
- Large datasets divided into smaller partitions or chunks.

Dask integrates with familiar Python tools and provides APIs such as:
- Dask DataFrame
- Dask Array
- Dask Delayed
- Dask Bag
- Dask Futures and Distributed Client

## Chapter 2 — Why do we need Dask?

Imagine a CSV file with tens or hundreds of gigabytes of data.

A basic pandas workflow may try to load the entire dataset into memory:

```python
import pandas as pd

df = pd.read_csv("very_large_file.csv")
```

If the file and intermediate operations exceed available RAM, the program may become slow or fail.

Dask can split work into partitions and execute tasks in parallel:

```python
import dask.dataframe as dd

df = dd.read_csv("very_large_file.csv")
```

This creates a Dask DataFrame backed by partitions. Most operations are lazy and build a task graph. Work is executed when a result is requested with methods such as `.compute()` or when data is written.

Dask does not make every task automatically faster. For small data, scheduling overhead may make it slower than pandas or Polars.

## Chapter 3 — Parallel vs distributed computing

**Parallel computing:** multiple tasks or parts of a task execute at the same time, commonly across multiple CPU cores.

**Distributed computing:** work is coordinated across multiple processes or machines connected over a network.

Dask supports both:
- Local threaded or process-based execution.
- Distributed execution across workers, including multiple machines.

## Chapter 4 — What is a task?

A task is a unit of work that a scheduler can execute.

Example:
1. Read partition 1.
2. Read partition 2.
3. Filter each partition.
4. Combine partial results.
5. Produce the final result.

Dask represents these operations as a graph of dependent tasks.

## Chapter 5 — What is a partition?

A partition is a piece of a larger dataset.

For a DataFrame, each partition is typically a smaller pandas DataFrame. Dask coordinates operations across those partitions.

Example:

```text
Large CSV dataset
       |
       v
+-------------+  +-------------+  +-------------+
| Partition 1 |  | Partition 2 |  | Partition 3 |
+-------------+  +-------------+  +-------------+
       |                |                |
       +----------------+----------------+
                        |
                  Dask scheduler
                        |
                   Final result
```

Partitions allow work to be performed in parallel, but too many tiny partitions or a few huge partitions can hurt performance.

## Chapter 6 — Install Dask

Create a virtual environment.

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the packages used in this course:

```bash
python -m pip install --upgrade pip
pip install "dask[dataframe,distributed]"
```

For optional Dask Array support:

```bash
pip install "dask[array]"
```

Check installation:

```bash
python -c "import dask; print(dask.__version__)"
```

## Chapter 7 — Import Dask

```python
import dask
import dask.dataframe as dd
import dask.array as da
from dask import delayed

print(dask.__version__)
```

Common aliases:
- `dd` for Dask DataFrame.
- `da` for Dask Array.

## Chapter 8 — Dask is lazy

Many Dask operations do not immediately calculate the final answer. They create a graph describing the work.

```python
import dask.dataframe as dd

df = dd.read_csv("data/input/sales.csv")
filtered = df[df["amount"] > 1000]

print(filtered)
```

The result is a Dask DataFrame, not necessarily a fully materialized pandas DataFrame.

To execute and bring the result into memory:

```python
result = filtered.compute()
print(result)
```

Only call `.compute()` when the result is small enough to fit in memory.

## Chapter 9 — What is a task graph?

A task graph describes operations and their dependencies.

```python
import dask

def add(a, b):
    return a + b

result = dask.delayed(add)(10, 20)

print(result)       # Delayed object
print(result.compute())  # Executes and returns 30
```

Dask knows that `add(10, 20)` must execute to produce the final result.

## Chapter 10 — Schedulers

The scheduler decides how tasks are executed.

Common choices:
- Synchronous: runs tasks sequentially; useful for debugging.
- Threads: uses multiple threads in one process.
- Processes: uses multiple worker processes.
- Distributed: uses Dask's distributed scheduler and workers.

Example:

```python
import dask

result = dask.delayed(sum)([1, 2, 3])

print(result.compute(scheduler="synchronous"))
print(result.compute(scheduler="threads"))
print(result.compute(scheduler="processes"))
```

The best scheduler depends on the task:
- Threads can work well for I/O and operations that release the Python GIL.
- Processes can help CPU-bound Python code but have process and data-transfer overhead.
- Distributed supports monitoring and multi-worker execution.

---

# Part 2 — Dask Delayed

## Chapter 11 — What is `delayed`?

`dask.delayed` wraps ordinary Python functions so that calls create delayed tasks instead of immediately running the function.

```python
from dask import delayed

@delayed
def multiply(a, b):
    return a * b

result = multiply(5, 4)
print(result.compute())
```

## Chapter 12 — Build multiple tasks

```python
from dask import delayed

@delayed
def square(number):
    return number * number

tasks = [square(number) for number in range(1, 6)]

results = delayed(sum)(tasks).compute()
print(results)
```

Dask can execute independent square operations in parallel before the final sum.

## Chapter 13 — Build a dependency graph

```python
from dask import delayed

@delayed
def load_value():
    return 10

@delayed
def multiply(value):
    return value * 5

@delayed
def add_tax(value):
    return value * 1.18

value = load_value()
subtotal = multiply(value)
final_value = add_tax(subtotal)

print(final_value.compute())
```

The graph contains dependencies: `multiply` waits for `load_value`, and `add_tax` waits for `multiply`.

## Chapter 14 — Parallel file processing

```python
from pathlib import Path
from dask import delayed, compute

def count_lines(file_path):
    with open(file_path, encoding="utf-8") as file:
        return sum(1 for _ in file)

files = list(Path("data").glob("*.txt"))
tasks = [delayed(count_lines)(path) for path in files]

counts = compute(*tasks)
print(counts)
```

This is useful when many independent files need similar processing.

## Chapter 15 — When to use Delayed

Good use cases:
- Independent file processing.
- CPU or I/O tasks that can run separately.
- Combining existing Python functions into a task graph.
- Workflows that are not naturally tabular or array-based.

For tabular data, consider Dask DataFrame. For chunked numerical arrays, consider Dask Array.

---

# Part 3 — Dask DataFrame

## Chapter 16 — What is a Dask DataFrame?

A Dask DataFrame is a collection of pandas DataFrame partitions with a Dask task graph coordinating operations.

```python
import dask.dataframe as dd

df = dd.read_csv("data/input/sales_part_*.csv")

print(df)
print(df.npartitions)
print(df.columns)
print(df.dtypes)
```

The partitions can be processed independently for many operations.

## Chapter 17 — Read CSV files

Read one file:

```python
df = dd.read_csv("data/input/sales.csv")
```

Read multiple matching files:

```python
df = dd.read_csv("data/input/sales_part_*.csv")
```

Dask can read multiple files as partitions. The exact partition layout depends on file sizes and read options.

## Chapter 18 — Read Parquet

```python
df = dd.read_parquet("data/input/parquet_folder/")
```

Parquet is commonly useful for analytical workloads because it is columnar and stores schema information.

## Chapter 19 — Inspect a Dask DataFrame

```python
print(df.head())
print(df.tail())
print(df.columns)
print(df.dtypes)
print(df.npartitions)
print(df.divisions)
```

`head()` typically computes only enough partitions to return the requested number of rows. Use `compute()` only when the result is safe to materialize.

## Chapter 20 — Select columns

```python
selected = df[["order_id", "region", "amount"]]
```

## Chapter 21 — Filter rows

```python
high_value = df[df["amount"] > 1000]
```

Multiple conditions:

```python
filtered = df[
    (df["amount"] > 1000) &
    (df["region"] == "West")
]
```

Use parentheses around each condition.

## Chapter 22 — Add calculated columns

```python
df["revenue"] = df["quantity"] * df["unit_price"]
```

This creates a lazy transformation in the Dask DataFrame graph.

## Chapter 23 — Group and aggregate

```python
summary = df.groupby("region")["revenue"].sum()
result = summary.compute()
```

Multiple aggregations:

```python
summary = df.groupby("region").agg({
    "revenue": ["sum", "mean"],
    "order_id": "count",
})

result = summary.compute()
```

The supported aggregation syntax and output column layout can vary with the operation; inspect the resulting metadata and dtypes.

## Chapter 24 — Sort values

```python
sorted_df = df.sort_values("revenue")
```

A global sort can require expensive shuffles and data movement. Do not sort a large distributed dataset unless the task requires it.

## Chapter 25 — Handle missing values

```python
null_counts = df.isna().sum().compute()
```

Fill missing values:

```python
cleaned = df.fillna({"quantity": 0})
```

Drop rows with missing values:

```python
cleaned = df.dropna()
```

Choose a data-quality rule based on business meaning. Zero is not a universal replacement for missing data.

## Chapter 26 — Remove duplicates

```python
unique_df = df.drop_duplicates(subset=["order_id"])
```

Duplicate removal can require data movement between partitions. Understand the cost and define which record should be retained.

## Chapter 27 — Join DataFrames

```python
joined = sales.merge(products, on="product_id", how="left")
```

Joins can be expensive, especially when data must be shuffled across partitions. Small lookup/reference tables may be handled differently from two large distributed tables.

## Chapter 28 — Concatenate DataFrames

```python
import dask.dataframe as dd

combined = dd.concat([df_2025, df_2026])
```

Ensure the schemas and dtypes are compatible before concatenating.

## Chapter 29 — Compute vs persist

`compute()` executes the graph and returns a concrete result, often a pandas DataFrame or scalar.

```python
small_result = df.head(10)
```

For a result you plan to reuse in multiple later computations, `persist()` can keep partitions available in the scheduler's memory:

```python
persisted = df.persist()
```

With a distributed client, persistence is coordinated across workers. It consumes memory, so use it intentionally.

## Chapter 30 — Write CSV output

```python
df.to_csv("output/part-*.csv", index=False)
```

Dask may write one output file per partition. The wildcard is a filename pattern for the output files.

To write a single file, use the supported single-file option for the installed version, but note that combining partitions into one file may require extra work and can reduce parallelism.

## Chapter 31 — Write Parquet output

```python
df.to_parquet("output/parquet_folder/", write_index=False)
```

Dask writes partitioned Parquet datasets. This is often a practical output format for larger analytics workloads.

---

# Part 4 — Dask Array

## Chapter 32 — What is Dask Array?

Dask Array is a chunked, parallel array library inspired by NumPy.

A large array is divided into smaller NumPy arrays called chunks.

```python
import dask.array as da

array = da.arange(0, 100, chunks=20)

print(array)
print(array.chunks)
```

## Chapter 33 — Create arrays

```python
import dask.array as da

a = da.ones((1000, 1000), chunks=(250, 250))
b = da.zeros((1000, 1000), chunks=(250, 250))
```

The arrays are represented lazily as chunked computations.

## Chapter 34 — Array operations

```python
c = a + b
d = c * 10

print(d.compute())
```

Calling `.compute()` materializes the complete result. Ensure it fits in memory.

## Chapter 35 — NumPy and Dask Array

Dask Array provides familiar array operations:

```python
import dask.array as da

values = da.random.random((10000, 10000), chunks=(1000, 1000))
mean_value = values.mean()

print(mean_value.compute())
```

Chunk size affects scheduling overhead, memory use, and performance. Choose chunks based on the operation and available memory.

---

# Part 5 — Distributed execution and dashboard

## Chapter 36 — What is `Client`?

The Dask Distributed Client connects your Python program to a scheduler and workers.

For a local cluster:

```python
from dask.distributed import Client

client = Client()
print(client)
```

This generally starts a local distributed scheduler and workers.

## Chapter 37 — LocalCluster

```python
from dask.distributed import Client, LocalCluster

cluster = LocalCluster(
    n_workers=2,
    threads_per_worker=2,
    processes=True,
    dashboard_address=":8787",
)

client = Client(cluster)
print(client.dashboard_link)
```

The dashboard link is usually available locally in a browser. The exact port can vary if the requested port is unavailable.

## Chapter 38 — Dask dashboard

The dashboard helps inspect:
- Task progress.
- Worker status.
- CPU and memory use.
- Task stream.
- Scheduler activity.
- Data transfer and communication.

Use the dashboard to understand what the cluster is doing rather than treating Dask as a black box.

## Chapter 39 — Submit tasks to the distributed scheduler

```python
from dask.distributed import Client

def square(x):
    return x * x

client = Client()
futures = client.map(square, range(10))
results = client.gather(futures)

print(results)
client.close()
```

Futures represent computations that may still be running. `gather()` collects their results.

## Chapter 40 — Close the client

```python
client.close()
```

Use context managers or `try/finally` in longer applications so cluster resources are released.

---

# Part 6 — Performance and best practices

## Chapter 41 — When Dask is useful

Dask is useful when:
- Data is too large for a straightforward in-memory workflow.
- Work can be divided into partitions or independent tasks.
- You need parallel execution across cores or machines.
- You need a scalable task graph and monitoring.

Dask may not be the best choice when:
- The dataset is small and fits comfortably in memory.
- The task is simple and scheduling overhead dominates.
- The algorithm cannot be divided efficiently.
- A database or distributed query engine is a better fit.

## Chapter 42 — Partition sizing

Very small partitions create scheduling overhead. Very large partitions can create memory pressure.

Choose partition sizes based on:
- Available RAM per worker.
- Number of workers.
- Operation complexity.
- Data types and intermediate expansion.
- Storage format and file sizes.

Inspect partition information:

```python
print(df.npartitions)
print(df.memory_usage_per_partition().compute())
```

## Chapter 43 — Avoid unnecessary `compute()`

Bad pattern:

```python
# Repeatedly executes separate work.
total = df["amount"].sum().compute()
average = df["amount"].mean().compute()
```

Prefer building related computations together where practical:

```python
result = df[["amount"]].agg(["sum", "mean"]).compute()
```

The exact aggregation API depends on the object and Dask version; the teaching principle is to avoid repeatedly executing overlapping graphs.

## Chapter 44 — Avoid unnecessary shuffles

Operations such as global sorting, certain joins, and groupings can require data movement between partitions.

- Filter and select columns early.
- Use appropriate partitioning where possible.
- Avoid global sort unless required.
- Consider whether a small lookup table can be broadcast or otherwise joined efficiently.
- Inspect the task graph and dashboard.

## Chapter 45 — Dask vs pandas vs Polars

| Feature | pandas | Polars | Dask |
|---|---|---|---|
| Typical execution | Eager | Eager and lazy | Lazy task graphs |
| Main focus | In-memory DataFrames | Fast DataFrame engine | Parallel/distributed computation |
| Scaling model | Usually one machine's memory | Efficient single-machine execution; streaming/lazy features | Partitions across cores or machines |
| API style | DataFrame/Series methods | Expressions | Dask collections and task graphs |
| Best fit | Small to medium in-memory work and broad ecosystem | Fast analytics and transformations | Workloads needing parallel/distributed execution |

These are broad tendencies, not absolute limits. Polars and Dask can overlap in capabilities; benchmark the actual workload.

## Chapter 46 — Common mistakes

1. Calling `.compute()` on a huge dataset and exhausting RAM.
2. Creating too many tiny partitions.
3. Creating partitions that are too large for worker memory.
4. Using Dask for tiny datasets where pandas or Polars is simpler.
5. Ignoring the cost of joins and shuffles.
6. Recomputing the same graph repeatedly.
7. Forgetting to close a distributed client.
8. Assuming every pandas operation has identical Dask behavior.
9. Treating a Dask DataFrame as if it were already a pandas DataFrame.
10. Not inspecting task graphs or the dashboard when performance is poor.

---

# Part 7 — Practical projects

## Project 1 — Large CSV Data Analysis

Location: `project_01_large_csv_data_analysis/`

Build a sales analytics pipeline that:
- Reads multiple CSV files with Dask.
- Inspects partitions and schema.
- Adds revenue calculations.
- Filters high-value sales.
- Joins region reference data.
- Aggregates sales by region.
- Writes partitioned CSV and Parquet outputs.

Run:

```bash
python project_01_large_csv_data_analysis/main.py
```

Read the project README for detailed walkthrough and exercises.

## Project 2 — Dask Parallel Processing

Location: `project_02_dask_parallel_processing/`

Build a parallel task-processing application that:
- Reads a list of numbers.
- Creates independent delayed tasks.
- Calculates square, cube, and summary values.
- Executes tasks using a local distributed cluster.
- Displays the dashboard link.
- Writes results and logs.

Run:

```bash
python project_02_dask_parallel_processing/main.py
```

Read the project README for detailed walkthrough and exercises.

---

# Part 8 — Practice questions

1. What is Dask?
2. Why might pandas run out of memory?
3. What is parallel computing?
4. What is distributed computing?
5. What is a task?
6. What is a task graph?
7. What is a partition?
8. What does lazy execution mean?
9. What does `.compute()` do?
10. What does `.persist()` do?
11. What is Dask Delayed?
12. When should you use Dask DataFrame?
13. What is the difference between Dask DataFrame and pandas DataFrame?
14. What does `dd.read_csv()` return?
15. Why can `head()` be safer than computing an entire dataset?
16. What is the purpose of `npartitions`?
17. Why can joins be expensive?
18. What is Dask Array?
19. What are chunks?
20. What does a Distributed Client do?
21. What is a LocalCluster?
22. What information can the dashboard show?
23. Why should you close a client?
24. What is a shuffle?
25. When might Polars be a better choice than Dask?
26. Why should partition sizes be tuned?
27. Why should repeated `.compute()` calls be avoided?
28. When is Dask not necessary?
29. What is the difference between `compute()` and `persist()`?
30. How would you process many independent files in parallel?

## Final teaching sequence

1. Explain the limitations of loading all data into memory.
2. Introduce parallel and distributed computing.
3. Explain tasks, graphs, and partitions.
4. Install Dask and run a Delayed example.
5. Build a dependency graph and process independent files.
6. Introduce Dask DataFrame and read multiple CSVs.
7. Filter, transform, group, and join.
8. Explain `compute()` and `persist()`.
9. Introduce Dask Array and chunks.
10. Start LocalCluster and open the dashboard.
11. Inspect task execution and memory.
12. Build Project 1.
13. Build Project 2.
14. Compare pandas, Polars, and Dask on a representative dataset.

## Key takeaway

Use **Dask when work can be divided into tasks, partitions, or chunks and benefits from parallel or distributed execution**. Understand lazy graphs, partition sizes, scheduler overhead, memory use, and data movement before scaling a workflow.
