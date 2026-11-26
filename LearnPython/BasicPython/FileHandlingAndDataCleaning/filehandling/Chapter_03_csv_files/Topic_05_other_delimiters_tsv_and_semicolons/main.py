# Import the module or specific tools needed for this lesson.
import csv

# Open/use the resource in a context manager so it is closed automatically.
with open("prices_eu.csv", newline="", encoding="utf-8") as f:
    # Loop through each item so the same operation is applied repeatedly.
    for row in csv.DictReader(f, delimiter=";"):
        # Assign the calculated or created value to price for later use.
        price = float(row["price"].replace(",", "."))
        # Display this value so we can inspect the program's result.
        print(row["product"], price)

# Open/use the resource in a context manager so it is closed automatically.
with open("cities.tsv", newline="", encoding="utf-8") as f:
    # Assign the calculated or created value to rows for later use.
    rows = list(csv.reader(f, delimiter="\t"))
# Display this value so we can inspect the program's result.
print(rows)

# Open/use the resource in a context manager so it is closed automatically.
with open("cities_out.csv", "w", newline="", encoding="utf-8") as f:
    # Call the relevant Python function/method to perform this file or data operation.
    csv.writer(f).writerows(rows)
# Display this value so we can inspect the program's result.
print(open("cities_out.csv", encoding="utf-8").read().strip())
