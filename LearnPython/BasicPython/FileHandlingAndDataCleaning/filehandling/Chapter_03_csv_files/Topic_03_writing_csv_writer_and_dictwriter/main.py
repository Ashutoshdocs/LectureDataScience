# Import the module or specific tools needed for this lesson.
import csv

# Assign the calculated or created value to rows for later use.
rows = [
    # Perform this operation; the expression or method shown determines the exact action.
    ["Asha", 91, "Pune"],
    # Perform this operation; the expression or method shown determines the exact action.
    ["Meena", 85, "Mumbai, MH"],
    # Perform this operation; the expression or method shown determines the exact action.
    ["Ravi", 78, 'Delhi "NCR"'],
# Perform this operation; the expression or method shown determines the exact action.
]
# Open/use the resource in a context manager so it is closed automatically.
with open("out.csv", "w", newline="", encoding="utf-8") as f:
    # Assign the calculated or created value to writer for later use.
    writer = csv.writer(f)
    # Perform this operation; the expression or method shown determines the exact action.
    writer.writerow(["name", "marks", "city"])
    # Perform this operation; the expression or method shown determines the exact action.
    writer.writerows(rows)

# Assign the calculated or created value to people for later use.
people = [{"name": "Zoya", "age": 21}, {"name": "Dev", "age": 23, "city": "Goa"}]
# Open/use the resource in a context manager so it is closed automatically.
with open("people.csv", "w", newline="", encoding="utf-8") as f:
    # Assign the calculated or created value to writer for later use.
    writer = csv.DictWriter(f, fieldnames=["name", "age"], extrasaction="ignore")
    # Perform this operation; the expression or method shown determines the exact action.
    writer.writeheader()
    # Perform this operation; the expression or method shown determines the exact action.
    writer.writerows(people)

# Loop through each item so the same operation is applied repeatedly.
for name in ["out.csv", "people.csv"]:
    # Open/use the resource in a context manager so it is closed automatically.
    with open(name, encoding="utf-8") as f:
        # Display this value so we can inspect the program's result.
        print("---", name)
        # Display this value so we can inspect the program's result.
        print(f.read().strip())
