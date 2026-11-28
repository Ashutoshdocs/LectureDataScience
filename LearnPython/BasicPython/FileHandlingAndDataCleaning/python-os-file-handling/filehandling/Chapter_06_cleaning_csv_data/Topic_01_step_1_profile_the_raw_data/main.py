# Import the module or specific tools needed for this lesson.
import csv
# Import the module or specific tools needed for this lesson.
from collections import Counter

# Open/use the resource in a context manager so it is closed automatically.
with open("raw_customers.csv", newline="", encoding="utf-8") as f:
    # Assign the calculated or created value to reader for later use.
    reader = csv.DictReader(f)
    # Assign the calculated or created value to header for later use.
    header = reader.fieldnames
    # Assign the calculated or created value to rows for later use.
    rows = list(reader)

# Display this value so we can inspect the program's result.
print("columns:", header)
# Display this value so we can inspect the program's result.
print("rows   :", len(rows))

# Display this value so we can inspect the program's result.
print("\nmissing values per column:")
# Loop through each item so the same operation is applied repeatedly.
for col in header:
    # Assign the calculated or created value to missing for later use.
    missing = sum(1 for r in rows if not r[col].strip())
    # Display this value so we can inspect the program's result.
    print(f"  {col!r:<10} {missing}")

# Display this value so we can inspect the program's result.
print("\nraw values (repr shows hidden spaces):")
# Loop through each item so the same operation is applied repeatedly.
for r in rows[:3]:
    # Display this value so we can inspect the program's result.
    print(" ", repr(r[" Name "]), repr(r["Age"]), repr(r["Spend"]))

# Display this value so we can inspect the program's result.
print("\ncity spellings:", dict(Counter(r[" City "] for r in rows)))
# Display this value so we can inspect the program's result.
print("ages:", [r["Age"] for r in rows])
