# Import the module or specific tools needed for this lesson.
import csv

# Open/use the resource in a context manager so it is closed automatically.
with open("students.csv", newline="", encoding="utf-8") as f:
    # Assign the calculated or created value to reader for later use.
    reader = csv.DictReader(f)
    # Display this value so we can inspect the program's result.
    print(reader.fieldnames)
    # Assign the calculated or created value to rows for later use.
    rows = list(reader)

# Display this value so we can inspect the program's result.
print(rows[0])
# Loop through each item so the same operation is applied repeatedly.
for r in rows:
    # Display this value so we can inspect the program's result.
    print(f"{r['name']:<6} {r['marks']:>3}  {r['city']}")

# Assign the calculated or created value to marks for later use.
marks = [int(r["marks"]) for r in rows]
# Display this value so we can inspect the program's result.
print("average:", sum(marks) / len(marks))
# Display this value so we can inspect the program's result.
print("top:", max(rows, key=lambda r: int(r["marks"]))["name"])
