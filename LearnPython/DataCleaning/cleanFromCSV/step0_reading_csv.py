"""
STEP 0 - Read a CSV file and inspect the data.

Input:
    raw_data.csv

Outputs:
    outputs/step0_report.txt

Run this script first. It inspects the raw CSV before cleaning begins.
"""

from pathlib import Path

import numpy as np
import pandas as pd

# Build paths relative to this script so it works from any current directory.
BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "raw_data.csv"
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

# 1. Read the CSV as plain text to inspect its raw lines.
with INPUT_FILE.open(encoding="utf-8") as file:
    lines = file.readlines()

print(len(lines), "lines (1 header + data rows)")
for line in lines[:4]:
    # repr() makes spaces and newline characters visible.
    print(repr(line))

# 2. Read the CSV into a pandas DataFrame (a table).
pd.set_option("display.max_columns", None)
df = pd.read_csv(INPUT_FILE)
print(df.head(10))

# 3. Inspect the number of rows, columns, data types, and missing values.
print("Shape:", df.shape)
df.info()

print("Missing values per column:")
print(df.isna().sum())

# Count exact duplicate rows.
print("Duplicate rows:", df.duplicated().sum())

# Inspect columns that may contain inconsistent text values.
for column in ["city", "department", "is_active"]:
    print(f"\n{column}:", df[column].unique())

# 4. Save a simple inspection report.
report_file = OUTPUT_DIR / "step0_report.txt"
with report_file.open("w", encoding="utf-8") as file:
    file.write(f"Rows, columns: {df.shape}\n")
    file.write(f"Duplicate rows: {df.duplicated().sum()}\n\n")
    file.write("Missing values per column:\n")
    file.write(df.isna().sum().to_string())

print(report_file.read_text(encoding="utf-8"))
print(f"Saved report: {report_file}")
