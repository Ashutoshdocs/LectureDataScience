# Project 2 — Dask Parallel Processing with Delayed and Distributed

## Goal

Build a parallel task workflow. Read numbers from a text file, create independent delayed calculations, execute them with a local distributed cluster, and save the results.

## Folder structure

```text
project_02_dask_parallel_processing/
├── README.md
├── main.py
├── tasks.py
├── data/
│   └── input/
│       └── numbers.txt
├── output/
└── logs/
```

## Setup

From repository root:

```bash
pip install -r requirements.txt
```

## Run

```bash
python project_02_dask_parallel_processing/main.py
```

The script starts a local Dask cluster. It prints the dashboard link; open it in a browser while the tasks run.

## What the project does

1. Reads numbers from `data/input/numbers.txt`.
2. Wraps square and cube calculations with `dask.delayed`.
3. Builds a graph of independent tasks.
4. Uses a distributed Client and LocalCluster.
5. Computes results.
6. Writes the results to `output/parallel_results.csv`.
7. Logs the run.

## Concepts demonstrated

```python
from dask import delayed, compute
from dask.distributed import Client, LocalCluster

@delayed
def square(value):
    return value * value

task = square(10)
task.compute()

cluster = LocalCluster(n_workers=2, threads_per_worker=1)
client = Client(cluster)
```

## Student exercises

1. Add a function that calculates the cube.
2. Add a function that determines whether a number is prime.
3. Process a much larger input list.
4. Compare synchronous, threaded, process, and distributed execution.
5. Increase worker count and observe dashboard changes.
6. Add a task that sleeps briefly to make task activity easier to observe.
7. Save a separate summary with minimum, maximum, and average.
8. Add error handling for invalid input lines.
9. Compare execution time for a sequential loop and Dask Delayed.
10. Close the client and cluster using a `finally` block or context managers.

## Important

Small arithmetic tasks are intentionally simple for teaching. Dask scheduling overhead may exceed the computation time. Use larger or more expensive independent tasks to demonstrate meaningful speedup.
