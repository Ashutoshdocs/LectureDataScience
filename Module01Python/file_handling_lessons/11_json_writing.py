# =============================================================
# LESSON 11 - WRITING JSON FILES
# Files used: products.json, students.csv
# Creates: output/profile.json, output/products_updated.json,
#          output/students.json
# =============================================================

import csv
import json
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.makedirs("output", exist_ok=True)


print("===== 1. json.dump(): Python -> file =====")
profile = {
    "name": "Asha",
    "age": 15,
    "hobbies": ["reading", "chess"],
    "is_student": True,
    "phone": None,
}
with open("output/profile.json", "w", encoding="utf-8") as f:
    json.dump(profile, f, indent=2)     # indent=2 makes it easy to read

with open("output/profile.json", encoding="utf-8") as f:
    print(f.read())


print("===== 2. json.dumps(): Python -> STRING =====")
print(json.dumps(profile))                  # all on one line
print(json.dumps({"b": 2, "a": 1}, sort_keys=True))


print("\n===== 3. Read, change, save (update a JSON file) =====")
with open("products.json", encoding="utf-8") as f:
    products = json.load(f)

for p in products:
    p["price"] = round(p["price"] * 0.9)    # 10% discount
products.append({"id": 21, "name": "Scale", "category": "Stationery",
                 "price": 25, "in_stock": True})

with open("output/products_updated.json", "w", encoding="utf-8") as f:
    json.dump(products, f, indent=2)
print("Saved", len(products), "products with discount.")


print("\n===== 4. Convert CSV -> JSON =====")
with open("students.csv", newline="", encoding="utf-8") as f:
    students = list(csv.DictReader(f))
for s in students:                          # make numbers real numbers
    s["age"] = int(s["age"])
    s["maths"] = int(s["maths"])
    s["science"] = int(s["science"])
with open("output/students.json", "w", encoding="utf-8") as f:
    json.dump(students, f, indent=2)
print("Saved output/students.json, first entry:")
print(json.dumps(students[0], indent=2))


print("\n===== 5. Hindi / emoji: use ensure_ascii=False =====")
print(json.dumps({"greeting": "नमस्ते"}))                     # escaped
print(json.dumps({"greeting": "नमस्ते"}, ensure_ascii=False))  # readable
