# Import the module or specific tools needed for this lesson.
import csv
# Import the module or specific tools needed for this lesson.
from parsers import clean_header, clean_str

# Open/use the resource in a context manager so it is closed automatically.
with open("raw_customers.csv", newline="", encoding="utf-8") as f:
    # Assign the calculated or created value to reader for later use.
    reader = csv.reader(f)
    # Assign the calculated or created value to header for later use.
    header = [clean_header(h) for h in next(reader)]
    # Assign the calculated or created value to rows for later use.
    rows = [dict(zip(header, (clean_str(v) for v in r))) for r in reader]
# Display this value so we can inspect the program's result.
print("start          :", len(rows))

# Assign the calculated or created value to rows for later use.
rows = [r for r in rows if any(r.values())]
# Display this value so we can inspect the program's result.
print("no empty rows  :", len(rows))

# Assign the calculated or created value to seen for later use.
seen = set()
# Perform this operation; the expression or method shown determines the exact action.
unique, dupes = [], []
# Loop through each item so the same operation is applied repeatedly.
for r in rows:
    # Assign the calculated or created value to key for later use.
    key = r["email"].lower()
    # Check this condition; the indented block runs only when it is true.
    if key in seen:
        # Perform this operation; the expression or method shown determines the exact action.
        dupes.append(r)
    # Handle the alternative path when the preceding condition was not met.
    else:
        # Perform this operation; the expression or method shown determines the exact action.
        seen.add(key)
        # Perform this operation; the expression or method shown determines the exact action.
        unique.append(r)

# Display this value so we can inspect the program's result.
print("no duplicates  :", len(unique))
# Display this value so we can inspect the program's result.
print("removed        :", [(d["name"], d["email"]) for d in dupes])
