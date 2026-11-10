# 🐻‍❄️ Python Polars – Industry Projects

**Beginner to Intermediate · Python + Polars + CSV**

Two real-world data analysis projects built with **Polars**, a fast DataFrame library for Python:

| # | Project | Domain | Input | Report |
|---|---|---|---|---|
| 01 | **Employee Data Analysis System** | HR Analytics | `employees.csv` | `employee_report.csv` |
| 02 | **E-Commerce Sales Analysis** | Business / Sales Analytics | `sales.csv` | `sales_report.csv` |

> All code and outputs in this guide were tested on **Polars 2.1.0** with **Python 3.13**. Small display differences may appear on other versions.

---

## 📁 What's in this folder

| File | Use it for |
|---|---|
| `README.md` | This guide: concepts, 24 labs, expected outputs, exercises and answers |
| `project1_employee_analysis.py` | Project 01, all 12 labs in one script |
| `project2_sales_analysis.py` | Project 02, all 12 labs in one script |
| `answers.py` | Answers to the 14 practice exercises |
| `requirements.txt` | Dependency list for `pip install -r requirements.txt` |

---

## 📚 Table of Contents

- [What You Will Learn](#-what-you-will-learn)
- [Setup](#%EF%B8%8F-setup)
- [Polars in 2 Minutes](#-polars-in-2-minutes)
- [Project 01 – Employee Data Analysis System](#-project-01--employee-data-analysis-system)
- [Project 02 – E-Commerce Sales Analysis](#-project-02--e-commerce-sales-analysis)
- [Project Comparison](#-project-comparison)
- [Common Mistakes & Gotchas](#%EF%B8%8F-common-mistakes--gotchas)
- [Important Polars Functions (Cheat Sheet)](#-important-polars-functions-cheat-sheet)
- [Practice Exercises](#-practice-exercises)
- [Answers](#-answers)
- [What to Learn Next](#-what-to-learn-next)

---

## 🎯 What You Will Learn

- ✅ Read and analyze CSV files
- ✅ Filter records using conditions
- ✅ Group data by department or by product
- ✅ Calculate sum, average and count
- ✅ Sort records
- ✅ Create new columns using expressions
- ✅ Export reports to CSV files

---

## ⚙️ Setup

**1. Install Polars** (in your terminal):

```bash
pip install polars
```

**2. Run the projects:**

```bash
python project1_employee_analysis.py
python project2_sales_analysis.py
python answers.py
```

Each script creates its CSV files in the folder you run it from.

> 💡 You can also type the labs one by one in a Python Shell or a Jupyter Notebook.

---

## 🧠 Polars in 2 Minutes

A **DataFrame** is a table with rows and named columns, like an Excel sheet. Polars works with **expressions**: small instructions that describe what to do with a column.

```python
pl.col("Salary")                   # refer to the Salary column
pl.col("Salary") > 50000           # a condition on the column
pl.col("Salary").sum()             # an aggregation
pl.col("Salary").alias("Pay")      # rename the result
```

You pass these expressions to DataFrame methods:

| Method | What it does | SQL equivalent |
|---|---|---|
| `df.filter(expr)` | Keep rows that match a condition | `WHERE` |
| `df.select(expr)` | Choose or calculate columns | `SELECT` |
| `df.with_columns(expr)` | Add or replace columns, keeping all others | `SELECT *, new_col` |
| `df.group_by(col).agg(expr)` | Group rows and summarise each group | `GROUP BY` |
| `df.sort(col)` | Order rows | `ORDER BY` |

### 📖 How to read Polars output

```
shape: (4, 2)                     ← (rows, columns)
┌────────────┬──────────────┐
│ Department ┆ Total_Salary │      ← column names
│ ---        ┆ ---          │
│ str        ┆ i64          │      ← data types: str = text, i64 = integer,
╞════════════╪══════════════╡                    f64 = decimal, u32 = count
│ Finance    ┆ 105000       │
└────────────┴──────────────┘
```

> ⚠️ **Polars DataFrames are immutable.** Methods return a **new** DataFrame. To keep a change, assign it back: `df = df.with_columns(...)`.

---

# 👔 PROJECT 01 – Employee Data Analysis System

**Level:** Beginner to Intermediate · **Domain:** HR Analytics · **Technology:** Python + Polars + CSV

### 🏢 Real-world scenario

You work as a **Data Analyst** in an IT company. The HR team gives you an employee CSV file. Management wants to know:
- employee salaries
- department-wise salary expenses
- employee counts per department
- which employees are experienced

Your job is to analyze the data with Polars and produce a **final HR report**.

### 📊 Dataset: `employees.csv`

| Employee_ID | Name | Department | Salary | Age | Experience |
|---|---|---|---|---|---|
| 101 | Rahul | IT | 50000 | 25 | 2 |
| 102 | Amit | HR | 40000 | 30 | 5 |
| 103 | Priya | IT | 65000 | 28 | 4 |
| 104 | Neha | Finance | 45000 | 27 | 3 |
| 105 | Rohit | IT | 75000 | 32 | 7 |
| 106 | Simran | HR | 55000 | 29 | 6 |
| 107 | Vikas | Finance | 60000 | 35 | 10 |
| 108 | Pooja | IT | 80000 | 31 | 8 |
| 109 | Ankit | Sales | 35000 | 24 | 1 |
| 110 | Anjali | Sales | 50000 | 28 | 4 |

---

### Lab 01 – Import Polars

```python
import polars as pl
```

**📝 Explanation:**
- `import` loads a Python library.
- `polars` is the library name.
- `pl` is the standard short name (alias) for Polars.

---

### Lab 02 – Create the Employee CSV File

```python
data = """Employee_ID,Name,Department,Salary,Age,Experience
101,Rahul,IT,50000,25,2
102,Amit,HR,40000,30,5
103,Priya,IT,65000,28,4
104,Neha,Finance,45000,27,3
105,Rohit,IT,75000,32,7
106,Simran,HR,55000,29,6
107,Vikas,Finance,60000,35,10
108,Pooja,IT,80000,31,8
109,Ankit,Sales,35000,24,1
110,Anjali,Sales,50000,28,4
"""

with open("employees.csv", "w") as file:
    file.write(data)
```

**📝 Explanation:**
- `"""..."""` (triple quotes) creates a multi-line string. **Each record must be on its own line**, because that's how CSV files separate rows.
- `open("employees.csv", "w")` creates the file, or opens it if it exists. `"w"` means **write mode**, which overwrites the old content.
- `with` closes the file automatically when the block ends.
- `write()` saves the text into the file.

> ⚠️ If the data is pasted on a single line (as in some handouts), Polars treats the whole line as the **header**. You get jumbled column names like `B 1` and `2 3`, and **0 rows**. Keep one record per line.

---

### Lab 03 – Read the Employee CSV File

```python
df = pl.read_csv("employees.csv")
print(df)
```

**✅ Output**
```
shape: (10, 6)
┌─────────────┬────────┬────────────┬────────┬─────┬────────────┐
│ Employee_ID ┆ Name   ┆ Department ┆ Salary ┆ Age ┆ Experience │
│ ---         ┆ ---    ┆ ---        ┆ ---    ┆ --- ┆ ---        │
│ i64         ┆ str    ┆ str        ┆ i64    ┆ i64 ┆ i64        │
╞═════════════╪════════╪════════════╪════════╪═════╪════════════╡
│ 101         ┆ Rahul  ┆ IT         ┆ 50000  ┆ 25  ┆ 2          │
│ 102         ┆ Amit   ┆ HR         ┆ 40000  ┆ 30  ┆ 5          │
│ …           ┆ …      ┆ …          ┆ …      ┆ …   ┆ …          │
│ 110         ┆ Anjali ┆ Sales      ┆ 50000  ┆ 28  ┆ 4          │
└─────────────┴────────┴────────────┴────────┴─────┴────────────┘
```
*(middle rows shortened here; you will see all 10)*

**📝 Explanation:** `read_csv()` reads the file and returns a Polars **DataFrame**. Polars detects the data types automatically: numbers become `i64` and text becomes `str`.

> 💡 Other quick checks: `df.shape` → `(10, 6)`, `df.columns` → list of column names, `df.head(3)` → first 3 rows.

---

### Lab 04 – Count Total Employees

```python
print(df.height)
```

**✅ Output**
```
10
```

**📝 Explanation:** `height` is the number of **rows**, which here is one row per employee. `df.width` gives the number of columns (6). It's an attribute, so there are no brackets.

---

### Lab 05 – Filter Salary Greater Than 50000

```python
print(df.filter(pl.col("Salary") > 50000))
```

**✅ Output:** 5 employees
```
shape: (5, 6)
┌─────────────┬────────┬────────────┬────────┬─────┬────────────┐
│ Employee_ID ┆ Name   ┆ Department ┆ Salary ┆ Age ┆ Experience │
╞═════════════╪════════╪════════════╪════════╪═════╪════════════╡
│ 103         ┆ Priya  ┆ IT         ┆ 65000  ┆ 28  ┆ 4          │
│ 105         ┆ Rohit  ┆ IT         ┆ 75000  ┆ 32  ┆ 7          │
│ 106         ┆ Simran ┆ HR         ┆ 55000  ┆ 29  ┆ 6          │
│ 107         ┆ Vikas  ┆ Finance    ┆ 60000  ┆ 35  ┆ 10         │
│ 108         ┆ Pooja  ┆ IT         ┆ 80000  ┆ 31  ┆ 8          │
└─────────────┴────────┴────────────┴────────┴─────┴────────────┘
```

**📝 Explanation:**
- `filter()` keeps only the rows that match a condition.
- `pl.col("Salary")` refers to the Salary column.
- `> 50000` keeps salaries **greater than** 50000. Rahul and Anjali (exactly 50000) are **not** included. Use `>=` to include them.

---

### Lab 06 – Find IT Department Employees

```python
print(df.filter(pl.col("Department") == "IT"))
```

**✅ Output:** 4 employees (Rahul, Priya, Rohit, Pooja)
```
shape: (4, 6)
┌─────────────┬───────┬────────────┬────────┬─────┬────────────┐
│ Employee_ID ┆ Name  ┆ Department ┆ Salary ┆ Age ┆ Experience │
╞═════════════╪═══════╪════════════╪════════╪═════╪════════════╡
│ 101         ┆ Rahul ┆ IT         ┆ 50000  ┆ 25  ┆ 2          │
│ 103         ┆ Priya ┆ IT         ┆ 65000  ┆ 28  ┆ 4          │
│ 105         ┆ Rohit ┆ IT         ┆ 75000  ┆ 32  ┆ 7          │
│ 108         ┆ Pooja ┆ IT         ┆ 80000  ┆ 31  ┆ 8          │
└─────────────┴───────┴────────────┴────────┴─────┴────────────┘
```

**📝 Explanation:** `==` checks whether the Department value is **equal to** `"IT"`. Text matching is **case-sensitive**, so `"it"` would match nothing.

---

### Lab 07 – Calculate Average Salary

```python
print(df.select(pl.col("Salary").mean()))
```

**✅ Output**
```
shape: (1, 1)
┌─────────┐
│ Salary  │
│ ---     │
│ f64     │
╞═════════╡
│ 55500.0 │
└─────────┘
```

**📝 Explanation:** `mean()` calculates the average of all salaries: 555000 ÷ 10 = **55500.0**. `select()` always returns a **DataFrame** (a table). To get just the number, use the column directly:

```python
print(df["Salary"].mean())    # 55500.0
```

---

### Lab 08 – Department-wise Total Salary

```python
print(
    df.group_by("Department")
    .agg(pl.col("Salary").sum().alias("Total_Salary"))
    .sort("Department")
)
```

**✅ Output**
```
shape: (4, 2)
┌────────────┬──────────────┐
│ Department ┆ Total_Salary │
│ ---        ┆ ---          │
│ str        ┆ i64          │
╞════════════╪══════════════╡
│ Finance    ┆ 105000       │
│ HR         ┆ 95000        │
│ IT         ┆ 270000       │
│ Sales      ┆ 85000        │
└────────────┴──────────────┘
```

**📝 Explanation:**
- `group_by("Department")` puts rows with the same department together.
- `agg()` runs a calculation on each group.
- `sum()` adds up the salaries in each group.
- `alias("Total_Salary")` names the result column.
- `sort("Department")` orders the result alphabetically.

```
  group_by("Department")          agg(sum of Salary)
  IT      → 50000, 65000,    →    IT      270000
            75000, 80000
  HR      → 40000, 55000     →    HR       95000
  Finance → 45000, 60000     →    Finance 105000
  Sales   → 35000, 50000     →    Sales    85000
```

> ⚠️ `group_by()` does **not** keep a fixed order. The groups can come out differently on every run, so always add `.sort()` for a stable result.
>
> 💡 Wrapping the whole chain in `( )` lets you split it across lines neatly.

---

### Lab 09 – Find the Highest-Paid Employee

```python
print(df.sort("Salary", descending=True).head(1))
```

**✅ Output**
```
shape: (1, 6)
┌─────────────┬───────┬────────────┬────────┬─────┬────────────┐
│ Employee_ID ┆ Name  ┆ Department ┆ Salary ┆ Age ┆ Experience │
╞═════════════╪═══════╪════════════╪════════╪═════╪════════════╡
│ 108         ┆ Pooja ┆ IT         ┆ 80000  ┆ 31  ┆ 8          │
└─────────────┴───────┴────────────┴────────┴─────┴────────────┘
```

**📝 Explanation:**
- `sort("Salary", descending=True)` orders employees from highest to lowest salary.
- `head(1)` returns the first row, which is the top earner.
- Use `head(3)` for the top 3.

---

### Lab 10 – Find Experienced Employees

**Task:** Find employees with **more than 5 years** of experience.

```python
print(df.filter(pl.col("Experience") > 5))
```

**✅ Output:** 4 employees
```
shape: (4, 6)
┌─────────────┬────────┬────────────┬────────┬─────┬────────────┐
│ Employee_ID ┆ Name   ┆ Department ┆ Salary ┆ Age ┆ Experience │
╞═════════════╪════════╪════════════╪════════╪═════╪════════════╡
│ 105         ┆ Rohit  ┆ IT         ┆ 75000  ┆ 32  ┆ 7          │
│ 106         ┆ Simran ┆ HR         ┆ 55000  ┆ 29  ┆ 6          │
│ 107         ┆ Vikas  ┆ Finance    ┆ 60000  ┆ 35  ┆ 10         │
│ 108         ┆ Pooja  ┆ IT         ┆ 80000  ┆ 31  ┆ 8          │
└─────────────┴────────┴────────────┴────────┴─────┴────────────┘
```

**📝 Explanation:** Amit has exactly 5 years, so he is **not** included (`> 5`, not `>= 5`).

---

### Lab 11 – Department-wise Employee Count

```python
print(
    df.group_by("Department")
    .agg(pl.len().alias("Total_Employees"))
    .sort("Department")
)
```

**✅ Output**
```
shape: (4, 2)
┌────────────┬─────────────────┐
│ Department ┆ Total_Employees │
│ ---        ┆ ---             │
│ str        ┆ u32             │
╞════════════╪═════════════════╡
│ Finance    ┆ 2               │
│ HR         ┆ 2               │
│ IT         ┆ 4               │
│ Sales      ┆ 2               │
└────────────┴─────────────────┘
```

**📝 Explanation:** `pl.len()` counts the **number of rows** in each group. The `u32` type is an unsigned (never negative) integer, which is used for counts.

---

### Lab 12 – Generate the Final HR Report

```python
report = (
    df.group_by("Department")
    .agg(
        pl.col("Salary").mean().alias("Average_Salary"),
        pl.col("Salary").sum().alias("Total_Salary"),
        pl.len().alias("Total_Employees"),
    )
    .sort("Department")
)

print(report)
report.write_csv("employee_report.csv")
```

**✅ Output**
```
shape: (4, 4)
┌────────────┬────────────────┬──────────────┬─────────────────┐
│ Department ┆ Average_Salary ┆ Total_Salary ┆ Total_Employees │
│ ---        ┆ ---            ┆ ---          ┆ ---             │
│ str        ┆ f64            ┆ i64          ┆ u32             │
╞════════════╪════════════════╪══════════════╪═════════════════╡
│ Finance    ┆ 52500.0        ┆ 105000       ┆ 2               │
│ HR         ┆ 47500.0        ┆ 95000        ┆ 2               │
│ IT         ┆ 67500.0        ┆ 270000       ┆ 4               │
│ Sales      ┆ 42500.0        ┆ 85000        ┆ 2               │
└────────────┴────────────────┴──────────────┴─────────────────┘
```

**📄 `employee_report.csv` contents**
```
Department,Average_Salary,Total_Salary,Total_Employees
Finance,52500.0,105000,2
HR,47500.0,95000,2
IT,67500.0,270000,4
Sales,42500.0,85000,2
```

**📝 Explanation:**
- `agg()` can calculate **several** results at once. Separate them with commas.
- `write_csv()` exports the DataFrame to a CSV file that opens in Excel or Google Sheets.

### ✅ Project 01 – Final Deliverables

- [x] Employee records analyzed
- [x] Salary-based filtering completed
- [x] Department-wise salary calculated
- [x] Employee count generated
- [x] Final HR report exported (`employee_report.csv`)

---

# 🛒 PROJECT 02 – E-Commerce Sales Analysis

**Level:** Beginner to Intermediate · **Domain:** Business / Sales Analytics · **Technology:** Python + Polars + CSV

### 🏢 Real-world scenario

You work as a **Data Analyst** in an e-commerce company that sells products online. Management wants to know:

1. How much **total revenue** does the company generate?
2. Which **product** generates the highest revenue?
3. Which **city** generates the highest sales?
4. How many **units** have been sold?
5. Which **category** generates the most revenue?

### 📊 Dataset: `sales.csv`

| Order_ID | Product | Category | City | Quantity | Price |
|---|---|---|---|---|---|
| 1001 | Laptop | Electronics | Delhi | 2 | 50000 |
| 1002 | Mobile | Electronics | Mumbai | 3 | 20000 |
| 1003 | Keyboard | Accessories | Delhi | 5 | 1000 |
| 1004 | Mouse | Accessories | Noida | 10 | 500 |
| 1005 | Laptop | Electronics | Noida | 1 | 50000 |
| 1006 | Mobile | Electronics | Delhi | 2 | 20000 |
| 1007 | Monitor | Electronics | Mumbai | 2 | 15000 |
| 1008 | Keyboard | Accessories | Noida | 4 | 1000 |
| 1009 | Mouse | Accessories | Delhi | 6 | 500 |
| 1010 | Monitor | Electronics | Noida | 3 | 15000 |

---

### Lab 01 – Import Polars

```python
import polars as pl
```

---

### Lab 02 – Create the Sales CSV File

```python
data = """Order_ID,Product,Category,City,Quantity,Price
1001,Laptop,Electronics,Delhi,2,50000
1002,Mobile,Electronics,Mumbai,3,20000
1003,Keyboard,Accessories,Delhi,5,1000
1004,Mouse,Accessories,Noida,10,500
1005,Laptop,Electronics,Noida,1,50000
1006,Mobile,Electronics,Delhi,2,20000
1007,Monitor,Electronics,Mumbai,2,15000
1008,Keyboard,Accessories,Noida,4,1000
1009,Mouse,Accessories,Delhi,6,500
1010,Monitor,Electronics,Noida,3,15000
"""

with open("sales.csv", "w") as file:
    file.write(data)
```

---

### Lab 03 – Read the Sales CSV File

```python
df = pl.read_csv("sales.csv")
print(df)
```

**✅ Output:** `shape: (10, 6)`, the 10 orders shown in the dataset table above.

---

### Lab 04 – Calculate Revenue for Each Order

**Business formula:** `Revenue = Quantity × Price`

```python
df = df.with_columns(
    (pl.col("Quantity") * pl.col("Price")).alias("Revenue")
)
print(df)
```

**✅ Output**
```
shape: (10, 7)
┌──────────┬──────────┬─────────────┬────────┬──────────┬───────┬─────────┐
│ Order_ID ┆ Product  ┆ Category    ┆ City   ┆ Quantity ┆ Price ┆ Revenue │
│ ---      ┆ ---      ┆ ---         ┆ ---    ┆ ---      ┆ ---   ┆ ---     │
│ i64      ┆ str      ┆ str         ┆ str    ┆ i64      ┆ i64   ┆ i64     │
╞══════════╪══════════╪═════════════╪════════╪══════════╪═══════╪═════════╡
│ 1001     ┆ Laptop   ┆ Electronics ┆ Delhi  ┆ 2        ┆ 50000 ┆ 100000  │
│ 1002     ┆ Mobile   ┆ Electronics ┆ Mumbai ┆ 3        ┆ 20000 ┆ 60000   │
│ 1003     ┆ Keyboard ┆ Accessories ┆ Delhi  ┆ 5        ┆ 1000  ┆ 5000    │
│ 1004     ┆ Mouse    ┆ Accessories ┆ Noida  ┆ 10       ┆ 500   ┆ 5000    │
│ 1005     ┆ Laptop   ┆ Electronics ┆ Noida  ┆ 1        ┆ 50000 ┆ 50000   │
│ 1006     ┆ Mobile   ┆ Electronics ┆ Delhi  ┆ 2        ┆ 20000 ┆ 40000   │
│ 1007     ┆ Monitor  ┆ Electronics ┆ Mumbai ┆ 2        ┆ 15000 ┆ 30000   │
│ 1008     ┆ Keyboard ┆ Accessories ┆ Noida  ┆ 4        ┆ 1000  ┆ 4000    │
│ 1009     ┆ Mouse    ┆ Accessories ┆ Delhi  ┆ 6        ┆ 500   ┆ 3000    │
│ 1010     ┆ Monitor  ┆ Electronics ┆ Noida  ┆ 3        ┆ 15000 ┆ 45000   │
└──────────┴──────────┴─────────────┴────────┴──────────┴───────┴─────────┘
```

**📝 Explanation:**
- `with_columns()` adds new columns (or replaces existing ones) and **keeps all the other columns**.
- `pl.col("Quantity") * pl.col("Price")` multiplies the two columns row by row.
- `alias("Revenue")` names the new column.
- `df = ...` saves the result. Without it, the Revenue column would be lost, because Polars returns a new DataFrame.

> 💡 **The rest of Project 02 needs the Revenue column.** If you restart Python, run Labs 03 and 04 again first.

---

### Lab 05 – Calculate Total Revenue

```python
print(df.select(pl.col("Revenue").sum()))
```

**✅ Output**
```
shape: (1, 1)
┌─────────┐
│ Revenue │
│ ---     │
│ i64     │
╞═════════╡
│ 342000  │
└─────────┘
```

**📝 Explanation:** `sum()` adds the Revenue of all 10 orders, for a total of **₹3,42,000**.

---

### Lab 06 – Product-wise Revenue

```python
print(
    df.group_by("Product")
    .agg(pl.col("Revenue").sum().alias("Total_Revenue"))
    .sort("Total_Revenue", descending=True)
)
```

**✅ Output**
```
shape: (5, 2)
┌──────────┬───────────────┐
│ Product  ┆ Total_Revenue │
│ ---      ┆ ---           │
│ str      ┆ i64           │
╞══════════╪═══════════════╡
│ Laptop   ┆ 150000        │
│ Mobile   ┆ 100000        │
│ Monitor  ┆ 75000         │
│ Keyboard ┆ 9000          │
│ Mouse    ┆ 8000          │
└──────────┴───────────────┘
```

**📝 Explanation:** **Laptop** brings in the most revenue. Sorting with `descending=True` puts the best product at the top.

---

### Lab 07 – City-wise Revenue

```python
print(
    df.group_by("City")
    .agg(pl.col("Revenue").sum().alias("Total_Revenue"))
    .sort("Total_Revenue", descending=True)
)
```

**✅ Output**
```
shape: (3, 2)
┌────────┬───────────────┐
│ City   ┆ Total_Revenue │
│ ---    ┆ ---           │
│ str    ┆ i64           │
╞════════╪═══════════════╡
│ Delhi  ┆ 148000        │
│ Noida  ┆ 104000        │
│ Mumbai ┆ 90000         │
└────────┴───────────────┘
```

**📝 Explanation:** **Delhi** generates the highest sales.

> ✏️ **Correction:** some versions of this handout list Noida as **99,000**. The correct value is **104,000**:
> Noida orders = 5,000 (Mouse) + 50,000 (Laptop) + 4,000 (Keyboard) + 45,000 (Monitor) = **104,000**.
> ✔ Check: 148,000 + 104,000 + 90,000 = **342,000**, which matches the total revenue in Lab 05.

---

### Lab 08 – Category-wise Revenue

```python
print(
    df.group_by("Category")
    .agg(pl.col("Revenue").sum().alias("Total_Revenue"))
    .sort("Total_Revenue", descending=True)
)
```

**✅ Output**
```
shape: (2, 2)
┌─────────────┬───────────────┐
│ Category    ┆ Total_Revenue │
│ ---         ┆ ---           │
│ str         ┆ i64           │
╞═════════════╪═══════════════╡
│ Electronics ┆ 325000        │
│ Accessories ┆ 17000         │
└─────────────┴───────────────┘
```

**📝 Explanation:** **Electronics** accounts for about 95% of all revenue.

---

### Lab 09 – Orders with Revenue Above 40000

```python
print(df.filter(pl.col("Revenue") > 40000))
```

**✅ Output:** 4 orders
```
shape: (4, 7)
┌──────────┬─────────┬─────────────┬────────┬──────────┬───────┬─────────┐
│ Order_ID ┆ Product ┆ Category    ┆ City   ┆ Quantity ┆ Price ┆ Revenue │
╞══════════╪═════════╪═════════════╪════════╪══════════╪═══════╪═════════╡
│ 1001     ┆ Laptop  ┆ Electronics ┆ Delhi  ┆ 2        ┆ 50000 ┆ 100000  │
│ 1002     ┆ Mobile  ┆ Electronics ┆ Mumbai ┆ 3        ┆ 20000 ┆ 60000   │
│ 1005     ┆ Laptop  ┆ Electronics ┆ Noida  ┆ 1        ┆ 50000 ┆ 50000   │
│ 1010     ┆ Monitor ┆ Electronics ┆ Noida  ┆ 3        ┆ 15000 ┆ 45000   │
└──────────┴─────────┴─────────────┴────────┴──────────┴───────┴─────────┘
```

**📝 Explanation:** Only orders whose **calculated** Revenue is greater than 40,000 are kept. Order 1006 (exactly 40,000) is excluded. Filtering on a column you created in Lab 04 is a common real-world pattern.

---

### Lab 10 – Total Quantity Sold

```python
print(df.select(pl.col("Quantity").sum()))
```

**✅ Output**
```
shape: (1, 1)
┌──────────┐
│ Quantity │
│ ---      │
│ i64      │
╞══════════╡
│ 38       │
└──────────┘
```

**📝 Explanation:** **38 units** were sold across all orders.

---

### Lab 11 – Average Order Revenue

```python
print(df.select(pl.col("Revenue").mean()))
```

**✅ Output**
```
shape: (1, 1)
┌─────────┐
│ Revenue │
│ ---     │
│ f64     │
╞═════════╡
│ 34200.0 │
└─────────┘
```

**📝 Explanation:** `mean()` gives the average revenue **per order**: 342,000 ÷ 10 = **34,200.0**. Businesses call this the **Average Order Value (AOV)**.

---

### Lab 12 – Generate the Final Sales Report

```python
sales_report = (
    df.group_by("Product")
    .agg(
        pl.col("Quantity").sum().alias("Total_Quantity"),
        pl.col("Revenue").sum().alias("Total_Revenue"),
    )
    .sort("Total_Revenue", descending=True)
)

print(sales_report)
sales_report.write_csv("sales_report.csv")
```

**✅ Output**
```
shape: (5, 3)
┌──────────┬────────────────┬───────────────┐
│ Product  ┆ Total_Quantity ┆ Total_Revenue │
│ ---      ┆ ---            ┆ ---           │
│ str      ┆ i64            ┆ i64           │
╞══════════╪════════════════╪═══════════════╡
│ Laptop   ┆ 3              ┆ 150000        │
│ Mobile   ┆ 5              ┆ 100000        │
│ Monitor  ┆ 5              ┆ 75000         │
│ Keyboard ┆ 9              ┆ 9000          │
│ Mouse    ┆ 16             ┆ 8000          │
└──────────┴────────────────┴───────────────┘
```

**📄 `sales_report.csv` contents**
```
Product,Total_Quantity,Total_Revenue
Laptop,3,150000
Mobile,5,100000
Monitor,5,75000
Keyboard,9,9000
Mouse,16,8000
```

**📝 Business insight:** Mouse sells the **most units** (16) but earns the **least revenue** (8,000). Laptop sells only 3 units but earns the most. High volume doesn't always mean high revenue.

### ✅ Project 02 – Final Deliverables

- [x] Sales data analyzed
- [x] Revenue calculated for each order
- [x] Product-wise revenue generated
- [x] City-wise sales analyzed
- [x] Category-wise sales analyzed
- [x] Final sales report exported (`sales_report.csv`)

### 📌 Answers to management's questions

| Question | Answer |
|---|---|
| Total revenue? | **₹3,42,000** |
| Highest-revenue product? | **Laptop** (₹1,50,000) |
| Highest-sales city? | **Delhi** (₹1,48,000) |
| Units sold? | **38** |
| Highest-revenue category? | **Electronics** (₹3,25,000) |

---

## 🆚 Project Comparison

| Feature | Project 01 | Project 02 |
|---|---|---|
| Project | Employee Analysis | E-Commerce Sales |
| Business domain | HR Analytics | Sales Analytics |
| Input file | `employees.csv` | `sales.csv` |
| New calculated column | — | ✅ Revenue (`with_columns`) |
| Filtering | ✅ | ✅ |
| Group by | ✅ | ✅ |
| Aggregation | ✅ | ✅ |
| Sorting | ✅ | ✅ |
| Report output | `employee_report.csv` | `sales_report.csv` |

---

## ⚠️ Common Mistakes & Gotchas

| Mistake | Error / Result | Fix |
|---|---|---|
| CSV data pasted on one line | Jumbled column names, 0 rows | Put each record on its own line |
| `pl.col("salary")` | `ColumnNotFoundError` | Column names are case-sensitive: use `"Salary"` |
| `df.groupby(...)` | `AttributeError` | Polars uses `group_by` (with an underscore) |
| `pl.col("A") == "IT" & pl.col("B") > 5` | `TypeError: the truth value of an Expr is ambiguous` | Wrap each condition in brackets: `(cond1) & (cond2)` |
| Using `and` / `or` between conditions | Error | Use `&` (and), `\|` (or), `~` (not) |
| `df.with_columns(...)` without `df =` | New column disappears | Assign it back: `df = df.with_columns(...)` |
| Group-by results in a different order each run | Not wrong, just unordered | Add `.sort(...)` after `agg()` |
| `print(df.select(pl.col("Salary").mean()))` shows a table | Expected | Use `df["Salary"].mean()` for a plain number |
| Revenue column missing in later labs | `ColumnNotFoundError: Revenue` | Run Lab 04 before Labs 05–12 |

---

## 📋 Important Polars Functions (Cheat Sheet)

| Function | Purpose | Example |
|---|---|---|
| `pl.DataFrame()` | Create a DataFrame from a dictionary | `pl.DataFrame({"A": [1, 2]})` |
| `pl.read_csv()` | Read a CSV file | `pl.read_csv("data.csv")` |
| `pl.col()` | Refer to a column in an expression | `pl.col("Salary")` |
| `filter()` | Keep rows that match a condition | `df.filter(pl.col("Age") > 25)` |
| `select()` | Choose or calculate columns | `df.select("Name", "Salary")` |
| `with_columns()` | Add or modify columns | `df.with_columns((pl.col("A") * 2).alias("B"))` |
| `group_by()` | Group rows by common values | `df.group_by("Department")` |
| `agg()` | Calculate per group | `.agg(pl.col("Salary").sum())` |
| `sum()` | Total | `pl.col("Revenue").sum()` |
| `mean()` | Average | `pl.col("Salary").mean()` |
| `max()` / `min()` | Largest / smallest | `pl.col("Salary").max()` |
| `pl.len()` | Count rows (per group) | `.agg(pl.len())` |
| `sort()` | Order rows | `df.sort("Salary", descending=True)` |
| `head()` | First n rows | `df.head(5)` |
| `alias()` | Name an expression's result | `pl.col("A").sum().alias("Total")` |
| `is_between()` | Range check (inclusive) | `pl.col("Salary").is_between(40000, 60000)` |
| `write_csv()` | Export to CSV | `df.write_csv("report.csv")` |
| `.height` / `.width` / `.shape` | Rows / columns / both | `df.shape` → `(10, 6)` |

**Combining conditions**

```python
df.filter((pl.col("Department") == "IT") & (pl.col("Salary") > 60000))   # AND
df.filter((pl.col("Department") == "HR") | (pl.col("Department") == "Sales"))  # OR
df.filter(pl.col("Department").is_in(["HR", "Sales"]))   # same as the OR above
```

---

## ✍️ Practice Exercises

Run both project scripts first (they create the CSV files), then try these yourself.

**Project 01 – Employee exercises**

| # | Exercise |
|---|---|
| E1 | Show all employees of the **HR** department. |
| E2 | Show only the **Name** and **Salary** columns. |
| E3 | Find the **youngest** employee. |
| E4 | Find employees with salary **between 45000 and 60000** (inclusive). |
| E5 | Find **IT** employees earning **more than 60000**. |
| E6 | Add a **Bonus** column equal to **10%** of Salary. |
| E7 | Find the **maximum experience** in each department. |

**Project 02 – Sales exercises**

| # | Exercise |
|---|---|
| S1 | Show all orders from **Delhi**. |
| S2 | Count the **number of orders** in each city. |
| S3 | Find the **best-selling product by quantity**. |
| S4 | Find **Electronics** orders with **Quantity of 2 or more**. |
| S5 | Add a **GST** column (18% of Revenue) and a **Final_Amount** column (Revenue + GST). |
| S6 | Find the **minimum, maximum and average** Revenue in one table. |
| S7 | Create a **city-wise report** (orders, quantity, revenue) and save it as `city_report.csv`. |

---

## ✅ Answers

> All answers are also in `answers.py`. Setup used by the answers:
> ```python
> import polars as pl
> emp = pl.read_csv("employees.csv")
> sales = pl.read_csv("sales.csv").with_columns(
>     (pl.col("Quantity") * pl.col("Price")).alias("Revenue")
> )
> ```

### Project 01 – Employee answers

<details>
<summary><b>E1. Show all employees of the HR department</b></summary>

```python
print(emp.filter(pl.col("Department") == "HR"))
```
**Result:** 2 rows: **Amit** (40000) and **Simran** (55000).
</details>

<details>
<summary><b>E2. Show only the Name and Salary columns</b></summary>

```python
print(emp.select("Name", "Salary"))
```
**Result:** `shape: (10, 2)`, all 10 employees with just their name and salary.
</details>

<details>
<summary><b>E3. Find the youngest employee</b></summary>

```python
print(emp.sort("Age").head(1))
```
**Result:** **Ankit**, age 24, Sales. `sort()` is ascending by default, so the smallest age comes first.
</details>

<details>
<summary><b>E4. Find employees with salary between 45000 and 60000 (inclusive)</b></summary>

```python
print(emp.filter(pl.col("Salary").is_between(45000, 60000)))
```
**Result:** 5 rows: **Rahul** (50000), **Neha** (45000), **Simran** (55000), **Vikas** (60000), **Anjali** (50000).
`is_between()` includes both ends by default. It's the same as `(pl.col("Salary") >= 45000) & (pl.col("Salary") <= 60000)`.
</details>

<details>
<summary><b>E5. Find IT employees earning more than 60000</b></summary>

```python
print(emp.filter((pl.col("Department") == "IT") & (pl.col("Salary") > 60000)))
```
**Result:** 3 rows: **Priya** (65000), **Rohit** (75000), **Pooja** (80000).
Each condition **must** be inside its own brackets when combined with `&`.
</details>

<details>
<summary><b>E6. Add a Bonus column equal to 10% of Salary</b></summary>

```python
print(emp.with_columns((pl.col("Salary") * 0.10).alias("Bonus")))
```
**Result:** a 7th column `Bonus` (f64). For example, Rahul gets 5000.0 and Pooja gets 8000.0.
</details>

<details>
<summary><b>E7. Find the maximum experience in each department</b></summary>

```python
print(
    emp.group_by("Department")
    .agg(pl.col("Experience").max().alias("Max_Experience"))
    .sort("Department")
)
```
**Result**
```
┌────────────┬────────────────┐
│ Department ┆ Max_Experience │
╞════════════╪════════════════╡
│ Finance    ┆ 10             │
│ HR         ┆ 6              │
│ IT         ┆ 8              │
│ Sales      ┆ 4              │
└────────────┴────────────────┘
```
</details>

### Project 02 – Sales answers

<details>
<summary><b>S1. Show all orders from Delhi</b></summary>

```python
print(sales.filter(pl.col("City") == "Delhi"))
```
**Result:** 4 orders: 1001 (Laptop), 1003 (Keyboard), 1006 (Mobile), 1009 (Mouse).
</details>

<details>
<summary><b>S2. Count the number of orders in each city</b></summary>

```python
print(
    sales.group_by("City")
    .agg(pl.len().alias("Total_Orders"))
    .sort("City")
)
```
**Result**
```
┌────────┬──────────────┐
│ City   ┆ Total_Orders │
╞════════╪══════════════╡
│ Delhi  ┆ 4            │
│ Mumbai ┆ 2            │
│ Noida  ┆ 4            │
└────────┴──────────────┘
```
</details>

<details>
<summary><b>S3. Find the best-selling product by quantity</b></summary>

```python
print(
    sales.group_by("Product")
    .agg(pl.col("Quantity").sum().alias("Total_Quantity"))
    .sort("Total_Quantity", descending=True)
    .head(1)
)
```
**Result:** **Mouse**, 16 units.
</details>

<details>
<summary><b>S4. Find Electronics orders with Quantity of 2 or more</b></summary>

```python
print(
    sales.filter(
        (pl.col("Category") == "Electronics") & (pl.col("Quantity") >= 2)
    )
)
```
**Result:** 5 orders: 1001, 1002, 1006, 1007, 1010. Order 1005 (Laptop, quantity 1) is excluded.
</details>

<details>
<summary><b>S5. Add a GST column (18%) and a Final_Amount column</b></summary>

```python
print(
    sales.with_columns(
        (pl.col("Revenue") * 0.18).alias("GST")
    ).with_columns(
        (pl.col("Revenue") + pl.col("GST")).alias("Final_Amount")
    ).select("Order_ID", "Product", "Revenue", "GST", "Final_Amount")
)
```
**Result (first 3 rows)**
```
┌──────────┬──────────┬─────────┬─────────┬──────────────┐
│ Order_ID ┆ Product  ┆ Revenue ┆ GST     ┆ Final_Amount │
╞══════════╪══════════╪═════════╪═════════╪══════════════╡
│ 1001     ┆ Laptop   ┆ 100000  ┆ 18000.0 ┆ 118000.0     │
│ 1002     ┆ Mobile   ┆ 60000   ┆ 10800.0 ┆ 70800.0      │
│ 1003     ┆ Keyboard ┆ 5000    ┆ 900.0   ┆ 5900.0       │
└──────────┴──────────┴─────────┴─────────┴──────────────┘
```
Why two `with_columns()` calls? `Final_Amount` uses the `GST` column, and a column must exist **before** another expression can refer to it.
</details>

<details>
<summary><b>S6. Find the minimum, maximum and average Revenue in one table</b></summary>

```python
print(
    sales.select(
        pl.col("Revenue").min().alias("Min_Revenue"),
        pl.col("Revenue").max().alias("Max_Revenue"),
        pl.col("Revenue").mean().alias("Avg_Revenue"),
    )
)
```
**Result**
```
┌─────────────┬─────────────┬─────────────┐
│ Min_Revenue ┆ Max_Revenue ┆ Avg_Revenue │
╞═════════════╪═════════════╪═════════════╡
│ 3000        ┆ 100000      ┆ 34200.0     │
└─────────────┴─────────────┴─────────────┘
```
`alias()` is needed here. Without it, all three columns would be called "Revenue" and Polars would raise a duplicate-name error.
</details>

<details>
<summary><b>S7. City-wise report saved as city_report.csv</b></summary>

```python
city_report = (
    sales.group_by("City")
    .agg(
        pl.len().alias("Total_Orders"),
        pl.col("Quantity").sum().alias("Total_Quantity"),
        pl.col("Revenue").sum().alias("Total_Revenue"),
    )
    .sort("Total_Revenue", descending=True)
)
print(city_report)
city_report.write_csv("city_report.csv")
```
**Result**
```
┌────────┬──────────────┬────────────────┬───────────────┐
│ City   ┆ Total_Orders ┆ Total_Quantity ┆ Total_Revenue │
╞════════╪══════════════╪════════════════╪═══════════════╡
│ Delhi  ┆ 4            ┆ 15             ┆ 148000        │
│ Noida  ┆ 4            ┆ 18             ┆ 104000        │
│ Mumbai ┆ 2            ┆ 5              ┆ 90000         │
└────────┴──────────────┴────────────────┴───────────────┘
```
</details>

---

## 🚀 What to Learn Next

| Topic | Why it matters |
|---|---|
| **LazyFrame and lazy execution** | Polars plans and optimizes the whole query before running it, which is much faster on big data |
| **`scan_csv()` vs `read_csv()`** | `scan_csv()` reads lazily, so it can handle files bigger than your RAM |
| **Polars expressions** | Conditional columns (`pl.when().then().otherwise()`), string and date functions |
| **Joins and concatenation** | Combine tables, e.g. orders + customers |
| **Handling missing values** | `null_count()`, `fill_null()`, `drop_nulls()` |
| **Working with large datasets** | Streaming and memory-efficient processing |
| **Parquet file processing** | A compressed, column-based format, much faster than CSV |
| **Pandas vs Polars performance** | Polars is multi-threaded and written in Rust, so it is often several times faster |

**A taste of lazy execution:**

```python
result = (
    pl.scan_csv("employees.csv")          # nothing is read yet
    .filter(pl.col("Salary") > 50000)
    .select("Name", "Salary")
    .collect()                            # now Polars runs the optimized query
)
```

### 🏭 Industry connection

Before an AI/ML model can be trained, data has to be **loaded, cleaned, filtered, transformed and analyzed**. Polars performs these data-processing steps quickly, even on millions of rows. These two projects show the same workflow analysts use every day: **read → clean → transform → aggregate → report**.

---

<p align="center"><b>🐻‍❄️ End of Polars Industry Projects · Happy Analyzing!</b></p>
