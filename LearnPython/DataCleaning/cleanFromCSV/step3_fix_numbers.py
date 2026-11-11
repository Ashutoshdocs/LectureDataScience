"""
STEP 3 - Fix numeric columns such as age and salary.

Input:
    outputs/step2_clean_text.csv

Output:
    outputs/step3_fixed_numbers.csv

Run after step 2.
"""

from pathlib import Path

import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "outputs" / "step2_clean_text.csv"
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

df = pd.read_csv(INPUT_FILE)

# Inspect age values before converting them.
print("Age values BEFORE:", df["age"].unique())

# Convert age values to numbers. Invalid text such as 'thirty' becomes NaN.
df["age"] = pd.to_numeric(df["age"], errors="coerce")

# Treat ages outside the expected range as missing values.
df.loc[~df["age"].between(18, 70), "age"] = np.nan

# Convert salary to text first, then remove currency symbols, commas, and spaces.
df["salary"] = (
    df["salary"]
    .astype(str)
    .str.replace(r"[₹,\s]", "", regex=True)
)

# Convert cleaned salary text into numbers. Invalid values become NaN.
df["salary"] = pd.to_numeric(df["salary"], errors="coerce")

# Treat salaries above this threshold as unrealistic outliers.
df.loc[df["salary"] > 500000, "salary"] = np.nan

# Review the cleaned numeric columns.
print(df[["age", "salary"]].describe())

# Save the fixed numeric data for step 4.
output_file = OUTPUT_DIR / "step3_fixed_numbers.csv"
df.to_csv(output_file, index=False)
print(f"Saved: {output_file}")
