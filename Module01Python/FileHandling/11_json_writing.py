# =============================================================
# LESSON 11 - WRITING JSON FILES
# Files used: products.json, students.csv
# Creates: output/profile.json, output/products_updated.json,
#          output/students.json
# =============================================================

import csv  # Imports the csv module to read/write CSV files
import json  # Imports the json module to work with JSON data
import os  # Imports the os module to handle file paths and directories

# Changes the current working directory to the directory where this script file is saved
os.chdir(os.path.dirname(os.path.abspath(__file__)))
# Creates a folder named "output" if it doesn't already exist; ignores error if it does
os.makedirs("output", exist_ok=True)


# Prints a header section to the terminal for the first example
print("===== 1. json.dump(): Python -> file =====")
# Defines a Python dictionary containing user profile details
profile = {
    "name": "Asha",  # String value for the name
    "age": 15,  # Integer value for the age
    "hobbies": ["reading", "chess"],  # List of strings for hobbies
    "is_student": True,  # Boolean value (becomes true in JSON)
    "phone": None,  # None value (becomes null in JSON)
}
# Opens (or creates) 'profile.json' inside the 'output' folder in write mode with UTF-8 encoding
with open("output/profile.json", "w", encoding="utf-8") as f:
    # Converts the profile dictionary to JSON and writes it to the file with 2-space indentation
    json.dump(profile, f, indent=2)  # indent=2 makes it easy to read

# Opens the newly created 'profile.json' file in read-only mode with UTF-8 encoding
with open("output/profile.json", encoding="utf-8") as f:
    # Reads the entire content of the file and prints it directly to the terminal
    print(f.read())


# Prints a header section to the terminal for the second example
print("===== 2. json.dumps(): Python -> STRING =====")
# Converts the profile dictionary into a single condensed JSON string and prints it
print(json.dumps(profile))  # all on one line
# Converts a dictionary to a JSON string while sorting its keys alphabetically ('a' before 'b')
print(json.dumps({"b": 2, "a": 1}, sort_keys=True))


# Prints a header section to the terminal for the third example
print("\n===== 3. Read, change, save (update a JSON file) =====")
# Opens an existing file named 'products.json' in read-only mode with UTF-8 encoding
with open("products.json", encoding="utf-8") as f:
    # Parses the JSON file content and converts it into a Python list of dictionaries
    products = json.load(f)

# Loops through each product dictionary inside the products list
for p in products:
    # Multiplies the price by 0.9 to apply a 10% discount, rounds it, and updates the price
    p["price"] = round(p["price"] * 0.9)  # 10% discount
# Appends a brand new product dictionary to the end of the products list
products.append(
    {
        "id": 21,
        "name": "Scale",
        "category": "Stationery",
        "price": 25,
        "in_stock": True,
    }
)

# Opens (or creates) 'products_updated.json' in write mode inside the 'output' folder
with open("output/products_updated.json", "w", encoding="utf-8") as f:
    # Saves the updated products list as formatted JSON into the file
    json.dump(products, f, indent=2)
# Prints a confirmation message showing the total number of products processed
print("Saved", len(products), "products with discount.")


# Prints a header section to the terminal for the fourth example
print("\n===== 4. Convert CSV -> JSON =====")
# Opens 'students.csv' in read-only mode, disabling automatic universal newline translation
with open("students.csv", newline="", encoding="utf-8") as f:
    # Reads CSV rows as dictionaries mapped to columns, and converts the whole map into a list
    students = list(csv.DictReader(f))
# Loops through each student dictionary in the list
for s in students:  # make numbers real numbers
    s["age"] = int(s["age"])  # Converts the age string from the CSV into a regular integer
    s["maths"] = int(
        s["maths"]
    )  # Converts the maths score string from the CSV into an integer
    s["science"] = int(
        s["science"]
    )  # Converts the science score string from the CSV into an integer
# Opens (or creates) 'students.json' in write mode inside the 'output' folder
with open("output/students.json", "w", encoding="utf-8") as f:
    # Saves the complete student list as formatted JSON into the file
    json.dump(students, f, indent=2)
# Prints a status message indicating the file was saved
print("Saved output/students.json, first entry:")
# Converts the very first student dictionary into a clean JSON string and prints it
print(json.dumps(students[0], indent=2))


# Prints a header section to the terminal for the fifth example
print("\n===== 5. Hindi / emoji: use ensure_ascii=False =====")
# Converts Hindi text to a JSON string; by default, it converts non-ASCII characters to Unicode escape codes (\u...)
print(json.dumps({"greeting": "नमस्ते"}))  # escaped
# Converts Hindi text to a JSON string but forces it to keep the native characters readable
print(
    json.dumps({"greeting": "नमस्ते"}, ensure_ascii=False)
)  # readablecomment each line
