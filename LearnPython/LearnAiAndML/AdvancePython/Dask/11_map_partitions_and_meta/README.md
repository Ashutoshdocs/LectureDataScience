# Lecture 11: `map_partitions` & `meta`: run any pandas code on each partition

Run: `python lecture.py`

## When the Dask API isn't enough

Dask implements most of pandas, but not everything. `map_partitions` is the escape hatch: it runs **your function on each partition** (a real pandas DataFrame), in parallel.

```python
def add_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["revenue"] = df["units"] * df["unit_price"]
    df["hour"] = df["timestamp"].dt.hour
    df["is_night"] = df["hour"].between(0, 5)
    return df

ddf2 = ddf.map_partitions(add_features)
```

Inside the function you have **all of pandas** (and NumPy, and any library), as long as the work only needs **the rows in that partition**.

## ⚠️ What a partition can't see

Each call only sees its own rows. These are **wrong** inside `map_partitions`:

| Wrong (per-partition result) | Right |
|------------------------------|-------|
| `df["x"] - df["x"].mean()` | compute the global mean first, pass it in (`.compute()` → argument) |
| `df["x"].rank()` | a global rank needs a shuffle/sort |
| `df["x"].shift(1)` across partition edges | `map_overlap` (Lecture 12) |
| `df.groupby("customer")...` (customers span partitions) | Dask `groupby`, or `shuffle(on=...)` first |

## `meta`: telling Dask what comes out

Dask needs to know the **output structure** (columns and dtypes) without running your function on the full data. By default it runs your function on **fake data with a couple of rows** (`lecture.py` shows this happening) and uses the result as a guess. If your function fails or behaves differently on tiny fake data, the guess breaks, sometimes with an error only at compute time. Provide `meta` yourself:

```python
meta = ddf._meta.assign(revenue=0.0, hour=0, is_night=False)     # empty pandas frame, right dtypes
ddf.map_partitions(add_features, meta=meta)

ddf.map_partitions(len, meta=("rows", "int64"))                    # a Series: (name, dtype)
ddf.map_partitions(lambda df: df.units.sum(), meta=("u", "f8"))
```

| `meta=` form | For output that is… |
|--------------|---------------------|
| empty pandas DataFrame | a DataFrame |
| `{"col": "dtype", ...}` | a DataFrame (dict form) |
| `("name", "dtype")` | a Series |
| a scalar dtype like `"f8"` | a scalar per partition |

## Passing extra arguments

```python
global_mean = ddf.units.mean().compute()
ddf.map_partitions(lambda df, m: df.assign(units_vs_mean=df.units - m), global_mean)
```

Extra Dask collections passed as arguments are aligned partition by partition. Plain values are sent to every partition.

## Related tools

| Tool | Does |
|------|------|
| `ddf.partitions[i]` | select one partition (as Dask) |
| `ddf.map_overlap(func, before, after)` | like `map_partitions`, with rows borrowed from neighbouring partitions |
| `ddf.reduction(chunk, aggregate)` | custom reduction over partitions |
| `ddf.to_delayed()` | a list of `Delayed` objects, one per partition |
| `dd.from_delayed(list, meta=...)` | the opposite |
| `da.map_blocks` | the Dask Array equivalent |

## Exercises

1. Write `add_features` with three new columns and supply `meta`.
2. Subtract the **global** mean of `units` correctly inside `map_partitions`.
3. Show that `df.units.rank()` inside `map_partitions` gives per-partition ranks.
4. Count orders per partition with `map_partitions(len)`.

<details><summary>Solutions</summary>

See `lecture.py`, sections 1–5.
</details>

**Next →** [Lecture 12: Time series](../12_time_series/)
