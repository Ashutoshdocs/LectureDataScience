# Lecture 10: Joins & merge

Run: `python lecture.py`

`dd.merge` / `ddf.merge` work like pandas: `on=`, `left_on=` / `right_on=`, `how=` (`inner`, `left`, `right`, `outer`), `suffixes=`. What changes is **how** Dask does the join, and that decides the speed.

## The three join strategies

### 1. Large ⨝ small: **broadcast join** (fast)

```
 big partition 0 ─┐
 big partition 1 ─┼─ each joined with a full copy of the small table
 big partition 2 ─┘          (the small table is "broadcast" to every partition)
```

Used automatically when one side is a pandas DataFrame or a single-partition Dask DataFrame. No shuffle at all. **This is the case you want.**

```python
ddf.merge(customers_pdf, on="customer_id", how="left")        # pandas on the right: broadcast
```

### 2. Large ⨝ large on the index, both with known divisions: **aligned join** (fast)

If both sides are indexed by the join key and partitioned the same way, partition *i* only meets partition *i*.

```python
left.set_index("customer_id").join(right.set_index("customer_id"))
```

### 3. Large ⨝ large on a column: **hash/shuffle join** (expensive)

Both sides are shuffled so equal keys land in the same partition, then joined partition by partition. Correct for any data, but moves all rows.

## Making joins fast

| Tip | Why |
|-----|-----|
| Keep lookup tables as **pandas** (if they fit in memory) | broadcast, no shuffle |
| Filter and select columns **before** the join | less data to move |
| Aggregate before joining when possible | join 8 rows instead of 2.4M |
| For repeated large joins, `set_index` on the key once and save as Parquet | later joins are aligned |
| Check row counts before/after | duplicate keys multiply rows, exactly as in pandas |
| Use `broadcast=True` to force a broadcast of a smallish Dask DataFrame | avoids a shuffle |

## Measured in `lecture.py` (2.4M orders ⨝ 20k customers, 2 cores)

| Approach | Time |
|----------|------|
| customers as **pandas** (broadcast) | ~0.5 s |
| customers as Dask, 4 partitions (shuffle join) | ~0.7 s |
| same, with `broadcast=True` | ~0.5 s |
| **aggregate per customer first**, then join 20k rows in pandas | **~0.14 s** |

On a single laptop with this data size the gaps are modest. On a cluster, a shuffle moves data across the network, and the difference between broadcast and shuffle becomes minutes vs seconds. Aggregating first wins either way.

## Concatenating

```python
dd.concat([ddf_2024, ddf_2025])               # stack partitions: cheap, no shuffle
dd.concat([a, b], axis=1)                     # side by side: only safe with aligned known divisions
```

## Exercises

1. Join the 2.4M orders to the 20,000-row customer table (pandas). Revenue by city × segment.
2. Repeat with the customer table as a Dask DataFrame with 4 partitions. Compare times.
3. Count orders whose `customer_id` has no match (use `how="left"` + `isna`).
4. Aggregate revenue per customer *first*, then join, and compare the time.

<details><summary>Solutions</summary>

See `lecture.py`. Broadcasting a pandas table, or aggregating first, are the two biggest speed-ups.
</details>

**Next →** [Lecture 11: `map_partitions` & `meta`](../11_map_partitions_and_meta/)
