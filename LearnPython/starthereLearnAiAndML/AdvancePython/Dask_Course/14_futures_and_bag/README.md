# Lecture 14: Futures (real-time tasks) & Dask Bag (semi-structured data)

Run: `python lecture.py`

## Part 1: Futures

`delayed` builds a whole graph first, then runs it. **Futures** start running **immediately** when you submit them. That's useful when the next step depends on results as they arrive.

```python
from dask.distributed import Client, as_completed

client = Client()
future = client.submit(func, arg)          # starts NOW, in the background
future.status                              # 'pending' / 'finished' / 'error'
future.result()                            # wait and fetch the value

futures = client.map(func, list_of_args)   # one task per item
results = client.gather(futures)           # fetch all
```

| Method | Does |
|--------|------|
| `client.submit(f, *args)` | run one task now → a `Future` |
| `client.map(f, iterable)` | many tasks → a list of `Future`s |
| `future.result()` / `client.gather(futures)` | wait and fetch |
| `as_completed(futures)` | iterate in the order tasks **finish** |
| `client.submit(g, future)` | pass a future into another task; it waits for the dependency on the worker |
| `client.scatter(big_object)` | send data to workers **once**, reuse it in many tasks |
| `future.cancel()` | stop a task |
| `wait(futures)` | block until all are done |

### `delayed` vs futures

| | `delayed` | futures |
|---|---|---|
| Runs | when you call `compute` | immediately on submit |
| Needs a `Client` | no | **yes** (distributed scheduler) |
| Dynamic workflows (decide next step from results) | awkward | ✅ natural |
| Process results as they finish | ❌ | ✅ `as_completed` |
| Optimisation of the full graph | ✅ | per task |

> **Purity:** futures with identical function + arguments share a key, so Dask may return the cached result instead of rerunning. Use `pure=False` for functions with randomness or side effects.

## Part 2: Dask Bag

A **Bag** is a parallel list of Python objects (dicts, strings, tuples) for **messy, semi-structured** data before it becomes a table: JSON lines, logs, text.

```python
import dask.bag as db, json

records = db.read_text("logs/*.jsonl").map(json.loads)   # each line → a dict
(records
   .filter(lambda r: r["status"] == "error")
   .pluck("service")                                     # take one field
   .frequencies()                                        # count values
   .topk(5, key=lambda kv: kv[1])
   .compute())
```

| Method | Like |
|--------|------|
| `.map(f)` | `map` |
| `.filter(pred)` | `filter` |
| `.pluck("key")` | `[d["key"] for d in ...]` |
| `.flatten()` | flatten lists |
| `.frequencies()` | `collections.Counter` |
| `.topk(k, key=)` | `heapq.nlargest` |
| `.groupby(key)` | full shuffle, slow |
| `.foldby(key, binop, initial, combine)` | **fast** grouped reduction |
| `.to_dataframe(meta=...)` | convert to a Dask DataFrame once the data is clean |

**Typical pipeline:** raw JSON/text → **Bag** (parse, clean, flatten) → `.to_dataframe()` → **DataFrame** (analyse) → Parquet.

Bags use the **processes** scheduler by default (pure-Python work), so scripts need the `__main__` guard.

## Exercises

1. Submit 10 tasks that sleep a random time; print each result as it completes.
2. Scatter a lookup dict once, then use it in 100 tasks.
3. Count the most common words in the course READMEs with a Bag.
4. Parse the JSON-lines file created in `lecture.py`, keep only errors, convert to a DataFrame.

<details><summary>Solutions</summary>

See `lecture.py` sections 1–6.
</details>

**Next →** [Lecture 15: `persist`, `compute` & memory](../15_persist_compute_memory/)
