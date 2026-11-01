# Datacleaning – Demo Project

A beginner-friendly demo showing how to **clean and structure messy data with Python (pandas)** inside an **Anaconda Jupyter Notebook**.

## 📁 Project Files

| File | Description |
|------|-------------|
| `README.md` | This guide |
| `raw_data.csv` | Randomly generated, intentionally messy employee dataset (104 rows) |
| `Datacleaning.ipynb` | Jupyter notebook with all the Python cleaning & structuring steps |

Running the notebook creates two more files:

| Output | Description |
|--------|-------------|
| `clean_data.csv` | Cleaned, structured dataset (100 rows) |
| `department_summary.csv` | Summary statistics by department |

## 🧹 Problems in the Raw Data

| Column | Issues |
|--------|--------|
| `id` | Duplicate rows |
| `name` | Extra spaces, mixed case (`priya patel`, `SNEHA IYER`) |
| `age` | Text values (`thirty`), impossible values (`-5`, `150`), blanks |
| `city` | Inconsistent spelling/case (`pune`, `PUNE `, `Bengaluru` vs `Bangalore`) |
| `department` | Trailing spaces, mixed case, missing |
| `salary` | Currency symbols (`₹45,000`), outliers (`9999999`), blanks |
| `join_date` | Mixed formats (`2023-01-15`, `15/02/2023`, `2023.03.20`, `March 5 2023`) |
| `email` | Invalid addresses (`user5@example`), blanks |
| `is_active` | Mixed values (`Y`, `yes`, `1`, `N`, `no`, `0`, blank) |

## 🔧 Cleaning Steps in the Notebook

1. Import libraries (`pandas`, `numpy`)
2. Load `raw_data.csv`
3. Inspect – shape, dtypes, missing values, duplicates, unique values
4. Remove duplicate rows
5. Clean text – trim, title-case, standardise city names
6. Fix numeric columns – coerce text to numbers, remove invalid ages & salary outliers
7. Parse mixed date formats into proper `datetime`
8. Validate emails with regex; convert `is_active` to `True/False`
9. Handle missing values – median fill for numbers, `Unknown` for categories
10. Structure – set dtypes, add `salary_band` and `join_year`, reorder & sort
11. Summarise by department
12. Export clean CSV files

## 🚀 How to Run (Anaconda)

1. Install [Anaconda](https://www.anaconda.com/download) if you don't have it.
2. Put all files in the same folder.
3. Open **Anaconda Navigator → Jupyter Notebook** (or run in Anaconda Prompt):
   ```bash
   cd path/to/your/folder
   jupyter notebook
   ```
4. Open `Datacleaning.ipynb`.
5. Click **Kernel → Restart & Run All** (or run cells one by one with `Shift + Enter`).

### Requirements
- Python 3.9+
- pandas, numpy (both included with Anaconda)

```bash
# Only if needed:
conda install pandas numpy
```

## 📊 Result

| | Before | After |
|---|---|---|
| Rows | 104 | 100 |
| Duplicates | 4 | 0 |
| Missing ages/salaries | Many | 0 |
| Date formats | 4 mixed | 1 (`datetime`) |
| City variants | 10 | 5 clean values |

## 📝 License
Free to use for learning and demos. All data is randomly generated – no real people.
