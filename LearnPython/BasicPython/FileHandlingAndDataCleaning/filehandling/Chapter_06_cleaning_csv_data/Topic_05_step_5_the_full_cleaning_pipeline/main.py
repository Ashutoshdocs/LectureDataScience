# Import the module or specific tools needed for this lesson.
import csv
# Import the module or specific tools needed for this lesson.
import json
# Import the module or specific tools needed for this lesson.
from parsers import clean_header, clean_str, to_int, to_money, to_date, valid_email

# Define a reusable function; parameters let the caller provide input.
def load(path):
    # Open/use the resource in a context manager so it is closed automatically.
    with open(path, newline="", encoding="utf-8") as f:
        # Assign the calculated or created value to reader for later use.
        reader = csv.reader(f)
        # Assign the calculated or created value to header for later use.
        header = [clean_header(h) for h in next(reader)]
        # Send this result back to the caller and finish the function.
        return [dict(zip(header, (clean_str(v) for v in r))) for r in reader]

# Define a reusable function; parameters let the caller provide input.
def transform(r):
    # Send this result back to the caller and finish the function.
    return {
        # Perform this operation; the expression or method shown determines the exact action.
        "name": r["name"].title(),
        # Perform this operation; the expression or method shown determines the exact action.
        "email": r["email"].lower(),
        # Perform this operation; the expression or method shown determines the exact action.
        "age": to_int(r["age"], 0, 120),
        # Perform this operation; the expression or method shown determines the exact action.
        "city": r["city"].title() or None,
        # Perform this operation; the expression or method shown determines the exact action.
        "joined": to_date(r["joined"]),
        # Perform this operation; the expression or method shown determines the exact action.
        "spend": to_money(r["spend"]),
    # Perform this operation; the expression or method shown determines the exact action.
    }

# Define a reusable function; parameters let the caller provide input.
def main():
    # Assign the calculated or created value to raw for later use.
    raw = load("raw_customers.csv")
    # Assign the calculated or created value to report for later use.
    report = {"raw_rows": len(raw), "empty_rows": 0, "duplicates": 0, "rejected": [], "missing": {}}
    # Perform this operation; the expression or method shown determines the exact action.
    clean, seen = [], set()

    # Loop through each item so the same operation is applied repeatedly.
    for r in raw:
        # Check this condition; the indented block runs only when it is true.
        if not any(r.values()):
            # Perform this operation; the expression or method shown determines the exact action.
            report["empty_rows"] += 1
            # Skip to the next iteration of the loop.
            continue
        # Assign the calculated or created value to row for later use.
        row = transform(r)
        # Check this condition; the indented block runs only when it is true.
        if not valid_email(row["email"]):
            # Perform this operation; the expression or method shown determines the exact action.
            report["rejected"].append({"name": row["name"], "reason": "invalid email"})
            # Skip to the next iteration of the loop.
            continue
        # Check this condition; the indented block runs only when it is true.
        if row["email"] in seen:
            # Perform this operation; the expression or method shown determines the exact action.
            report["duplicates"] += 1
            # Skip to the next iteration of the loop.
            continue
        # Perform this operation; the expression or method shown determines the exact action.
        seen.add(row["email"])
        # Perform this operation; the expression or method shown determines the exact action.
        clean.append(row)

    # Loop through each item so the same operation is applied repeatedly.
    for col in clean[0]:
        # Assign the calculated or created value to report["missing"][col] for later use.
        report["missing"][col] = sum(1 for row in clean if row[col] is None)
    # Assign the calculated or created value to report["clean_rows"] for later use.
    report["clean_rows"] = len(clean)

    # Open/use the resource in a context manager so it is closed automatically.
    with open("clean_customers.csv", "w", newline="", encoding="utf-8") as f:
        # Assign the calculated or created value to writer for later use.
        writer = csv.DictWriter(f, fieldnames=clean[0].keys())
        # Perform this operation; the expression or method shown determines the exact action.
        writer.writeheader()
        # Perform this operation; the expression or method shown determines the exact action.
        writer.writerows(clean)

    # Open/use the resource in a context manager so it is closed automatically.
    with open("cleaning_report.json", "w", encoding="utf-8") as f:
        # Call the relevant Python function/method to perform this file or data operation.
        json.dump(report, f, indent=2)

    # Display this value so we can inspect the program's result.
    print(open("clean_customers.csv", encoding="utf-8").read().strip())
    # Display this value so we can inspect the program's result.
    print(json.dumps(report, indent=2))

# Run this block only when this file is executed directly, not when imported.
if __name__ == "__main__":
    # Perform this operation; the expression or method shown determines the exact action.
    main()
