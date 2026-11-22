# Lecture 05: Expressions, the core idea of Polars

Run: `python lecture.py`

If you understand this lecture, the rest of Polars is just vocabulary.

## What is an expression?

An **expression** is a *recipe* for producing a column. It doesn't hold data and doesn't run by itself:

```python
pl.col("units") * pl.col("unit_price")      # "multiply units by unit_price"
```

It only runs when you hand it to a **context**, a DataFrame method that says *where* the result goes.

## The four contexts

| Context | What it does with the expressions | Output rows |
|---------|-----------------------------------|-------------|
| `df.select(...)` | builds a **new** table from only these columns | same, or 1 if aggregated |
| `df.with_columns(...)` | **adds / replaces** columns, keeps the rest | same |
| `df.filter(...)` | keeps rows where a boolean expression is true | fewer |
| `df.group_by(...).agg(...)` | runs the expressions **per group** | one per group |

The **same expression** works in all four:

```python
rev = pl.col("units") * pl.col("unit_price")

df.select(rev)                           # a 1-column table
df.with_columns(rev.alias("revenue"))    # original + revenue
df.filter(rev > 100_000)                 # big orders only
df.group_by("region").agg(rev.sum())     # revenue per region
```

## Building blocks

| Piece | Example |
|-------|---------|
| a column | `pl.col("units")` |
| several columns | `pl.col("maths", "science")` or `pl.col(pl.Int64)` |
| all columns | `pl.all()` |
| a constant | `pl.lit(1.18)`, `pl.lit("North")` |
| arithmetic | `+ - * / // % **` |
| comparison | `> < >= <= == !=` → boolean expression |
| logic | `&` and, `\|` or, `~` not |
| methods | `.sum() .mean() .round(2) .abs() .is_null() .cast(...)` |
| namespaces | `.str.…`, `.dt.…`, `.list.…` |
| naming | `.alias("new_name")` or keyword: `with_columns(revenue=...)` |
| conditionals | `pl.when(...).then(...).otherwise(...)` (Lecture 08) |
| per-group | `.over("region")` (Lecture 14) |

## Expressions run in parallel

All the expressions inside **one** `select` / `with_columns` are independent and run **at the same time on different CPU cores**. So they all see the *original* columns:

```python
df.with_columns(
    revenue=pl.col("units") * pl.col("unit_price"),
    gst=pl.col("revenue") * 0.18,       # ❌ error: 'revenue' doesn't exist yet
)
```

Fix: chain a second `with_columns`:

```python
(df.with_columns(revenue=pl.col("units") * pl.col("unit_price"))
   .with_columns(gst=pl.col("revenue") * 0.18))
```

## Expressions can be stored and reused

```python
revenue = (pl.col("units") * pl.col("unit_price")).alias("revenue")
is_big = revenue > 100_000
df.select(revenue, is_big.alias("big"))
```

Because they are plain Python objects, you can build expression libraries: functions that return expressions.

## Why expressions instead of `apply`?

| `apply` / loops (pandas style) | Polars expressions |
|---|---|
| A Python function per row | Compiled Rust over whole columns |
| One CPU core | All cores |
| A black box to the optimiser | Polars can see, reorder and combine them |

## Exercises

1. Using one expression, compute `revenue` in `select`, then reuse it in `filter` to keep orders above Rs 1,00,000.
2. In one `select`, compute total units, mean unit price and number of distinct products.
3. Show the "doesn't exist yet" error, then fix it with two `with_columns`.

<details><summary>Solutions</summary>

```python
rev = pl.col("units") * pl.col("unit_price")
sales.filter(rev > 100_000)
sales.select(pl.col("units").sum(), pl.col("unit_price").mean(), pl.col("product").n_unique())
```
</details>

**Next →** [Lecture 06: Selecting columns](../06_selecting_columns/)
