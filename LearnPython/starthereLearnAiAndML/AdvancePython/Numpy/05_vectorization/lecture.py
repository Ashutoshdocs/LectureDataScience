"""Lecture 05 — Vectorization: replace loops with whole-array operations."""
import math
import numpy as np

prices = [120, 560, 999, 45]

# Loop version: plain Python, one price at a time
with_tax = []
for p in prices:
    with_tax.append(round(p * 1.18, 2))
print(with_tax)

# Vectorized version: NumPy, every price at once
arr = np.array(prices)
print(np.round(arr * 1.18, 2))

# Bonus: 10% off only the prices over 500
print(np.where(arr > 500, arr * 0.9, arr))

print("\n--- Watch the loop step by step ---")
with_tax = []
for step, p in enumerate(prices, start=1):
    with_tax.append(round(p * 1.18, 2))
    print(f"step {step}: p = {p:4} -> with_tax = {with_tax}")
print("NumPy did the same in ONE step:", np.round(arr * 1.18, 2))

print("\n--- Loop pattern  ->  vectorized ---")
a = np.array([4, -1, 9, 0, 16, -5])
b = np.array([1, 2, 3, 4, 5, 6])
al, bl = a.tolist(), b.tolist()

print("double     :", [x * 2 for x in al], "->", a * 2)
print("pair sum   :", [x + y for x, y in zip(al, bl)], "->", a + b)
print("sqrt (>=0) :", [math.sqrt(x) for x in al if x >= 0], "->", np.sqrt(a[a >= 0]))
print("filter >0  :", [x for x in al if x > 0], "->", a[a > 0])
print("clip neg   :", [x if x > 0 else 0 for x in al], "->", np.where(a > 0, a, 0))

total = 0
for x in al:
    total += x
print("total      :", total, "->", a.sum())

count = 0
for x in al:
    if x > 5:
        count += 1
print("count > 5  :", count, "->", (a > 5).sum())

print("\n--- A formula, vectorized ---")
x = np.arange(10)
print("x**2 - 3x + 2 =", x**2 - 3*x + 2)
print("labels:", np.where(arr > 500, "costly", "cheap"))
