"""
STEP 1 - REMOVE DUPLICATES
--------------------------
Two kinds of duplicates to check:
  a) Exact duplicate rows  -> the same record was entered twice; safe to drop.
  b) Same id, different data -> a conflict; a person must decide which row
     is correct, so we only report these and don't delete them.

Things to consider:
  * Keep the first occurrence (keep="first") so the original order is kept.
  * Two rows with the same NAME are not duplicates - this file has many
    different employees called 'SNEHA IYER' with different ids.
  * Some duplicates only show after cleaning (e.g. 'Pune' vs 'PUNE '),
    so we check again at the end in step 7.
"""
from utils import banner, load, save

df = load("step0_raw")
rows_before = len(df)

banner("Exact duplicate rows (all copies shown)")
dupes = df[df.duplicated(keep=False)].sort_values("id")
print(dupes)

df = df.drop_duplicates(keep="first").reset_index(drop=True)

banner("Same id but different data (needs a human decision)")
conflicts = df[df["id"].duplicated(keep=False)]
print(conflicts if not conflicts.empty else "None found.")

banner("Result")
print(f"Rows before: {rows_before}  ->  after: {len(df)}  (removed {rows_before - len(df)})")

save(df, "step1_no_duplicates")
