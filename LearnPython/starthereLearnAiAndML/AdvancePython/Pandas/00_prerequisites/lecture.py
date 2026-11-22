"""Lecture 00: Prerequisites. Plain-Python tables, dicts, lambda and a NumPy recap.

No pandas yet. This shows how awkward table work is without it.
"""
import csv
import io
import numpy as np

print("--- 1. Dictionaries ---")
student = {"name": "Asha", "maths": 78, "science": 85}
student["english"] = 62
for key, value in student.items():
    print(f"  {key:8} -> {value}")

print("\n--- 2. Two ways to store a table ---")
table = {                                   # dict of lists (column-oriented)
    "name":  ["Asha", "Ravi", "Meena", "John"],
    "class": ["10A", "10A", "10B", "10B"],
    "maths": [78, 92, 45, 83],
}
rows = [                                    # list of dicts (row-oriented)
    {"name": n, "class": c, "maths": m}
    for n, c, m in zip(table["name"], table["class"], table["maths"])
]
print("dict of lists:", table)
print("list of dicts:", rows[:2], "...")

print("\n--- 3. Answering questions the hard way ---")
avg = sum(r["maths"] for r in rows) / len(rows)
print("average maths     :", avg)
print("scored above 60   :", [r["name"] for r in rows if r["maths"] > 60])
print("sorted by maths   :", [r["name"] for r in sorted(rows, key=lambda r: r["maths"], reverse=True)])
print("top student       :", max(rows, key=lambda r: r["maths"])["name"])

per_class = {}                              # average per class: a lot of code
for r in rows:
    per_class.setdefault(r["class"], []).append(r["maths"])
print("average per class :", {k: sum(v) / len(v) for k, v in per_class.items()})

print("\n--- 4. Reading a CSV the hard way ---")
csv_text = "name,maths\nAsha,78\nRavi,92\nMeena,\n"
parsed = []
for rec in csv.DictReader(io.StringIO(csv_text)):
    # every value arrives as TEXT, and missing values are empty strings
    rec["maths"] = int(rec["maths"]) if rec["maths"] else None
    parsed.append(rec)
print(parsed)
valid = [r["maths"] for r in parsed if r["maths"] is not None]
print("mean ignoring missing:", sum(valid) / len(valid))

print("\n--- 5. lambda ---")
double = lambda x: x * 2
print(double(21), list(map(double, [1, 2, 3])))

print("\n--- 6. NumPy recap ---")
marks = np.array(table["maths"])
print("mean       :", marks.mean())
print("mask > 60  :", marks[marks > 60])
print("pass/fail  :", np.where(marks >= 50, "pass", "fail"))
print("pass rate  :", (marks >= 50).mean())
print("But NumPy has no column NAMES, no row labels, and one dtype per array.")
print("pandas adds all of that. See Lecture 01.")
