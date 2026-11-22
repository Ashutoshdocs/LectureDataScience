# Lecture 02: Series & DataFrame

Run: `python lecture.py`

## Series: one typed column

```python
s = pl.Series("steps", [4200, 6100, 5300])
```

A Series has a **name**, a **dtype** and **values**. There's **no index**: rows are identified by position only.

| | pandas Series | Polars Series |
|---|---|---|
| Labels | index (`"Mon"`, `"Tue"`) | none. Store labels as their own column |
| Missing | `NaN` / `None` | `null` |
| Maths | vectorized | vectorized |

## DataFrame: several Series of equal length

| From | Code |
|------|------|
| dict of lists | `pl.DataFrame({"name": [...], "maths": [...]})` |
| list of dicts | `pl.DataFrame([{"name": "Asha", "maths": 78}, ...])` |
| list of rows + schema | `pl.DataFrame([["Asha", 78]], schema=["name", "maths"], orient="row")` |
| with explicit types | `pl.DataFrame(data, schema={"name": pl.String, "maths": pl.Int32})` |
| pandas | `pl.from_pandas(pdf)` |
| NumPy | `pl.DataFrame(arr, schema=["x", "y"])` |

## The schema

Every column has a fixed type, shown under its name when printed:

| Short | dtype | Holds |
|-------|-------|-------|
| `i64`, `i32`… | `pl.Int64`, `pl.Int32` | whole numbers |
| `f64` | `pl.Float64` | decimals |
| `str` | `pl.String` | text |
| `bool` | `pl.Boolean` | true/false |
| `date` | `pl.Date` | calendar dates |
| `datetime[μs]` | `pl.Datetime` | date + time |
| `cat` / `enum` | `pl.Categorical` / `pl.Enum` | repeated labels |
| `list[i64]` | `pl.List` | a list in each cell |
| `struct[2]` | `pl.Struct` | several named fields in each cell |

## Anatomy

| Attribute | Gives |
|-----------|-------|
| `df.shape` | `(rows, columns)` |
| `df.height` / `df.width` | rows / columns |
| `df.columns` | names |
| `df.schema` / `df.dtypes` | name → type |
| `df["col"]` / `df.get_column("col")` | one column as a Series |
| `df.row(0)` / `df.row(0, named=True)` | one row as a tuple / dict |
| `df.to_dicts()` | list of row dicts |

## No index: what replaces it?

- **Look up a row by a key** → `df.filter(pl.col("name") == "Ravi")`
- **Row numbers** → `df.with_row_index("row_nr")`
- **Align by labels** → `join` on a key column (Lecture 15)

This makes Polars more predictable: there's no hidden index to reset, sort or misalign.

## Immutability

Methods return a **new** DataFrame. `df.sort("maths")` leaves `df` unchanged, so reassign: `df = df.sort("maths")`. Under the hood, Polars shares memory between the old and new tables, so this is cheap.

## Exercises

1. Build a DataFrame of 4 products (`product`, `price`, `stock`) from a list of dicts.
2. Force `price` to `Float32` with `schema_overrides`.
3. Get the third row as a dict.
4. Add a row number column.

<details><summary>Solutions</summary>

```python
p = pl.DataFrame([{"product": "Pen", "price": 10, "stock": 300}, ...],
                 schema_overrides={"price": pl.Float32})
p.row(2, named=True)
p.with_row_index("row_nr")
```
</details>

**Next →** [Lecture 03: Reading & writing files](../03_reading_writing_files/)
