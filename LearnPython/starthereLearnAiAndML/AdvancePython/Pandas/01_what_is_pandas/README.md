# Lecture 01: What is pandas, and why use it?

Run: `python lecture.py`

## Definition

**pandas** is the free, open-source Python library for working with **tables of data**: loading, cleaning, exploring, transforming, summarising and saving them. The name comes from **pan**el **da**ta, an economics term for tables measured over time.

It gives you two objects:

| Object | What it is | Think of it as |
|--------|-----------|----------------|
| **Series** | a 1D column of values **with labels** (an index) | one spreadsheet column |
| **DataFrame** | a 2D table: several Series sharing one index | a whole spreadsheet / SQL table |

```
                 columns →
            ┌──────────┬───────┬───────┐
   index ↓  │ name     │ class │ maths │
            ├──────────┼───────┼───────┤
        0   │ Asha     │ 10A   │  78   │   ← a row
        1   │ Ravi     │ 10A   │  92   │
        2   │ Meena    │ 10B   │  45   │
            └──────────┴───────┴───────┘
                                  ↑ each column is a Series
```

## How pandas relates to NumPy

```
          pandas  (labels, mixed column types, missing data, files, groupby, dates)
             │
           NumPy  (fast typed arrays, vectorized maths)
             │
           Python
```

- Each column is stored as a NumPy-style array, so column maths is **vectorized and fast**.
- Different columns can have **different types**: text, integers, floats, dates.
- `df["maths"].to_numpy()` gives you the underlying array.

## Why pandas? Compare the tools

| Task | Plain Python | NumPy | Excel | **pandas** |
|------|-------------|-------|-------|-----------|
| Column names | dict keys, manual | ❌ | ✅ | ✅ |
| Mixed types (text + numbers) | ✅ | ❌ one dtype | ✅ | ✅ per column |
| Fast maths on millions of rows | ❌ | ✅ | ❌ slow / ~1M row limit | ✅ |
| Missing values | manual `None` checks | `nan` only for floats | blanks | ✅ built-in |
| Read CSV/Excel/JSON/SQL | lots of code | limited | ✅ | ✅ one line |
| Group & summarise | loops + dicts | awkward | pivot tables | ✅ `groupby` |
| Join two tables | nested loops | ❌ | VLOOKUP | ✅ `merge` |
| Repeatable / automatable | ✅ | ✅ | ❌ manual clicks | ✅ |

## The typical pandas workflow

```
 load  →  explore  →  clean  →  transform  →  analyse  →  save / plot
read_csv   head/info   dropna    new columns    groupby     to_csv / plot
           describe    astype    filter, sort   pivot_table
```

The course follows exactly this order.

## Who uses it

Data analysts, scientists, finance teams, journalists, researchers, engineers. It's the standard first step in nearly every Python data or machine-learning project. scikit-learn, Matplotlib, seaborn and statsmodels all accept DataFrames directly.

## Exercises

1. Add a `"science"` column to the dict in `lecture.py` and rebuild the DataFrame.
2. Print `df.dtypes`. Why is `name` a different type from `maths`?
3. Print `type(df["maths"])` and `type(df["maths"].to_numpy())`.

<details><summary>Solutions</summary>

2. `name` holds text (`str`/`object`), `maths` holds integers (`int64`). Each column has its own type.
3. `pandas.Series` and `numpy.ndarray`.
</details>

**Next →** [Lecture 02: Series](../02_series/)
