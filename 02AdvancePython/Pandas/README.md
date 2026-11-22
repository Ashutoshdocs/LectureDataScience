# pandas — From Zero to Confident

A hands-on pandas course in 23 short lectures (00–22). It follows on from the NumPy course, since pandas is built on top of NumPy.

Every lecture folder has:

| File | What it is |
|------|------------|
| `README.md` | The lesson: concepts, diagrams, tables, common mistakes, exercises (with solutions) |
| `lecture.py` | Runnable code for the lesson. Read it, run it, change it |

The `data/` folder holds the CSV files the lectures read:

| File | Rows | What's in it |
|------|------|--------------|
| `sales.csv` | 240 | Orders across 2025: date, region, product, category, units, unit price, customer |
| `customers.csv` | 41 | Customer id, name, city, join date, segment |
| `students.csv` | 12 | Marks in 4 subjects, with a few missing values |
| `messy_customers.csv` | 10 | Deliberately dirty data for the cleaning project |
| `make_data.py` | n/a | Script that regenerates all of the above |

## How to use this course

1. **Install Python 3.10+** (check with `python --version`).
2. **Install the libraries** from your terminal (not inside Python):
   ```bash
   python -m pip install -r requirements.txt
   ```
3. Go through the folders **in order**. For each lecture:
   - Read `README.md`
   - Run the code from inside the folder: `python lecture.py`
   - Do the exercises at the bottom of the README

## Course map

| # | Lecture | Big idea |
|---|---------|----------|
| 00 | [Prerequisites](00_prerequisites/) | Python dicts & lists, NumPy basics, tabular thinking |
| 01 | [What is pandas?](01_what_is_pandas/) | Series + DataFrame, and why pandas instead of lists/NumPy/Excel |
| 02 | [Series](02_series/) | A labelled 1D array: values + index |
| 03 | [DataFrame basics](03_dataframe_basics/) | Building tables; columns, index, shape, dtypes |
| 04 | [Reading & writing files](04_reading_writing_files/) | `read_csv`, `to_csv`, Excel, JSON |
| 05 | [Exploring data](05_exploring_data/) | `head`, `info`, `describe`, `value_counts` |
| 06 | [Selecting: `[]`, `loc`, `iloc`](06_selecting_loc_iloc/) | Labels vs positions |
| 07 | [Filtering rows](07_filtering_rows/) | Boolean masks, `isin`, `between`, `query` |
| 08 | [Adding & modifying columns](08_adding_modifying_columns/) | Vectorized columns, `assign`, `np.where`, `map` |
| 09 | [Sorting & ranking](09_sorting_and_ranking/) | `sort_values`, `nlargest`, `rank` |
| 10 | [Missing data](10_missing_data/) | `isna`, `dropna`, `fillna` |
| 11 | [Data types](11_data_types/) | `astype`, `to_numeric`, `category`, memory |
| 12 | [String methods](12_string_methods/) | The `.str` accessor |
| 13 | [GroupBy & aggregation](13_groupby_aggregation/) | Split, apply, combine |
| 14 | [Pivot tables & crosstab](14_pivot_tables_crosstab/) | Excel-style summaries |
| 15 | [Merge, join & concat](15_merge_join_concat/) | Combining tables like SQL |
| 16 | [Reshaping: melt & pivot](16_reshaping_melt_pivot/) | Wide ↔ long data |
| 17 | [Dates & time series](17_dates_and_time_series/) | `to_datetime`, `.dt`, `resample`, `rolling` |
| 18 | [Vectorization vs apply](18_vectorization_vs_apply/) | Why loops and `apply` are slow, and what to use instead |
| 19 | [Plotting](19_plotting/) | `df.plot()` charts saved as PNG |
| 20 | [Project: sales analysis](20_project_sales_analysis/) | A full analysis, start to finish |
| 21 | [Project: data cleaning](21_project_data_cleaning/) | Turning messy data into tidy data |
| 22 | [Recap & cheat sheet](22_recap_cheatsheet/) | Everything on one page |

## Run everything at once

```bash
python run_all.py
```

## Version notes

Examples were tested with **pandas 3.0** and NumPy 2.5. Almost everything also works on pandas 2.x. The differences that matter:

- **Text columns** show dtype `str` in pandas 3 and `object` in pandas 2.
- **Copy-on-Write** is always on in pandas 3. Chained assignment like `df[df.x > 0]["y"] = 1` silently does nothing. Use `df.loc[df.x > 0, "y"] = 1` (Lecture 08).
