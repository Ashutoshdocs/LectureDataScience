"""
TASK 4 - Combine both recommendation tasks into one report.

Inputs:
    outputs/people_you_may_know.csv
    outputs/pages_you_might_like.csv

Output:
    outputs/recommendations.csv

Run after Task 2 and Task 3.
"""

from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "outputs"

# Read the people recommendations created in Task 2.
people_file = OUTPUT_DIR / "people_you_may_know.csv"
people_df = pd.read_csv(people_file)

# Read the page recommendations created in Task 3.
pages_file = OUTPUT_DIR / "pages_you_might_like.csv"
pages_df = pd.read_csv(pages_file)

# Merge the two tables using the common user_id and user columns.
combined = people_df.merge(
    pages_df,
    on=["user_id", "user"],
    how="outer",
)

# Save the final combined recommendation report.
output_file = OUTPUT_DIR / "recommendations.csv"
combined.to_csv(output_file, index=False)

print("Combined recommendation report:")
print(combined.head(10))
print(f"\nSaved: {output_file}")
