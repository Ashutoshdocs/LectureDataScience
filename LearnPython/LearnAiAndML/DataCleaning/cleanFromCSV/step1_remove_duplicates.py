"""
STEP 1 - Remove duplicate rows.

Input:
    raw_data.csv

Output:
    outputs/step1_no_duplicates.csv

Run after step 0. This script starts again from the original raw CSV.
"""

from pathlib import Path

import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "raw_data.csv"
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

# Load the original data.
df = pd.read_csv(INPUT_FILE)
before = len(df)

# Remove rows that are exact duplicates.
df = df.drop_duplicates()

# Reset the row index to 0, 1, 2, ... after removing rows.
df = df.reset_index(drop=True)

print(f"Removed {before - len(df)} duplicates -> {len(df)} rows")

# Save the result without writing the pandas index as an extra column.
output_file = OUTPUT_DIR / "step1_no_duplicates.csv"
df.to_csv(output_file, index=False)
print(f"Saved: {output_file}")
