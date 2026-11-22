# Lecture 22: Recap & cheat sheet

Run: `python lecture.py` (a self-test: predict each answer before you look)

## pandas in one picture

```
           pandas ─ labels, mixed column types, missing data, files, groupby, dates, plotting
             │
           NumPy  ─ fast typed arrays, vectorized maths
             │
           Python
```

| | Python lists/dicts | NumPy | **pandas** |
|---|---|---|---|
| Column names / row labels | manual | ❌ | ✅ |
| Different type per column | ✅ | ❌ | ✅ |
| Fast vectorized maths | ❌ | ✅ | ✅ |
| Missing values | manual | floats only | ✅ |
| Read/write CSV, Excel, JSON, SQL | lots of code | limited | ✅ one line |
| Group, pivot, join | loops | ❌ | ✅ |
| Dates & time series | `datetime` module | basic | ✅ |

## Cheat sheet

### Load & save
```python
df = pd.read_csv("f.csv", usecols=[...], parse_dates=["date"], dtype={"id": str}, na_values=["n/a"])
pd.read_excel("f.xlsx", sheet_name="S1");  pd.read_json("f.json")
df.to_csv("out.csv", index=False);  df.to_excel("out.xlsx", index=False)
```

### Explore
```python
df.head()  df.tail()  df.sample(5)  df.shape  df.columns  df.dtypes
df.info()  df.describe()  df["c"].value_counts()  df["c"].nunique()
df.isna().sum()  df.duplicated().sum()
```

### Select
```python
df["c"]   df[["a", "b"]]
df.loc[row_label, "col"]    df.loc[cond, ["a", "b"]]     # labels, end included
df.iloc[0]  df.iloc[:5, :2]                             # positions, end excluded
df.at["r", "c"]  df.iat[0, 0]
```

### Filter
```python
df[df["x"] > 5]   df[(df.a > 1) & (df.b == "y")]   df[~cond]
df[df["c"].isin([...])]   df[df["x"].between(1, 9)]   df.query("x > 5 and c == 'y'")
df.nlargest(5, "x")
```

### Create & change columns
```python
df["new"] = df["a"] * df["b"]
df["lab"] = np.where(cond, "yes", "no");  np.select([c1, c2], [v1, v2], default)
pd.cut(df["x"], bins=[...], labels=[...]);  df["c"].map({...});  df["c"].replace({...})
df.assign(new=lambda d: d.a + d.b);  df.rename(columns={...});  df.drop(columns=[...])
df.loc[cond, "col"] = value          # never df[cond]["col"] = value
```

### Clean
```python
df.dropna(subset=[...]);  df.fillna({...});  s.ffill();  s.interpolate()
df.drop_duplicates();  df["c"].str.strip().str.lower()
pd.to_numeric(s, errors="coerce");  pd.to_datetime(s, format="%Y-%m-%d", errors="coerce")
df["c"].astype("category");  s.astype("Int64")
```

### Sort & rank
```python
df.sort_values(["a", "b"], ascending=[True, False]);  df.sort_index()
df["x"].rank(ascending=False, method="min")
```

### Group & summarise
```python
df.groupby("g")["x"].sum()
df.groupby(["g1", "g2"])["x"].mean().unstack()
df.groupby("g").agg(n=("id", "count"), total=("x", "sum"))
df["share"] = df["x"] / df.groupby("g")["x"].transform("sum")
df.pivot_table(index="r", columns="c", values="x", aggfunc="sum", margins=True)
pd.crosstab(df["a"], df["b"], normalize="index")
```

### Combine & reshape
```python
a.merge(b, on="key", how="left", validate="many_to_one")
pd.concat([df1, df2], ignore_index=True)
df.melt(id_vars=[...], var_name="k", value_name="v");  long.pivot(index=..., columns=..., values=...)
```

### Dates
```python
df["date"].dt.year / .month / .day_name() / .to_period("M")
ts = df.set_index("date").sort_index();  ts.loc["2025-03"]
ts["x"].resample("ME").sum();  s.rolling(7).mean();  s.pct_change();  s.shift(1)
```

### Plot
```python
df.groupby("g")["x"].sum().sort_values().plot.barh(title="...")
s.plot();  s.plot.hist(bins=20);  df.plot.scatter(x="a", y="b")
```

## Top 12 beginner mistakes

| Mistake | Fix |
|---------|-----|
| `df[cond]["col"] = v` (chained assignment) | `df.loc[cond, "col"] = v` |
| `cond1 and cond2` | `(cond1) & (cond2)` |
| `df.a > 1 & df.b < 5` | brackets around each condition |
| `df.sort_values("x")` and expecting `df` to change | `df = df.sort_values("x")` |
| `to_csv` without `index=False` → `Unnamed: 0` | `index=False` |
| Numbers stored as text (`"12,500"`) | `str.replace` + `pd.to_numeric` |
| Dates left as text | `pd.to_datetime` / `parse_dates` |
| `== np.nan` | `.isna()` |
| Merge with duplicate keys doubles totals | `validate="many_to_one"` and check `len()` |
| `apply(axis=1)` / `iterrows` on big data | vectorized columns, `np.where`, `.str`, `.dt`, `map` |
| `s[1]` on a labelled Series | `s.iloc[1]` or `s.loc["label"]` |
| Mixed date formats with `dayfirst=True` | parse each format separately |

## Where to go next

- **Jupyter / VS Code notebooks**: the natural home for pandas exploration
- **seaborn**: statistical plots from DataFrames
- **scikit-learn**: machine learning; it takes DataFrames as input
- **SQL**: the same ideas (filter, group, join) inside databases
- **Polars / DuckDB**: faster engines for very large data, with similar ideas
- Official docs: https://pandas.pydata.org/docs/

## Final exercises

1. Take a CSV from your own work or a public dataset (Kaggle, data.gov.in) and run the Lecture 05 checklist on it.
2. Write three business questions about it and answer each in one pandas chain.
3. Save the answers to an Excel workbook with one sheet per question.
