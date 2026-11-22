# Lecture 04: Dask Array: NumPy in chunks

Run: `python lecture.py`

## The idea

A **Dask Array** is a grid of NumPy arrays (**chunks**) that behaves like one big NumPy array:

```
 shape (20_000, 20_000), chunks (5_000, 5_000)  → 4 × 4 = 16 NumPy chunks

 ┌──────┬──────┬──────┬──────┐
 │ 0,0  │ 0,1  │ 0,2  │ 0,3  │   each chunk: 5,000 × 5,000 float64 = 200 MB
 ├──────┼──────┼──────┼──────┤   the whole array: 3.2 GB, never all in memory at once
 │ 1,0  │ ...  │      │      │
 └──────┴──────┴──────┴──────┘
```

## Creating arrays

| Code | Makes |
|------|-------|
| `da.from_array(np_arr, chunks=1000)` | from an existing NumPy array |
| `da.zeros / ones / full(shape, chunks=...)` | filled arrays |
| `da.arange(n, chunks=...)`, `da.linspace(...)` | ranges |
| `da.random.default_rng(42).random(shape, chunks=...)` | random data |
| `da.from_zarr("data.zarr")`, `da.from_npy_stack(dir)` | from chunked files on disk |
| `ddf.to_dask_array(lengths=True)` | from a Dask DataFrame |

## Same API as NumPy

```python
x.mean(), x.std(), x.max(axis=0)       # reductions
x + 1, x * y, da.sqrt(x), da.exp(x)    # element-wise (ufuncs)
x[::2, :100], x[x > 0.5]               # slicing and masks
x.T, x.reshape(...), x @ y             # linear algebra
da.where(x > 0.5, 1, 0)
```

All of these are **lazy**; call `.compute()` (or `dask.compute(a, b)`) to get a NumPy result.

## Choosing chunk sizes

| Chunk size | Effect |
|------------|--------|
| too small (KB) | thousands of tiny tasks, so scheduling overhead dominates |
| **about 100 MB** | ✅ a good default |
| too large (GB) | few tasks (little parallelism) and possible memory errors |

```python
x.chunks           # sizes along each axis
x.chunksize        # shape of one chunk
x.npartitions      # number of chunks
x.nbytes / 1e9     # total GB
x.rechunk((2000, 2000))   # change chunking (costs a shuffle of data)
chunks="auto"      # let Dask pick ~128 MB chunks
```

Measured in `lecture.py` (mean of a 10,000 × 10,000 array, 2 cores):

| Chunks | Number of chunks | Tasks | Time |
|--------|------------------|-------|------|
| 250 × 250 | 1,600 | 3,739 | 0.90 s (too small) |
| 1,000 × 1,000 | 100 | 239 | 0.18 s |
| 2,500 × 2,500 | 16 | 37 | 0.19 s |
| 5,000 × 5,000 | 4 | 9 | 0.31 s (too few to keep cores busy) |

The same lecture computes the mean of a **3.2 GB** array in about 1.4 s, on a machine with 8 GB of RAM and without ever holding the whole array.

Match chunks to how you'll access the data: row-wise analysis → chunk along columns fully, rows partially.

## Reductions run as trees

`x.sum()` sums each chunk, then sums the partial sums in a tree. That's how a 3 GB array is summed using only ~200 MB of memory at a time.

## Where Dask Array is used

Climate and satellite data (with **Xarray**), medical images, large simulations, and ML preprocessing. Formats like **Zarr** and **HDF5** store arrays in chunks that line up with Dask's chunks.

## Exercises

1. Create a 10,000 × 10,000 random array with 2,500 × 2,500 chunks. How many chunks? How many GB?
2. Compute the mean of each column (`axis=0`). What's the result shape?
3. Count how many values are above 0.99.
4. Compare the time of `.mean()` with chunks of 500 vs 2,500.

<details><summary>Solutions</summary>

1. 16 chunks; 0.8 GB.
2. `(10000,)`.
3. `(x > 0.99).sum().compute()`, about 1% of 100M = ~1,000,000.
4. Tiny chunks make 400 tasks instead of 16, so they're slower.
</details>

**Next →** [Lecture 05: DataFrame basics & partitions](../05_dataframe_basics_partitions/)
