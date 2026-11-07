"""
STEP 7 - FINAL STRUCTURE: TYPES, COLUMN ORDER, NEW COLUMNS, CHECKS
-----------------------------------------------------------------
Get the table ready for analysis:
  1. Set final data types ('category' for repeated text saves memory and
     makes grouping faster).
  2. Add useful derived columns: age_group, salary_band, join_month.
  3. Put the columns in a logical order and sort by id.
  4. Run final checks (assert) so the script fails loudly if something
     is still wrong.
  5. Save the clean file: output/cleaned_data.csv

Things to consider:
  * assert statements are your safety net. If new raw data breaks a rule,
    you find out right away instead of in a wrong report later.
  * Check duplicates again: cleaning can make two rows identical that
    weren't before.
  * Keep the flag columns (email_valid, *_imputed). They are part of the
    honest record of what was changed.
"""
import pandas as pd
from utils import banner, load, save, OUT_DIR

df = load("step6_missing_values")

# 1. Types
df["city"] = df["city"].astype("category")
df["department"] = df["department"].astype("category")
df["age"] = df["age"].astype("Int64")
df["salary"] = df["salary"].astype("Int64")

# 2. Derived columns
df["age_group"] = pd.cut(df["age"], bins=[17, 29, 39, 49, 70], labels=["18-29", "30-39", "40-49", "50+"])
df["salary_band"] = pd.cut(
    df["salary"], bins=[0, 50_000, 100_000, float("inf")], labels=["<50k", "50k-100k", "100k+"]
)
df["join_month"] = df["join_date"].dt.to_period("M").astype(str).replace("NaT", pd.NA)

# 3. Column order + sort
COLUMNS = [
    "id", "name", "age", "age_group", "city", "department",
    "salary", "salary_band", "join_date", "join_month",
    "email", "email_valid", "is_active", "age_imputed", "salary_imputed",
]
df = df[COLUMNS].sort_values("id").reset_index(drop=True)

# 4. Final checks
assert df["id"].is_unique, "Duplicate ids found"
assert not df.duplicated().any(), "Duplicate rows found"
assert df["age"].between(18, 70).all(), "Age out of range"
assert (df["salary"] > 0).all(), "Bad salary"
assert df["name"].str.strip().eq(df["name"]).all(), "Untrimmed names"
banner("All checks passed")

banner("Final structure")
df.info()

banner("First 10 rows of the clean data")
print(df.head(10).to_string(index=False))

save(df, "step7_structured")
df.to_csv(OUT_DIR / "cleaned_data.csv", index=False)
print(">> Final clean file: output/cleaned_data.csv")
