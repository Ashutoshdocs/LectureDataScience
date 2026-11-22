# Lecture 11: Data types & casting

Run: `python lecture.py`

Polars is **strict about types**. Every column has exactly one dtype, and Polars refuses to silently mix them. This catches bugs early, but it means you'll cast often when cleaning data.

## Main dtypes

| Group | Types |
|-------|-------|
| Integers | `Int8 Int16 Int32 Int64`, unsigned `UInt8 … UInt64` |
| Floats | `Float32 Float64` |
| Text | `String` |
| Logical | `Boolean` |
| Time | `Date`, `Datetime`, `Duration`, `Time` |
| Labels | `Categorical` (open set), `Enum` (fixed, ordered set) |
| Nested | `List`, `Array`, `Struct` |
| Other | `Decimal`, `Binary`, `Null` |

## `cast`

```python
pl.col("units").cast(pl.Int32)
pl.col("customer_id").cast(pl.String)
pl.col("age").cast(pl.Int64, strict=False)     # bad values → null instead of an error
```

| `strict=` | Unconvertible value like `"n/a"` |
|-----------|----------------------------------|
| `True` (default) | **raises an error**, so you find out immediately |
| `False` | becomes `null`. Count them afterwards with `.null_count()` |

## Text → numbers / dates

```python
pl.col("spend").str.replace_all(",", "").cast(pl.Float64, strict=False)   # "12,500" → 12500.0
pl.col("date").str.to_date("%Y-%m-%d")
pl.col("date").str.to_date("%d/%m/%Y", strict=False)                        # bad → null
pl.col("ts").str.to_datetime("%Y-%m-%d %H:%M")
```

## `Categorical` vs `Enum`

| | `Categorical` | `Enum` |
|---|---|---|
| Categories known in advance? | no, learned from the data | **yes**, you list them |
| Unknown value | added | **error** (protects against typos) |
| Sort order | lexical | **the order you listed** |
| Use for | many/unknown labels (city names) | small fixed sets (`low < mid < high`, weekdays) |

```python
size = pl.Enum(["small", "medium", "large"])
df.with_columns(pl.col("size").cast(size)).sort("size")    # small, medium, large
```

Both speed up `group_by`, joins and sorting on repeated text. For memory, `lecture.py` measures 100,000 rows of `region`: **Enum** was about 4.5× smaller than `String`, while `Categorical` saved only ~10% in Polars 2.1. If you know the labels in advance, prefer `Enum`.

## Shrinking memory

```python
df.estimated_size("mb")
df.with_columns(pl.col("units").cast(pl.Int8))
df["units"].shrink_dtype()               # Series method: smallest numeric type that fits
```

> Polars 2.0 removed `Expr.shrink_dtype`. Only the Series version remains.

## Exercises

1. Cast `customer_id` to `String`. Why is that sensible for IDs?
2. Convert `["12,500", "8,200", "n/a"]` to floats; how many failed?
3. Make an `Enum` for `low < mid < high` and sort by it.
4. Compare `estimated_size` of `region` as `String` vs `Categorical` on 100,000 rows.

<details><summary>Solutions</summary>

1. IDs aren't quantities, so you never sum them, and text keeps leading zeros.
2. `.str.replace_all(",", "").cast(pl.Float64, strict=False)` → 1 null.
3. `pl.col("lvl").cast(pl.Enum(["low", "mid", "high"]))` then `.sort("lvl")`.
</details>

**Next →** [Lecture 12: String methods](../12_string_methods/)
