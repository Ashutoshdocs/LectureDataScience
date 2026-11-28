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

json_data = """
[
    {"Name": "Amit", "Salary": 60000},
    {"Name": "Neha", "Salary": 55000}
]
"""

df = pd.read_json(json_data)

print(df)
```

For nested JSON, `pd.json_normalize()` can flatten nested records into tabular columns.

```python
records = [
    {"name": "Amit", "department": {"name": "IT", "floor": 2}},
    {"name": "Neha", "department": {"name": "HR", "floor": 1}}
]

df = pd.json_normalize(records)

print(df)
```

---

# Part 5 – Select rows and columns

## Chapter 13 – Select a single column

```python
print(df["Name"])
```

Returns a Series.

## Chapter 14 – Select multiple columns

```python
print(df[["Name", "Salary"]])
```

Returns a DataFrame.

## Chapter 15 – Select rows using `loc`

`loc` selects by index label.

```python
print(df.loc[0])
```

Select a range of labels:

```python
print(df.loc[0:2])
```

With the default integer index, label slicing with `loc` includes the ending label when it exists.

Select rows and columns together:

```python
print(df.loc[0:2, ["Name", "Salary"]])
```

## Chapter 16 – Select rows using `iloc`

`iloc` selects by integer position.

```python
print(df.iloc[0])
```

Select the first three rows:

```python
print(df.iloc[0:3])
```

Select first three rows and first two columns:

```python
print(df.iloc[0:3, 0:2])
```

With `iloc`, the stop position is excluded, like normal Python slicing.

## Chapter 17 – `at` and `iat`

Use `at` to access one value by row and column labels:

```python
print(df.at[0, "Name"])
```

Use `iat` to access one value by integer positions:

```python
print(df.iat[0, 1])
```

These are useful for scalar access.

---

# Part 6 – Filter and sort data

## Chapter 18 – Filter using one condition

```python
it_employees = df[df["Department"] == "IT"]

print(it_employees)
```

This returns rows where the department is IT.

## Chapter 19 – Filter using multiple conditions

Employees in IT with salary greater than 65000:

```python
result = df[
    (df["Department"] == "IT") &
    (df["Salary"] > 65000)
]

print(result)
```

Use `&` for element-wise AND and `|` for element-wise OR. Put each condition in parentheses.

### OR condition

```python
result = df[
    (df["City"] == "Pune") |
    (df["City"] == "Delhi")
]

print(result)
```

### NOT condition

```python
result = df[df["Department"] != "HR"]

print(result)
```

### Use `isin()`

```python
result = df[df["Department"].isin(["IT", "Finance"])]

print(result)
```

### Use `between()`

```python
result = df[df["Salary"].between(55000, 70000)]

print(result)
```

By default, `between()` includes both endpoints.

## Chapter 20 – Sort data

Sort by one column:

```python
sorted_df = df.sort_values(by="Salary")

print(sorted_df)
```

Descending order:

```python
sorted_df = df.sort_values(
    by="Salary",
    ascending=False
)

print(sorted_df)
```

Sort by multiple columns:

```python
sorted_df = df.sort_values(
    by=["Department", "Salary"],
    ascending=[True, False]
)

print(sorted_df)
```

Sort by index:

```python
print(df.sort_index())
```

---

# Part 7 – Add, update, and remove data

## Chapter 21 – Add a new column

```python
df["Bonus"] = df["Salary"] * 0.10

print(df)
```

A new column is calculated for each row.

## Chapter 22 – Create a column using conditions

```python
df["SalaryLevel"] = "Standard"

df.loc[df["Salary"] >= 70000, "SalaryLevel"] = "High"

print(df[["Name", "Salary", "SalaryLevel"]])
```

A vectorized alternative:

```python
import numpy as np

df["SalaryLevel"] = np.where(
    df["Salary"] >= 70000,
    "High",
    "Standard"
)
```

## Chapter 23 – Update existing values

```python
df.loc[df["Name"] == "Amit", "City"] = "Pune"
```

Update a scalar using `at`:

```python
df.at[0, "Salary"] = 62000
```

## Chapter 24 – Rename columns

```python
df = df.rename(
    columns={
        "Name": "EmployeeName",
        "Salary": "MonthlySalary"
    }
)

print(df.columns)
```

## Chapter 25 – Drop columns and rows

Drop a column:

```python
df = df.drop(columns=["Bonus"])
```

Drop multiple columns:

```python
df = df.drop(columns=["Age", "City"])
```

Drop rows by index label:

```python
df = df.drop(index=[0, 2])
```

`drop()` returns a new DataFrame by default. Assign the result if you want to keep the change.

## Chapter 26 – Insert a column

```python
df.insert(
    1,
    "Country",
    "India"
)

print(df)
```

The first argument is the insertion position.

---

# Part 8 – Missing values and data cleaning

## Chapter 27 – What are missing values?

Real datasets are often incomplete. A value may be missing because:

- A person did not provide it.
- A sensor failed.
- A system did not collect it.
- A data integration process lost it.
- The value is not applicable.

Pandas commonly represents missing data with values such as `NaN`, `None`, or `pd.NA`, depending on the column dtype.

Create a sample:

```python
import numpy as np
import pandas as pd

data = {
    "Name": ["Amit", "Neha", "Ravi", "Sara", "John"],
    "Age": [25, np.nan, 30, 28, np.nan],
    "Salary": [60000, 55000, np.nan, 65000, 70000],
    "Department": ["IT", "HR", "IT", None, "Finance"]
}

df = pd.DataFrame(data)

print(df)
```

## Chapter 28 – Detect missing values

```python
print(df.isna())
```

Count missing values per column:

```python
print(df.isna().sum())
```

Check whether any values are missing:

```python
print(df.isna().any())
```

Check rows containing at least one missing value:

```python
print(df[df.isna().any(axis=1)])
```

`isnull()` is an alias for `isna()`.

## Chapter 29 – Remove missing values with `dropna()`

Remove rows containing any missing value:

```python
cleaned = df.dropna()

print(cleaned)
```

Remove columns containing missing values:

```python
cleaned = df.dropna(axis=1)
```

Require at least three non-missing values in a row:

```python
cleaned = df.dropna(thresh=3)
```

Use `subset` to check selected columns:

```python
cleaned = df.dropna(subset=["Name", "Salary"])
```

Do not remove missing rows automatically in every project. First understand why the values are missing and whether dropping those records could bias the analysis.

## Chapter 30 – Fill missing values with `fillna()`

Fill a numeric column with its mean:

```python
df["Age"] = df["Age"].fillna(df["Age"].mean())
```

Fill a numeric column with its median:

```python
df["Salary"] = df["Salary"].fillna(df["Salary"].median())
```

Fill a categorical column with a label:

```python
df["Department"] = df["Department"].fillna("Unknown")
```

Fill different columns using a dictionary:

```python
df = df.fillna({
    "Age": df["Age"].median(),
    "Salary": df["Salary"].median(),
    "Department": "Unknown"
})
```

### Forward fill and backward fill

```python
df = df.ffill()
```

Forward fill uses the previous valid value. Backward fill uses the next valid value:

```python
df = df.bfill()
```

These methods are most meaningful when the row order has a valid interpretation, such as ordered time-series records.

## Chapter 31 – Duplicate records

Create duplicate rows:

```python
data = {
    "EmployeeID": [101, 102, 103, 102],
    "Name": ["Amit", "Neha", "Ravi", "Neha"],
    "Department": ["IT", "HR", "IT", "HR"]
}

df = pd.DataFrame(data)
```

Find duplicate rows:

```python
print(df.duplicated())
```

Count duplicates:

```python
print(df.duplicated().sum())
```

Remove duplicate rows:

```python
df = df.drop_duplicates()
```

Check duplicates based on selected columns:

```python
print(df.duplicated(subset=["EmployeeID"]))
```

Keep the last occurrence:

```python
df = df.drop_duplicates(
    subset=["EmployeeID"],
    keep="last"
)
```

Always decide which record should be retained. Duplicate-looking rows may represent legitimate repeated events.

---

# Part 9 – Data types and conversion

## Chapter 32 – Inspect data types

```python
print(df.dtypes)
```

Common pandas dtypes include:

- `int64`
- `float64`
- `bool`
- `object`
- `string`
- `category`
- `datetime64[ns]`

The exact dtype can vary with the values, pandas version, and dtype backend.

## Chapter 33 – Convert data types

Convert a column to integer:

```python
df["Age"] = df["Age"].astype("int64")
```

Only do this if the values are valid integers and do not contain missing values that the chosen dtype cannot represent.

Use nullable integer dtype when missing values must be retained:

```python
df["Age"] = df["Age"].astype("Int64")
```

Convert to string:

```python
df["EmployeeID"] = df["EmployeeID"].astype("string")
```

Convert to numeric safely:

```python
df["Salary"] = pd.to_numeric(
    df["Salary"],
    errors="coerce"
)
```

With `errors="coerce"`, values that cannot be parsed become missing values.

## Chapter 34 – Category data type

A category is useful for columns containing a limited set of repeated labels.

```python
df["Department"] = df["Department"].astype("category")

print(df["Department"].dtype)
```

Examples include department, city, product category, and status.

Use categories when they suit the data and operations. They are not automatically better for every string column.

---

# Part 10 – String operations

## Chapter 35 – Work with text columns using `.str`

Pandas provides vectorized string operations through the `.str` accessor.

```python
import pandas as pd

df = pd.DataFrame({
    "Name": [" amit ", "NEHA", "Ravi Kumar", "sara"]
})
```

Convert to lowercase:

```python
df["NameLower"] = df["Name"].str.lower()
```

Convert to uppercase:

```python
df["NameUpper"] = df["Name"].str.upper()
```

Remove leading and trailing spaces:

```python
df["NameClean"] = df["Name"].str.strip()
```

Replace text:

```python
df["NameClean"] = df["NameClean"].str.replace(
    "Kumar",
    "K",
    regex=False
)
```

Check whether a value contains text:

```python
mask = df["NameClean"].str.contains(
    "amit",
    case=False,
    na=False
)

print(df[mask])
```

Other useful methods:

```python
df["Name"].str.len()
df["Name"].str.startswith("A")
df["Name"].str.endswith("a")
df["Name"].str.split(" ")
```

### Extract text using a regular expression

```python
emails = pd.Series([
    "amit@example.com",
    "neha@example.org",
    "invalid-email"
])

domains = emails.str.extract(r"@(.+)$")

print(domains)
```

Regular expressions are powerful but should be introduced gradually. Test patterns against valid, invalid, and missing values.

---

# Part 11 – Date and time operations

## Chapter 36 – Convert text to datetime

```python
import pandas as pd

df = pd.DataFrame({
    "OrderDate": [
        "2026-01-10",
        "2026-02-15",
        "2026-03-20"
    ]
})

df["OrderDate"] = pd.to_datetime(df["OrderDate"])

print(df)
print(df.dtypes)
```

For values that may not be valid dates:

```python
df["OrderDate"] = pd.to_datetime(
    df["OrderDate"],
    errors="coerce"
)
```

Invalid values become `NaT`, pandas' missing datetime value.

## Chapter 37 – Extract date parts

```python
df["Year"] = df["OrderDate"].dt.year
df["Month"] = df["OrderDate"].dt.month
df["Day"] = df["OrderDate"].dt.day
df["DayName"] = df["OrderDate"].dt.day_name()

print(df)
```

Other useful datetime properties include:

```python
df["OrderDate"].dt.quarter
df["OrderDate"].dt.dayofweek
df["OrderDate"].dt.is_month_end
df["OrderDate"].dt.is_month_start
```

## Chapter 38 – Filter by date

```python
start_date = "2026-02-01"
end_date = "2026-02-28"

result = df[
    df["OrderDate"].between(start_date, end_date)
]

print(result)
```

For timezone-aware timestamps, understand the source timezone and convert consistently before comparing values.

## Chapter 39 – Date differences

```python
df["DeliveryDate"] = pd.to_datetime([
    "2026-01-13",
    "2026-02-18",
    "2026-03-25"
])

df["DeliveryDays"] = (
    df["DeliveryDate"] - df["OrderDate"]
).dt.days

print(df)
```

---

# Part 12 – Grouping and aggregation

## Chapter 40 – What is `groupby()`?

`groupby()` follows the split–apply–combine pattern:

1. Split rows into groups based on one or more keys.
2. Apply a calculation to each group.
3. Combine the results.

Example:

```python
import pandas as pd

df = pd.DataFrame({
    "Department": ["IT", "HR", "IT", "Finance", "HR", "IT"],
    "Employee": ["Amit", "Neha", "Ravi", "Sara", "Priya", "John"],
    "Salary": [60000, 55000, 72000, 65000, 58000, 80000]
})
```

Average salary by department:

```python
result = df.groupby("Department")["Salary"].mean()

print(result)
```

Total salary by department:

```python
result = df.groupby("Department")["Salary"].sum()

print(result)
```

Employee count by department:

```python
result = df.groupby("Department")["Employee"].count()

print(result)
```

## Chapter 41 – Group by multiple columns

```python
df = pd.DataFrame({
    "Department": ["IT", "IT", "HR", "HR", "IT"],
    "City": ["Pune", "Mumbai", "Pune", "Mumbai", "Pune"],
    "Salary": [60000, 70000, 50000, 55000, 80000]
})

result = df.groupby(
    ["Department", "City"]
)["Salary"].mean()

print(result)
```

The result uses a MultiIndex representing the grouping keys.

## Chapter 42 – Multiple aggregations with `agg()`

```python
result = df.groupby("Department").agg(
    AverageSalary=("Salary", "mean"),
    MaximumSalary=("Salary", "max"),
    MinimumSalary=("Salary", "min"),
    TotalSalary=("Salary", "sum"),
    EmployeeCount=("Salary", "count")
)

print(result)
```

Named aggregation gives the output columns clear names.

## Chapter 43 – `size()` versus `count()`

- `size()` counts rows in each group.
- `count()` counts non-missing values in a selected column.

```python
grouped = df.groupby("Department")

print(grouped.size())
print(grouped["Salary"].count())
```

These may differ when a group contains missing values in the selected column.

## Chapter 44 – Transform

`transform()` returns a result aligned to the original rows.

```python
df["DepartmentAverage"] = (
    df.groupby("Department")["Salary"]
      .transform("mean")
)

print(df)
```

This is useful when each row needs a group-level statistic.

## Chapter 45 – Filter groups

```python
result = df.groupby("Department").filter(
    lambda group: len(group) >= 2
)

print(result)
```

This keeps rows belonging to groups with at least two records.

---

# Part 13 – Combining datasets

## Chapter 46 – Why do we combine datasets?

Business information is often split across files or tables.

Example:

**Employees table**

| EmployeeID | Name | DepartmentID |
|---:|---|---:|
| 101 | Amit | 1 |
| 102 | Neha | 2 |
| 103 | Ravi | 1 |

**Departments table**

| DepartmentID | DepartmentName |
|---:|---|
| 1 | IT |
| 2 | HR |

We can combine these tables using a common key.

## Chapter 47 – Merge DataFrames

```python
employees = pd.DataFrame({
    "EmployeeID": [101, 102, 103],
    "Name": ["Amit", "Neha", "Ravi"],
    "DepartmentID": [1, 2, 1]
})

departments = pd.DataFrame({
    "DepartmentID": [1, 2],
    "DepartmentName": ["IT", "HR"]
})

result = pd.merge(
    employees,
    departments,
    on="DepartmentID",
    how="inner"
)

print(result)
```

### Join types

| Type | Meaning |
|---|---|
| `inner` | Keep matching keys from both DataFrames |
| `left` | Keep all left rows and matching right rows |
| `right` | Keep all right rows and matching left rows |
| `outer` | Keep all keys from both sides |

### Left merge

```python
result = pd.merge(
    employees,
    departments,
    on="DepartmentID",
    how="left"
)
```

### Merge on differently named columns

```python
result = pd.merge(
    employees,
    departments,
    left_on="DepartmentID",
    right_on="DepartmentID",
    how="left"
)
```

For different key names, change `left_on` and `right_on` to the actual column names.

### Validate merge relationships

Unexpected duplicate keys can multiply rows in a merge. Where appropriate, use `validate`:

```python
result = pd.merge(
    employees,
    departments,
    on="DepartmentID",
    how="left",
    validate="many_to_one"
)
```

This checks that many employee rows may refer to one department row.

## Chapter 48 – Concatenate DataFrames

`concat()` stacks or places DataFrames along an axis.

### Stack rows

```python
january = pd.DataFrame({
    "Employee": ["Amit", "Neha"],
    "Salary": [60000, 55000]
})

february = pd.DataFrame({
    "Employee": ["Ravi", "Sara"],
    "Salary": [72000, 65000]
})

combined = pd.concat(
    [january, february],
    ignore_index=True
)

print(combined)
```

### Combine columns

```python
names = pd.DataFrame({"Name": ["Amit", "Neha"]})
salaries = pd.DataFrame({"Salary": [60000, 55000]})

combined = pd.concat(
    [names, salaries],
    axis=1
)

print(combined)
```

When concatenating columns, pandas aligns by index labels. Make sure the indexes represent corresponding records before combining.

## Chapter 49 – Join using index

```python
employees = pd.DataFrame(
    {"Name": ["Amit", "Neha"]},
    index=[101, 102]
)

salaries = pd.DataFrame(
    {"Salary": [60000, 55000]},
    index=[101, 102]
)

result = employees.join(salaries)

print(result)
```

`join()` is commonly used for index-based combinations.

---

# Part 14 – Reshape data

## Chapter 50 – Pivot

`pivot()` reshapes data from long form to wide form. It requires each index/column combination to identify a single value.

```python
df = pd.DataFrame({
    "Month": ["Jan", "Jan", "Feb", "Feb"],
    "Product": ["Laptop", "Mobile", "Laptop", "Mobile"],
    "Sales": [100, 200, 120, 220]
})

result = df.pivot(
    index="Month",
    columns="Product",
    values="Sales"
)

print(result)
```

If there are duplicate combinations, `pivot()` raises an error. Use `pivot_table()` when aggregation is required.

## Chapter 51 – Pivot table

```python
df = pd.DataFrame({
    "Month": ["Jan", "Jan", "Jan", "Feb", "Feb"],
    "Product": ["Laptop", "Laptop", "Mobile", "Laptop", "Mobile"],
    "Sales": [100, 150, 200, 120, 220]
})

result = pd.pivot_table(
    df,
    index="Month",
    columns="Product",
    values="Sales",
    aggfunc="sum",
    fill_value=0
)

print(result)
```

## Chapter 52 – Melt

`melt()` changes wide data into long form.

```python
wide = pd.DataFrame({
    "Product": ["Laptop", "Mobile"],
    "January": [100, 200],
    "February": [120, 220]
})

long = pd.melt(
    wide,
    id_vars=["Product"],
    var_name="Month",
    value_name="Sales"
)

print(long)
```

## Chapter 53 – Crosstab

`crosstab()` creates a frequency table.

```python
df = pd.DataFrame({
    "Department": ["IT", "HR", "IT", "Finance", "HR", "IT"],
    "City": ["Pune", "Mumbai", "Mumbai", "Delhi", "Pune", "Pune"]
})

result = pd.crosstab(
    df["Department"],
    df["City"]
)

print(result)
```

---

# Part 15 – Apply, map, and vectorized operations

## Chapter 54 – Vectorized column calculations

Prefer direct column operations when possible.

```python
df = pd.DataFrame({
    "Price": [100, 200, 300],
    "Quantity": [2, 3, 4]
})

df["Total"] = df["Price"] * df["Quantity"]

print(df)
```

This is usually clearer and often more efficient than iterating row by row in Python.

## Chapter 55 – `map()` on a Series

Use `map()` to replace or transform individual Series values.

```python
df = pd.DataFrame({
    "DepartmentCode": ["IT", "HR", "FN", "IT"]
})

department_map = {
    "IT": "Information Technology",
    "HR": "Human Resources",
    "FN": "Finance"
}

df["Department"] = df["DepartmentCode"].map(department_map)

print(df)
```

Unmapped values become missing unless another mapping strategy is used.

## Chapter 56 – `replace()`

```python
df = pd.DataFrame({
    "Status": ["Y", "N", "Y", "N"]
})

df["Status"] = df["Status"].replace({
    "Y": "Active",
    "N": "Inactive"
})

print(df)
```

## Chapter 57 – `apply()`

`apply()` applies a function along a Series or DataFrame axis.

Series example:

```python
marks = pd.Series([35, 65, 85, 95])

def grade_mark(mark):
    if mark >= 90:
        return "A"
    elif mark >= 75:
        return "B"
    elif mark >= 50:
        return "C"
    else:
        return "F"

grades = marks.apply(grade_mark)

print(grades)
```

DataFrame row example:

```python
df = pd.DataFrame({
    "Math": [80, 90, 70],
    "Science": [85, 88, 75]
})

df["Average"] = df.apply(
    lambda row: (row["Math"] + row["Science"]) / 2,
    axis=1
)

print(df)
```

For simple numerical expressions, prefer vectorized operations such as:

```python
df["Average"] = (df["Math"] + df["Science"]) / 2
```

Use `apply()` when the operation is genuinely easier to express as a function and a vectorized alternative is not practical.

---

# Part 16 – Time-series analysis

## Chapter 58 – Set a datetime index

```python
import pandas as pd

df = pd.DataFrame({
    "Date": pd.date_range(
        start="2026-01-01",
        periods=6,
        freq="D"
    ),
    "Sales": [100, 120, 90, 150, 170, 160]
})

df = df.set_index("Date")

print(df)
```

## Chapter 59 – Select a date range

```python
print(df.loc["2026-01-02":"2026-01-04"])
```

Datetime indexing is especially useful when the index is sorted and contains datetime values.

## Chapter 60 – Resample data

Resampling changes the frequency of time-series data.

```python
daily = pd.DataFrame({
    "Date": pd.date_range("2026-01-01", periods=10, freq="D"),
    "Sales": [10, 20, 15, 25, 30, 20, 35, 40, 25, 30]
})

daily = daily.set_index("Date")

weekly = daily["Sales"].resample("W").sum()

print(weekly)
```

Resampling requires a datetime-like index or an explicitly selected datetime column.

## Chapter 61 – Rolling calculations

A rolling mean calculates a moving average over a window.

```python
df["MovingAverage"] = df["Sales"].rolling(window=3).mean()

print(df)
```

The first two values are missing because a full three-observation window is not yet available.

## Chapter 62 – `shift()` and `diff()`

```python
df["PreviousDaySales"] = df["Sales"].shift(1)
df["Change"] = df["Sales"].diff()

print(df)
```

- `shift(1)` moves values down by one row.
- `diff()` calculates the difference from the previous row by default.

These are useful for day-over-day or month-over-month comparisons.

---

# Part 17 – Export and save data

## Chapter 63 – Write CSV

```python
df.to_csv(
    "cleaned_data.csv",
    index=False
)
```

`index=False` prevents the DataFrame index from being written as an extra CSV column.

## Chapter 64 – Write Excel

```python
df.to_excel(
    "cleaned_data.xlsx",
    sheet_name="Report",
    index=False
)
```

This generally requires an Excel-writing engine such as `openpyxl` for `.xlsx` files.

## Chapter 65 – Write multiple Excel sheets

```python
with pd.ExcelWriter("business_report.xlsx") as writer:
    df.to_excel(
        writer,
        sheet_name="Data",
        index=False
    )

    summary = df.describe()
    summary.to_excel(
        writer,
        sheet_name="Summary"
    )
```

## Chapter 66 – Other useful formats

Parquet:

```bash
python -m pip install pyarrow
```

```python
df.to_parquet("data.parquet", index=False)
loaded = pd.read_parquet("data.parquet")
```

JSON:

```python
df.to_json("data.json", orient="records", indent=2)
```

Pick a format based on the consumer, data types, file size, and interoperability requirements.

---

# Part 18 – Data analysis workflow and best practices

## Chapter 67 – A reusable data-cleaning workflow

A practical workflow often looks like this:

1. Read the source file.
2. Inspect shape, columns, dtypes, and sample records.
3. Check missing values and duplicates.
4. Validate identifiers and business rules.
5. Convert columns to appropriate data types.
6. Clean text and date columns.
7. Handle missing and invalid values intentionally.
8. Create derived columns.
9. Filter and group records.
10. Validate totals and row counts.
11. Export the cleaned dataset and summary.

Example template:

```python
import pandas as pd

# 1. Read the source data.
df = pd.read_csv("input.csv")

# 2. Inspect the data.
print(df.head())
print(df.info())
print(df.isna().sum())

# 3. Remove exact duplicate rows, if duplicates are not valid events.
df = df.drop_duplicates()

# 4. Clean text columns.
if "Name" in df.columns:
    df["Name"] = df["Name"].astype("string").str.strip()

# 5. Convert a numeric column safely.
if "Salary" in df.columns:
    df["Salary"] = pd.to_numeric(
        df["Salary"],
        errors="coerce"
    )

# 6. Create a summary if the required column exists.
if "Department" in df.columns and "Salary" in df.columns:
    summary = df.groupby("Department").agg(
        AverageSalary=("Salary", "mean"),
        EmployeeCount=("Salary", "count")
    )
    print(summary)

# 7. Save the cleaned data.
df.to_csv("cleaned_output.csv", index=False)
```

This is a teaching template. Real cleaning decisions should be based on the actual meaning and quality rules of the dataset.

## Chapter 68 – Performance and memory best practices

- Read only the columns you need with `usecols`.
- Specify data types when the source format and values are understood.
- Use vectorized column operations instead of Python row loops where practical.
- Avoid repeatedly concatenating one row at a time.
- Use `category` for suitable low-cardinality repeated labels.
- Use chunked CSV reading for files too large to comfortably fit in memory.
- Check `memory_usage(deep=True)` when investigating DataFrame memory.
- Avoid unnecessary copies of large DataFrames.
- Validate joins to avoid accidental row multiplication.
- Measure performance on representative data.

### Read a large CSV in chunks

```python
total_rows = 0

for chunk in pd.read_csv(
    "large_file.csv",
    chunksize=100_000
):
    total_rows += len(chunk)

print("Total rows:", total_rows)
```

Each chunk is a DataFrame. Process or aggregate each chunk rather than collecting every chunk in memory if the file is too large.

### Check memory usage

```python
print(df.memory_usage(deep=True))
print("Total bytes:", df.memory_usage(deep=True).sum())
```

---

# Part 19 – Project 1: Employee Data Analysis

<badge color="success">Beginner to intermediate</badge>

## Project objective

Build an employee analysis program using pandas.

The program will:

- Read employee records from a CSV file.
- Inspect the dataset.
- Clean text values.
- Handle missing values.
- Remove duplicate employee IDs using a defined rule.
- Convert salary and joining date columns.
- Calculate experience in years.
- Create salary bands.
- Filter employees by department, city, and salary.
- Calculate department-wise statistics.
- Find the highest-paid employee.
- Export a cleaned employee file and summary report.

## Step 1 – Create `employees.csv`

Save this file inside `project_1_employee_analysis/`.

```csv
EmployeeID,Name,Department,Age,Salary,City,JoiningDate
101,Amit,IT,25,60000,Pune,2022-01-10
102,Neha,HR,28,55000,Mumbai,2021-05-15
103,Ravi,IT,30,72000,Pune,2020-03-20
104,Sara,Finance,27,65000,Delhi,2023-02-01
105,Priya,HR,29,58000,Mumbai,2022-07-12
106,John,IT,32,80000,Pune,2019-11-05
107,Meera,Finance,,62000,Delhi,2021-09-18
108,Arun,IT,26,,Pune,2024-01-08
109, Kiran ,HR,31,59000,Mumbai,2020-06-11
109, Kiran ,HR,31,59000,Mumbai,2020-06-11
110,David,Sales,35,70000,Chennai,2018-04-25
```

This dataset intentionally includes:
- One missing age.
- One missing salary.
- Extra spaces around a name.
- A duplicated employee record.

## Step 2 – Read and inspect

Create `main.py`:

```python
import pandas as pd

df = pd.read_csv("employees.csv")

print("First five rows:")
print(df.head())

print("\nDataset information:")
df.info()

print("\nShape:")
print(df.shape)

print("\nMissing values:")
print(df.isna().sum())

print("\nDuplicate rows:")
print(df.duplicated().sum())
```

## Step 3 – Clean column values

```python
# Remove leading and trailing spaces from names.
df["Name"] = df["Name"].astype("string").str.strip()

# Normalize department and city labels.
df["Department"] = df["Department"].astype("string").str.strip()
df["City"] = df["City"].astype("string").str.strip()
```

## Step 4 – Convert data types

```python
df["Age"] = pd.to_numeric(df["Age"], errors="coerce")
df["Salary"] = pd.to_numeric(df["Salary"], errors="coerce")

df["JoiningDate"] = pd.to_datetime(
    df["JoiningDate"],
    errors="coerce"
)
```

## Step 5 – Remove duplicate employee records

For this teaching dataset, EmployeeID identifies one employee. Keep the first record for each ID:

```python
df = df.drop_duplicates(
    subset=["EmployeeID"],
    keep="first"
)
```

In a real HR system, investigate conflicting duplicate records before deciding which record to retain.

## Step 6 – Handle missing values

For this project, use the median age and median salary:

```python
df["Age"] = df["Age"].fillna(df["Age"].median())
df["Salary"] = df["Salary"].fillna(df["Salary"].median())
```

This is a teaching choice. In a real HR dataset, missing salary or age may need to be investigated rather than automatically imputed.

## Step 7 – Create derived columns

```python
# Extract the joining year.
df["JoiningYear"] = df["JoiningDate"].dt.year

# Calculate completed years of service as of a fixed teaching date.
as_of_date = pd.Timestamp("2026-01-01")

df["ExperienceYears"] = (
    (as_of_date - df["JoiningDate"]).dt.days / 365.25
).clip(lower=0).astype("float").round(1)

# Create a salary category.
df["SalaryBand"] = pd.cut(
    df["Salary"],
    bins=[0, 60000, 75000, float("inf")],
    labels=["Entry", "Mid", "Senior"],
    right=True
)

print(df)
```

The fixed date makes classroom output reproducible. In a live HR report, use the required reporting date and consider employment start/end dates and policy rules.

## Step 8 – Filter employees

IT employees:

```python
it_employees = df[df["Department"] == "IT"]

print(it_employees)
```

Employees earning more than 65000:

```python
high_salary = df[df["Salary"] > 65000]

print(high_salary)
```

Employees in Pune with salary above 65000:

```python
result = df[
    (df["City"] == "Pune") &
    (df["Salary"] > 65000)
]

print(result)
```

## Step 9 – Department-wise analysis

```python
department_summary = df.groupby("Department").agg(
    EmployeeCount=("EmployeeID", "count"),
    AverageSalary=("Salary", "mean"),
    MinimumSalary=("Salary", "min"),
    MaximumSalary=("Salary", "max"),
    AverageAge=("Age", "mean")
)

print(department_summary)
```

## Step 10 – Find top-paid employees

```python
top_employees = df.sort_values(
    by="Salary",
    ascending=False
).head(3)

print(top_employees[["Name", "Department", "Salary"]])
```

## Step 11 – City-wise employee count

```python
city_summary = df.groupby("City").agg(
    EmployeeCount=("EmployeeID", "count"),
    AverageSalary=("Salary", "mean")
)

print(city_summary)
```

## Step 12 – Export results

```python
df.to_csv("cleaned_employees.csv", index=False)

with pd.ExcelWriter("employee_report.xlsx") as writer:
    df.to_excel(
        writer,
        sheet_name="Cleaned Employees",
        index=False
    )

    department_summary.to_excel(
        writer,
        sheet_name="Department Summary"
    )

    city_summary.to_excel(
        writer,
        sheet_name="City Summary"
    )

print("Reports created successfully.")
```

## Project 1 – Concepts covered

| Pandas concept | Project use |
|---|---|
| `read_csv()` | Read employee records |
| `head()`, `info()` | Inspect data |
| `isna()` | Find missing values |
| `drop_duplicates()` | Remove duplicate employee IDs |
| `.str.strip()` | Clean names and labels |
| `to_numeric()` | Convert salary and age |
| `to_datetime()` | Convert joining date |
| `fillna()` | Handle missing values |
| `.dt` | Extract date information |
| `pd.cut()` | Create salary bands |
| Boolean filtering | Select employees |
| `groupby()` and `agg()` | Department and city summaries |
| `sort_values()` | Find top-paid employees |
| `to_csv()`, `to_excel()` | Export results |

## Project 1 – Student challenges

1. Add a `Gender` column and calculate department-wise counts.
2. Find employees with more than five years of experience.
3. Calculate average salary by city and department.
4. Find the department with the highest average salary.
5. Find employees whose salary is above their department average.
6. Create age groups using `pd.cut()`.
7. Calculate the percentage of employees in each department.
8. Create a report containing only IT and Finance employees.
9. Export one Excel sheet per department.
10. Add a validation that EmployeeID must be unique after cleaning.

---

# Part 20 – Project 2: Retail Sales Analysis

<badge color="success">Intermediate to advanced</badge>

## Project objective

Build a retail sales analysis system using multiple CSV files.

The program will:

- Read order and product data.
- Inspect and clean both datasets.
- Convert dates and numeric columns.
- Merge order records with product information.
- Calculate revenue and profit.
- Analyze product and category performance.
- Calculate monthly sales.
- Find top products and regions.
- Create a pivot table.
- Export a multi-sheet Excel report.

## Step 1 – Create `products.csv`

Save inside `project_2_retail_sales_analysis/`.

```csv
ProductID,ProductName,Category,UnitCost
P101,Laptop,Electronics,40000
P102,Mobile,Electronics,12000
P103,Desk,Furniture,5000
P104,Chair,Furniture,2000
P105,Headphones,Accessories,800
P106,Keyboard,Accessories,500
```

## Step 2 – Create `orders.csv`

```csv
OrderID,OrderDate,ProductID,Region,Quantity,UnitPrice,Discount
5001,2026-01-05,P101,West,2,55000,0.05
5002,2026-01-08,P102,South,5,18000,0.10
5003,2026-01-12,P103,North,3,8000,0.00
5004,2026-02-02,P104,West,10,3500,0.05
5005,2026-02-10,P105,South,8,1500,0.00
5006,2026-02-15,P106,East,12,1000,0.05
5007,2026-03-01,P101,North,1,56000,0.00
5008,2026-03-07,P102,West,4,17500,0.05
5009,2026-03-18,P103,South,6,8200,0.10
5010,2026-03-22,P105,East,10,1600,0.05
5011,2026-04-03,P104,North,7,3600,0.00
5012,2026-04-14,P106,West,15,950,0.00
```

## Step 3 – Read both datasets

Create `main.py`:

```python
import pandas as pd

orders = pd.read_csv("orders.csv")
products = pd.read_csv("products.csv")

print("Orders:")
print(orders.head())

print("\nProducts:")
print(products.head())

print("\nOrders information:")
orders.info()

print("\nProducts information:")
products.info()
```

## Step 4 – Clean and validate the data

```python
# Remove exact duplicate records.
orders = orders.drop_duplicates()
products = products.drop_duplicates()

# Convert the order date.
orders["OrderDate"] = pd.to_datetime(
    orders["OrderDate"],
    errors="coerce"
)

# Convert numeric columns.
numeric_order_columns = [
    "Quantity",
    "UnitPrice",
    "Discount"
]

for column in numeric_order_columns:
    orders[column] = pd.to_numeric(
        orders[column],
        errors="coerce"
    )

products["UnitCost"] = pd.to_numeric(
    products["UnitCost"],
    errors="coerce"
)

# Check missing values.
print(orders.isna().sum())
print(products.isna().sum())

# Check that product identifiers are unique in the product table.
print("Duplicate product IDs:", products["ProductID"].duplicated().sum())
```

Do not automatically fill missing order quantities, prices, or costs without a business rule. For this sample dataset, the provided values are complete.

## Step 5 – Merge orders with products

```python
sales = pd.merge(
    orders,
    products,
    on="ProductID",
    how="left",
    validate="many_to_one"
)

print(sales)
```

Why `many_to_one`?

- Many order rows can refer to one product.
- Each ProductID should identify one row in the product table.

Check unmatched products:

```python
unmatched = sales[sales["ProductName"].isna()]

print("Unmatched order rows:")
print(unmatched)
```

## Step 6 – Calculate revenue

For this project:

```text
GrossSales = Quantity × UnitPrice

DiscountAmount = GrossSales × Discount

NetSales = GrossSales − DiscountAmount
```

Code:

```python
sales["GrossSales"] = (
    sales["Quantity"] * sales["UnitPrice"]
)

sales["DiscountAmount"] = (
    sales["GrossSales"] * sales["Discount"]
)

sales["NetSales"] = (
    sales["GrossSales"] - sales["DiscountAmount"]
)

print(sales[
    ["OrderID", "ProductName", "GrossSales", "DiscountAmount", "NetSales"]
])
```

## Step 7 – Calculate cost and profit

```python
sales["TotalCost"] = (
    sales["Quantity"] * sales["UnitCost"]
)

sales["Profit"] = (
    sales["NetSales"] - sales["TotalCost"]
)

sales["ProfitMarginPercent"] = (
    sales["Profit"] / sales["NetSales"] * 100
)

print(sales[
    ["ProductName", "NetSales", "TotalCost", "Profit", "ProfitMarginPercent"]
])
```

For this teaching dataset, discounts are applied to selling revenue and costs are not discounted. Real accounting definitions may require additional rules for taxes, shipping, returns, and other costs.

## Step 8 – Overall business summary

```python
total_orders = sales["OrderID"].nunique()
total_units = sales["Quantity"].sum()
total_revenue = sales["NetSales"].sum()
total_profit = sales["Profit"].sum()

print("Total orders:", total_orders)
print("Total units sold:", total_units)
print("Total net sales:", round(total_revenue, 2))
print("Total profit:", round(total_profit, 2))
```

## Step 9 – Category-wise performance

```python
category_summary = sales.groupby("Category").agg(
    UnitsSold=("Quantity", "sum"),
    Revenue=("NetSales", "sum"),
    TotalCost=("TotalCost", "sum"),
    Profit=("Profit", "sum"),
    OrderCount=("OrderID", "nunique")
)

category_summary["ProfitMarginPercent"] = (
    category_summary["Profit"] /
    category_summary["Revenue"] * 100
)

print(category_summary)
```

## Step 10 – Product-wise performance

```python
product_summary = sales.groupby(
    ["ProductID", "ProductName"]
).agg(
    UnitsSold=("Quantity", "sum"),
    Revenue=("NetSales", "sum"),
    Profit=("Profit", "sum")
).sort_values(
    by="Revenue",
    ascending=False
)

print(product_summary)
```

## Step 11 – Region-wise sales

```python
region_summary = sales.groupby("Region").agg(
    Revenue=("NetSales", "sum"),
    Profit=("Profit", "sum"),
    UnitsSold=("Quantity", "sum")
).sort_values(
    by="Revenue",
    ascending=False
)

print(region_summary)
```

## Step 12 – Monthly sales analysis

```python
sales["YearMonth"] = sales["OrderDate"].dt.to_period("M")

monthly_summary = sales.groupby("YearMonth").agg(
    Revenue=("NetSales", "sum"),
    Profit=("Profit", "sum"),
    UnitsSold=("Quantity", "sum")
)

print(monthly_summary)
```

If you need a timestamp rather than a Period index, convert the period values to timestamps as appropriate for your reporting convention.

## Step 13 – Find top products

```python
top_products = product_summary.head(3)

print("Top three products:")
print(top_products)
```

## Step 14 – Pivot table

```python
region_category = pd.pivot_table(
    sales,
    index="Region",
    columns="Category",
    values="NetSales",
    aggfunc="sum",
    fill_value=0
)

print(region_category)
```

## Step 15 – Add a sales band

```python
sales["OrderValueBand"] = pd.cut(
    sales["NetSales"],
    bins=[0, 10000, 50000, float("inf")],
    labels=["Small", "Medium", "Large"]
)

print(sales[
    ["OrderID", "NetSales", "OrderValueBand"]
])
```

## Step 16 – Export the report

```python
with pd.ExcelWriter("retail_sales_report.xlsx") as writer:
    sales.to_excel(
        writer,
        sheet_name="Detailed Sales",
        index=False
    )

    category_summary.to_excel(
        writer,
        sheet_name="Category Summary"
    )

    product_summary.to_excel(
        writer,
        sheet_name="Product Summary"
    )

    region_summary.to_excel(
        writer,
        sheet_name="Region Summary"
    )

    monthly_summary.to_excel(
        writer,
        sheet_name="Monthly Summary"
    )

    region_category.to_excel(
        writer,
        sheet_name="Region by Category"
    )

print("Retail sales report created.")
```

## Project 2 – Concepts covered

| Pandas concept | Project use |
|---|---|
| `read_csv()` | Load orders and products |
| `drop_duplicates()` | Remove exact duplicate records |
| `to_datetime()` | Convert order dates |
| `to_numeric()` | Validate numeric fields |
| `merge()` | Combine order and product data |
| `validate` | Check merge relationship |
| Column arithmetic | Revenue, cost, and profit |
| `groupby()` | Category, product, region, and month analysis |
| `agg()` | Multiple summary metrics |
| `.dt.to_period()` | Group by month |
| `sort_values()` | Rank products |
| `pivot_table()` | Region/category report |
| `pd.cut()` | Order value bands |
| `ExcelWriter` | Multi-sheet Excel report |

## Project 2 – Student challenges

1. Add a customer table and merge it with orders.
2. Calculate average order value.
3. Find the region with the highest profit.
4. Calculate each category's percentage contribution to revenue.
5. Find products with negative profit.
6. Compare monthly revenue with the previous month.
7. Calculate a three-month rolling revenue total if more months are added.
8. Find the largest order in each region.
9. Create a month-by-region pivot table.
10. Export a CSV containing only orders with NetSales above a chosen threshold.
11. Add returns and calculate net units sold.
12. Validate that every order ProductID exists in the product table.

---

# Part 21 – Common pandas mistakes

## Chapter 69 – Mistakes to avoid

### Mistake 1: Confusing `loc` and `iloc`

- `loc` uses labels.
- `iloc` uses integer positions.

```python
df.loc[0, "Name"]
df.iloc[0, 0]
```

### Mistake 2: Using Python `and` instead of `&`

Incorrect:

```python
# df[(df["Age"] > 25) and (df["Salary"] > 60000)]
```

Correct:

```python
df[(df["Age"] > 25) & (df["Salary"] > 60000)]
```

### Mistake 3: Forgetting parentheses around conditions

Correct:

```python
df[(df["Age"] > 25) | (df["Department"] == "IT")]
```

### Mistake 4: Confusing Series and DataFrame selection

```python
df["Salary"]       # Series
df[["Salary"]]     # DataFrame
```

### Mistake 5: Ignoring missing values

Always inspect:

```python
df.isna().sum()
```

### Mistake 6: Converting data types without validating values

Use `pd.to_numeric(..., errors="coerce")` when invalid values should be identified as missing, and inspect how many values were converted to missing.

### Mistake 7: Merging on the wrong key

Check key uniqueness and expected relationships before merging. A many-to-many merge can multiply rows.

### Mistake 8: Assuming `concat()` matches records by their meaning

When concatenating along columns, pandas aligns on index labels. Confirm that indexes refer to corresponding records.

### Mistake 9: Modifying a filtered DataFrame without understanding the result

Prefer an explicit copy when creating an independent working subset:

```python
it_df = df.loc[df["Department"] == "IT"].copy()

it_df["Bonus"] = it_df["Salary"] * 0.10
```

This makes the intended independent working DataFrame clear.

### Mistake 10: Using `apply()` for every calculation

Prefer vectorized operations when they express the calculation clearly.

---

# Part 22 – Revision questions

## Beginner questions

1. What is pandas?
2. What is the difference between a Series and a DataFrame?
3. What does `pd` represent in `import pandas as pd`?
4. How do you create a Series from a list?
5. How do you create a DataFrame from a dictionary?
6. What does `df.shape` return?
7. What is the purpose of `head()` and `tail()`?
8. What information does `info()` display?
9. What does `describe()` calculate?
10. How do you read a CSV file?

## Intermediate questions

11. What is the difference between `loc` and `iloc`?
12. How do you select multiple columns?
13. How do you filter rows using two conditions?
14. Why do we use `&` rather than `and` in a pandas Boolean filter?
15. How do you sort by salary in descending order?
16. How do you create a new column using an existing column?
17. How do you find missing values?
18. What is the difference between `dropna()` and `fillna()`?
19. How do you remove duplicate records?
20. How do you convert a text column to datetime?

## Advanced questions

21. Explain the split–apply–combine pattern.
22. What is the difference between `agg()` and `transform()`?
23. What is the difference between `merge()`, `join()`, and `concat()`?
24. Explain inner, left, right, and outer merge.
25. Why can a merge unexpectedly increase the number of rows?
26. What is the difference between `pivot()` and `pivot_table()`?
27. What does `melt()` do?
28. How can you calculate month-over-month sales changes?
29. When should you use `apply()` and when should you use vectorized operations?
30. How can you read a large CSV file in chunks?
31. What is a categorical dtype?
32. What is the purpose of `validate` in `merge()`?
33. How can you create a rolling average?
34. What is the difference between `size()` and `count()` in grouped data?
35. How would you design a reliable data-cleaning pipeline?

---

# Final learning roadmap

| Stage | Topics | Expected outcome |
|---|---|---|
| 1. Introduction | pandas, Series, DataFrame | Understand pandas structures |
| 2. Inspection | head, tail, info, describe | Inspect datasets |
| 3. Input | CSV, Excel, JSON | Load external data |
| 4. Selection | loc, iloc, columns | Select required records |
| 5. Filtering | Conditions, isin, between | Find relevant records |
| 6. Cleaning | Missing values, duplicates, dtypes | Prepare reliable data |
| 7. Transformation | Strings, dates, calculated columns | Create useful fields |
| 8. Analysis | groupby, agg, transform | Summarize data |
| 9. Combining | merge, join, concat | Integrate datasets |
| 10. Reshaping | pivot, pivot_table, melt | Change data layout |
| 11. Advanced | Time series, chunks, memory | Work with larger and time-based data |
| 12. Projects | Employee and retail analysis | Apply pandas to real scenarios |

## What should students learn after pandas?

A recommended next sequence:

1. **Matplotlib** – create charts and visualizations.
2. **Seaborn** – statistical data visualization.
3. **Exploratory Data Analysis (EDA)** – investigate and understand real datasets.
4. **Data cleaning and feature engineering** – prepare datasets for analysis and machine learning.
5. **scikit-learn** – build machine-learning models.

## Teaching recommendation

Do not rush through pandas syntax. Spend extra time on:

- Series versus DataFrame.
- `loc` versus `iloc`.
- Boolean filtering with multiple conditions.
- Missing values and data types.
- `groupby()` with a clear understanding of which records belong to each group.
- `merge()` and join validation.
- `pivot_table()` and `melt()`.
- Date conversion and time-series operations.

Students should understand not only which method to call, but also what the rows represent, what each column means, how missing values are handled, and whether the output still represents the original business records correctly.
