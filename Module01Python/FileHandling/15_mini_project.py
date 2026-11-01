# =============================================================
# LESSON 15 - MINI PROJECT: SCHOOL REPORT GENERATOR
# Uses EVERYTHING: txt, csv, json, writing, errors, folders
# Files used: students.csv, products.json, shopping.txt, story.txt
# Creates: output/report.txt, output/summary.json
# =============================================================

import csv
import json
import os

# Changes the working directory to the script's folder to ensure file paths resolve reliably.
os.chdir(os.path.dirname(os.path.abspath(__file__)))
# Creates a designated 'output' directory if it does not already exist on disk.
os.makedirs("output", exist_ok=True)


def load_students(name):
    """Read the CSV and return a list of dictionaries."""
    # Guard block to intercept file system issues and prevent a hard program crash.
    try:
        # Opens the target CSV file. newline="" is required by the csv parser engine.
        with open(name, newline="", encoding="utf-8") as f:
            # Converts the parsing stream immediately into a list of row data dictionaries.
            return list(csv.DictReader(f))
    # Activates specifically if the requested CSV file name is missing from the directory.
    except FileNotFoundError:
        print("Could not find", name)
        # Returns a clean, empty list structure to let the code continue running safely.
        return []


def load_products(name):
    """Read the JSON catalog file and deserialize it into Python objects."""
    with open(name, encoding="utf-8") as f:
        # Reads the text and returns its parsed representation (a list of dictionaries).
        return json.load(f)


def count_words(name):
    """Calculate the total number of words inside a plain text file."""
    with open(name, encoding="utf-8") as f:
        # Reads the entire file as a single string, splits it by whitespace, and counts the list elements.
        return len(f.read().split())


# Executes the file loader functions to populate memory with our core datasets.
students = load_students("students.csv")
products = load_products("products.json")

# --- calculations ---
# Iterates through every student dictionary record to calculate performance benchmarks.
for s in students:
    # Converts the raw subject strings to integers and stores their sum inside a new dictionary key "total".
    s["total"] = int(s["maths"]) + int(s["science"])

# Sorts the student dictionaries in place based on their total marks from highest to lowest (descending).
students.sort(key=lambda s: s["total"], reverse=True)

# Calculates the collective class average mark by dividing the total score sum by student count.
average = sum(s["total"] for s in students) / len(students)

# List comprehension that filters out and retains only the product dictionaries where "in_stock" is True.
in_stock = [p for p in products if p["in_stock"]]

# Opens shopping.txt, reads line by line, discards empty rows, and splits columns into [item, quantity] pairs.
with open("shopping.txt", encoding="utf-8") as f:
    items = [line.split() for line in f if line.strip()]

# --- write a text report ---
# Opens a target text report file in write mode ("w") to clear any old contents and start fresh.
with open("output/report.txt", "w", encoding="utf-8") as r:
    # Uses print() with the 'file' argument to direct formatted text layouts straight into the file.
    print("=" * 40, file=r)
    print("         SCHOOL REPORT", file=r)
    print("=" * 40, file=r)
    # Prints global counts and formats the class average float value to a single decimal place (.1f).
    print(f"Students: {len(students)}   Class average: {average:.1f}", file=r)
    print("\nTop 5 students:", file=r)
    
    # Iterates over a sliced index of the top 5 sorted student rows, counting rank values starting at 1.
    for rank, s in enumerate(students[:5], start=1):
        # Pads the layout columns using string alignment modifiers (<8 left aligns by 8 character spaces).
        print(f"  {rank}. {s['name']:<8} {s['city']:<8} {s['total']}", file=r)
        
    # Streams contextual stock status summaries directly down into the file layer.
    print(f"\nShop: {len(in_stock)} of {len(products)} products in stock", file=r)
    # Evaluates the sum of list tokens, converting string quantities (q) to numeric types on the fly.
    print(f"Shopping list: {len(items)} items, "
          f"{sum(int(q) for _, q in items)} units", file=r)
    # Dynamically triggers the file word counting routine and appends its result directly to the text stream.
    print(f"Story length: {count_words('story.txt')} words", file=r)

# --- save the same summary as JSON ---
# Bundles the core statistical results together into a unified data structure map.
summary = {
    "students": len(students),
    "class_average": round(average, 1),
    "topper": students[0]["name"], # The absolute first element represents the topper due to our earlier sort.
    "products_in_stock": len(in_stock),
}
# Opens summary.json in write mode to store the telemetry mappings.
with open("output/summary.json", "w", encoding="utf-8") as f:
    # Serializes the dictionary structure using 2 spaces of structural tree indentation for human readability.
    json.dump(summary, f, indent=2)

# --- show the results ---
# Reopens the newly populated file to stream verification outputs to the standard terminal window.
with open("output/report.txt", encoding="utf-8") as f:
    print(f.read())
print("Saved output/report.txt and output/summary.json")

# YOUR TURN - try adding:
#   1. The student with the lowest maths marks
#   2. Total price of all in-stock products
#   3. Save the top 5 students to output/top5.csv
