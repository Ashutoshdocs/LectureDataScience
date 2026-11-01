# =============================================================
# LESSON 09 - WRITING CSV FILES
# File used: students.csv
# Creates: output/new_students.csv, output/results.csv
# =============================================================

import csv
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.makedirs("output", exist_ok=True)


print("===== 1. csv.writer: write rows as lists =====")
rows = [
    ["name", "age", "city"],
    ["Tom", 14, "Goa"],
    ["Lily", 15, "Surat"],
]
with open("output/new_students.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["id", "note"])     # writerow  = ONE row
    writer.writerows(rows)              # writerows = MANY rows

with open("output/new_students.csv", encoding="utf-8") as f:
    print(f.read())


print("===== 2. A comma inside a value is handled for you =====")
with open("output/new_students.csv", "a", newline="", encoding="utf-8") as f:
    csv.writer(f).writerow(["Ravi", 16, "Pune, Maharashtra"])
with open("output/new_students.csv", encoding="utf-8") as f:
    print(f.read().splitlines()[-1])    # quotes were added automatically


print("\n===== 3. csv.DictWriter: write rows as dictionaries =====")
with open("students.csv", newline="", encoding="utf-8") as f:
    students = list(csv.DictReader(f))

with open("output/results.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "total", "grade"])
    writer.writeheader()                # writes the heading row
    for s in students:
        total = int(s["maths"]) + int(s["science"])
        if total >= 170:
            grade = "A"
        elif total >= 140:
            grade = "B"
        else:
            grade = "C"
        writer.writerow({"name": s["name"], "total": total, "grade": grade})

with open("output/results.csv", encoding="utf-8") as f:
    for line in f.readlines()[:6]:
        print(line.strip())
print("... saved output/results.csv")
