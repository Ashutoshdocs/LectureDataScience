# Lecture 21: Project: cleaning messy data

Run: `python lecture.py`. It prints every step and saves `output/customers_clean.csv`.

Analysts often say most of their time goes into cleaning. `data/messy_customers.csv` packs the usual problems into 10 rows:

```
Customer ID, Full Name ,Email,Age,City,Signup Date,Spend (Rs)
001,  asha rao,asha@mail.com,34,delhi,2024-01-15,"12,500"
002,RAVI KUMAR,ravi@MAIL.com,29,Mumbai ,15/02/2024,"8,200"
003,Meena Iyer ,meena@mail.com,41,chennai,2024-03-01,"15,000"
003,Meena Iyer ,meena@mail.com,41,chennai,2024-03-01,"15,000"     ← duplicate
004,john d'souza,john@mail,-5,Delhi,2024-04-10,"3,400"           ← bad email, impossible age
...
007,ali  hasan,ali@mail.com,n/a,pune,not known,"9,900"           ← double space, text in number/date
009,karan mehta,karan@mail.com,250,bangalore,...                 ← age 250, old city name
```

## The problems and the fixes

| Problem | Example | Fix |
|---------|---------|-----|
| Messy column names | `" Full Name "`, `"Spend (Rs)"` | strip, lowercase, snake_case with `.str` on `df.columns` |
| Duplicate rows | customer 003 twice | `drop_duplicates()` |
| Extra / double spaces | `"  asha rao"`, `"ali  hasan"` | `.str.strip()`, `.str.replace(r"\s+", " ")` |
| Inconsistent case | `"RAVI KUMAR"`, `"delhi"` | `.str.title()` / `.str.lower()` |
| Synonyms / old names | `"bangalore"` vs `"Bengaluru"` | `.replace({...})` |
| Empty strings that mean missing | `""` | `.replace("", np.nan)` |
| Numbers stored as text | `"12,500"`, `"n/a"` | remove commas → `pd.to_numeric(errors="coerce")` |
| Impossible values | age `-5`, `250` | range check → `NaN` with `.where()` / `.mask()` |
| Mixed date formats | `2024-01-15` and `15/02/2024` | parse each format separately, then combine |
| Invalid emails | `"john@mail"` | regex check with `.str.match()` |
| IDs losing leading zeros | `001` → `1` | read with `dtype={"Customer ID": str}` |

## ⚠️ The mixed-date trap

```python
pd.to_datetime(s, format="mixed", dayfirst=True)
```
looks convenient, but `dayfirst=True` also flips ISO dates: `2024-03-01` becomes **3 January**. The safe way is to try each known format and combine:

```python
iso = pd.to_datetime(s, format="%Y-%m-%d", errors="coerce")
dmy = pd.to_datetime(s, format="%d/%m/%Y", errors="coerce")
dates = iso.fillna(dmy)
```

## A cleaning workflow you can reuse

1. **Look** first: `head()`, `info()`, `value_counts()` on every text column.
2. **Keep the raw data.** Work on a copy, and never overwrite the original file.
3. Fix **structure**: column names, duplicates.
4. Fix **types**: numbers, dates, IDs.
5. Fix **values**: whitespace, case, synonyms, impossible values.
6. **Flag** instead of silently deleting (`email_valid` column).
7. **Report** what changed: rows before and after, missing values before and after.
8. **Save** the clean version separately.

`lecture.py` wraps steps 3–6 in a single `clean()` function, so the same cleaning runs on next month's file.

## Extension exercises

1. Add an `age_group` column (`<30`, `30–39`, `40+`) with `pd.cut`.
2. Fill missing `spend` with the city median.
3. Extract the email domain into its own column.
4. Write the rows that failed any check to `output/needs_review.csv`.

<details><summary>Hints</summary>

```python
pd.cut(df["age"], bins=[0, 29, 39, 120], labels=["<30", "30-39", "40+"])
df["spend"].fillna(df.groupby("city")["spend"].transform("median"))
df["email"].str.split("@").str[1]
df[~df["email_valid"] | df["age"].isna() | df["signup_date"].isna()].to_csv(...)
```
</details>

**Next →** [Lecture 22: Recap & cheat sheet](../22_recap_cheatsheet/)
