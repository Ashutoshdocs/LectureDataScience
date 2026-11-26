# Import the module or specific tools needed for this lesson.
import csv
# Import the module or specific tools needed for this lesson.
import re

# Assign the calculated or created value to EMOJI for later use.
EMOJI = re.compile("[\U0001F300-\U0001FAFF\U00002600-\U000027BF\uFE0F\u200D]+")

# Define a reusable function; parameters let the caller provide input.
def clean_header(h):
    # Send this result back to the caller and finish the function.
    return "_".join(h.strip().lower().split())

# Define a reusable function; parameters let the caller provide input.
def clean_str(value):
    # Send this result back to the caller and finish the function.
    return " ".join(EMOJI.sub("", value).split())

# Open/use the resource in a context manager so it is closed automatically.
with open("raw_customers.csv", newline="", encoding="utf-8") as f:
    # Assign the calculated or created value to reader for later use.
    reader = csv.reader(f)
    # Assign the calculated or created value to header for later use.
    header = [clean_header(h) for h in next(reader)]
    # Assign the calculated or created value to rows for later use.
    rows = [dict(zip(header, (clean_str(v) for v in r))) for r in reader]

# Display this value so we can inspect the program's result.
print(header)

# Loop through each item so the same operation is applied repeatedly.
for r in rows:
    # Assign the calculated or created value to r["name"] for later use.
    r["name"] = r["name"].title()
    # Assign the calculated or created value to r["email"] for later use.
    r["email"] = r["email"].lower()
    # Assign the calculated or created value to r["city"] for later use.
    r["city"] = r["city"].title()

# Loop through each item so the same operation is applied repeatedly.
for r in rows:
    # Display this value so we can inspect the program's result.
    print(f"{r['name']:<12} {r['email']:<15} {r['city']:<10} {r['spend']!r}")
