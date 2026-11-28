"""
STEP 4 - Parse dates that use multiple formats.

Input:
    outputs/step3_fixed_numbers.csv

Output:
    outputs/step4_dates.csv

Run after step 3.
"""

from pathlib import Path

import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "outputs" / "step3_fixed_numbers.csv"
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

df = pd.read_csv(INPUT_FILE)

# Inspect the original date values before parsing.
print("Join dates BEFORE:", df["join_date"].unique())

# These are the date formats expected in the source CSV.
date_formats = (
    "%Y-%m-%d",   # Example: 2023-01-15
    "%d/%m/%Y",   # Example: 15/02/2023
    "%Y.%m.%d",   # Example: 2023.03.20
    "%B %d %Y",   # Example: March 5 2023
)


def parse_date(value):
    """Try each supported date format and return a pandas timestamp."""
    if pd.isna(value):
        return pd.NaT  # NaT means 'Not a Time' (a missing date).

    for date_format in date_formats:
        try:
            return pd.to_datetime(value, format=date_format)
        except ValueError:
            # This format did not match; try the next one.
            continue

    # Return a missing date if none of the formats matched.
    return pd.NaT


# Apply the parser to every value in the join_date column.
df["join_date"] = df["join_date"].apply(parse_date)

print("Join dates AFTER:")
print(df["join_date"].value_counts(dropna=False))

# Save dates in a consistent format.
output_file = OUTPUT_DIR / "step4_dates.csv"
df.to_csv(output_file, index=False)
print(f"Saved: {output_file}")
