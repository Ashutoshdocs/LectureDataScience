# Lecture 08: GroupBy & aggregation

Run: `python lecture.py`

## Same syntax as pandas

```python
ddf.groupby("region").revenue.sum().compute()
ddf.groupby(["region", "category"]).agg({"revenue": "sum", "units": "mean"}).compute()
ddf.groupby("region").agg(orders=("order_id", "count"), revenue=("revenue", "sum")).compute()
```

## How it works: tree reduction

```
 partition 0 ─► groupby-sum ─┐
 partition 1 ─► groupby-sum ─┼─► combine partial sums ─┐
 partition 2 ─► groupby-sum ─┘                         ├─► final result
 partition 3 ─► groupby-sum ─┐                         │
 partition 4 ─► groupby-sum ─┴─► combine partial sums ─┘
```

1. **Chunk:** each partition is grouped and aggregated on its own (in parallel).
2. **Combine:** the small partial results are merged in a **tree**.
3. **Aggregate:** the final answer.

This works for any aggregation that can be built from partial results:

| Aggregation | Combinable? |
|-------------|-------------|
| `sum`, `count`, `size`, `min`, `max` | ✅ directly |
| `mean` | ✅ (sum and count are combined, then divided) |
| `std`, `var` | ✅ (sum, sum of squares and count) |
| `nunique` | ✅ but more expensive (unique sets are combined) |
| `first`, `last` | ✅ (order-dependent) |
| `median` | ⚠️ approximate, or needs a shuffle (`median(shuffle_method="tasks")`) |
| arbitrary Python function | via `dd.Aggregation` (below) or `groupby().apply` (slow: full shuffle) |

## Many groups: `split_out`

The result of a groupby is normally **one partition**, so it must fit in memory. With **millions of groups** (e.g. per customer on a huge dataset), spread the output:

```python
ddf.groupby("customer_id").revenue.sum(split_out=8)    # result has 8 partitions
```

## Custom aggregations: `dd.Aggregation`

Describe how to compute per chunk, how to combine, and how to finish:

```python
price_range = dd.Aggregation(
    name="range",
    chunk=lambda s: (s.max(), s.min()),             # per partition, per group
    agg=lambda mx, mn: (mx.max(), mn.min()),         # combine partials
    finalize=lambda mx, mn: mx - mn,                 # final result
)
ddf.groupby("product").unit_price.agg(price_range)
```

> ⚠️ `chunk` receives a **grouped** series (`SeriesGroupBy`), not a plain Series. `s.max()` works because grouped objects have `max()`, but `s >= 4` fails. Use `g.apply(...)` inside `chunk` for element-wise logic, or, often simpler, make a helper column and use a built-in aggregation:
> ```python
> ddf.assign(bulk=ddf.units >= 4).groupby("region").bulk.mean()    # share of bulk orders
> ```
>
> In `lecture.py` the two give slightly different answers (0.4002 vs 0.3998). The custom version's `count()` skips missing `units`, while `NaN >= 4` is `False`, so missing rows count as "not bulk" in the mean. Neither is wrong; decide how missing values should count.

## `groupby().apply` / `transform`: use with care

These run arbitrary pandas code per group, which requires **shuffling** all rows of a group into one partition first. That's expensive on big data. Prefer built-in aggregations, then `merge` the result back if you need a per-row value.

## Exercises

1. Revenue and orders per region, sorted.
2. Average units per product × region, unstacked into a table (after `compute`).
3. Number of distinct customers and products per region.
4. Total spend per customer with `split_out=4`. How many partitions is the result?
5. Write a custom aggregation for "share of orders with 4+ units".

<details><summary>Solutions</summary>

See `lecture.py`. For 5: `chunk=lambda g: (g.apply(lambda s: (s >= 4).sum()), g.count())`, `agg=lambda a, b: (a.sum(), b.sum())`, `finalize=lambda a, b: a / b`. Or simply `ddf.assign(bulk=ddf.units >= 4).groupby("region").bulk.mean()`.
</details>

**Next →** [Lecture 09: Index, divisions & shuffling](../09_index_divisions_shuffling/)
