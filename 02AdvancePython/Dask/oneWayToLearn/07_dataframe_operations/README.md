# Lecture 07: DataFrame operations, the pandas API lazily

Run: `python lecture.py`

Most pandas code works on a Dask DataFrame unchanged. It just becomes lazy.

## Works the same as pandas (lazily)

| Category | Examples |
|----------|----------|
| Select | `ddf["a"]`, `ddf[["a", "b"]]`, `ddf.drop(columns=...)`, `ddf.rename(columns=...)` |
| Filter | `ddf[ddf.units >= 4]`, `ddf.query("units >= 4 and region == 'North'")`, `.isin()`, `.between()` |
| New columns | `ddf["rev"] = ddf.units * ddf.unit_price`, `ddf.assign(...)` |
| Conditionals | `ddf.units.where(cond, other)`, `ddf.units.mask(...)`, `ddf.units.clip(...)` |
| Text / dates | `.str.upper()`, `.str.contains()`, `.dt.month`, `.dt.day_name()` |
| Maps | `ddf.region.map({...})`, `.replace({...})`, `.astype(...)` |
| Missing values | `.isna()`, `.fillna(...)`, `.dropna(subset=...)` |
| Reductions | `.sum()`, `.mean()`, `.min()`, `.max()`, `.std()`, `.count()`, `.nunique()`, `.value_counts()` |
| Summary | `.describe()`, `.corr()` |
| Dedupe | `.drop_duplicates(subset=...)` |
| Top N | `.nlargest(5, "rev")`, `.nsmallest(...)` |

All return lazy Dask objects. Add `.compute()` at the end.

## Different from pandas, or slow

| Operation | Why it's different | Do instead |
|-----------|--------------------|------------|
| `ddf.iloc[5]` / row positions | partitions don't know global row numbers | filter by a column, or `head` |
| `ddf.loc[label]` | fine **only** with a sorted index and known divisions | `set_index` first (Lecture 09) |
| `sort_values` over everything | needs a full shuffle | only if necessary; often `nlargest` is enough |
| `median`, `quantile` | can't combine from pieces exactly | `quantile` is **approximate**; `median_approximate()` |
| `ddf.apply(f, axis=1)` | Python per row | vectorized columns, or `map_partitions` (Lecture 11) |
| `ddf["x"] = some_pandas_series` | partitions don't line up | build the column from Dask columns |
| `pivot_table` with unknown categories | Dask must know the output columns | `categorize()` first, or groupby + `unstack` after compute |
| `np.where(cond, a, b)` on Dask columns | may compute eagerly | `ddf.x.where(cond, b)` / `.mask(...)` |

## Conditional columns, the Dask-friendly way

```python
ddf["size"] = "single"
ddf["size"] = ddf["size"].mask(ddf.units >= 4, "bulk")             # if units >= 4 → "bulk"
ddf["discount"] = (ddf.revenue * 0.1).where(ddf.category == "Electronics", 0)
```

## Exercises

1. Add `revenue` and `with_gst` to the big table and show the first rows.
2. How many orders have missing `units`? Fill them with the median of a sample.
3. Top 5 orders by revenue in March.
4. Average order value per weekday (`.dt.day_name()`).

<details><summary>Solutions</summary>

See sections 2–6 of `lecture.py`.
</details>

**Next →** [Lecture 08: GroupBy & aggregation](../08_groupby_aggregation/)
