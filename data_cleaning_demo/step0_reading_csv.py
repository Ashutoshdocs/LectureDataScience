"""
STEP 0 - READ THE CSV AND INSPECT IT
------------------------------------
Rule #1 of data cleaning: LOOK before you change anything.
We read the file, check its size, column types, missing values, duplicates
and the distinct values in each text column. Every problem we find here
becomes a task for one of the later steps.
"""
import pandas as pd
from utils import banner, read_raw, save, RAW_FILE

df = read_raw()

banner("1. Shape (rows, columns)")
print(df.shape)

banner("2. First 10 rows")
print(df.head(10))

banner("3. What pandas would guess WITHOUT dtype=str")
guessed = pd.read_csv(RAW_FILE)
print(guessed.dtypes)
print("\nNote: age and salary come out as text (str/object), not numbers,")
print("because of values like 'thirty' and '₹45,000'.")

banner("4. Missing values per column")
missing = df.isna().sum()
print(pd.DataFrame({"missing": missing, "percent": (missing / len(df) * 100).round(1)}))

banner("5. Duplicates")
print("Fully duplicated rows :", df.duplicated().sum())
print("Duplicated ids        :", df["id"].duplicated().sum())

banner("6. Distinct values in text columns (spot spelling/case problems)")
for col in ["name", "city", "department", "is_active"]:
    # repr() shows hidden spaces, e.g. 'PUNE ' vs 'Pune'
    values = sorted(repr(v) for v in df[col].dropna().unique())
    print(f"\n{col} ({len(values)} distinct): {', '.join(values)}")

banner("7. Values that are not plain numbers")
for col in ["age", "salary"]:
    bad = df.loc[~df[col].fillna("0").str.fullmatch(r"-?\d+"), col].unique()
    print(f"{col}: {list(bad)}")
print("Suspicious ages  :", sorted(set(df["age"].dropna()) & {"-5", "150"}))
print("Rows with salary 9999999:", (df["salary"] == "9999999").sum())

banner("8. Date formats used in join_date")
print(df["join_date"].value_counts(dropna=False))

save(df, "step0_raw")
