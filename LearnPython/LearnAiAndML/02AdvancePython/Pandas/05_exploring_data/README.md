# Lecture 05: Exploring data, the first five minutes with any dataset

Run: `python lecture.py`

Before analysing anything, get to know the data. These commands answer: *How big is it? What columns are there? What types? Anything missing? What do typical values look like?*

## The exploration toolkit

| Command | Answers |
|---------|---------|
| `df.head(n)` / `df.tail(n)` | What do the first / last rows look like? |
| `df.sample(n)` | A few random rows (avoids a misleading start of file) |
| `df.shape` | How many rows and columns? |
| `df.columns` | What are the column names? |
| `df.info()` | Types, non-null counts, memory: **the single most useful command** |
| `df.dtypes` | Type of each column |
| `df.describe()` | count, mean, std, min, quartiles, max of numeric columns |
| `df.describe(include="all")` | also text columns: count, unique, top, freq |
| `df["col"].value_counts()` | How often does each value appear? |
| `df["col"].value_counts(normalize=True)` | …as fractions |
| `df["col"].unique()` / `.nunique()` | Distinct values / how many |
| `df.isna().sum()` | Missing values per column |
| `df.duplicated().sum()` | How many fully duplicated rows? |
| `df["col"].min()`, `.max()` | Range check: any impossible values? |
| `df.corr(numeric_only=True)` | How do numeric columns move together? |

## Reading `describe()`

```
             units     unit_price
count   240.000000     240.000000     ← non-missing values
mean      2.9...       ...            ← average
std       1.4...       ...            ← spread
min       1.000000     900.000000
25%       2.000000     ...            ← 25% of values are below this
50%       3.000000     ...            ← the median
75%       4.000000     ...
max       5.000000   55000.000000
```

Look for: **min/max that don't make sense** (negative age, 1000% discount), **mean very different from median** (skew or outliers), **count lower than rows** (missing values).

## A checklist to run on every new dataset

1. `shape`: is the size what you expected?
2. `info()`: are the types right? Dates as `datetime`? Numbers not stored as text?
3. `isna().sum()`: where are the gaps?
4. `describe()`: impossible or extreme values?
5. `value_counts()` on each category column: typos? `"Delhi"` vs `"delhi"`?
6. `duplicated().sum()`: repeated rows?

## Display settings

```python
pd.set_option("display.max_columns", 20)
pd.set_option("display.width", 120)
pd.set_option("display.float_format", "{:,.2f}".format)
```

## Exercises

1. Which region has the most orders?
2. What fraction of orders are Electronics?
3. How many different customers placed orders?
4. In `students.csv`, which columns have missing values, and how many?

<details><summary>Solutions</summary>

```python
sales["region"].value_counts().idxmax()
sales["category"].value_counts(normalize=True)["Electronics"]
sales["customer_id"].nunique()
students.isna().sum()       # maths 1, science 1, english 1
```
</details>

**Next →** [Lecture 06: Selecting with `[]`, `loc`, `iloc`](../06_selecting_loc_iloc/)
