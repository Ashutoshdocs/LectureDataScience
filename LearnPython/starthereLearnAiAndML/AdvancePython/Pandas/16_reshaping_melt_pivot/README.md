# Lecture 16: Reshaping: wide ↔ long with `melt`, `pivot`, `stack`

Run: `python lecture.py`

The same data can be laid out two ways.

**Wide**: one row per student, one column per subject. Easy for humans to read:
```
 name   maths  science  english
 Asha     78       85       62
 Ravi     92       88       79
```

**Long (tidy)**: one row per *observation*. Easy for computers to group, filter and plot:
```
 name   subject  mark
 Asha   maths      78
 Asha   science    85
 Asha   english    62
 Ravi   maths      92
 ...
```

> **Tidy data rule:** each variable is a column, each observation is a row. Long format makes `groupby("subject")`, filtering by subject, and plotting one line per subject trivial.

## Wide → long: `melt`

```python
long = wide.melt(id_vars=["name", "class"],              # columns to keep as-is
                 value_vars=["maths", "science"],         # columns to unpivot (default: all others)
                 var_name="subject",                      # name for the old column headers
                 value_name="mark")                       # name for the values
```

## Long → wide: `pivot` / `pivot_table`

```python
wide = long.pivot(index="name", columns="subject", values="mark")
```

> ⚠️ `pivot` raises `ValueError: Index contains duplicate entries` if any (index, column) pair appears twice. Use `pivot_table(..., aggfunc="mean")` to combine duplicates.

## `stack` / `unstack`

They move a level between the **columns** and the **index**:

| | Does |
|---|---|
| `df.stack()` | columns → inner index level (wide → long) |
| `s.unstack()` | inner index level → columns (long → wide) |

You met `unstack()` after a two-key `groupby` in Lecture 13.

## Other reshaping tools

| Tool | Does |
|------|------|
| `df.T` | transpose rows ↔ columns |
| `df.explode("col")` | a list in each cell → one row per item |
| `pd.wide_to_long(...)` | columns like `sales_2023, sales_2024` → long |
| `pd.get_dummies(df["col"])` | one category column → 0/1 indicator columns |

## Exercises

1. Melt `students.csv` into `name, class, subject, mark`.
2. Average mark per subject from the long table.
3. Best subject for each student (`idxmax` on the long table, per student).
4. Pivot the long table back to wide and check it matches.

<details><summary>Solutions</summary>

```python
long = students.melt(id_vars=["name", "class", "gender"], var_name="subject", value_name="mark")
long.groupby("subject")["mark"].mean()
long.loc[long.groupby("name")["mark"].idxmax(), ["name", "subject"]]
long.pivot(index="name", columns="subject", values="mark")
```
</details>

**Next →** [Lecture 17: Dates & time series](../17_dates_and_time_series/)
