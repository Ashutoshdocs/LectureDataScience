# Lecture 09: Sorting & ranking

Run: `python lecture.py`

## `sort`

| Code | Does |
|------|------|
| `df.sort("revenue")` | ascending |
| `df.sort("revenue", descending=True)` | descending |
| `df.sort("region", "revenue", descending=[False, True])` | several keys, mixed directions |
| `df.sort("maths", nulls_last=True)` | where nulls go (default: **first**) |
| `df.sort(pl.col("name").str.to_lowercase())` | sort by an expression |
| `df.sort("x", maintain_order=True)` | stable sort: ties keep their original order |

> pandas puts missing values **last** by default; Polars puts nulls **first**. Use `nulls_last=True` when you want the pandas behaviour.

## Top / bottom N

```python
df.top_k(5, by="revenue")        # 5 largest
df.bottom_k(3, by="units")       # 3 smallest
```

Faster than `sort().head()` because it doesn't need to sort everything.

## Sorting inside an expression

```python
pl.col("maths").sort()                       # sort one column (others untouched!)
pl.col("name").sort_by("maths", descending=True)   # sort one column by another
```
Use these inside `select` / `agg`. For example, *names ordered by score within each class*.

## `rank`

| `method=` | Ties `[90, 85, 85, 70]` (descending) | Use for |
|-----------|--------------------------------------|---------|
| `"average"` (default) | 1, 2.5, 2.5, 4 | statistics |
| `"min"` | 1, 2, 2, 4 | competition ranking |
| `"dense"` | 1, 2, 2, 3 | no gaps |
| `"ordinal"` | 1, 2, 3, 4 | unique ranks, ties by position |
| `"max"` | 1, 3, 3, 4 | n/a |

```python
pl.col("total").rank("min", descending=True)
pl.col("total").rank("min", descending=True).over("class")    # rank within each class (Lecture 14)
```

## Exercises

1. Sort sales by region A→Z, then revenue high→low.
2. The 5 biggest orders by revenue with `top_k`.
3. Rank students by `cs` (competition style).
4. For each class, list student names from best to worst maths mark.

<details><summary>Solutions</summary>

```python
sales.sort("region", "revenue", descending=[False, True])
sales.top_k(5, by="revenue")
students.with_columns(pl.col("cs").rank("min", descending=True))
students.group_by("class").agg(pl.col("name").sort_by("maths", descending=True, nulls_last=True))
```
</details>

**Next →** [Lecture 10: Missing data](../10_missing_data/)
