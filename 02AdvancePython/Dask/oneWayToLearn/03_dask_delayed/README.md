# Lecture 03: `dask.delayed`: parallelise your own Python functions

Run: `python lecture.py`

Not every problem is a big table or array. Often you have **your own functions** that run one after another: process 100 files, call a model with 50 settings, simulate 1,000 scenarios. `dask.delayed` turns those calls into a **task graph** that runs in parallel.

## How it works

```python
import dask

@dask.delayed
def load(path): ...

@dask.delayed
def clean(df): ...

@dask.delayed
def summarise(df): ...

results = [summarise(clean(load(p))) for p in paths]   # instant: builds a graph
totals = dask.compute(*results)                       # runs it in parallel
```

- Calling a delayed function returns a **`Delayed`** object, a promise of a result.
- Passing a `Delayed` into another delayed function creates a **dependency**.
- Nothing runs until `.compute()` / `dask.compute(...)`.

```
 load(p1) ─► clean ─► summarise ─┐
 load(p2) ─► clean ─► summarise ─┼─► combine ─► result
 load(p3) ─► clean ─► summarise ─┘
```

## Two ways to write it

```python
@dask.delayed                       # decorator
def f(x): ...

g = dask.delayed(existing_function) # wrap a function you didn't write
g(1, 2)
```

## Rules of thumb

| Do | Don't |
|----|-------|
| Make each task do **real work** (≥ ~100 ms) | Wrap tiny operations like `x + 1`: overhead beats benefit |
| Call `dask.compute(*many)` **once** | Call `.compute()` inside a loop |
| Pass delayed objects between functions | Call `.compute()` inside a delayed function |
| Keep functions **pure** (same input → same output, no global state) | Mutate shared lists or globals from tasks |
| Use `nout=2` if a function returns a tuple you want to split | Index a delayed tuple and expect laziness without `nout` |

## Threads or processes?

The default scheduler for `delayed` is a **thread pool**:
- ✅ great for NumPy/pandas work and I/O (file reads, web requests), which release the GIL
- ❌ pure-Python loops won't speed up with threads, because of the GIL

For pure-Python CPU work use processes: `dask.compute(*tasks, scheduler="processes")` (inside the `__main__` guard).

> ⚠️ **Gotcha:** the processes scheduler sends tasks to workers in **batches of 6** (`chunksize=6`) to save overhead. With a *few big* tasks, they can all land on one worker, giving no speed-up at all. Pass `chunksize=1`:
> ```python
> dask.compute(*tasks, scheduler="processes", chunksize=1)
> ```

Measured in `lecture.py` (4 prime-counting tasks, 2 cores):

| Run | Time |
|-----|------|
| plain loop | ~4.2 s |
| threads | ~4.4 s (no gain: the GIL) |
| processes (default) | ~4.7 s (no gain: all 4 tasks in one batch) |
| processes, `chunksize=1` | **~2.3 s** |

For waiting tasks (sleep / I/O), threads work well, and you can use **more threads than cores**: 8 half-second sleeps took 4.0 s sequentially, 2.2 s with the default 2 threads, and **0.5 s with `num_workers=8`**.

Lecture 13 covers schedulers in depth. The distributed scheduler doesn't have the batching gotcha.

## Exercises

1. Turn a loop that "processes" 8 items with `time.sleep(0.5)` each into delayed tasks. What's the speed-up?
2. Build a pipeline `load → clean → summarise` for the three small CSV files and combine the results.
3. Compare `scheduler="threads"` and `scheduler="processes"` for a pure-Python CPU function.

<details><summary>Solutions</summary>

1. Sleeping releases the GIL, so threads overlap. With the default pool (one thread per core) 4 s becomes ~2 s on 2 cores; with `num_workers=8` it becomes ~0.5 s.
3. Threads give no speed-up for pure-Python CPU work. Processes give up to ~N× on N cores, as long as you use `chunksize=1` for a few big tasks.
</details>

**Next →** [Lecture 04: Dask Array](../04_dask_array/)
