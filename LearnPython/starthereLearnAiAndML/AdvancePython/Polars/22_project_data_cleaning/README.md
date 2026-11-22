# Lecture 22: Project: cleaning messy data with expressions

Run: `python lecture.py`. It saves `output/customers_clean.parquet`, `output/customers_clean.csv` and `output/needs_review.csv`.

Same messy file as the pandas course (`data/messy_customers.csv`), cleaned entirely with Polars expressions.

## Problems → Polars fixes

| Problem | Example | Polars fix |
|---------|---------|-----------|
| Messy column names | `" Full Name "`, `"Spend (Rs)"` | `df.rename(lambda c: ...)` with a cleaning function |
| IDs losing zeros | `001` → `1` | `schema_overrides={"Customer ID": pl.String}` |
| Duplicate rows | customer 003 twice | `.unique(maintain_order=True)` |
| Spaces / case | `"  asha rao"`, `"ali  hasan"` | `.str.strip_chars().str.replace_all(r"\s+", " ").str.to_titlecase()` |
| Synonyms | `"bangalore"` | `.replace({"Bangalore": "Bengaluru"})` |
| Empty strings | `""` | `pl.when(pl.col(c) == "").then(None).otherwise(pl.col(c))` |
| Numbers as text | `"12,500"`, `"n/a"` | `.str.replace_all(",", "").cast(pl.Float64, strict=False)` |
| Impossible values | age `-5`, `250` | `pl.when(pl.col("age").is_between(0, 120)).then(pl.col("age"))` |
| Mixed date formats | `2024-01-15` / `15/02/2024` | `pl.coalesce(str.to_date(fmt1, strict=False), str.to_date(fmt2, strict=False))` |
| Invalid emails | `"john@mail"` | `.str.contains(r"^[\w.+-]+@[\w-]+\.[a-z]{2,}$")` |

## Polars-specific lessons

- **One `with_columns` = parallel cleaning.** Each column's recipe is independent, so they all run at once.
- **Strict casting finds problems.** A strict cast fails loudly and tells you which values broke it. Then you choose `strict=False` on purpose and **count** the nulls it created.
- **The whole cleaner is one function returning a LazyFrame**, so the same code works on a 10-row file or a 10-million-row file with `scan_csv`.
- **Save as Parquet**: the types (dates, `Int64` ages, text IDs) survive, unlike CSV.

## Workflow

1. Look (`glimpse`, `value_counts` per text column)
2. Fix structure (names, duplicates)
3. Fix types (numbers, dates, IDs)
4. Fix values (spaces, case, synonyms, impossible values)
5. Flag (`email_valid`), don't silently delete
6. Report (rows and nulls before → after)
7. Save clean + "needs review" files separately

## Extension exercises

1. Add `age_group` (`<30`, `30–39`, `40+`) with `when/then`.
2. Fill missing `spend` with the city median (`.over("city")`).
3. Add an `email_domain` column.
4. Run `clean()` on `pl.scan_csv(...)` and print the optimised plan.

<details><summary>Hints</summary>

```python
pl.when(pl.col("age") < 30).then(pl.lit("<30")).when(pl.col("age") < 40).then(pl.lit("30-39")).otherwise(pl.lit("40+"))
pl.col("spend").fill_null(pl.col("spend").median().over("city"))
pl.col("email").str.split("@").list.last()
clean(pl.scan_csv(...)).explain()
```
</details>

**Next →** [Lecture 23: Recap & cheat sheet](../23_recap_cheatsheet/)
