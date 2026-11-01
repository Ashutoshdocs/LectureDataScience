# =============================================================
# LESSON 10 - READING JSON FILES
# File used: products.json
# =============================================================
# JSON looks like Python lists and dictionaries:
#   [ {"id": 1, "name": "Notebook", "price": 40, "in_stock": true}, ... ]
# JSON -> Python:  object {} -> dict   array [] -> list
#                  true/false -> True/False   null -> None

import json
import os

# Changes the working directory to the folder containing this script to avoid path errors.
os.chdir(os.path.dirname(os.path.abspath(__file__)))


print("===== 1. json.load(): file -> Python =====")
# Opens products.json in standard read mode with UTF-8 character handling.
with open("products.json", encoding="utf-8") as f:
    # json.load() reads the file object and converts the raw JSON structure into Python lists and dicts.
    products = json.load(f)

# Prints the variable type, matching the JSON array wrapper: <class 'list'>
print("Type:", type(products))              # list
# Counts the total number of dictionary elements tracked within the parsed data list.
print("How many products:", len(products))
# Fetches the dictionary record stored at index 0 of the items list.
print("First product:", products[0])
# Accesses the value mapped to the "name" key inside the first dictionary element.
print("Its name:", products[0]["name"])


print("\n===== 2. Loop through the data =====")
# Iterates through a list slice containing only the first 5 product elements.
for p in products[:5]:
    # Prints a formatted string: padding the ID to 2 spaces, aligning the name left by 12 spaces (<12), and tracking the price.
    print(f'{p["id"]:2}. {p["name"]:<12} Rs {p["price"]}')


print("\n===== 3. Filter: products in stock under Rs 300 =====")
# List comprehension that checks each element, filtering for true boolean stock states and price properties under 300.
cheap = [p["name"] for p in products if p["in_stock"] and p["price"] < 300]
print(cheap)


print("\n===== 4. Totals and maximum =====")
# Collects all the numerical value attributes across the database entries into a flat number array.
prices = [p["price"] for p in products]
# Computes the collective sum of all item prices inside the dataset.
print("Total value :", sum(prices))
# Divides the calculated sum by the length count to get the classic arithmetic average value.
print("Average     :", sum(prices) / len(prices))
# Uses max() with a lambda key mapping to scan the profile objects and identify the item dictionary with the highest price.
expensive = max(products, key=lambda p: p["price"])
print("Most expensive:", expensive["name"], expensive["price"])


print("\n===== 5. Group by category =====")
# Initialises an empty dictionary structure to compile grouped string properties.
groups = {}
# Loops over every product record object in the catalog array.
for p in products:
    # setdefault checks if a category list key exists; if not, it assigns an empty list [] before appending the name value.
    groups.setdefault(p["category"], []).append(p["name"])
# Iterates over the categorized dictionary records to print out lists associated with each unique item category.
for category, names in groups.items():
    print(category, "->", names)


print("\n===== 6. json.loads(): STRING -> Python =====")
# Defines a literal string variable containing valid double-quoted JSON metadata.
text = '{"city": "Pune", "pin": 411001, "metro": true}'
# json.loads() (load string) deserialises raw text strings directly into standard Python dictionary types.
data = json.loads(text)          # 's' at the end = string
print(data, type(data))
# Displays the dictionary property, showing that 'true' was automatically transformed into the Python boolean 'True'.
print("Metro?", data["metro"])

# load  = from a FILE      loads = from a STRING
