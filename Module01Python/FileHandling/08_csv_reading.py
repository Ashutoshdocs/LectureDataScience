# =============================================================
# LESSON 08 - READING CSV FILES
# File used: students.csv
# =============================================================
# CSV = Comma Separated Values. A table saved as plain text:
#   name,age,city,maths,science
#   Asha,15,Pune,88,92
# Python has a built-in 'csv' module to read them correctly.

import csv
import os

# Changes the working directory to the folder containing this script to avoid path errors.
os.chdir(os.path.dirname(os.path.abspath(__file__)))


print("===== 1. csv.reader: each row is a LIST =====")
# Opens students.csv. newline="" is mandatory for the csv module to parse line breaks safely across platforms.
with open("students.csv", newline="", encoding="utf-8") as f:
    # Creates a standard CSV reader object that splits rows into lists using commas as boundaries
    reader = csv.reader(f)
    # next() grabs the very first element (the table column names) and advances the internal file cursor
    header = next(reader)            # next() takes the first row (the headings)
    print("Header:", header)
    # Iterates over the remaining lines in the file, where each row is a clean list of strings
    for row in reader:
        print(row)
        # Checks if the first column index (name) matches "Fatima"
        if row[0] == "Fatima":       # show only the first few rows
            # Halts the file loop early if Fatima is encountered
            break
# Always open CSV files with newline="" - the csv module needs it.


print("\n===== 2. csv.DictReader: each row is a DICTIONARY =====")
with open("students.csv", newline="", encoding="utf-8") as f:
    # DictReader uses the first line as dictionary keys for all following rows; 
    # list() consumes the entire reader object to build a list of rows immediately.
    students = list(csv.DictReader(f))
# Prints the dictionary representing the first student row in the dataset
print(students[0])
# Accesses the specific row value associated with the "name" column key
print("Name of first student:", students[0]["name"])
# Counts the total number of dictionary records stored in the students list
print("Total students:", len(students))


print("\n===== 3. Everything is a STRING - convert numbers =====")
# Pulls out the dictionary for the first student record
first = students[0]
# Prints the datatype of the data under "maths", confirming it is <class 'str'>
print(type(first["maths"]))                  # <class 'str'>
# Converts both raw string text values to integers so they can be mathematically added together
print("Total marks:", int(first["maths"]) + int(first["science"]))


print("\n===== 4. Average maths marks =====")
# List comprehension that loops over all student records, casts their "maths" strings to integers, and stores them in a list
maths = [int(s["maths"]) for s in students]
# Calculates the arithmetic mean by dividing the sum of the list by its length, then rounds the result to 2 decimal places
print("Average:", round(sum(maths) / len(maths), 2))
# Finds and displays the extreme maximum and minimum integer values inside the maths list
print("Highest:", max(maths), " Lowest:", min(maths))


print("\n===== 5. Filter: students from Pune =====")
# Iterates through the list of student records row by row
for s in students:
    # Conditional block that only activates if the "city" value is exactly "Pune"
    if s["city"] == "Pune":
        # Prints out the name and math score for the matching records
        print(s["name"], s["maths"])


print("\n===== 6. Top 3 students by total marks =====")
# Creates a new copy of the student list sorted dynamically by calculating the sum of math + science scores, 
# sorted from highest total mark to lowest (reverse=True)
ranked = sorted(students,
                key=lambda s: int(s["maths"]) + int(s["science"]),
                reverse=True)
# Iterates through a list slice containing only the first 3 elements of the sorted database
for s in ranked[:3]:
    # Prints the name and total numeric calculated score for the highest achieving students
    print(s["name"], int(s["maths"]) + int(s["science"]))


print("\n===== 7. Count students per city =====")
# Initialises an empty dictionary to hold our unique category frequencies
cities = {}
# Iterates over every student profile dictionary item
for s in students:
    # Looks up the current city count (defaulting to 0 if it's the first time seeing this city) and increments it by 1
    cities[s["city"]] = cities.get(s["city"], 0) + 1
# Prints the final key-value dictionary summary mapping cities to student numbers
print(cities)
