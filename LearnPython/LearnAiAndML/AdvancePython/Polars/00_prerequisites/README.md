# Lecture 00: Prerequisites, what you need before Polars

Run: `python lecture.py`

## Checklist

| Skill | You should be able to… | Why Polars needs it |
|-------|------------------------|---------------------|
| Lists, dicts, loops, functions | the Python basics | Data starts as dicts and lists |
| `lambda` | `lambda x: x * 2` | Occasionally needed (Polars mostly avoids it) |
| **Method chaining** | `text.strip().lower().replace("a", "b")` | Polars code is one long chain of methods |
| **Keyword arguments** | `f(x, descending=True)` | Most Polars options are keywords |
| Tuples / lists of names | `["a", "b"]` | Selecting several columns |
| NumPy basics | vectorized maths, boolean masks | Same "whole column at once" idea |
| pandas basics (helpful) | `DataFrame`, `groupby`, `merge` | Polars solves the same problems differently (Lecture 23 has a translation table) |
| Files & paths | CSV, relative paths | `pl.read_csv("data/sales.csv")` |

## 1. Method chaining, Polars' style

Each method returns a new object, so you keep calling methods on the result:

```python
"  Hello World  ".strip().lower().replace(" ", "_")     # 'hello_world'
```

Polars code reads the same way, top to bottom:

```python
(df
 .filter(pl.col("units") > 2)
 .with_columns(revenue=pl.col("units") * pl.col("price"))
 .group_by("region")
 .agg(pl.col("revenue").sum())
 .sort("revenue", descending=True))
```

Wrap the chain in **brackets** `( … )` so you can break it over lines.

## 2. Row-oriented vs column-oriented

```
 Row-oriented (list of dicts)          Column-oriented (dict of lists)
 [{"name": "Asha", "m": 78},           {"name": ["Asha", "Ravi"],
  {"name": "Ravi", "m": 92}]            "m":    [78,      92]}
```

Polars (and Apache Arrow underneath it) stores data **by column**. Each column is a contiguous block of one type, which is ideal for fast maths and compression. Thinking "column at a time" is the key mindset.

## 3. "Describe what, not how"

Instead of loops, you write **expressions**: recipes for a column.

```python
# how (a loop)                         # what (an expression)
out = []                               pl.col("price") * 1.18
for p in prices:
    out.append(p * 1.18)
```

Lecture 05 is entirely about this.

## 4. Installing

```bash
python -m pip install polars pyarrow
python -c "import polars as pl; print(pl.__version__)"
```

The convention is `import polars as pl`.

## Exercises

1. Chain string methods to turn `"  New DELHI "` into `"new-delhi"`.
2. Convert `[{"a": 1, "b": 2}, {"a": 3, "b": 4}]` into a dict of lists.
3. Rewrite `[x ** 2 for x in nums if x > 2]` as NumPy using a mask.

<details><summary>Solutions</summary>

```python
"  New DELHI ".strip().lower().replace(" ", "-")
{"a": [1, 3], "b": [2, 4]}
a = np.array(nums); a[a > 2] ** 2
```
</details>

**Next →** [Lecture 01: What is Polars?](../01_what_is_polars/)
