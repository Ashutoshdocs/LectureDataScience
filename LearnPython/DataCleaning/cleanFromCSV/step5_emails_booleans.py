"""
STEP 5 - Validate email strings and standardise yes/no values.

Input:
    outputs/step4_dates.csv

Output:
    outputs/step5_emails_booleans.csv

Run after step 4.
"""

from pathlib import Path

import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "outputs" / "step4_dates.csv"
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

# Parse join_date while loading the CSV.
df = pd.read_csv(INPUT_FILE, parse_dates=["join_date"])

# A simple pattern for checking the basic structure of an email address.
email_pattern = r"^[\w.+-]+@[\w-]+\.[\w.]+$"

# str.match() returns True for a match. Missing values are treated as False.
valid_email = df["email"].str.match(email_pattern, na=False)

# Print invalid, non-empty email values before replacing them.
invalid_emails = df.loc[
    ~valid_email & df["email"].notna(),
    "email",
].tolist()
print("Invalid emails:", invalid_emails)

# Replace invalid and missing email values with NaN.
df.loc[~valid_email, "email"] = np.nan

# Standardise different representations of yes and no.
print("is_active BEFORE:", df["is_active"].unique())

bool_map = {
    "y": True,
    "yes": True,
    "1": True,
    "n": False,
    "no": False,
    "0": False,
}

# Convert values to lowercase text, then map them to True or False.
# Values not present in bool_map become NaN.
df["is_active"] = (
    df["is_active"]
    .astype(str)
    .str.strip()
    .str.lower()
    .map(bool_map)
)

print("is_active AFTER:", df["is_active"].unique())

# Save the validated email and boolean columns.
output_file = OUTPUT_DIR / "step5_emails_booleans.csv"
df.to_csv(output_file, index=False)
print(f"Saved: {output_file}")
