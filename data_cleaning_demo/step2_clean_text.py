"""
STEP 2 - CLEAN TEXT COLUMNS
---------------------------
Problems found in step 0:
  name       : ' Rohan Mehta' (leading space), 'SNEHA IYER', 'priya patel'
  city       : 'PUNE ', 'pune', 'mumbai', and 'Bangalore'/'Bengaluru',
               'Delhi'/'New Delhi' (same city, different names)
  department : 'engineering ' (trailing space), 'sales' vs 'Sales'

Fix in this order:
  1. strip()  - remove spaces at the start and end
  2. title()  - one consistent case: 'Priya Patel', 'Pune'
  3. map      - merge different names for the same thing

Things to consider:
  * Decide which spelling to keep (here 'Bengaluru' and 'Delhi') and use it
    everywhere.
  * title() can be wrong: 'HR' -> 'Hr', 'McDonald' -> 'Mcdonald'.
    Always check the result and fix exceptions with a mapping.
  * Don't fill blanks here. Missing values are handled in step 6.
"""
from utils import banner, load, save

df = load("step1_no_duplicates")
before = df.copy()

CITY_MAP = {"Bangalore": "Bengaluru", "New Delhi": "Delhi"}
DEPT_MAP = {"Hr": "HR"}  # title() turns the acronym 'HR' into 'Hr' - put it back

df["name"] = df["name"].str.strip().str.title()
df["city"] = df["city"].str.strip().str.title().replace(CITY_MAP)
df["department"] = df["department"].str.strip().str.title().replace(DEPT_MAP)
df["email"] = df["email"].str.strip().str.lower()

for col in ["name", "city", "department"]:
    banner(f"{col}: before vs after")
    print("BEFORE:", sorted(repr(v) for v in before[col].dropna().unique()))
    print("AFTER :", sorted(repr(v) for v in df[col].dropna().unique()))
    print("\nCounts after cleaning:")
    print(df[col].value_counts(dropna=False).to_string())

save(df, "step2_clean_text")
