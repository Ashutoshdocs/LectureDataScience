# 🐍 Python Dask – 20 Basic Practical Labs

Hands-on labs for learning **Dask DataFrames** straight from the Python Shell (interactive mode), with **no extra variables**: each lab is a single command you can type and run.

> All commands and outputs in this guide were tested on **Dask 2026.8.0** with **Pandas 3.0.5**. Your output may look slightly different on other versions.

---

## 📁 What's in this folder

| File | Use it for |
|---|---|
| `README.md` | This guide: theory, commands, expected outputs, explanations |
| `commands.txt` | Copy-and-paste sheet of every command, in order |
| `run_all_labs.py` | Runs all 20 labs in one go and prints the results (the instructor's reference run) |
| `requirements.txt` | Dependency list for `pip install -r requirements.txt` |

---

## 📚 Table of Contents

- [What is Dask?](#-what-is-dask)
- [Setup](#%EF%B8%8F-setup)
- [Part A – Creating & Exploring Data (Labs 1–6)](#part-a--creating--exploring-data-labs-16)
- [Part B – Filtering (Labs 7–8)](#part-b--filtering-labs-78)
- [Part C – Aggregations (Labs 9–13)](#part-c--aggregations-labs-913)
- [Part D – Sorting & Grouping (Labs 14–15)](#part-d--sorting--grouping-labs-1415)
- [Part E – Working with CSV Files (Labs 16–19)](#part-e--working-with-csv-files-labs-1619)
- [Part F – Mini Project: Salary Report (Lab 20)](#part-f--mini-project-salary-report-lab-20)
- [Key Concept: Lazy Execution](#-key-concept-lazy-execution)
- [Quick Revision Cheat Sheet](#-quick-revision-cheat-sheet)
- [Practice Exercises](#-practice-exercises)
- [Troubleshooting](#-troubleshooting)

---

## 🤔 What is Dask?

**Dask** is a Python library for **parallel and larger-than-memory computing**. A Dask DataFrame looks and feels like a Pandas DataFrame, but under the hood it is split into many smaller Pandas DataFrames called **partitions**.

```
            Dask DataFrame
 ┌────────────────────────────────────┐
 │ Partition 0  →  Rahul 25, Amit 30  │  ← a normal Pandas DataFrame
 │ Partition 1  →  Priya 28           │  ← a normal Pandas DataFrame
 └────────────────────────────────────┘
```

Two ideas run through every lab:

1. **Partitions.** Data is split into chunks that can be processed in parallel.
2. **Lazy execution.** Dask first *plans* the work (it builds a task graph) and only *does* the work when you call `.compute()`.

> 💡 The labs use tiny datasets so you can check every answer by eye. Dask pays off on datasets that are too big or too slow for plain Pandas.

---

## ⚙️ Setup

### Step 1: Install Dask (in your **system terminal**, not inside Python)

```bash
pip install "dask[dataframe]"
```

### Step 2: Open the Python Shell

```bash
python
```

### Step 3: Run these imports once at the start of every session

```python
>>> import dask
>>> import dask.dataframe as dd
>>> import pandas as pd
```

> ⚠️ **Don't type `>>>`.** That is the Python prompt. Type only what comes after it.

---

## Part A – Creating & Exploring Data (Labs 1–6)

### Lab 1 – Check Dask Version

**Purpose:** Check which Dask version is installed.

```python
>>> dask.__version__
```

**Expected output (example):**
```
'2026.8.0'
```

**Explanation:** `__version__` holds the installed version. Yours depends on when you installed Dask.

---

### Lab 2 – Create a Dask DataFrame

**Purpose:** Create a Dask DataFrame from a small Pandas DataFrame and display it.

```python
>>> dd.from_pandas(pd.DataFrame({"Name":["Rahul","Amit","Priya"],"Age":[25,30,28]}), npartitions=2).compute()
```

**Expected output:**
```
    Name  Age
0  Rahul   25
1   Amit   30
2  Priya   28
```

**Explanation:**
- `pd.DataFrame({...})` creates a Pandas DataFrame from a dictionary.
- `dd.from_pandas(...)` converts it into a Dask DataFrame.
- `npartitions=2` splits the data into **2 partitions**.
- `.compute()` runs the Dask task and returns a normal Pandas result.

---

### Lab 3 – Check Number of Partitions

**Purpose:** Find how many partitions the Dask DataFrame has.

```python
>>> dd.from_pandas(pd.DataFrame({"Name":["Rahul","Amit","Priya"]}), npartitions=2).npartitions
```

**Expected output:**
```
2
```

**Explanation:** A partition is one chunk of a Dask DataFrame. Dask can process partitions independently and in parallel, which is how it handles large workloads. `npartitions` is an **attribute**, not a method, so it has no `()`.

---

### Lab 4 – Display First Two Records

**Purpose:** Display the first two records.

```python
>>> dd.from_pandas(pd.DataFrame({"Name":["Rahul","Amit","Priya"],"Age":[25,30,28]}), npartitions=2).head(2)
```

**Expected output:**
```
    Name  Age
0  Rahul   25
1   Amit   30
```

**Explanation:** `head(2)` shows the first 2 rows. Unlike most Dask methods, `head()` **computes automatically**, so you don't need `.compute()`.

---

### Lab 5 – Display Last Two Records

**Purpose:** Display the last two records.

```python
>>> dd.from_pandas(pd.DataFrame({"Name":["Rahul","Amit","Priya"],"Age":[25,30,28]}), npartitions=1).tail(2)
```

**Expected output:**
```
    Name  Age
1   Amit   30
2  Priya   28
```

**Explanation:** `tail(2)` shows the last 2 rows. Like `head()`, it computes automatically.

> ⚠️ **Teaching moment: `head()` and `tail()` only look at ONE partition.**
> `head()` reads only the **first** partition and `tail()` reads only the **last** one. Run the same command with `npartitions=2`:
>
> ```python
> >>> dd.from_pandas(pd.DataFrame({"Name":["Rahul","Amit","Priya"],"Age":[25,30,28]}), npartitions=2).tail(2)
> ```
> ```
>     Name  Age
> 2  Priya   28
> ```
> You get **only 1 row**. With 3 rows in 2 partitions, the split is `[Rahul, Amit]` + `[Priya]`, and the last partition holds only Priya. That's why this lab uses `npartitions=1`. Dask does this on purpose: it avoids scanning the whole dataset just to show a few rows.

---

### Lab 6 – Display Only the Name Column

**Purpose:** Select and display one column.

```python
>>> dd.from_pandas(pd.DataFrame({"Name":["Rahul","Amit","Priya"],"Age":[25,30,28]}), npartitions=2)["Name"].compute()
```

**Expected output** (dtype wording can vary by version, e.g. `object` on older ones):
```
0    Rahul
1     Amit
2    Priya
Name: Name, dtype: string
```

**Explanation:** `["Name"]` selects only the Name column (a Dask **Series**). `.compute()` runs the selection and returns the result.

---

## Part B – Filtering (Labs 7–8)

### Lab 7 – Filter Age Greater Than 25

**Purpose:** Find employees older than 25.

```python
>>> dd.from_pandas(pd.DataFrame({"Name":["Rahul","Amit","Priya"],"Age":[25,30,28]}), npartitions=2).query("Age > 25").compute()
```

**Expected output:**
```
    Name  Age
1   Amit   30
2  Priya   28
```

**Explanation:** `query("Age > 25")` keeps only the rows where the condition is true. Rahul (25) is dropped because 25 is not *greater than* 25.

---

### Lab 8 – Filter Age Less Than 30

**Purpose:** Find employees younger than 30.

```python
>>> dd.from_pandas(pd.DataFrame({"Name":["Rahul","Amit","Priya"],"Age":[25,30,28]}), npartitions=2).query("Age < 30").compute()
```

**Expected output:**
```
    Name  Age
0  Rahul   25
2  Priya   28
```

**Explanation:** `query("Age < 30")` keeps rows where Age is less than 30. Notice the **original index** (0, 2) is kept.

---

## Part C – Aggregations (Labs 9–13)

### Lab 9 – Calculate Total Salary

```python
>>> dd.from_pandas(pd.DataFrame({"Salary":[30000,40000,50000]}), npartitions=2)["Salary"].sum().compute()
```

**Expected output:**
```
120000
```

**Explanation:** `sum()` *plans* the total and `.compute()` *calculates* it. Dask sums each partition separately, then adds the partial sums together.

---

### Lab 10 – Calculate Average Salary

```python
>>> dd.from_pandas(pd.DataFrame({"Salary":[30000,40000,50000]}), npartitions=2)["Salary"].mean().compute()
```

**Expected output:**
```
40000.0
```

**Explanation:** `mean()` calculates the average. The result is a **float** (`40000.0`) because an average can have decimals.

---

### Lab 11 – Find Maximum Salary

```python
>>> dd.from_pandas(pd.DataFrame({"Salary":[30000,40000,50000]}), npartitions=2)["Salary"].max().compute()
```

**Expected output:**
```
50000
```

**Explanation:** `max()` finds the largest value in the column.

---

### Lab 12 – Find Minimum Salary

```python
>>> dd.from_pandas(pd.DataFrame({"Salary":[30000,40000,50000]}), npartitions=2)["Salary"].min().compute()
```

**Expected output:**
```
30000
```

**Explanation:** `min()` finds the smallest value in the column.

---

### Lab 13 – Count Employee Names

```python
>>> dd.from_pandas(pd.DataFrame({"Name":["Rahul","Amit","Priya","Neha"]}), npartitions=2)["Name"].count().compute()
```

**Expected output:**
```
4
```

**Explanation:** `count()` counts **non-null** values. Missing values (`None`/`NaN`) are not counted.

---

## Part D – Sorting & Grouping (Labs 14–15)

### Lab 14 – Sort Employees by Salary

```python
>>> dd.from_pandas(pd.DataFrame({"Name":["Rahul","Amit","Priya"],"Salary":[30000,50000,40000]}), npartitions=2).sort_values("Salary").compute()
```

**Expected output:**
```
    Name  Salary
0  Rahul   30000
2  Priya   40000
1   Amit   50000
```

**Explanation:** `sort_values("Salary")` sorts rows by Salary in **ascending** order (the default). For descending order, add `ascending=False`.

---

### Lab 15 – Group Employees by Department

**Purpose:** Calculate the total salary for each department.

```python
>>> dd.from_pandas(pd.DataFrame({"Department":["IT","HR","IT","HR"],"Salary":[30000,20000,40000,25000]}), npartitions=2).groupby("Department")["Salary"].sum().compute()
```

**Expected output:**
```
Department
HR    45000
IT    70000
Name: Salary, dtype: int64
```

**Explanation:**
- `groupby("Department")` puts rows with the same department together.
- `["Salary"].sum()` adds up the salaries within each group.
- HR = 20000 + 25000 = **45000**, IT = 30000 + 40000 = **70000**.

---

## Part E – Working with CSV Files (Labs 16–19)

> 📂 Files are created in your **current working directory** (the folder you were in when you typed `python`). To check where that is:
> `>>> import os; os.getcwd()`

### Lab 16 – Create a CSV File

```python
>>> pd.DataFrame({"Name":["Rahul","Amit","Priya"],"Age":[25,30,28]}).to_csv("employees.csv", index=False)
```

**Expected output:** Nothing is printed. The file `employees.csv` is created.

**Explanation:** `to_csv()` writes the DataFrame to a file. `index=False` stops Pandas from adding the row numbers as an extra column.

---

### Lab 17 – Read CSV Using Dask

```python
>>> dd.read_csv("employees.csv").compute()
```

**Expected output:**
```
    Name  Age
0  Rahul   25
1   Amit   30
2  Priya   28
```

**Explanation:** `dd.read_csv()` reads the file as a Dask DataFrame, and `.compute()` loads and displays it. `dd.read_csv` also accepts wildcards such as `"data/*.csv"` to read **many files at once**.

---

### Lab 18 – Check Partitions in the CSV

```python
>>> dd.read_csv("employees.csv").npartitions
```

**Expected output:**
```
1
```

**Explanation:** A small file is read as a single partition. The number of partitions depends on file size and the `blocksize` setting (for example, `dd.read_csv("big.csv", blocksize="64MB")`).

---

### Lab 19 – Save Dask DataFrame into CSV

```python
>>> dd.read_csv("employees.csv").to_csv("dask_output/employee-*.csv", index=False)
```

**Expected output:** A list of the files it created (the full path depends on your folder):
```
['/your/folder/dask_output/employee-0.csv']
```

**Explanation:** Dask writes **one file per partition**, and the `*` is replaced by the partition number (0, 1, 2…). The `dask_output` folder is created automatically if it doesn't exist.

---

## Part F – Mini Project: Salary Report (Lab 20)

**Purpose:** Build a full employee salary report.

**Dataset:**

| Name | Salary |
|---|---|
| Rahul | 30000 |
| Amit | 40000 |
| Priya | 35000 |
| Neha | 45000 |

| Report item | Command | Expected output |
|---|---|---|
| Total employees | `...["Name"].count().compute()` | `4` |
| Total salary | `...["Salary"].sum().compute()` | `150000` |
| Average salary | `...["Salary"].mean().compute()` | `37500.0` |
| Highest salary | `...["Salary"].max().compute()` | `45000` |
| Lowest salary | `...["Salary"].min().compute()` | `30000` |

Full commands:

```python
>>> dd.from_pandas(pd.DataFrame({"Name":["Rahul","Amit","Priya","Neha"],"Salary":[30000,40000,35000,45000]}), npartitions=2)["Name"].count().compute()
>>> dd.from_pandas(pd.DataFrame({"Name":["Rahul","Amit","Priya","Neha"],"Salary":[30000,40000,35000,45000]}), npartitions=2)["Salary"].sum().compute()
>>> dd.from_pandas(pd.DataFrame({"Name":["Rahul","Amit","Priya","Neha"],"Salary":[30000,40000,35000,45000]}), npartitions=2)["Salary"].mean().compute()
>>> dd.from_pandas(pd.DataFrame({"Name":["Rahul","Amit","Priya","Neha"],"Salary":[30000,40000,35000,45000]}), npartitions=2)["Salary"].max().compute()
>>> dd.from_pandas(pd.DataFrame({"Name":["Rahul","Amit","Priya","Neha"],"Salary":[30000,40000,35000,45000]}), npartitions=2)["Salary"].min().compute()
```

> 💡 **Tip for after the course:** In real projects you would store the DataFrame in a variable once (`df = dd.from_pandas(...)`) instead of rebuilding it every time. These labs avoid variables only so each command stands on its own.

---

## 🧠 Key Concept: Lazy Execution

Many Dask operations are **lazy**: Dask builds a *task graph* (a plan) and doesn't calculate anything until you call `.compute()`.

**Without `.compute()`, you get a plan, not a number:**

```python
>>> dd.from_pandas(pd.DataFrame({"Salary":[30000,40000,50000]}), npartitions=2)["Salary"].sum()
```
```
<dask_expr.expr.Scalar: expr=df['Salary'].sum(), dtype=int64>
```

**With `.compute()`, you get the answer:**

```python
>>> dd.from_pandas(pd.DataFrame({"Salary":[30000,40000,50000]}), npartitions=2)["Salary"].sum().compute()
```
```
120000
```

```
  Your code           Task graph (plan)              .compute()
 ───────────   →   ┌──────────────────────┐   →   ───────────────
  .sum()           │ sum(part 0) ─┐       │        actual result
                   │              ├─ add  │          120000
                   │ sum(part 1) ─┘       │
                   └──────────────────────┘
```

**Why be lazy?** Dask can look at the whole plan, optimize it, and run independent pieces in parallel before doing any real work.

| Needs `.compute()` | Computes automatically |
|---|---|
| `sum()`, `mean()`, `max()`, `min()`, `count()` | `head()` |
| `query()`, `sort_values()`, `groupby()` | `tail()` |
| Selecting columns `["Name"]` | `to_csv()` (writes immediately) |

---

## 📋 Quick Revision Cheat Sheet

| Function / Attribute | What it does |
|---|---|
| `dd.from_pandas(df, npartitions=n)` | Convert a Pandas DataFrame into a Dask DataFrame |
| `dd.read_csv("file.csv")` | Read a CSV file (or many, with `*`) |
| `.compute()` | Run a lazy Dask computation |
| `.head(n)` | First *n* rows (first partition only) |
| `.tail(n)` | Last *n* rows (last partition only) |
| `["col"]` | Select a column |
| `.query("condition")` | Filter rows |
| `.sum()` | Total |
| `.mean()` | Average |
| `.max()` / `.min()` | Maximum / Minimum |
| `.count()` | Count non-null values |
| `.sort_values("col")` | Sort rows |
| `.groupby("col")` | Group rows |
| `.to_csv("out-*.csv")` | Save to CSV (one file per partition) |
| `.npartitions` | Number of partitions |

---

## ✍️ Practice Exercises

Try these on your own. Answers are in the collapsed section below.

1. Create a Dask DataFrame with 4 cities and their populations, split into 2 partitions, and display it.
2. Find employees with Age **between 26 and 29**.
3. Sort the Lab 14 data by Salary in **descending** order.
4. Find the **average** salary per department using the Lab 15 data.
5. Read `employees.csv` and display only the `Age` column.

<details>
<summary>👉 Show answers</summary>

```python
# 1
dd.from_pandas(pd.DataFrame({"City":["Delhi","Mumbai","Pune","Jaipur"],"Population":[32,21,7,4]}), npartitions=2).compute()

# 2
dd.from_pandas(pd.DataFrame({"Name":["Rahul","Amit","Priya"],"Age":[25,30,28]}), npartitions=2).query("Age > 26 and Age < 29").compute()

# 3
dd.from_pandas(pd.DataFrame({"Name":["Rahul","Amit","Priya"],"Salary":[30000,50000,40000]}), npartitions=2).sort_values("Salary", ascending=False).compute()

# 4
dd.from_pandas(pd.DataFrame({"Department":["IT","HR","IT","HR"],"Salary":[30000,20000,40000,25000]}), npartitions=2).groupby("Department")["Salary"].mean().compute()

# 5
dd.read_csv("employees.csv")["Age"].compute()
```
</details>

---

## 🛠️ Troubleshooting

| Problem | Cause & Fix |
|---|---|
| `ModuleNotFoundError: No module named 'dask'` | Dask isn't installed in this Python. Run `pip install "dask[dataframe]"` in the terminal (try `python -m pip install ...` if you have several Pythons). |
| `ImportError` mentioning pandas/pyarrow | You installed plain `dask`. Reinstall with the `[dataframe]` extra, keeping the quotes. |
| `SyntaxError` when pasting | You copied the `>>>` or curly quotes (`“ ”`). Use straight quotes `" "` only. |
| `pip` gives `SyntaxError` | You ran `pip` *inside* Python. Type `exit()` first, then run it in the terminal. |
| `FileNotFoundError: employees.csv` | Run Lab 16 first, and in the same folder. |
| `tail(2)` shows only 1 row | Expected Dask behavior: see the note in [Lab 5](#lab-5--display-last-two-records). |
| You see `<dask_expr...>` instead of a value | You forgot `.compute()`. |

---

## ▶️ Run Everything at Once (for instructors)

```bash
pip install -r requirements.txt
python run_all_labs.py
```

This prints every lab's command and output. Use it to check your environment before class.

---

**🎉 End of 20 Dask Practical Labs. Happy learning!**
