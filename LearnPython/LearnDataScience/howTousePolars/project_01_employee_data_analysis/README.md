# Project 1 — Employee Data Analysis with Polars

## Goal

Build a practical employee analytics project using Polars expressions, joins, data cleaning, aggregations, and file exports.

## Folder structure

```text
project_01_employee_data_analysis/
├── README.md
├── main.py
├── analysis.py
├── data/
│   ├── input/
│   │   ├── employees.csv
│   │   └── departments.csv
│   └── reference/
└── output/
```

## Setup

From the repository root:

```bash
python -m venv .venv
```

Activate the environment, then:

```bash
pip install -r requirements.txt
```

## Run

```bash
python project_01_employee_data_analysis/main.py
```

## What the project does

1. Reads employee and department CSV files.
2. Displays the input schema.
3. Checks for missing salary values.
4. Fills missing salary values using a clearly stated teaching rule (the sample uses the department-independent median).
5. Adds annual salary and salary band.
6. Joins department descriptions.
7. Calculates salary and employee-count summaries by department.
8. Saves cleaned employee data and summary CSV reports.

## Concepts demonstrated

```python
pl.read_csv(path)                         # Read CSV
df.schema                                 # Inspect data types
df.null_count()                           # Count nulls per column
pl.col("salary").fill_null(value)         # Fill missing values
df.with_columns(expression)               # Add/replace columns
pl.when(condition).then(x).otherwise(y)   # Conditional expression
df.join(other, on="department_id")        # Join DataFrames
df.group_by("department").agg(...)        # Group and aggregate
df.write_csv(path)                        # Export results
```

## Student exercises

1. Change the missing-salary strategy and explain why.
2. Add a column for monthly salary after tax using a hypothetical tax percentage.
3. Find the top three paid employees.
4. Calculate average salary by location.
5. Count employees in each department.
6. Add a conditional salary band with three categories.
7. Export the cleaned data as Parquet.
8. Introduce a duplicate employee ID and decide how to handle it.
9. Add a validation check for required columns.
10. Create a report of employees whose salary is null before cleaning.
