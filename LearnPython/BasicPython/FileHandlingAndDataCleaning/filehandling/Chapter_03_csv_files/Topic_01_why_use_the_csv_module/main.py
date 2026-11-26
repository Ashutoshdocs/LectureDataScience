# Import the module or specific tools needed for this lesson.
import csv

# Open/use the resource in a context manager so it is closed automatically.
with open("students.csv", encoding="utf-8") as f:
    # Assign the calculated or created value to lines for later use.
    lines = f.read().splitlines()
# Display this value so we can inspect the program's result.
print("split(','):", lines[3].split(","))

# Open/use the resource in a context manager so it is closed automatically.
with open("students.csv", newline="", encoding="utf-8") as f:
    # Assign the calculated or created value to reader for later use.
    reader = csv.reader(f)
    # Assign the calculated or created value to header for later use.
    header = next(reader)
    # Display this value so we can inspect the program's result.
    print("header:", header)
    # Loop through each item so the same operation is applied repeatedly.
    for row in reader:
        # Display this value so we can inspect the program's result.
        print(row)
