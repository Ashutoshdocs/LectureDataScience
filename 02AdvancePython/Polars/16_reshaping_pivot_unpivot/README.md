# Lecture 16: Reshaping: `unpivot` (wide → long) and `pivot` (long → wide)

Run: `python lecture.py`

**Wide** (one row per student, a column per subject):
```
 name   maths  science
 Asha     78       85
 Ravi     92       88
```
**Long** (one row per observation):
```
 name   subject  mark
 Asha   maths      78
 Asha   science    85
 Ravi   maths      92
 Ravi   science    88
```

Long ("tidy") data is easier to `group_by`, `filter` and plot. Wide data is easier for humans to read and for reports.

## Wide → long: `unpivot`

```python
long = wide.unpivot(
    index=["name", "class"],        # columns to keep
    on=["maths", "science"],        # columns to stack (default: all others)
    variable_name="subject",
    value_name="mark",
)
```

> Polars < 1.0 called this `melt`. Selectors work too: `on=cs.numeric()`.

## Long → wide: `pivot`

```python
long.pivot(on="subject", index="name", values="mark")
```

| Argument | Meaning |
|----------|---------|
| `on` | the column whose **values** become new column names |
| `index` | the column(s) that identify each output row |
| `values` | what fills the cells |
| `aggregate_function` | how to combine duplicates: `"sum"`, `"mean"`, `"first"`, `"len"`… |

> `pivot` is **eager only** (DataFrame, not LazyFrame) because Polars must see the data to know which columns to create. In lazy pipelines, `group_by` + `agg` with `filter` per category is the alternative.

## A pivot table (Excel-style)

```python
sales.pivot(on="category", index="region", values="revenue", aggregate_function="sum")
```

Add totals with `with_columns(Total=pl.sum_horizontal(...))`, plus a `vstack` of the column sums.

## Other reshaping tools

| Tool | Does |
|------|------|
| `df.transpose(include_header=True)` | rows ↔ columns |
| `df.explode("items")` | a list per cell → one row per item |
| `df.group_by(...).agg(pl.col("x"))` | the opposite: rows → a list per group |
| `df.unnest("struct_col")` | struct fields → columns |
| `df.to_dummies(["class"])` | one-hot encode |

## Exercises

1. Unpivot `students` into `name, class, subject, mark`.
2. Average mark per subject from the long table.
3. Each student's best subject.
4. Pivot back to wide and check it matches the original.
5. Count orders by region × category with `aggregate_function="len"`.

<details><summary>Solutions</summary>

```python
long = students.unpivot(index=["name", "class", "gender"], variable_name="subject", value_name="mark")
long.group_by("subject").agg(pl.col("mark").mean())
long.group_by("name").agg(pl.col("subject").sort_by("mark").last())
long.pivot(on="subject", index=["name", "class", "gender"], values="mark")
sales.pivot(on="category", index="region", values="order_id", aggregate_function="len")
```
</details>

**Next →** [Lecture 17: Dates & time series](../17_dates_and_time_series/)
