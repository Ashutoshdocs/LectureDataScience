# =============================================================
# LESSON 15 - MINI PROJECT: SCHOOL REPORT GENERATOR
# Uses EVERYTHING: txt, csv, json, writing, errors, folders
# Files used: students.csv, products.json, shopping.txt, story.txt
# Creates: output/report.txt, output/summary.json
# =============================================================

import csv
import json
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.makedirs("output", exist_ok=True)


def load_students(name):
    """Read the CSV and return a list of dictionaries."""
    try:
        with open(name, newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))
    except FileNotFoundError:
        print("Could not find", name)
        return []


def load_products(name):
    with open(name, encoding="utf-8") as f:
        return json.load(f)


def count_words(name):
    with open(name, encoding="utf-8") as f:
        return len(f.read().split())


students = load_students("students.csv")
products = load_products("products.json")

# --- calculations ---
for s in students:
    s["total"] = int(s["maths"]) + int(s["science"])
students.sort(key=lambda s: s["total"], reverse=True)
average = sum(s["total"] for s in students) / len(students)
in_stock = [p for p in products if p["in_stock"]]

with open("shopping.txt", encoding="utf-8") as f:
    items = [line.split() for line in f if line.strip()]

# --- write a text report ---
with open("output/report.txt", "w", encoding="utf-8") as r:
    print("=" * 40, file=r)
    print("         SCHOOL REPORT", file=r)
    print("=" * 40, file=r)
    print(f"Students: {len(students)}   Class average: {average:.1f}", file=r)
    print("\nTop 5 students:", file=r)
    for rank, s in enumerate(students[:5], start=1):
        print(f"  {rank}. {s['name']:<8} {s['city']:<8} {s['total']}", file=r)
    print(f"\nShop: {len(in_stock)} of {len(products)} products in stock", file=r)
    print(f"Shopping list: {len(items)} items, "
          f"{sum(int(q) for _, q in items)} units", file=r)
    print(f"Story length: {count_words('story.txt')} words", file=r)

# --- save the same summary as JSON ---
summary = {
    "students": len(students),
    "class_average": round(average, 1),
    "topper": students[0]["name"],
    "products_in_stock": len(in_stock),
}
with open("output/summary.json", "w", encoding="utf-8") as f:
    json.dump(summary, f, indent=2)

# --- show the results ---
with open("output/report.txt", encoding="utf-8") as f:
    print(f.read())
print("Saved output/report.txt and output/summary.json")

# YOUR TURN - try adding:
#   1. The student with the lowest maths marks
#   2. Total price of all in-stock products
#   3. Save the top 5 students to output/top5.csv
