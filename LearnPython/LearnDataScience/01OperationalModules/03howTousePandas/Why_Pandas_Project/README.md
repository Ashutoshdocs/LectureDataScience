# Why Use Pandas When We Already Have File Handling and NumPy?

A small, beginner-friendly Python project that compares three ways to work with tabular data:

1. **Python file handling** — read a CSV file as text and process it manually.
2. **NumPy** — store numeric values in arrays and perform fast numerical calculations.
3. **Pandas** — work with rows and columns using labels, filtering, grouping, missing-value handling, and summaries.

## Learning objective

By the end, students should understand that these tools are not competitors:

- File handling helps us read and write files.
- NumPy is excellent for numerical arrays and mathematical operations.
- Pandas builds on the Python data ecosystem and makes real-world tabular data easier to inspect, clean, filter, transform, and summarize.

## Project structure

```text
Why_Pandas_Project/
├── data/
│   └── sales.csv
├── examples/
│   ├── 01_file_handling.py
│   ├── 02_numpy.py
│   └── 03_pandas.py
├── requirements.txt
└── README.md
```

## 1. Set up the environment

Open a terminal in this project folder.

### Windows

```bash
python -m venv .venv
.venv\\Scripts\\activate
python -m pip install -r requirements.txt
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## 2. Look at the data

Open `data/sales.csv`. It contains a small sales table with:

- Order ID
- Product
- Region
- Quantity
- Unit price
- Salesperson
- A few missing values in the salesperson column

The total amount for a row is:

```text
quantity × unit_price
```

## 3. Run the three approaches

Run these commands from the project root:

```bash
python examples/01_file_handling.py
python examples/02_numpy.py
python examples/03_pandas.py
```

## 4. What each approach demonstrates

### A. File handling

`01_file_handling.py` uses Python's built-in `csv` module.

It can:
- Open and read a CSV file.
- Convert text values into numbers.
- Calculate each order's amount.
- Calculate total sales.
- Filter orders from a region.

But we must manually handle column names, data conversion, missing values, filtering, and grouping. As the dataset and number of operations grow, this manual code becomes longer and easier to get wrong.

### B. NumPy

`02_numpy.py` loads numeric columns into NumPy arrays.

It can:
- Multiply quantity and unit price element by element.
- Calculate total, mean, minimum, and maximum.
- Apply numeric conditions.

But a table with mixed data types (product names, regions, names, quantities, prices) is not naturally represented as one ordinary NumPy numeric array. We also need to manage column positions and keep related arrays aligned.

### C. Pandas

`03_pandas.py` loads the CSV into a DataFrame.

It can:
- Display the table with column names and row indexes.
- Inspect data types and missing values.
- Create a calculated column.
- Filter rows using readable conditions.
- Group by region and calculate totals.
- Sort results.
- Fill missing values.
- Export the result to a new CSV file.

Pandas makes common data-analysis tasks concise and readable.

## 5. Important comparison

| Task | File handling (`csv`) | NumPy | Pandas |
|---|---|---|---|
| Read CSV | Yes | Possible, with numeric focus | Yes, very convenient |
| Mixed text and numbers | Manual parsing | Possible, but less natural in numeric arrays | Natural |
| Row/column labels | Manual | Usually positional indexes | Built-in |
| Missing values | Handle manually | Special values / masks | Built-in tools |
| Filter rows | Write loops | Boolean masks | Readable conditions |
| Group by category | Build dictionaries/loops | More manual | `groupby()` |
| Summary statistics | Write calculations | Excellent for numeric arrays | Convenient for columns/groups |
| Best fit | Basic file input/output | Numerical computing | Tabular data analysis |

## 6. Teaching walkthrough

Ask students to answer these questions after running the scripts:

1. Which approach needs the most manual code to filter orders from the East region?
2. Why does NumPy work well for quantity and unit price?
3. Why is a single NumPy numeric array awkward for product names and regions?
4. What does `df.isna().sum()` tell us?
5. What does `df.groupby("region")["sales"].sum()` do?
6. Why is `df.loc[...]` often easier to understand than manually checking each row?

## 7. Try these exercises

### Beginner
1. In the file-handling script, calculate the average order amount.
2. In the NumPy script, calculate the total quantity sold.
3. In the Pandas script, display only `product`, `quantity`, and `sales`.

### Intermediate
4. Filter orders where sales are greater than 500.
5. Find total sales for each salesperson.
6. Sort the DataFrame by sales from highest to lowest.
7. Replace missing salesperson values with `"Unknown"`.

### Challenge
8. Find the top-selling product by total sales.
9. Calculate the percentage contribution of each region to total sales.
10. Save only orders above 500 to `data/high_value_orders.csv`.

## 8. Key takeaway

Use the right tool for the job:

- **File handling** answers: "How do I read or write this file?"
- **NumPy** answers: "How do I efficiently calculate with numerical data?"
- **Pandas** answers: "How do I work with, clean, transform, filter, and analyze a table?"

Pandas does not make file handling or NumPy obsolete. It makes structured data analysis much easier, and it can work alongside NumPy.
