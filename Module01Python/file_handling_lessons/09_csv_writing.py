# =============================================================
# LESSON 09 - WRITING CSV FILES
# File used: students.csv
# Creates: output/new_students.csv, output/results.csv
# =============================================================

import csv
import os

# Changes the working directory to the folder containing this script to avoid path errors.
os.chdir(os.path.dirname(os.path.abspath(__file__)))
# Creates an 'output' directory if it doesn't already exist.
os.makedirs("output", exist_ok=True)


print("===== 1. csv.writer: write rows as lists =====")
# A matrix list where each element represents a complete row of table values.
rows = [
    ["name", "age", "city"],
    ["Tom", 14, "Goa"],
    ["Lily", 15, "Surat"],
]
# Opens the target destination file in "w" (Write) mode. newline="" is mandatory to prevent empty row gaps.
with open("output/new_students.csv", "w", newline="", encoding="utf-8") as f:
    # Initialises a basic CSV writer engine tied to the opened file handler
    writer = csv.writer(f)
    # writerow() accepts a flat list and streams it out as a single row of text data
    writer.writerow(["id", "note"])     # writerow  = ONE row
    # writerows() accepts a 2D iterable matrix and automatically writes out every nested row sequence
    writer.writerows(rows)              # writerows = MANY rows

# Reopens the newly created CSV file in standard text mode to print out the final resulting text structure
with open("output/new_students.csv", encoding="utf-8") as f:
    print(f.read())


print("===== 2. A comma inside a value is handled for you =====")
# Opens the new file in "a" (Append) mode so we can add new rows to the end without erasing it.
with open("output/new_students.csv", "a", newline="", encoding="utf-8") as f:
    # Appends a single row containing a value with an embedded comma ("Pune, Maharashtra")
    csv.writer(f).writerow(["Ravi", 16, "Pune, Maharashtra"])

# Reopens the file, converts it into a list of strings, and displays the very last element to inspect formatting
with open("output/new_students.csv", encoding="utf-8") as f:
    print(f.read().splitlines()[-1])    # quotes were added automatically


print("\n===== 3. csv.DictWriter: write rows as dictionaries =====")
# Opens the original dataset file to load data fields into Python memory
with open("students.csv", newline="", encoding="utf-8") as f:
    # Consumes the source spreadsheet file row by row into a collection of structured dictionaries
    students = list(csv.DictReader(f))

# Opens a brand new spreadsheet file to house the grade calculation report
with open("output/results.csv", "w", newline="", encoding="utf-8") as f:
    # DictWriter maps dictionary key identifiers out to matching column tags specified in 'fieldnames'
    writer = csv.DictWriter(f, fieldnames=["name", "total", "grade"])
    # Generates and prints the very first row using the labels defined inside the fieldnames argument
    writer.writeheader()                # writes the heading row
    
    # Iterates over each student record mapping object imported from the source spreadsheet
    for s in students:
        # Casts math and science text records into numeric integers and finds their mathematical sum
        total = int(s["maths"]) + int(s["science"])
        # Conditional decision engine to establish grade classifications based on mark benchmarks
        if total >= 170:
            grade = "A"
        elif total >= 140:
            grade = "B"
        else:
            grade = "C"
        # Feeds a data map into writerow(); the dictionary keys must line up exactly with the specified fieldnames
        writer.writerow({"name": s["name"], "total": total, "grade": grade})

# Reopens the resulting generated grade sheet file for extraction and display
with open("output/results.csv", encoding="utf-8") as f:
    # Reads through all generated lines but uses a slice to print out only the top 6 data rows
    for line in f.readlines()[:6]:
        print(line.strip())
print("... saved output/results.csv")
