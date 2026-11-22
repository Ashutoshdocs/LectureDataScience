# Lecture 03: DataFrame basics

Run: `python lecture.py`

## Creating a DataFrame

| From | Code |
|------|------|
| dict of lists (columns) | `pd.DataFrame({"name": [...], "maths": [...]})` |
| list of dicts (rows) | `pd.DataFrame([{"name": "Asha", "maths": 78}, ...])` |
| list of lists + column names | `pd.DataFrame([["Asha", 78], ...], columns=["name", "maths"])` |
| NumPy 2D array | `pd.DataFrame(arr, columns=[...])` |
| a file | `pd.read_csv("file.csv")` (Lecture 04) |

When rows (dicts) have different keys, missing ones become `NaN`.

## Anatomy

| Attribute | Gives |
|-----------|-------|
| `df.shape` | `(rows, columns)` |
| `df.columns` | column labels |
| `df.index` | row labels |
| `df.dtypes` | type of each column |
| `len(df)` | number of rows |
| `df.size` | rows × columns |
| `df.values` / `df.to_numpy()` | the data as a NumPy array |

## Columns

```python
df["maths"]            # one column → Series
df[["name", "maths"]]  # list of columns → DataFrame (note the double brackets)
df["total"] = df["maths"] + df["science"]    # new column, vectorized
df = df.drop(columns=["total"])               # remove
df = df.rename(columns={"maths": "math"})     # rename
```

> `df.maths` (attribute style) also works, but fails for names with spaces or names that clash with methods (`df.count`!). Prefer `df["maths"]`.

## The index

The index labels rows. By default it is `0, 1, 2, …`, but any column can become the index:

```python
df = df.set_index("name")      # rows are now labelled by name
df.loc["Ravi"]                  # look up a row by label
df = df.reset_index()           # back to 0, 1, 2 … (name becomes a column again)
```

A good index is **unique** and **meaningful**: an ID, a name, a date.

## Methods return new DataFrames

Most pandas methods **don't change** `df`. They return a new one:

```python
df.sort_values("maths")       # df itself is unchanged
df = df.sort_values("maths")  # reassign to keep the result
```

This lets you **chain** steps:

```python
(df
 .drop(columns=["gender"])
 .rename(columns={"cs": "computer"})
 .sort_values("maths", ascending=False)
 .head(3))
```

## Exercises

1. Build a DataFrame of 4 products with `product`, `price`, `stock` from a list of dicts.
2. Add a `value = price * stock` column.
3. Make `product` the index and look up one product's row.
4. Print `shape`, `columns` and `dtypes`.

<details><summary>Solutions</summary>

```python
p = pd.DataFrame([{"product": "Pen", "price": 10, "stock": 300}, ...])
p["value"] = p["price"] * p["stock"]
p = p.set_index("product"); p.loc["Pen"]
```
</details>

**Next →** [Lecture 04: Reading & writing files](../04_reading_writing_files/)
