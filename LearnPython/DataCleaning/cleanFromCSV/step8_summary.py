"""
STEP 8 - Summarise the cleaned data by department.

Input:
    outputs/clean_data.csv

Output:
    outputs/department_summary.csv

Run after step 7.
"""

from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "outputs" / "clean_data.csv"
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

# Load the final cleaned dataset created in step 7.
df = pd.read_csv(INPUT_FILE)

# Create one summary row for each department.
summary = (
    df.groupby("department")
    .agg(
        employees=("id", "count"),       # Number of employees.
        avg_age=("age", "mean"),         # Average employee age.
        avg_salary=("salary", "mean"),   # Average salary.
        active=("is_active", "sum"),     # True values count as 1.
    )
    .round(1)                            # Keep one decimal place.
)

print(summary)

# Save the summary. The department index is kept in the CSV.
output_file = OUTPUT_DIR / "department_summary.csv"
summary.to_csv(output_file)
print(f"Saved: {output_file}")
