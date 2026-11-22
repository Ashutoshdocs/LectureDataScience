# Lecture 08: Adding columns & `when / then / otherwise`

Run: `python lecture.py`

## `with_columns`: add or replace columns

```python
sales = sales.with_columns(
    revenue=pl.col("units") * pl.col("unit_price"),
    with_gst=(pl.col("units") * pl.col("unit_price") * 1.18).round(2),
)
```

- Using a **new** name **adds** a column; an **existing** name **replaces** it.
- Remember: expressions in one `with_columns` can't see each other's results (Lecture 05). Chain another `with_columns` when one column depends on another.

## `pl.when().then().otherwise()`: if/elif/else for columns

```python
pl.when(pl.col("units") >= 4).then(pl.lit("bulk")).otherwise(pl.lit("single"))
```

Chain more `.when().then()` for elif:

```python
pl.when(pl.col("revenue") >= 100_000).then(pl.lit("gold"))
  .when(pl.col("revenue") >= 20_000).then(pl.lit("silver"))
  .otherwise(pl.lit("bronze"))
```

- Conditions are checked **in order**; the first true one wins.
- Without `.otherwise(...)`, non-matching rows become `null`.
- Use `pl.lit("text")` for constant text. A bare string like `"gold"` is read as a **column name**.
- `then` can be another column or expression: `.then(pl.col("revenue") * 0.1)`.

### Change only some rows

Polars has no `df.loc[cond, "col"] = value`. Rebuild the column instead:

```python
df.with_columns(
    discount=pl.when(pl.col("region") == "West")
               .then(pl.col("discount") + 500)
               .otherwise(pl.col("discount"))
)
```

## Binning numbers into labels

`when/then` works on every Polars version. Polars 2 also has `bin_intervals` (it replaced the deprecated `cut`):

```python
pl.col("revenue").bin_intervals([5_000, 50_000], labels=["small", "medium", "large"])
```

## Mapping values

| Tool | Values not in the mapping | Output type |
|------|---------------------------|-------------|
| `.replace({"North": "N"})` | stay **unchanged** | same as input |
| `.replace_strict({"North": "N"}, default=None)` | become `default` (error if no default) | can change |

## Other useful column tools

| Expression | Does |
|------------|------|
| `pl.max_horizontal("a", "b")`, `pl.sum_horizontal(...)`, `pl.mean_horizontal(...)` | across columns, per row |
| `pl.concat_str(["a", "b"], separator=" ")` | join text columns |
| `pl.col("x").clip(0, 100)` | keep within bounds |
| `pl.col("x").round(2)`, `.abs()`, `.sqrt()`, `.log()` | maths |
| `pl.struct(...)` + `.map_elements(f)` | last resort: custom Python per row (slow, Lecture 19) |

## Exercises

1. `discount` = 10% of revenue for Electronics, else 0.
2. Label units: `low` (1–2), `mid` (3), `high` (4–5).
3. Add `total` (sum of 4 subjects) and `best` (max of 4) to `students`.
4. Combine `product` and `region` into one text column like `"Phone - North"`.

<details><summary>Solutions</summary>

```python
pl.when(pl.col("category") == "Electronics").then(pl.col("revenue") * 0.1).otherwise(0)
pl.when(pl.col("units") <= 2).then(pl.lit("low")).when(pl.col("units") == 3).then(pl.lit("mid")).otherwise(pl.lit("high"))
students.with_columns(total=pl.sum_horizontal(marks), best=pl.max_horizontal(marks))
pl.concat_str(["product", "region"], separator=" - ")
```
</details>

**Next →** [Lecture 09: Sorting & ranking](../09_sorting_and_ranking/)
