# Pandas – Complete Beginner-to-Advanced Course

> **Course continuity**
>
> This guide follows the learning sequence:
>
> 1. **Python Vectors: Complete Foundation to NumPy** – learned vectors and numerical operations using core Python.
> 2. **NumPy Environment Setup – Theory and Practical** – prepared Python and installed NumPy.
> 3. **NumPy – Complete Beginner to Advanced** – learned arrays, dimensions, indexing, broadcasting, statistics, filtering, and numerical operations.
> 4. **This course: Pandas – Complete Beginner to Advanced** – uses those NumPy foundations to work with real-world tabular data such as CSV files, Excel sheets, and business datasets.

Pandas is especially useful when data is arranged in rows and columns. We will begin with the concepts, then learn the main pandas objects and operations, and finally build two complete projects.

---

# Course outcomes

By the end of this course, students should be able to:

- Explain what pandas is and when to use it.
- Understand the difference between a NumPy array, a pandas Series, and a DataFrame.
- Install pandas and verify the environment.
- Create Series and DataFrames from lists, dictionaries, and NumPy arrays.
- Read and write CSV and Excel files.
- Inspect, select, filter, sort, and update data.
- Understand indexes, columns, and data types.
- Handle missing values and duplicate records.
- Convert data types and work with text and dates.
- Create new columns and apply calculations.
- Group data and calculate aggregations.
- Combine datasets using merge, join, and concat.
- Reshape data using pivot, pivot_table, melt, and crosstab.
- Work with time-series data and rolling calculations.
- Use vectorized operations and understand when `apply()` is appropriate.
- Build reusable data-cleaning and analysis workflows.
- Complete two end-to-end data-analysis projects.

## Prerequisites

Students should be comfortable with:

- Python variables, lists, dictionaries, loops, conditions, and functions.
- NumPy arrays, indexing, slicing, and basic statistics.
- Basic CSV concepts: rows, columns, headers, and records.

Pandas is built on top of the Python scientific-computing ecosystem and works closely with NumPy. You do not need to master every advanced NumPy feature before starting pandas, but understanding arrays, data types, and Boolean filtering will help.

## Environment setup

Activate the virtual environment created in the earlier chapters.

### Install pandas

```bash
python -m pip install pandas
```

For Excel `.xlsx` files, install an Excel engine as well:

```bash
python -m pip install openpyxl
```

Optional plotting support:

```bash
python -m pip install matplotlib
```

Verify the installation:

```bash
python -c "import pandas as pd; print(pd.__version__)"
```

### Save project dependencies

```bash
python -m pip freeze > requirements.txt
```

A focused requirements file for this course could contain:

```text
numpy
pandas
openpyxl
matplotlib
```

For a reproducible classroom or team project, pin tested package versions rather than relying on unpinned names.

## Suggested folder structure

```text
pandas-course/
│
├── .venv/
├── requirements.txt
│
├── 01_pandas_introduction.py
├── 02_series.py
├── 03_dataframe.py
├── 04_dataframe_attributes.py
├── 05_read_csv.py
├── 06_select_columns_rows.py
├── 07_filter_sort.py
├── 08_add_update_columns.py
├── 09_missing_values.py
├── 10_duplicates.py
├── 11_data_types.py
├── 12_string_operations.py
├── 13_datetime_operations.py
├── 14_groupby.py
├── 15_aggregation.py
├── 16_merge_join_concat.py
├── 17_pivot_melt_crosstab.py
├── 18_apply_map_vectorization.py
├── 19_time_series.py
├── 20_read_write_files.py
│
├── project_1_employee_analysis/
│   ├── README.md
│   ├── employees.csv
│   └── main.py
│
└── project_2_retail_sales_analysis/
    ├── README.md
    ├── orders.csv
    ├── products.csv
    └── main.py
```

---

# Part 1 – Understand pandas

## Chapter 1 – What is pandas?

Pandas is a Python library used to load, clean, transform, analyze, and summarize structured data.

Structured data is commonly arranged in rows and columns, for example:

| Employee ID | Name | Department | Salary |
|---|---|---|---:|
| 101 | Amit | IT | 60000 |
| 102 | Neha | HR | 55000 |
| 103 | Ravi | IT | 72000 |

This kind of data is commonly stored in:

- CSV files.
- Excel workbooks.
- Database query results.
- JSON records.
- Data collected from APIs.

Pandas provides two central data structures:

1. **Series** – a one-dimensional labeled array.
2. **DataFrame** – a two-dimensional labeled table with rows and columns.

### Why do we need pandas when we already know NumPy?

NumPy is excellent for numerical arrays and mathematical operations. Pandas adds convenient labels and tools for working with tabular data.

| Feature | NumPy | pandas |
|---|---|---|
| Main structure | `ndarray` | `Series`, `DataFrame` |
| Labels | Mainly positional | Row index and column labels |
| Tabular data | Possible using 2D arrays | A primary use case |
| Different column types | Usually one dtype per array | Different dtypes per column |
| Missing data | Supports NaN and related tools | Rich missing-data operations |
| CSV/Excel workflow | Basic numerical text/file tools | Convenient data import/export |
| Grouped analysis | Numerical operations can be written manually | `groupby()` and aggregations |

### A simple mental model

- NumPy array: a numerical array.
- Series: one labeled column of values.
- DataFrame: a table containing one or more labeled columns.

Pandas uses NumPy extensively for many operations, but modern pandas also supports other data types and storage approaches.

## Chapter 2 – Import pandas

The standard convention is:

```python
import pandas as pd
```

`pd` is an alias, just like `np` is the standard alias for NumPy.

```python
import pandas as pd
import numpy as np

print("pandas version:", pd.__version__)
print("NumPy version:", np.__version__)
```

### First pandas object

```python
import pandas as pd

marks = pd.Series([75, 80, 92, 68, 88])

print(marks)
```

Unlike a normal NumPy array, the Series displays an index alongside its values.

---

# Part 2 – Pandas data structures

## Chapter 3 – Series from scratch

A Series is a one-dimensional labeled data structure.

```python
import pandas as pd

marks = pd.Series([75, 80, 92, 68, 88])

print(marks)
```

The default index is `0, 1, 2, ...`.

### Create a Series with a custom index

```python
marks = pd.Series(
    [75, 80, 92],
    index=["Amit", "Neha", "Ravi"]
)

print(marks)
```

Now each value is associated with a student name.

### Access Series values

```python
print(marks["Amit"])
print(marks["Ravi"])
```

### Access by position with `iloc`

```python
print(marks.iloc[0])
print(marks.iloc[1])
```

### Access by label with `loc`

```python
print(marks.loc["Amit"])
```

**Important:** `loc` is label-based, while `iloc` is integer-position-based. This distinction is essential when the index contains custom labels.

### Create a Series from a dictionary

```python
student_marks = {
    "Amit": 75,
    "Neha": 80,
    "Ravi": 92
}

marks = pd.Series(student_marks)

print(marks)
```

Dictionary keys become the Series index.

### Series attributes

```python
print("Values:", marks.values)
print("Index:", marks.index)
print("Dtype:", marks.dtype)
print("Shape:", marks.shape)
print("Size:", marks.size)
```

### Series operations

```python
marks = pd.Series([75, 80, 92, 68, 88])

print("Sum:", marks.sum())
print("Mean:", marks.mean())
print("Maximum:", marks.max())
print("Minimum:", marks.min())
print("Median:", marks.median())
```

### Series arithmetic

```python
marks = pd.Series([70, 80, 90])

print(marks + 5)
print(marks * 2)
```

Series operations align values by index labels when combining labeled Series. This differs from simply combining values by position.

```python
first = pd.Series([10, 20], index=["A", "B"])
second = pd.Series([100, 200], index=["B", "C"])

print(first + second)
```

Only matching labels have values available on both sides; unmatched labels produce missing results.

## Chapter 4 – DataFrame from scratch

A DataFrame is a two-dimensional labeled table.

### Create a DataFrame from a dictionary

```python
import pandas as pd

data = {
    "Name": ["Amit", "Neha", "Ravi"],
    "Age": [25, 28, 30],
    "Department": ["IT", "HR", "IT"],
    "Salary": [60000, 55000, 72000]
}

df = pd.DataFrame(data)

print(df)
```

Each dictionary key becomes a column name. Each list supplies the values for that column.

### Create a DataFrame from a list of dictionaries

```python
employees = [
    {"Name": "Amit", "Age": 25, "Salary": 60000},
    {"Name": "Neha", "Age": 28, "Salary": 55000},
    {"Name": "Ravi", "Age": 30, "Salary": 72000}
]

df = pd.DataFrame(employees)

print(df)
```

This format is common when data arrives as JSON records from an API.

### Create a DataFrame from a NumPy array

```python
import numpy as np
import pandas as pd

values = np.array([
    [101, 60000],
    [102, 55000],
    [103, 72000]
])

df = pd.DataFrame(
    values,
    columns=["EmployeeID", "Salary"]
)

print(df)
```

### Create a DataFrame with a custom index

```python
df = pd.DataFrame(
    {
        "Department": ["IT", "HR", "Finance"],
        "Employees": [20, 12, 8]
    },
    index=["Pune", "Mumbai", "Delhi"]
)

print(df)
```

### DataFrame attributes

```python
print("Shape:", df.shape)
print("Rows and columns:", df.ndim)
print("Column names:", df.columns)
print("Row index:", df.index)
print("Data types:")
print(df.dtypes)
print("Total elements:", df.size)
```

For a DataFrame, `shape` returns `(number_of_rows, number_of_columns)`.

## Chapter 5 – Series versus DataFrame

| Feature | Series | DataFrame |
|---|---|---|
| Dimensions | One-dimensional | Two-dimensional |
| Structure | One labeled sequence | Labeled rows and columns |
| Example | One salary column | Employee table |
| Selection | A value or subset | A column, row, or table subset |
| Common creation | `pd.Series()` | `pd.DataFrame()` |

A single DataFrame column selected with `df["Salary"]` is normally a Series. Selecting it with double brackets, `df[["Salary"]]`, returns a DataFrame.

---

# Part 3 – Inspect and understand data

## Chapter 6 – Create a sample DataFrame

Use the following dataset in the next chapters:

```python
import pandas as pd

data = {
    "EmployeeID": [101, 102, 103, 104, 105, 106],
    "Name": ["Amit", "Neha", "Ravi", "Sara", "Priya", "John"],
    "Department": ["IT", "HR", "IT", "Finance", "HR", "IT"],
    "Age": [25, 28, 30, 27, 29, 32],
    "Salary": [60000, 55000, 72000, 65000, 58000, 80000],
    "City": ["Pune", "Mumbai", "Pune", "Delhi", "Mumbai", "Pune"]
}

df = pd.DataFrame(data)

print(df)
```

## Chapter 7 – `head()`, `tail()`, and `sample()`

```python
print(df.head())
```

Displays the first five rows by default.

```python
print(df.head(3))
```

Displays the first three rows.

```python
print(df.tail(2))
```

Displays the last two rows.

```python
print(df.sample(3, random_state=42))
```

Displays a random sample. The fixed `random_state` makes this classroom example reproducible.

## Chapter 8 – `info()` and `describe()`

### `info()`

```python
df.info()
```

Shows:

- Number of rows.
- Column names.
- Non-null counts.
- Data types.
- Memory usage information.

### `describe()`

```python
print(df.describe())
```

Provides descriptive statistics for numeric columns by default.

For categorical columns:

```python
print(df.describe(include="object"))
```

For all columns:

```python
print(df.describe(include="all"))
```

### `shape`, `columns`, and `dtypes`

```python
print(df.shape)
print(df.columns)
print(df.dtypes)
```

### Count records and values

```python
print("Rows:", len(df))
print("Non-null values per column:")
print(df.count())

print("Department counts:")
print(df["Department"].value_counts())
```

`count()` excludes missing values. `value_counts()` counts each distinct value by default and normally excludes missing values unless requested.

---

# Part 4 – Read data from files

## Chapter 9 – What is a CSV file?

CSV means Comma-Separated Values. It is a text format commonly used to store tabular data.

Example:

```csv
EmployeeID,Name,Department,Salary
101,Amit,IT,60000
102,Neha,HR,55000
103,Ravi,IT,72000
```

Each line represents a record. The first line commonly contains column names.

## Chapter 10 – Read a CSV file

Create `employees.csv`:

```csv
EmployeeID,Name,Department,Salary,City
101,Amit,IT,60000,Pune
102,Neha,HR,55000,Mumbai
103,Ravi,IT,72000,Pune
104,Sara,Finance,65000,Delhi
105,Priya,HR,58000,Mumbai
```

Read it:

```python
import pandas as pd

df = pd.read_csv("employees.csv")

print(df)
```

The file path is interpreted relative to the program's current working directory unless you provide an absolute path.

### Useful `read_csv()` options

```python
df = pd.read_csv(
    "employees.csv",
    header=0,
    encoding="utf-8"
)
```

Other useful options include:

| Parameter | Purpose |
|---|---|
| `filepath_or_buffer` | File path or supported data source |
| `sep` | Field separator |
| `header` | Row used for column labels |
| `names` | Explicit column names |
| `usecols` | Read selected columns |
| `dtype` | Specify data types |
| `na_values` | Additional values treated as missing |
| `parse_dates` | Parse selected columns as dates |
| `nrows` | Read only a specified number of rows |
| `skiprows` | Skip selected rows |
| `encoding` | Text encoding |

Example:

```python
df = pd.read_csv(
    "employees.csv",
    usecols=["Name", "Department", "Salary"]
)

print(df)
```

### Read a tab-separated file

```python
df = pd.read_csv("employees.tsv", sep="\t")
```

## Chapter 11 – Read Excel files

Install an Excel engine:

```bash
python -m pip install openpyxl
```

Read an Excel workbook:

```python
df = pd.read_excel("employees.xlsx", sheet_name="Employees")

print(df)
```

Read the first sheet:

```python
df = pd.read_excel("employees.xlsx")
```

Read all sheets:

```python
sheets = pd.read_excel("employees.xlsx", sheet_name=None)

print(sheets.keys())
```

When `sheet_name=None`, pandas returns a dictionary of DataFrames keyed by sheet name.

## Chapter 12 – Read JSON data

```python
df = pd.read_json("employees.json")

print(df)
```

For JSON records held in a Python string:

```python
import pandas as pd

json_data = 