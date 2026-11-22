# Lecture 00: Prerequisites, what you need before Dask

Run: `python lecture.py`

Dask is a tool for **scaling** Python you already know. It doesn't replace pandas or NumPy; it runs **many** pandas/NumPy pieces in parallel. You need those first.

## Checklist

| Skill | Why Dask needs it |
|-------|-------------------|
| **pandas**: read_csv, filter, assign, groupby, merge, dtypes | Dask DataFrame *is* many pandas DataFrames, with the same API |
| **NumPy**: arrays, shapes, vectorized maths | Dask Array *is* many NumPy arrays |
| Functions, `lambda`, `if __name__ == "__main__":` | You'll parallelise your own functions; worker processes need the main guard |
| Lists, comprehensions, `zip` | Building lists of tasks |
| Files & glob patterns | `dd.read_csv("data/big/*.csv")` reads many files at once |
| A rough idea of **CPU cores** and **RAM** | That's what Dask manages for you |

## 1. Your computer's resources

```python
import os, psutil
os.cpu_count()                         # logical cores, e.g. 8
psutil.virtual_memory().total / 1e9    # RAM in GB
```

- **RAM** limits how much data pandas can hold. pandas usually needs **5–10× the file size** in memory to work comfortably.
- **Cores**: plain pandas and Python loops use **one** core. The others sit idle.

Dask attacks both limits: it splits data into pieces that fit in RAM, and processes pieces on all cores.

## 2. Parallel vs sequential

```
 sequential (1 core):   [task1][task2][task3][task4]          → 4 units of time
 parallel   (4 cores):  [task1]
                        [task2]
                        [task3]
                        [task4]                                → 1 unit of time (ideal)
```

The ideal is rarely reached. Coordinating tasks has **overhead**, so tiny tasks don't benefit (Lecture 16).

## 3. Threads vs processes (just the idea)

| | Threads | Processes |
|---|---|---|
| Share memory? | yes, so no copying | no, data is copied between them |
| Python's GIL | only one thread runs *Python* code at a time | each process has its own GIL |
| Good for | NumPy / pandas (they release the GIL), I/O | pure-Python code (loops, string parsing) |

You don't have to manage these yourself. Dask picks sensible defaults, and Lecture 13 shows how to choose.

## 4. Chunked processing by hand

`lecture.py` processes a CSV in chunks with plain pandas (`read_csv(chunksize=...)`) to compute a total that never needs the whole file in memory. That's the core idea of Dask, done manually. Dask automates it, parallelises it, and lets you write normal pandas-style code instead of a loop.

## 5. The `__main__` guard

```python
def main():
    ...

if __name__ == "__main__":
    main()
```

When Dask starts worker **processes**, each one may re-import your script. The guard stops them re-running your whole program.

## Exercises

1. How many cores and how much RAM does your machine have?
2. Change the chunk size in `lecture.py`. Does the answer change? Does the time?
3. Why can't a chunked loop easily compute the **median** the way it computes a sum?

<details><summary>Solutions</summary>

3. A sum can be combined from partial sums. A median can't: the median of medians isn't the true median. Dask uses special algorithms (approximate quantiles) for such cases. This "can it be combined from pieces?" question appears throughout the course.
</details>

**Next →** [Lecture 01: What is Dask?](../01_what_is_dask/)
