# Lecture 06: Selecting data with `[]`, `loc` and `iloc`

Run: `python lecture.py`

## Three ways to select

| Tool | Selects by | Slice end | Typical use |
|------|-----------|-----------|-------------|
| `df["col"]`, `df[["a", "b"]]` | column name | n/a | grab columns |
| `df.loc[rows, cols]` | **labels** (index values, column names) | **included** | most selection |
| `df.iloc[rows, cols]` | **positions** (0, 1, 2…) | excluded (like Python) | "first 5 rows", "last column" |

> **Memory trick:** `loc` = **l**abels, `iloc` = **i**nteger **loc**ations.

## `loc` examples

The example table uses `name` as the index:

```
         class  maths  science  english
name
Asha       10A   78.0     85.0     62.0
Ravi       10A   92.0     88.0     79.0
Meena      10B   45.0     52.0     68.0
...
```

| Code | Selects |
|------|---------|
| `df.loc["Ravi"]` | one row → Series |
| `df.loc["Ravi", "maths"]` | one value |
| `df.loc[["Asha", "Meena"]]` | several rows |
| `df.loc["Asha":"Meena"]` | rows Asha **through** Meena (end included) |
| `df.loc[:, "maths":"english"]` | all rows, a range of columns |
| `df.loc[df["maths"] > 80, ["class", "maths"]]` | **condition** + chosen columns |

## `iloc` examples

| Code | Selects |
|------|---------|
| `df.iloc[0]` | first row |
| `df.iloc[-1]` | last row |
| `df.iloc[:3]` | first 3 rows |
| `df.iloc[:, 0]` | first column |
| `df.iloc[2, 1]` | row 2, column 1 |
| `df.iloc[[0, 2], [1, 3]]` | rows 0 & 2, columns 1 & 3 |

## Fast single values: `at` and `iat`

`df.at["Ravi", "maths"]` (label) and `df.iat[1, 1]` (position) are faster for one cell.

## Changing values: always use `loc`

```python
df.loc["Meena", "maths"] = 50                    # one cell
df.loc[df["maths"] < 50, "maths"] = 50           # every matching row
```

> ⚠️ **Chained assignment does not work:**
> ```python
> df[df["maths"] < 50]["maths"] = 50   # ❌ changes a temporary copy, df is untouched
> ```
> In pandas 3 (Copy-on-Write) this **never** modifies `df` and prints a `ChainedAssignmentError` warning. In pandas 2 it showed a `SettingWithCopyWarning` and *sometimes* worked, which was worse. Always do row selection and column selection **inside one `.loc[...]`**.

## Exercises

1. Select Zara's science mark with `loc` and with `at`.
2. Select the last 3 rows and the first 2 columns with `iloc`.
3. Select `maths` and `cs` for all students in class 10B.
4. Set every `cs` mark below 50 to 50.

<details><summary>Solutions</summary>

```python
df.loc["Zara", "science"]; df.at["Zara", "science"]
df.iloc[-3:, :2]
df.loc[df["class"] == "10B", ["maths", "cs"]]
df.loc[df["cs"] < 50, "cs"] = 50
```
</details>

**Next →** [Lecture 07: Filtering rows](../07_filtering_rows/)
