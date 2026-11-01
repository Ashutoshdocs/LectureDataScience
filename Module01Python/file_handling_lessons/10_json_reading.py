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
os.chdir(os.path.dirname(os.path.abspath(__file__)))


print("===== 1. json.load(): file -> Python =====")
with open("products.json", encoding="utf-8") as f:
    products = json.load(f)
print("Type:", type(products))              # list
print("How many products:", len(products))
print("First product:", products[0])
print("Its name:", products[0]["name"])


print("\n===== 2. Loop through the data =====")
for p in products[:5]:
    print(f'{p["id"]:2}. {p["name"]:<12} Rs {p["price"]}')


print("\n===== 3. Filter: products in stock under Rs 300 =====")
cheap = [p["name"] for p in products if p["in_stock"] and p["price"] < 300]
print(cheap)


print("\n===== 4. Totals and maximum =====")
prices = [p["price"] for p in products]
print("Total value :", sum(prices))
print("Average     :", sum(prices) / len(prices))
expensive = max(products, key=lambda p: p["price"])
print("Most expensive:", expensive["name"], expensive["price"])


print("\n===== 5. Group by category =====")
groups = {}
for p in products:
    groups.setdefault(p["category"], []).append(p["name"])
for category, names in groups.items():
    print(category, "->", names)


print("\n===== 6. json.loads(): STRING -> Python =====")
text = '{"city": "Pune", "pin": 411001, "metro": true}'
data = json.loads(text)          # 's' at the end = string
print(data, type(data))
print("Metro?", data["metro"])

# load  = from a FILE      loads = from a STRING
