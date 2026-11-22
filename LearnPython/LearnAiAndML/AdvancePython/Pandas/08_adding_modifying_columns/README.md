# Lecture 08: Adding & modifying columns

Run: `python lecture.py`

## 1. Vectorized arithmetic: the default way

Column maths is NumPy vectorization: no loops.

```python
sales["revenue"] = sales["units"] * sales["unit_price"]
sales["revenue_k"] = sales["revenue"] / 1000
sales["with_gst"] = sales["revenue"] * 1.18
```

## 2. Conditional columns

| Need | Tool |
|------|------|
| two outcomes | `np.where(cond, "yes", "no")` |
| several outcomes | `np.select([c1, c2], ["A", "B"], default="C")` |
| number ranges → labels | `pd.cut(col, bins=[...], labels=[...])` |
| equal-sized groups | `pd.qcut(col, q=4, labels=[...])` |
| keep some values, replace others | `col.where(cond, other)` / `col.mask(cond, other)` |
| change only matching rows | `df.loc[cond, "col"] = value` |

```python
sales["size"] = np.where(sales["units"] >= 4, "bulk", "single")
sales["band"] = pd.cut(sales["revenue"], bins=[0, 5000, 50000, np.inf],
                       labels=["small", "medium", "large"])
```

## 3. Mapping values

```python
codes = {"North": "N", "South": "S", "East": "E", "West": "W"}
sales["region_code"] = sales["region"].map(codes)       # values not in dict → NaN
sales["region"].replace({"North": "Northern"})          # values not in dict stay the same
```

## 4. `assign`: add columns inside a method chain

```python
report = sales.assign(
    revenue=lambda d: d["units"] * d["unit_price"],
    gst=lambda d: d["revenue"] * 0.18,          # can use a column made just above
)
```

`assign` returns a **new** DataFrame and leaves the original unchanged.

## 5. `apply`: the last resort

```python
sales["label"] = sales["product"].apply(lambda p: p.upper()[:3])
```

`apply` runs a Python function **once per row/value**. It's flexible but **slow** (it's a hidden loop). Use vectorized operations, `.str` methods, `np.where` or `map` when you can. Lecture 18 measures the difference.

## 6. Renaming, dropping, reordering

```python
df = df.rename(columns={"unit_price": "price"})
df = df.drop(columns=["region_code"])
df = df[["order_id", "date", "product", "revenue"]]      # reorder / subset
df.insert(1, "year", 2025)                              # insert at position 1
```

## Exercises

1. Add `discount` = 10% of revenue for Electronics orders, 0 otherwise.
2. Label `units` as `"low"` (1–2), `"mid"` (3), `"high"` (4–5) using `pd.cut`.
3. Use `assign` to add `net = revenue - discount` in a chain.
4. Map `category` to `"E"` / `"F"`.

<details><summary>Solutions</summary>

```python
sales["discount"] = np.where(sales["category"] == "Electronics", sales["revenue"] * 0.1, 0)
pd.cut(sales["units"], bins=[0, 2, 3, 5], labels=["low", "mid", "high"])
sales.assign(net=lambda d: d["revenue"] - d["discount"])
sales["category"].map({"Electronics": "E", "Furniture": "F"})
```
</details>

**Next →** [Lecture 09: Sorting & ranking](../09_sorting_and_ranking/)
