"""
STEP 7 - Set data types, add useful columns, and export clean data.

Input:
    outputs/step6_no_missing.csv

Outputs:
    outputs/clean_data.csv
    outputs/clean_data.json

Run after step 6.
"""

from pathlib import Path

import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "outputs" / "step6_no_missing.csv"
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

df = pd.read_csv(INPUT_FILE, parse_dates=["join_date"])

# Assign appropriate data types to the columns.
df = df.astype({
    "id": "int64",             # Whole-number identifier.
    "age": "int64",            # Whole-number age.
    "salary": "float64",       # Numeric salary.
    "is_active": "bool",       # True or False.
    "city": "category",        # Repeated city labels.
    "department": "category", # Repeated department labels.
})

# Create salary bands using the specified salary ranges.
df["salary_band"] = pd.cut(
    df["salary"],
    bins=[0, 50000, 100000, np.inf],
    labels=["Low", "Medium", "High"],
)

# Extract the year from join_date. Nullable Int64 supports missing years.
df["join_year"] = df["join_date"].dt.year.astype("Int64")

# Arrange columns in a clear, consistent order.
df = df[
    [
        "id",
        "name",
        "age",
        "city",
        "department",
        "salary",
        "salary_band",
        "join_date",
        "join_year",
        "email",
        "is_active",
    ]
]

# Sort by employee ID and reset the DataFrame index.
df = df.sort_values("id").reset_index(drop=True)

# Display a final structure check and sample rows.
df.info()
print(df.head(10))

# Export the cleaned data as CSV and JSON.
csv_file = OUTPUT_DIR / "clean_data.csv"
json_file = OUTPUT_DIR / "clean_data.json"

df.to_csv(csv_file, index=False)
df.to_json(
    json_file,
    orient="records",  # One JSON object per row.
    indent=4,
    date_format="iso",
)

print("Saved clean_data.csv and clean_data.json")
print("Final shape:", df.shape)
