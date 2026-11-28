# Python Pandas Data Cleaning – 9 Python Scripts

This project converts the nine provided notebook lessons (Steps 0–8) into regular `.py` files. Each script includes comments explaining the operations.

## Project structure

```text
python_pandas_data_cleaning_scripts/
├── raw_data.csv                  # You provide this input file
├── step0_reading_csv.py
├── step1_remove_duplicates.py
├── step2_clean_text.py
├── step3_fix_numbers.py
├── step4_parse_dates.py
├── step5_emails_booleans.py
├── step6_missing_values.py
├── step7_structure.py
├── step8_summary.py
├── requirements.txt
└── outputs/                      # Created automatically
```

## Requirements

Python 3. Install the required third-party libraries:

```bash
python3 -m pip install -r requirements.txt
```

The scripts use:
- `pandas` – read, inspect, clean, transform, and export tabular data.
- `numpy` – represent missing values and define an infinite upper salary band.

## Before running

1. Place your source file named `raw_data.csv` in the same directory as the Python scripts.
2. Ensure it contains the columns used by the lessons:

```text
id, name, age, city, department, salary, join_date, email, is_active
```

3. Run the scripts in order. Each step reads the output of the previous step.

## Run all steps in order

From the project directory:

```bash
python3 step0_reading_csv.py
python3 step1_remove_duplicates.py
python3 step2_clean_text.py
python3 step3_fix_numbers.py
python3 step4_parse_dates.py
python3 step5_emails_booleans.py
python3 step6_missing_values.py
python3 step7_structure.py
python3 step8_summary.py
```

On Windows, you can use `py` instead of `python3`.

## Step-by-step input and output

| Script | Reads | Creates |
|---|---|---|
| `step0_reading_csv.py` | `raw_data.csv` | `outputs/step0_report.txt` |
| `step1_remove_duplicates.py` | `raw_data.csv` | `outputs/step1_no_duplicates.csv` |
| `step2_clean_text.py` | `outputs/step1_no_duplicates.csv` | `outputs/step2_clean_text.csv` |
| `step3_fix_numbers.py` | `outputs/step2_clean_text.csv` | `outputs/step3_fixed_numbers.csv` |
| `step4_parse_dates.py` | `outputs/step3_fixed_numbers.csv` | `outputs/step4_dates.csv` |
| `step5_emails_booleans.py` | `outputs/step4_dates.csv` | `outputs/step5_emails_booleans.csv` |
| `step6_missing_values.py` | `outputs/step5_emails_booleans.csv` | `outputs/step6_no_missing.csv` |
| `step7_structure.py` | `outputs/step6_no_missing.csv` | `outputs/clean_data.csv`, `outputs/clean_data.json` |
| `step8_summary.py` | `outputs/clean_data.csv` | `outputs/department_summary.csv` |

## Important teaching notes

- The scripts are intended to be run in sequence because later steps depend on files produced by earlier steps.
- Every script creates the `outputs` directory if it does not already exist.
- File paths are based on the script's location, so you do not need to launch Python from a particular working directory.
- Step 6 intentionally leaves missing email addresses and join dates blank rather than guessing those values.
- The email regular expression in Step 5 checks a basic email-like format; it does not verify that an address exists.
- Step 7 uses the salary bands and column data types from the original lesson.

## Troubleshooting

**FileNotFoundError: raw_data.csv**
- Put `raw_data.csv` beside the `.py` files.

**FileNotFoundError for an outputs CSV**
- Run the scripts in numerical order. Do not skip an earlier step.

**ModuleNotFoundError: No module named 'pandas'**
- Install dependencies using `python3 -m pip install -r requirements.txt`.

**KeyError for a column**
- Check that your CSV has the expected column names listed above.
