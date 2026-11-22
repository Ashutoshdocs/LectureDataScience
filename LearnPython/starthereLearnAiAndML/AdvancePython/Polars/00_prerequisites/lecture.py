"""Lecture 00: Prerequisites: chaining, column thinking, 'what not how'. No Polars yet."""
import numpy as np

print("--- 1. Method chaining ---")
city = "  New DELHI "
print(repr(city), "->", repr(city.strip().lower().replace(" ", "-")))

print("\n--- 2. Row-oriented vs column-oriented ---")
rows = [{"name": "Asha", "maths": 78}, {"name": "Ravi", "maths": 92}, {"name": "Meena", "maths": 45}]
columns = {key: [r[key] for r in rows] for key in rows[0]}
print("rows   :", rows)
print("columns:", columns)
print("average from columns is one step:", sum(columns["maths"]) / len(columns["maths"]))

print("\n--- 3. 'How' (loop) vs 'what' (vectorized) ---")
prices = [120, 560, 999, 45]
with_tax = []
for p in prices:
    with_tax.append(round(p * 1.18, 2))
print("loop     :", with_tax)
print("numpy    :", np.round(np.array(prices) * 1.18, 2))

nums = [1, 2, 3, 4, 5]
a = np.array(nums)
print("comprehension:", [x ** 2 for x in nums if x > 2], "| numpy mask:", a[a > 2] ** 2)

print("\n--- 4. Keyword arguments ---")
print(sorted([3, 1, 2], reverse=True))

print("\nPolars combines all three ideas: chains of methods, column-at-a-time")
print("data, and expressions that describe WHAT you want. See Lecture 01.")
