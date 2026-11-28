# Python Polars — From Scratch to Advanced

A beginner-friendly, practical teaching guide to Polars: a fast DataFrame library for working with tabular data in Python. It introduces DataFrames, expressions, filtering, transformations, aggregation, joins, missing values, CSV and Parquet, lazy execution, query optimization, and two complete projects.

> **Core idea:** Polars is designed around expressions and an optimized query engine. You describe the transformation you want, and Polars can optimize how it executes—especially when you use LazyFrames.

---

## Repository structure

```text
Python_Polars_Toolkit/
│
├── README.md
├── requirements.txt
│
├── project_01_employee_data_analysis/
│   ├── README.md
│   ├── main.py
│   ├── analysis.py
│   ├── data/
│   │   ├── input/
│   │   │   ├── employees.csv
│   │   │   └── departments.csv
│   │   └── reference/
│   │       └── README.md
│   └── output/
│
└── project_02_lazy_sales_pipeline/
    ├── README.md
    ├── main.py
    ├── pipeline.py
    ├── data/
    │   ├── input/
    │   │   ├── sales_2025.csv
    │   │   └── sales_2026.csv
    │   └── reference/
    │       └── products.csv
    ├── output/
    │   ├── reports/
    │   └── parquet/
    └── logs/
```

Input datasets are kept under `data/input/`, reference data under `data/reference/`, and generated reports or Parquet files under `output/`. The Python code is not mixed with generated files.

## Learning outcomes

By the end, learners should be able to:

1. Explain what Polars is and why it is used.
2. Install Polars and inspect its version.
3. Create Series and DataFrames.
4. Inspect rows, columns, schema, and data types.
5. Read CSV, JSON, and Parquet data.
6. Select, filter, sort, rename, and drop columns.
7. Create and transform columns with expressions.
8. Use `when/then/otherwise` conditional logic.
9. Handle null values and duplicates.
10. Work with strings, dates, and numeric columns.
11. Group data and calculate aggregations.
12. Join and concatenate DataFrames.
13. Understand eager and lazy execution.
14. Use `scan_csv()` and `scan_parquet()`.
15. Explain query optimization and inspect a query plan.
16. Write CSV and Parquet output.
17. Build an employee analysis project.
18. Build a lazy sales analytics pipeline.

---

# Part 1 — Foundations

## Chapter 1 — What is Polars?

Polars is a DataFrame library for Python and other languages. It is used to load, transform, analyze, and write structured data arranged in rows and columns.

A DataFrame is similar to a spreadsheet table or a database query result.

Example:

| employee_id | name | department | salary |
|---:|---|---|---:|
| 101 | Asha | Engineering | 65000 |
| 102 | Ravi | Operations | 58000 |
| 103 | Meera | Analytics | 72000 |

Polars provides tools to:
- Read data from files.
- Filter rows.
- Select and transform columns.
- Group and aggregate data.
- Join datasets.
- Process larger datasets efficiently.
- Execute optimized lazy queries.

## Chapter 2 — Why learn Polars?

Polars is useful when:
- You work with CSV or Parquet datasets.
- You need fast DataFrame transformations.
- You want a modern expression-based API.
- You need lazy query execution.
- You are building data engineering or analytics pipelines.

### Polars and pandas

| Polars | pandas |
|---|---|
| Expression-oriented API | Often uses Series/DataFrame methods and vectorized operations |
| Supports eager and lazy execution | Primarily eager DataFrame workflow |
| Built around a Rust execution engine | Primarily Python/C-backed ecosystem |
| Strong Parquet and lazy query workflows | Broad ecosystem and extensive integrations |
| Can optimize lazy query plans | Execution is generally performed as operations are called |

Both libraries are useful. Choose based on the project, ecosystem, integrations, and workload rather than assuming one replaces the other in every situation.

## Chapter 3 — Install Polars

Create a virtual environment (recommended).

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install:

```bash
python -m pip install --upgrade pip
pip install polars
```

For optional Excel support or other integrations, install the additional package required by that workflow. The core course examples use CSV and Parquet.

Check installation:

```bash
python -c "import polars as pl; print(pl.__version__)"
```

## Chapter 4 — Import Polars

```python
import polars as pl

print(pl.__version__)
```

The common alias is `pl`.

## Chapter 5 — Create a Series

A Series is a one-dimensional column of data.

```python
import polars as pl

names = pl.Series("name", ["Asha", "Ravi", "Meera"])
salaries = pl.Series("salary", [65000, 58000, 72000])

print(names)
print(salaries)
```

A Series has a name and a data type.

## Chapter 6 — Create a DataFrame

A DataFrame is a collection of columns.

```python
import polars as pl

employees = pl.DataFrame({
    "employee_id": [101, 102, 103],
    "name": ["Asha", "Ravi", "Meera"],
    "department": ["Engineering", "Operations", "Analytics"],
    "salary": [65000, 58000, 72000],
})

print(employees)
```

You can also construct a DataFrame from a list of dictionaries:

```python
rows = [
    {"name": "Asha", "salary": 65000},
    {"name": "Ravi", "salary": 58000},
]

df = pl.DataFrame(rows)
print(df)
```

## Chapter 7 — Inspect a DataFrame

```python
print(df.head())
print(df.tail())
print(df.shape)
print(df.columns)
print(df.schema)
print(df.dtypes)
print(df.height)
print(df.width)
print(df.describe())
```

- `shape`: number of rows and columns.
- `columns`: column names.
- `schema`: column names and data types.
- `height`: row count.
- `width`: column count.
- `describe()`: summary statistics for supported columns.

## Chapter 8 — Understand data types

Common Polars data types:

| Type | Example |
|---|---|
| `pl.Int64` | Whole numbers |
| `pl.Float64` | Decimal numbers |
| `pl.String` | Text |
| `pl.Boolean` | True/False |
| `pl.Date` | Calendar date |
| `pl.Datetime` | Date and time |
| `pl.Null` | Null-only values |

Example:

```python
print(df.schema)
```

Explicitly set a type when constructing data if needed:

```python
df = pl.DataFrame({
    "employee_id": pl.Series([101, 102], dtype=pl.Int64),
    "salary": pl.Series([65000, 58000], dtype=pl.Float64),
})
```

## Chapter 9 — Read a CSV file

```python
import polars as pl

df = pl.read_csv("data/input/employees.csv")
print(df)
```

Useful options:

```python
df = pl.read_csv(
    "data/input/employees.csv",
    infer_schema_length=1000,
    try_parse_dates=True,
)
```

Schema inference depends on the data sampled and the file contents. For production pipelines, explicitly define or validate important column types.

## Chapter 10 — Read JSON

For newline-delimited JSON (NDJSON):

```python
df = pl.read_ndjson("data/input/events.ndjson")
```

For a JSON file containing a supported table-like structure:

```python
df = pl.read_json("data/input/data.json")
```

JSON can represent nested structures. Inspect the resulting schema and decide whether nested columns need to be unnested or transformed.

## Chapter 11 — Write CSV

```python
df.write_csv("output/employees_export.csv")
```

Create the output folder first:

```python
from pathlib import Path

output_dir = Path("output")
output_dir.mkdir(parents=True, exist_ok=True)

df.write_csv(output_dir / "employees_export.csv")
```

## Chapter 12 — Parquet format

Parquet is a columnar file format commonly used in analytics and data engineering.

Benefits:
- Efficient column-oriented storage.
- Supports data types and schema information.
- Often smaller than equivalent CSV data.
- Works well with analytical query engines.

Write and read:

```python
df.write_parquet("output/employees.parquet")
restored = pl.read_parquet("output/employees.parquet")
```

## Chapter 13 — Select columns

Use `select()` to choose columns or calculate expressions:

```python
df.select("name", "salary")
```

Expression syntax:

```python
df.select(
    pl.col("name"),
    pl.col("salary"),
)
```

Select all columns:

```python
df.select(pl.all())
```

## Chapter 14 — Filter rows

```python
high_salary = df.filter(pl.col("salary") > 60000)
print(high_salary)
```

Multiple conditions:

```python
result = df.filter(
    (pl.col("salary") > 60000) &
    (pl.col("department") == "Engineering")
)
```

Use `&` for AND and `|` for OR. Put each comparison in parentheses.

## Chapter 15 — Sort rows

```python
sorted_df = df.sort("salary")
highest_first = df.sort("salary", descending=True)
```

Sort by multiple columns:

```python
df.sort(["department", "salary"], descending=[False, True])
```

## Chapter 16 — Rename and drop columns

```python
renamed = df.rename({"salary": "monthly_salary"})
without_id = df.drop("employee_id")
```

## Chapter 17 — Add a calculated column with `with_columns()`

```python
df = df.with_columns(
    (pl.col("salary") * 12).alias("annual_salary")
)
```

`with_columns()` adds or replaces columns while retaining the other columns.

## Chapter 18 — Create multiple columns

```python
df = df.with_columns(
    (pl.col("salary") * 12).alias("annual_salary"),
    (pl.col("salary") * 0.10).alias("estimated_bonus"),
)
```

Each expression is given a name using `.alias()`.

## Chapter 19 — Conditional logic with `when/then/otherwise`

```python
df = df.with_columns(
    pl.when(pl.col("salary") >= 70000)
    .then(pl.lit("High"))
    .otherwise(pl.lit("Standard"))
    .alias("salary_band")
)
```

This is similar to an if/else expression applied to a column.

## Chapter 20 — Null values

Polars uses `null` for missing values.

Count nulls:

```python
df.null_count()
```

Filter nulls:

```python
df.filter(pl.col("salary").is_null())
```

Filter non-null values:

```python
df.filter(pl.col("salary").is_not_null())
```

Fill nulls:

```python
df = df.with_columns(
    pl.col("salary").fill_null(0)
)
```

Dropping rows with nulls:

```python
cleaned = df.drop_nulls()
```

Choose a missing-value strategy based on the meaning of the column. Replacing all missing values with zero is not always correct.

## Chapter 21 — Duplicates

```python
unique_rows = df.unique()
```

Keep the first row for each employee ID:

```python
unique_employees = df.unique(
    subset=["employee_id"],
    keep="first",
    maintain_order=True,
)
```

Decide which record should survive when duplicates have different values. Deduplication is a business rule, not merely a technical operation.

## Chapter 22 — String operations

```python
df = df.with_columns(
    pl.col("name").str.to_uppercase().alias("name_upper"),
    pl.col("name").str.to_lowercase().alias("name_lower"),
    pl.col("name").str.strip_chars().alias("name_clean"),
)
```

Contains:

```python
df.filter(pl.col("name").str.contains("ash", literal=False))
```

String expressions can be combined with filtering and transformations.

## Chapter 23 — Numeric operations

```python
df = df.with_columns(
    pl.col("salary").round(0).alias("rounded_salary"),
    pl.col("salary").abs().alias("absolute_salary"),
)
```

Useful aggregations:

```python
df.select(
    pl.col("salary").min().alias("minimum"),
    pl.col("salary").max().alias("maximum"),
    pl.col("salary").mean().alias("average"),
    pl.col("salary").sum().alias("total"),
)
```

## Chapter 24 — Group by and aggregate

```python
summary = df.group_by("department").agg(
    pl.col("salary").mean().alias("average_salary"),
    pl.col("salary").max().alias("maximum_salary"),
    pl.len().alias("employee_count"),
)
```

Sort the result:

```python
summary.sort("average_salary", descending=True)
```

## Chapter 25 — Multiple grouping columns

```python
summary = df.group_by(["department", "location"]).agg(
    pl.col("salary").mean().alias("average_salary"),
    pl.len().alias("employee_count"),
)
```

## Chapter 26 — Join DataFrames

Suppose one table contains employee records and another contains department details.

```python
employees = pl.DataFrame({
    "employee_id": [101, 102],
    "department_id": [10, 20],
})

departments = pl.DataFrame({
    "department_id": [10, 20],
    "department_name": ["Engineering", "Operations"],
})

result = employees.join(
    departments,
    on="department_id",
    how="left",
)
```

Common join types:
- `inner`
- `left`
- `full`
- `semi`
- `anti`
- `cross`

Choose a join type based on which unmatched records should be retained.

## Chapter 27 — Concatenate DataFrames

Stack rows from similar DataFrames:

```python
combined = pl.concat([df_january, df_february], how="vertical")
```

For horizontally combining columns:

```python
combined_columns = pl.concat([left_df, right_df], how="horizontal")
```

The schemas must be compatible for the chosen concatenation strategy. Inspect column names and types before combining.

## Chapter 28 — Date and datetime columns

Parse a date string:

```python
df = df.with_columns(
    pl.col("order_date").str.to_date("%Y-%m-%d")
)
```

Extract date parts:

```python
df = df.with_columns(
    pl.col("order_date").dt.year().alias("year"),
    pl.col("order_date").dt.month().alias("month"),
)
```

Date parsing formats must match the input data. Inspect the resulting dtype after parsing.

## Chapter 29 — Expressions: the most important Polars concept

An expression describes a computation:

```python
pl.col("salary") * 12
```

It is not simply a Python value. Polars evaluates the expression in a context such as:
- `select()`
- `with_columns()`
- `filter()`
- `group_by().agg()`

Example:

```python
df.select(
    (pl.col("salary") * 12).alias("annual_salary")
)
```

Learning expressions is central to writing idiomatic Polars code.

---

# Part 2 — Lazy execution and optimization

## Chapter 30 — Eager vs lazy execution

**Eager execution:** operations run and produce a result immediately.

```python
df = pl.read_csv("data/input/employees.csv")
result = df.filter(pl.col("salary") > 60000)
```

**Lazy execution:** Polars builds a query plan first. The plan runs when you call `.collect()`.

```python
query = (
    pl.scan_csv("data/input/employees.csv")
    .filter(pl.col("salary") > 60000)
    .select("name", "salary")
)

result = query.collect()
```

## Chapter 31 — `scan_csv()` vs `read_csv()`

| `read_csv()` | `scan_csv()` |
|---|---|
| Reads data eagerly | Creates a LazyFrame scan |
| Returns a DataFrame | Returns a LazyFrame |
| Data is read as part of the call | Execution is deferred until collection |
| Useful for smaller interactive work | Useful for building optimized pipelines |

## Chapter 32 — LazyFrame

```python
lazy_df = pl.scan_csv("data/input/employees.csv")

print(type(lazy_df))
```

A LazyFrame describes a query. It is not the same as a fully materialized DataFrame.

## Chapter 33 — Build a lazy pipeline

```python
query = (
    pl.scan_csv("data/input/employees.csv")
    .filter(pl.col("salary") > 60000)
    .with_columns((pl.col("salary") * 12).alias("annual_salary"))
    .select("name", "department", "annual_salary")
)

result = query.collect()
```

The transformations are described before execution.

## Chapter 34 — Query optimization

Polars can optimize lazy queries. Common optimization concepts include:
- **Predicate pushdown:** apply filters as close to the scan as possible.
- **Projection pushdown:** read only columns needed by the query when possible.
- **Common subexpression elimination:** reuse repeated computations where applicable.
- **Expression simplification:** simplify parts of the query plan.

These optimizations depend on the query and data source. They are not a guarantee that every query becomes faster.

## Chapter 35 — Inspect the query plan

```python
query = (
    pl.scan_csv("data/input/employees.csv")
    .filter(pl.col("salary") > 60000)
    .select("name", "salary")
)

print(query.explain())
```

Use this to teach students that a LazyFrame represents a plan, not just a DataFrame waiting to be printed.

## Chapter 36 — Collect the result

```python
result = query.collect()
print(result)
```

`collect()` executes the lazy query and returns a DataFrame.

## Chapter 37 — Lazy Parquet scan

```python
query = (
    pl.scan_parquet("data/input/employees.parquet")
    .filter(pl.col("salary") > 60000)
    .select("name", "salary")
)

result = query.collect()
```

Parquet is well suited to analytical pipelines because it is columnar and stores schema information.

## Chapter 38 — Streaming collection

Polars supports execution strategies intended to process data in batches for workloads that benefit from streaming. Availability and behavior depend on the Polars version and query plan.

For a version that supports it, investigate the `engine` option on `collect()` and the current Polars documentation before teaching a particular engine setting. Do not assume every operation can be streamed.

---

# Part 3 — Data engineering practices

## Chapter 39 — Validate a schema

```python
df = pl.read_csv("data/input/employees.csv")

required_columns = {"employee_id", "name", "department", "salary"}
missing = required_columns - set(df.columns)

if missing:
    raise ValueError(f"Missing required columns: {sorted(missing)}")
```

Validate required columns and data types at the beginning of a pipeline.

## Chapter 40 — Handle invalid data

```python
df = df.with_columns(
    pl.col("salary").cast(pl.Float64, strict=False)
)
```

With `strict=False`, values that cannot be converted may become null. Inspect and report invalid rows rather than silently ignoring data quality problems.

## Chapter 41 — Reusable transformation functions

```python
import polars as pl

def add_annual_salary(df: pl.DataFrame) -> pl.DataFrame:
    return df.with_columns(
        (pl.col("salary") * 12).alias("annual_salary")
    )
```

Keep transformations in functions so they can be tested and reused.

## Chapter 42 — Write Parquet output

```python
result.write_parquet("output/processed_data.parquet")
```

For a lazy query, you can collect and write, or use supported lazy sink APIs in the installed Polars version. Verify the relevant API for the version used in class.

## Chapter 43 — Performance best practices

- Prefer expressions over Python row-by-row loops.
- Use LazyFrames for multi-step query pipelines where appropriate.
- Select only the columns you need.
- Filter early in a lazy query.
- Prefer Parquet for repeated analytical workloads when suitable.
- Avoid converting to Python lists or dictionaries unnecessarily.
- Avoid calling `.collect()` repeatedly in the middle of one lazy pipeline.
- Validate schemas and data quality.
- Benchmark with representative data; do not assume every workload benefits equally.

## Chapter 44 — Polars and pandas interoperability

You may need to work with both libraries:

```python
import polars as pl
import pandas as pd

polars_df = pl.DataFrame({
    "name": ["Asha", "Ravi"],
    "score": [90, 85],
})

pandas_df = polars_df.to_pandas()
polars_again = pl.from_pandas(pandas_df)
```

Conversion may require optional dependencies such as PyArrow depending on the operation and installed versions. Conversion can also use additional memory.

---

# Part 4 — Practical projects

## Project 1 — Employee Data Analysis

Location: `project_01_employee_data_analysis/`

Build an employee analytics application that:
- Reads employee and department CSV files.
- Inspects schema and data quality.
- Handles missing salary values.
- Adds annual salary and salary bands.
- Joins employee and department details.
- Calculates department-level summaries.
- Exports cleaned data and summary reports.

Run:

```bash
python project_01_employee_data_analysis/main.py
```

Read the project README for the walkthrough and exercises.

## Project 2 — Lazy Sales Analytics Pipeline

Location: `project_02_lazy_sales_pipeline/`

Build a small data engineering pipeline that:
- Scans multiple monthly CSV files lazily.
- Selects and casts required columns.
- Joins product reference data.
- Calculates revenue.
- Aggregates sales by product and region.
- Inspects the query plan.
- Writes Parquet and CSV outputs.

Run:

```bash
python project_02_lazy_sales_pipeline/main.py
```

Read the project README for the walkthrough and exercises.

---

# Part 5 — Practice questions

1. What is Polars?
2. What is a DataFrame?
3. What is a Series?
4. Why do we commonly import Polars as `pl`?
5. What is the difference between `height` and `width`?
6. What does `schema` tell us?
7. How do you read a CSV file?
8. What is Parquet and why is it useful?
9. What is the difference between `select()` and `filter()`?
10. What does `with_columns()` do?
11. What does `.alias()` do?
12. How does `when/then/otherwise` work?
13. What is a null value?
14. How can you count nulls?
15. What does `group_by().agg()` do?
16. What is the purpose of a join?
17. What is the difference between vertical and horizontal concatenation?
18. What is an expression in Polars?
19. What is the difference between a DataFrame and a LazyFrame?
20. What does `scan_csv()` return?
21. When does a lazy query execute?
22. What does `collect()` do?
23. What is predicate pushdown?
24. What is projection pushdown?
25. Why should you inspect a query plan?
26. Why are Python row-by-row loops often less suitable for Polars transformations?
27. Why should schemas be validated?
28. When might pandas still be the better choice?
29. Why should you benchmark a real workload?
30. What are the benefits of keeping input, reference, and output data in separate folders?

## Final teaching sequence

1. Explain DataFrames and where Polars fits in data work.
2. Install Polars and inspect the version.
3. Create Series and DataFrames.
4. Read CSV and inspect schema.
5. Select, filter, sort, and transform columns.
6. Teach expressions and conditional logic.
7. Handle nulls and duplicates.
8. Group, aggregate, join, and concatenate.
9. Introduce date and string operations.
10. Explain eager versus lazy execution.
11. Build a lazy scan/filter/select pipeline.
12. Inspect the query plan and collect the result.
13. Compare CSV and Parquet workflows.
14. Build Project 1.
15. Build Project 2.

## Key takeaway

Use **Polars expressions to describe DataFrame transformations**. Use eager DataFrames for straightforward interactive tasks and LazyFrames to build optimizable multi-step pipelines. Validate schemas, handle missing data intentionally, and keep input, reference, and output files organized.
