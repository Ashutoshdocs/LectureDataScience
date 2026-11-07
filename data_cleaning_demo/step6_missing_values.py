"""
STEP 6 - HANDLE MISSING VALUES
------------------------------
The earlier steps turned every bad value into a missing value (NaN/NaT/<NA>).
Now decide, column by column, what to do with them:

  column      strategy                          why
  ----------  --------------------------------  ---------------------------------
  department  fill with 'Unknown'               text category; keeps the row
  city        fill with 'Unknown'               same
  salary      median of the same department     salaries differ by department;
                                                median isn't pulled by outliers
  age         median of the same department     same idea
  email       leave missing                     can't invent a contact address
  join_date   leave missing                     can't invent a date
  is_active   leave <NA>                        guessing would bias active-rate

Things to consider:
  * Look at HOW MUCH is missing first. If a column is, say, 60% empty,
    filling it creates more made-up data than real data. Consider dropping
    the column instead.
  * Median vs mean: the mean is pulled by extreme values; the median isn't.
  * Always add an '_imputed' flag column so anyone using the data can tell
    real values from estimated ones.
  * Never fill ids or other identifying columns.
  * In machine learning, compute medians on the TRAINING data only, then
    apply them to the test data.
"""
from utils import banner, load, save

df = load("step5_emails_booleans")

banner("Missing values BEFORE")
before = df.isna().sum()
print((before[before > 0]).to_frame("missing").assign(percent=lambda t: (t.missing / len(df) * 100).round(1)))

# 1. Categories -> 'Unknown'
for col in ["department", "city"]:
    df[col] = df[col].fillna("Unknown")

# 2. Numbers -> median of the same department (overall median as a fallback)
for col in ["salary", "age"]:
    df[f"{col}_imputed"] = df[col].isna()
    group_median = df.groupby("department")[col].transform("median")
    df[col] = df[col].fillna(group_median.round()).fillna(round(df[col].median()))

banner("Medians used for filling (by department)")
print(df[~df["salary_imputed"] & ~df["age_imputed"]].groupby("department")[["salary", "age"]].median())

banner("Missing values AFTER")
after = df.isna().sum()
print(after[after > 0].to_frame("missing (left on purpose)"))
print(f"\nSalaries filled: {df['salary_imputed'].sum()}   Ages filled: {df['age_imputed'].sum()}")

save(df, "step6_missing_values")
