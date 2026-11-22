# Lecture 23: Recap, pandas → Polars translation & cheat sheet

Run: `python lecture.py` (a self-test: predict each answer first)

## Polars in one sentence

**Expressions** (`pl.col(...)` recipes) run inside **contexts** (`select`, `with_columns`, `filter`, `group_by().agg()`), in parallel, in Rust, optionally as a **lazy, optimised** query.

## pandas → Polars translation table

| Task | pandas | Polars |
|------|--------|--------|
| Import | `import pandas as pd` | `import polars as pl` |
| Read CSV | `pd.read_csv(f, parse_dates=["d"])` | `pl.read_csv(f, try_parse_dates=True)` / `pl.scan_csv(f)` |
| Write CSV | `df.to_csv(f, index=False)` | `df.write_csv(f)` |
| Info | `df.info()` | `df.glimpse()`, `df.schema` |
| Missing count | `df.isna().sum()` | `df.null_count()` |
| One column | `df["a"]` | `df["a"]` (Series) / `df.select("a")` (DataFrame) |
| Columns | `df[["a", "b"]]` | `df.select("a", "b")` |
| Filter | `df[df["a"] > 5]` | `df.filter(pl.col("a") > 5)` |
| `isin` | `df["a"].isin([...])` | `pl.col("a").is_in([...])` |
| Row by label | `df.loc["Ravi"]` | `df.filter(pl.col("name") == "Ravi")` |
| Row by position | `df.iloc[3]` | `df.row(3)` / `df[3]` |
| New column | `df["c"] = df["a"] * 2` | `df = df.with_columns(c=pl.col("a") * 2)` |
| Several new | `df.assign(c=..., d=...)` | `df.with_columns(c=..., d=...)` |
| If/else | `np.where(cond, x, y)` | `pl.when(cond).then(x).otherwise(y)` |
| Set some rows | `df.loc[cond, "c"] = v` | `with_columns(c=pl.when(cond).then(v).otherwise(pl.col("c")))` |
| Rename | `df.rename(columns={"a": "b"})` | `df.rename({"a": "b"})` |
| Drop column | `df.drop(columns=["a"])` | `df.drop("a")` |
| Sort | `df.sort_values("a", ascending=False)` | `df.sort("a", descending=True)` |
| Top N | `df.nlargest(5, "a")` | `df.top_k(5, by="a")` |
| Group | `df.groupby("g")["x"].sum()` | `df.group_by("g").agg(pl.col("x").sum())` |
| Named aggs | `.agg(total=("x", "sum"))` | `.agg(total=pl.col("x").sum())` |
| Count per group | `df.groupby("g").size()` | `df.group_by("g").len()` |
| transform | `df.groupby("g")["x"].transform("mean")` | `pl.col("x").mean().over("g")` |
| Merge | `a.merge(b, on="k", how="left")` | `a.join(b, on="k", how="left")` |
| Anti-join | merge + indicator + filter | `a.join(b, on="k", how="anti")` |
| Concat | `pd.concat([a, b])` | `pl.concat([a, b])` |
| Melt | `df.melt(id_vars=..., ...)` | `df.unpivot(index=..., ...)` |
| Pivot table | `df.pivot_table(index, columns, values, aggfunc)` | `df.pivot(on, index, values, aggregate_function)` |
| Fill NA | `df["a"].fillna(0)` | `pl.col("a").fill_null(0)` |
| Forward fill | `s.ffill()` | `pl.col("a").fill_null(strategy="forward")` |
| Drop NA | `df.dropna()` | `df.drop_nulls()` |
| Cast | `df["a"].astype(int)` | `pl.col("a").cast(pl.Int64)` |
| To number (lenient) | `pd.to_numeric(s, errors="coerce")` | `.cast(pl.Float64, strict=False)` |
| To date | `pd.to_datetime(s, format=...)` | `pl.col("s").str.to_date(format)` |
| String | `s.str.upper()` | `pl.col("s").str.to_uppercase()` |
| Date part | `s.dt.month` | `pl.col("d").dt.month()` |
| Resample | `ts.resample("ME").sum()` | `df.group_by_dynamic("date", every="1mo").agg(...)` |
| Rolling | `s.rolling(7).mean()` | `pl.col("x").rolling_mean(7)` |
| apply | `s.apply(f)` | `pl.col("x").map_elements(f)` (slow, avoid) |
| SQL | n/a | `df.sql("SELECT ... FROM self")` |
| Lazy | n/a | `pl.scan_*`, `.lazy()`, `.collect()` |

## Cheat sheet

```python
# load
df = pl.read_csv("f.csv", try_parse_dates=True, schema_overrides={"id": pl.String})
lf = pl.scan_parquet("big.parquet")                            # lazy
# explore
df.glimpse(); df.describe(); df.null_count(); df["c"].value_counts(sort=True)
# core contexts
df.select("a", pl.col("b") * 2, cs.numeric().mean())
df.with_columns(c=pl.col("a") + pl.col("b"))
df.filter((pl.col("a") > 1) & pl.col("g").is_in(["x", "y"]))
df.group_by("g").agg(n=pl.len(), total=pl.col("x").sum(), top=pl.col("k").sort_by("x").last())
# windows
pl.col("x").sum().over("g");  pl.col("x").rank("min", descending=True).over("g")
# conditionals & cleaning
pl.when(c1).then(pl.lit("a")).when(c2).then(pl.lit("b")).otherwise(pl.lit("c"))
pl.col("s").str.strip_chars().str.to_titlecase();  pl.col("n").cast(pl.Float64, strict=False)
pl.col("x").fill_null(pl.col("x").median());  pl.coalesce("a", "b")
# combine & reshape
a.join(b, on="k", how="left", validate="m:1");  pl.concat([a, b], how="diagonal")
df.unpivot(index=["id"], variable_name="k", value_name="v");  long.pivot(on="k", index="id", values="v")
# time
df.sort("date").group_by_dynamic("date", every="1mo").agg(pl.col("x").sum())
# lazy
lf.filter(...).group_by(...).agg(...).collect();  lf.explain();  lf.sink_parquet("out.parquet")
# save
df.write_parquet("out.parquet");  df.write_csv("out.csv");  df.write_excel("out.xlsx")
```

## Top 10 Polars mistakes

| Mistake | Fix |
|---------|-----|
| `pl.lit` forgotten: `.then("gold")` reads a **column** called gold | `.then(pl.lit("gold"))` |
| Using a column created in the **same** `with_columns` | chain a second `with_columns` |
| Expecting group order to be stable | `.sort(...)` or `maintain_order=True` |
| `and` / `or` between expressions | `&` / `\|` with brackets |
| `df["c"] = ...` (pandas habit) | `df = df.with_columns(...)` |
| Treating `NaN` as missing | it isn't; use `fill_nan(None)` then null tools |
| `map_elements` for logic that has a native expression | `when/then`, `.str`, `.dt`, arithmetic |
| `read_csv` a huge file, then filter | `scan_csv(...).filter(...).collect()` |
| Strict cast errors on messy text | clean first, or `strict=False` and **count** the nulls |
| Old tutorial names (`groupby`, `melt`, `apply`, `cut`) | `group_by`, `unpivot`, `map_elements`, `when/then` / `bin_intervals` |

## pandas or Polars?

| Choose **Polars** when… | Choose **pandas** when… |
|-------------------------|-------------------------|
| data is large (≥ hundreds of MB) or growing | data is small and a library needs pandas |
| you want fast, readable pipelines | you rely on index-based alignment / `.loc` |
| you work with Parquet or many files | your team's existing code is pandas |
| you want lazy / streaming processing | you need the widest ecosystem |

They work well together: **Polars for the heavy lifting, `.to_pandas()` at the edge.**

## Where to go next

- Official user guide: https://docs.pola.rs/
- **DuckDB**: SQL on Parquet and Polars DataFrames, a great companion
- **Altair / hvPlot**: plotting that accepts Polars directly
- **Polars Cloud / GPU engine**: the same code at bigger scale
