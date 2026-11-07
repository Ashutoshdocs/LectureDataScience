"""
STEP 3 - FIX NUMERIC COLUMNS (age, salary)
------------------------------------------
age problems   : 'thirty' (a word), -5 and 150 (impossible), blanks
salary problems: '₹45,000' (currency sign and comma), 9999999 (a placeholder
                 meaning "unknown"), blanks

How:
  1. Convert words to numbers using a small dictionary ('thirty' -> 30).
  2. Remove symbols: '₹45,000' -> '45000'.
  3. pd.to_numeric(errors="coerce"): anything that still isn't a number
     becomes NaN instead of crashing the script.
  4. Check the range: an age outside 18-70 is a data-entry error -> NaN.
  5. Placeholder values: 9999999 is not a real salary -> NaN.

Things to consider:
  * Bad values become NaN (missing). Don't guess a number here; imputing
    belongs in step 6, where you can see how much data is missing.
  * Use the nullable 'Int64' type (capital I) so a whole-number column can
    still hold missing values.
  * The valid range is a business rule. Agree it with whoever owns the data.
"""
import numpy as np
import pandas as pd
from utils import banner, load, save

df = load("step2_clean_text")

WORD_NUMBERS = {"twenty": "20", "thirty": "30", "forty": "40", "fifty": "50", "sixty": "60"}
AGE_MIN, AGE_MAX = 18, 70
SALARY_PLACEHOLDERS = [9999999]

# ---------- id ----------
df["id"] = pd.to_numeric(df["id"]).astype("Int64")

# ---------- age ----------
raw_age = df["age"].copy()
age = df["age"].str.strip().str.lower().replace(WORD_NUMBERS)
age = pd.to_numeric(age, errors="coerce")
out_of_range = ~age.between(AGE_MIN, AGE_MAX) & age.notna()
age[out_of_range] = np.nan
df["age"] = age.astype("Int64")

banner("Age fixes")
print("Words converted        :", (raw_age.str.lower() == "thirty").sum(), "('thirty' -> 30)")
print("Out of range -> NaN    :", out_of_range.sum(), "values:", sorted(raw_age[out_of_range].unique()))
print("Missing after cleaning :", df["age"].isna().sum())

# ---------- salary ----------
raw_salary = df["salary"].copy()
salary = df["salary"].str.replace(r"[₹,\s]", "", regex=True)
salary = pd.to_numeric(salary, errors="coerce")
placeholder = salary.isin(SALARY_PLACEHOLDERS)
salary[placeholder] = np.nan
df["salary"] = salary.astype("Int64")

banner("Salary fixes")
print("Currency text fixed    :", raw_salary.str.contains("₹", na=False).sum(), "('₹45,000' -> 45000)")
print("Placeholder 9999999    :", placeholder.sum(), "-> NaN")
print("Missing after cleaning :", df["salary"].isna().sum())

banner("Summary of the numeric columns")
print(df[["age", "salary"]].describe())
print("\nTypes:\n", df[["id", "age", "salary"]].dtypes, sep="")

save(df, "step3_numbers")
