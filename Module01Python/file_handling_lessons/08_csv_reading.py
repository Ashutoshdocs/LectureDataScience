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
os.chdir(os.path.dirname(os.path.abspath(__file__)))


print("===== 1. csv.reader: each row is a LIST =====")
with open("students.csv", newline="", encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader)            # next() takes the first row (the headings)
    print("Header:", header)
    for row in reader:
        print(row)
        if row[0] == "Fatima":       # show only the first few rows
            break
# Always open CSV files with newline="" - the csv module needs it.


print("\n===== 2. csv.DictReader: each row is a DICTIONARY =====")
with open("students.csv", newline="", encoding="utf-8") as f:
    students = list(csv.DictReader(f))
print(students[0])
print("Name of first student:", students[0]["name"])
print("Total students:", len(students))


print("\n===== 3. Everything is a STRING - convert numbers =====")
first = students[0]
print(type(first["maths"]))                  # <class 'str'>
print("Total marks:", int(first["maths"]) + int(first["science"]))


print("\n===== 4. Average maths marks =====")
maths = [int(s["maths"]) for s in students]
print("Average:", round(sum(maths) / len(maths), 2))
print("Highest:", max(maths), " Lowest:", min(maths))


print("\n===== 5. Filter: students from Pune =====")
for s in students:
    if s["city"] == "Pune":
        print(s["name"], s["maths"])


print("\n===== 6. Top 3 students by total marks =====")
ranked = sorted(students,
                key=lambda s: int(s["maths"]) + int(s["science"]),
                reverse=True)
for s in ranked[:3]:
    print(s["name"], int(s["maths"]) + int(s["science"]))


print("\n===== 7. Count students per city =====")
cities = {}
for s in students:
    cities[s["city"]] = cities.get(s["city"], 0) + 1
print(cities)
