# Lecture 09: Sorting & ranking

Run: `python lecture.py`

## Sorting rows

| Code | Does |
|------|------|
| `df.sort_values("col")` | ascending by one column |
| `df.sort_values("col", ascending=False)` | descending |
| `df.sort_values(["a", "b"])` | by `a`, then ties broken by `b` |
| `df.sort_values(["a", "b"], ascending=[True, False])` | mixed directions |
| `df.sort_values("col", na_position="first")` | where missing values go (default: last) |
| `df.sort_index()` | by the index |
| `df.sort_values("col", key=lambda s: s.str.lower())` | custom sort key |

Remember: these **return a new DataFrame**. Reassign, or chain.

After sorting, the old index labels travel with their rows. Use `.reset_index(drop=True)` for a clean 0, 1, 2… index.

## Top / bottom N

```python
df.nlargest(5, "revenue")     # faster and clearer than sort + head
df.nsmallest(3, "units")
```

## Ranking

`.rank()` gives each value its position in the ordering:

| `method=` | Ties `[90, 85, 85, 70]` get | Use for |
|-----------|-----------------------------|---------|
| `"average"` (default) | 1, 2.5, 2.5, 4 | statistics |
| `"min"` | 1, 2, 2, 4 | **competition ranking** ("joint 2nd") |
| `"dense"` | 1, 2, 2, 3 | no gaps after ties |
| `"first"` | 1, 2, 3, 4 | ties broken by order of appearance |

`ascending=False` makes the biggest value rank 1. `pct=True` gives a percentile rank from 0 to 1.

```python
students["rank"] = students["total"].rank(ascending=False, method="min")
```

Ranking within groups (preview of Lecture 13):

```python
students["class_rank"] = students.groupby("class")["total"].rank(ascending=False, method="min")
```

## Exercises

1. Sort sales by region (A→Z), then revenue (high→low).
2. The 5 biggest orders by revenue.
3. Rank students by `cs` with competition ranking.
4. Each student's percentile rank in maths.

<details><summary>Solutions</summary>

```python
sales.sort_values(["region", "revenue"], ascending=[True, False])
sales.nlargest(5, "revenue")
students["cs"].rank(ascending=False, method="min")
students["maths"].rank(pct=True)
```
</details>

**Next →** [Lecture 10: Missing data](../10_missing_data/)
