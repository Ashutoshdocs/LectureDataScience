# 🧪 CSV Playground

A Streamlit app for exploring CSV files with Python. Upload a CSV, look through your data, run **pandas**, **NumPy** and file-handling code against it, see the output on screen, and download the results.

---

## ✨ Features

- **CSV upload**: drag and drop a `.csv` file, with options for the delimiter (`,` `;` tab `|`), the encoding (`utf-8`, `latin-1`, `utf-16`) and the header row.
- **Data preview**
  - Summary cards for file name, rows, columns and missing cells
  - **Table** tab with an adjustable row count (up to 1,000)
  - **Column info** tab showing type, non-null count, nulls, unique values and a sample value
  - **Statistics** tab showing `df.describe()` for every column
- **Live Python editor**: your data is already loaded, so you can start writing code straight away.
- **Output panel**: printed output and full error messages appear in a console panel, along with how long the code took to run.
- **Downloads**
  - `result` as CSV (or `.txt` for values that aren't tables)
  - Console output as `.txt`
  - The current, possibly modified `df` as CSV
  - Any file your code saves into the workspace
- **Ready-made snippets**: overview, NumPy statistics, data cleaning, group-by, file handling and filtering
- **Run history**: the last 15 runs, each of which you can load back into the editor
- **Reset**: go back to the originally uploaded data at any time

---

## 🚀 Getting started

### Requirements
- Python 3.9+
- Streamlit 1.50 or newer

### Install

```bash
pip install "streamlit>=1.50" pandas numpy
```

Or with a virtual environment:

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install "streamlit>=1.50" pandas numpy
```

### Run

```bash
streamlit run app.py
```

The app opens at **http://localhost:8501**.

---

## 🐍 Writing code

These names are ready to use in the editor:

| Name          | What it is                                                    |
|---------------|---------------------------------------------------------------|
| `df`          | Your working DataFrame (changes are kept between runs)        |
| `original_df` | An untouched copy of the uploaded file                        |
| `pd`          | pandas                                                        |
| `np`          | NumPy                                                         |
| `os`, `io`    | Standard-library modules for working with files               |
| `WORKDIR`     | A temporary folder for files you create (it's also the current directory while your code runs) |
| `result`      | Assign to this to show a table or value and make it downloadable |

### Rules
- `print(...)` sends output to the console panel.
- `result = ...` shows a DataFrame, Series, NumPy array or any other value.
- If your code changes `df`, the change carries over to the next run. Use **Reset data to original** in the sidebar to undo all changes.
- Files written with relative paths (for example `df.to_csv("out.csv")`) are saved in the workspace and listed under **Workspace files** for download.

### Examples

**Quick overview**
```python
print(df.shape)
print(df.isna().sum())
result = df.describe(include="all").T
```

**NumPy statistics**
```python
num = df.select_dtypes(include=np.number)
result = pd.DataFrame({
    "mean": np.nanmean(num, axis=0),
    "std":  np.nanstd(num, axis=0),
}, index=num.columns)
```

**Clean the data**
```python
df = df.drop_duplicates()
df = df.fillna(df.median(numeric_only=True))
result = df
```

**File handling**
```python
df.head(20).to_csv("top_rows.csv", index=False)

with open("report.txt", "w") as f:
    f.write(f"Rows: {len(df)}\nColumns: {list(df.columns)}")

print(os.listdir(WORKDIR))
result = pd.read_csv("top_rows.csv")
```

**Group and aggregate**
```python
result = df.groupby("category")["sales"].agg(["sum", "mean", "count"])
```

---

## 📁 Project structure

```
.
├── app.py       # The Streamlit app
└── README.md    # This file
```

---

## ⚠️ Security note

The editor runs **any Python code you type**, with the same access to your computer as the user who started the app. That's fine for local, personal use. **Don't put this app on a public or shared server as it is**, because anyone who opens it could run commands on that machine.

---

## 🛠️ Troubleshooting

| Problem | Fix |
|---|---|
| `UnicodeDecodeError` when uploading | Change **Encoding** to `latin-1` in *Read options* |
| All data ends up in one column | Change the **Delimiter** (for example `;`) |
| Column names look like data | Turn on or off **First row is header** |
| `TypeError` about `width` | Upgrade Streamlit: `pip install -U streamlit` |
| A snippet fails on your file | Some snippets expect at least one numeric and one text column; adjust the column names |
