"""
STEP 8 - SUMMARY: BEFORE/AFTER REPORT AND FIRST INSIGHTS
--------------------------------------------------------
  1. Data quality report: raw vs clean (rows, missing values, types).
  2. Descriptive statistics.
  3. Group-by analysis: by department, city and age group.
  4. Save the report to output/summary_report.txt.

Things to consider:
  * Report imputed values separately. Averages that include filled-in
    salaries look more certain than they are, so compare with real-only.
  * Small groups (only 2-3 people) give unreliable averages; always show
    the count next to the mean.
  * A summary is only as good as the cleaning. Keep this report with the
    clean file so others know what was changed.
"""
import io
from contextlib import redirect_stdout

import pandas as pd
from utils import banner, load, read_raw, OUT_DIR

raw = read_raw()
df = load("step7_structured")

buffer = io.StringIO()
with redirect_stdout(buffer):
    banner("1. DATA QUALITY: RAW vs CLEAN")
    quality = pd.DataFrame({
        "raw_missing": raw.isna().sum(),
        "clean_missing": df[raw.columns].isna().sum(),
        "raw_type": raw.dtypes.astype(str),
        "clean_type": df[raw.columns].dtypes.astype(str),
    })
    print(quality)
    print(f"\nRows: {len(raw)} raw -> {len(df)} clean (exact duplicates removed)")
    print(f"Salaries imputed: {df['salary_imputed'].sum()}  |  Ages imputed: {df['age_imputed'].sum()}")
    print(f"Invalid/blank emails: {(~df['email_valid']).sum()}")

    banner("2. DESCRIPTIVE STATISTICS")
    print(df[["age", "salary"]].describe().round(0))

    banner("3. BY DEPARTMENT")
    by_dept = df.groupby("department", observed=True).agg(
        employees=("id", "count"),
        avg_salary=("salary", "mean"),
        median_salary=("salary", "median"),
        avg_age=("age", "mean"),
        active_rate=("is_active", "mean"),
    ).round(2).sort_values("employees", ascending=False)
    print(by_dept)

    real_only = df[~df["salary_imputed"]].groupby("department", observed=True)["salary"].mean().round(0)
    print("\nAverage salary using REAL values only (no imputed):")
    print(real_only.to_string())

    banner("4. BY CITY")
    print(df.groupby("city", observed=True).agg(
        employees=("id", "count"), avg_salary=("salary", "mean")
    ).round(0).sort_values("employees", ascending=False))

    banner("5. AGE GROUP x SALARY BAND (head count)")
    print(pd.crosstab(df["age_group"], df["salary_band"], margins=True))

    banner("6. JOINERS PER MONTH")
    print(df["join_month"].value_counts(dropna=False).sort_index().to_string())

report = buffer.getvalue()
print(report)
(OUT_DIR / "summary_report.txt").write_text(report, encoding="utf-8")
print("\n>> Report saved: output/summary_report.txt")
