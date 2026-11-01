# 🧹 Panama Tech Academy — Data Cleaning with pandas, Step by Step

Learn to **read a messy CSV file and clean it with pandas**, one small step at a time.
**Every step reads a file, does one job, and writes a new output file**, so you can open it and see exactly what changed.

---

## 📁 Start With These Files

| File | What it is |
|---|---|
| `raw_data.csv` | Messy employee data, 104 rows (the only data file you need) |
| `step0_reading_csv.ipynb` … `step8_summary.ipynb` | One notebook per step |
| `README.md` | This guide |

The `outputs/` folder is **created for you** when you run step 0. Every other file lands there.

---

## 🧨 What's Messy in `raw_data.csv`

| Column | Problems |
|---|---|
| `id` | 4 duplicate rows |
| `name` | Extra spaces, mixed case (`priya patel`, `SNEHA IYER`) |
| `age` | Text (`thirty`), impossible values (`-5`, `150`), blanks |
| `city` | `pune`, `PUNE `, `Bengaluru` vs `Bangalore`, `New Delhi` vs `Delhi` |
| `department` | Trailing spaces, mixed case, blanks |
| `salary` | Currency text (`₹45,000`), outliers (`9999999`), blanks |
| `join_date` | 4 formats: `2023-01-15`, `15/02/2023`, `2023.03.20`, `March 5 2023` |
| `email` | Invalid addresses (`user5@example`), blanks |
| `is_active` | `Y`, `yes`, `1`, `N`, `no`, `0`, blank |

---

## 🔁 The Flow

```
raw_data.csv
   │ step 0  read & inspect             ─▶ outputs/step0_report.txt
   │ step 1  remove duplicates          ─▶ outputs/step1_no_duplicates.csv
   │ step 2  clean text                 ─▶ outputs/step2_clean_text.csv
   │ step 3  fix age & salary           ─▶ outputs/step3_fixed_numbers.csv
   │ step 4  parse dates                ─▶ outputs/step4_dates.csv
   │ step 5  emails & yes/no            ─▶ outputs/step5_emails_booleans.csv
   │ step 6  fill missing values        ─▶ outputs/step6_no_missing.csv
   │ step 7  structure & export         ─▶ outputs/clean_data.csv + clean_data.json
   │ step 8  summary by department      ─▶ outputs/department_summary.csv
```

Each step reads the **previous step's output**, so run them **in order**.

---

## 🚀 Steps

**Setup (Anaconda)**
1. Install [Anaconda](https://www.anaconda.com/download) — pandas and numpy are included.
2. Put all files in one folder.
3. Open **Anaconda Navigator → Jupyter Notebook**, or in Anaconda Prompt:
   ```bash
   cd path/to/datacleaning-steps
   jupyter notebook
   ```
4. Open each notebook and run all cells (**Kernel → Restart & Run All**).

Requirements: Python 3.9+, pandas, numpy (`conda install pandas numpy` if needed).

### Step 0 — Read & inspect
Read the CSV as plain text with `open()`, then with `pd.read_csv` · `head()` · `shape` · `info()` · `isna().sum()` · `duplicated()` · `unique()`
**Output:** `step0_report.txt` — 104 rows, 9 columns, 4 duplicates, missing counts per column

### Step 1 — Remove duplicates
`drop_duplicates()` · `reset_index()` · `to_csv(index=False)`
**Output:** `step1_no_duplicates.csv` — 104 → **100 rows**

### Step 2 — Clean text
`str.strip()` · `str.title()` · `str.lower()` · `replace()` with a mapping
**Output:** `step2_clean_text.csv` — city variants 10 → **5** (Mumbai, Bangalore, Delhi, Pune, blank)

### Step 3 — Fix age & salary
`pd.to_numeric(errors="coerce")` · `between()` · regex `str.replace` to remove `₹` and commas · remove outliers
**Output:** `step3_fixed_numbers.csv` — ages now 21–60, salaries 25k–149k

### Step 4 — Parse dates
A function that tries each format · `apply()` · `NaT` for missing dates
**Output:** `step4_dates.csv` — every date is now `YYYY-MM-DD`

### Step 5 — Validate emails & fix yes/no
Regex with `str.match()` · `map()` to turn `Y`/`yes`/`1` into `True` and `N`/`no`/`0` into `False`
**Output:** `step5_emails_booleans.csv` — 10 invalid emails removed

### Step 6 — Handle missing values
Median for `age` · department median for `salary` (`groupby().transform()`) · `Unknown` for text · `False` for status · dates and emails stay missing because they can't be guessed
**Output:** `step6_no_missing.csv`

### Step 7 — Structure & export
`astype()` for proper types · `pd.cut()` for `salary_band` (Low / Medium / High) · `dt.year` for `join_year` · reorder & sort · `to_csv` and `to_json`
**Output:** `clean_data.csv` and `clean_data.json` — 100 rows, 11 columns
```json
{
    "id": 1,
    "name": "Sneha Iyer",
    "age": 28,
    "city": "Pune",
    "department": "Marketing",
    "salary": 122196.0,
    "salary_band": "High",
    "join_date": "2023-01-15T00:00:00.000",
    "join_year": 2023,
    "email": "user1@example.com",
    "is_active": true
}
```

### Step 8 — Summary by department
`groupby()` · `agg()` with count / mean / sum
**Output:** `department_summary.csv`

| department | employees | avg_age | avg_salary | active |
|---|---|---|---|---|
| Engineering | 18 | 43.1 | 90,558.8 | 8 |
| HR | 21 | 40.4 | 63,679.9 | 7 |
| Marketing | 9 | 46.0 | 108,458.3 | 5 |
| Sales | 36 | 39.2 | 92,247.3 | 18 |
| Unknown | 16 | 40.4 | 94,540.5 | 4 |

---

## 📊 Before vs After

| | Before | After |
|---|---|---|
| Rows | 104 | 100 |
| Duplicates | 4 | 0 |
| Missing ages / salaries | 32 / 31 (after removing bad values) | 0 / 0 |
| Date formats | 4 mixed | 1 |
| City variants | 10 | 5 |
| `is_active` values | 7 different | `True` / `False` |

---

## 💡 Practice

1. In step 3, change the age range to 20–65. How many more ages become missing?
2. In step 6, fill missing `age` with the **mean** instead of the median. Compare the results.
3. Add a `"Chennai"` row to `raw_data.csv` with messy spacing and re-run every step.
4. In step 8, also find the department with the highest average salary.

---

*Randomly generated sample data — no real people. Prepared for teaching by **Panama Tech Academy**.*
