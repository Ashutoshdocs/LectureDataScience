"""
STEP 6 - Handle missing values.

Input:
    outputs/step5_emails_booleans.csv

Output:
    outputs/step6_no_missing.csv

Run after step 5.
"""

from pathlib import Path

import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "outputs" / "step5_emails_booleans.csv"
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

df = pd.read_csv(INPUT_FILE, parse_dates=["join_date"])

# Review missing values before filling them.
print("Missing values BEFORE:")
print(df.isna().sum())

# Fill missing ages with the median age of the dataset.
df["age"] = df["age"].fillna(df["age"].median())

# Fill missing salaries with the median salary in each department.
df["salary"] = (
    df.groupby("department")["salary"]
    .transform(lambda values: values.fillna(values.median()))
)

# If a department has no usable median, use the overall salary median.
df["salary"] = df["salary"].fillna(df["salary"].median())

# Use a clear placeholder for missing text categories.
df["city"] = df["city"].fillna("Unknown")
df["department"] = df["department"].fillna("Unknown")

# Treat a missing activity status as False, then make the column boolean.
df["is_active"] = df["is_active"].fillna(False).astype(bool)

# Email and join_date are left missing when unknown; do not guess them.
print("Missing values AFTER:")
print(df.isna().sum())

# Save the data after handling the selected missing values.
output_file = OUTPUT_DIR / "step6_no_missing.csv"
df.to_csv(output_file, index=False)
print(f"Saved: {output_file}")
