"""Lecture 11 — Element-wise arithmetic, ufuncs, np.where, nan/inf."""
import numpy as np

print("=== 1. Element-wise arithmetic ===")
a = np.array([10, 20, 30, 40])
b = np.array([ 1,  2,  3,  4])

print("a + b  =", a + b)
print("a - b  =", a - b)
print("a * b  =", a * b)
print("a / b  =", a / b)
print("a // b =", a // b)
print("a % 3  =", a % 3)
print("b ** 2 =", b ** 2)
print("% change =", (a - b) / b * 100)

try:
    a + np.array([1, 2, 3])
except ValueError as e:
    print("shape mismatch ->", e)

print("\n=== 2. Universal functions ===")
x = np.array([1, 4, 9, 16, 25])
print(np.sqrt(x))
print(np.square(x))

v = np.array([-2.7, -0.5, 1.2, 3.5])
print(np.abs(v))
print(np.round(v))
print(np.floor(v))
print(np.ceil(v))
print("round(2.5) =", np.round(2.5), "| round(3.5) =", np.round(3.5))

angles = np.array([0, 30, 90])
print(np.sin(np.radians(angles)).round(3))
print(np.log10([1, 10, 100, 1000]))
print(np.exp([0, 1, 2]).round(3))

print(np.maximum([1, 5, 3], [4, 2, 6]))
print(np.clip([-5, 3, 12, 8], 0, 10))

print("\n=== 3. np.where ===")
temps = np.array([28, 35, 31, 40])
print(np.where(temps > 32, "hot", "ok"))

print("\n=== 4. nan and inf ===")
with np.errstate(divide="ignore", invalid="ignore"):   # silence the warnings
    print(np.array([1.0, 0.0]) / 0)
data = np.array([4.0, np.nan, 6.0, 8.0])
print("data          :", data)
print("mean          :", data.mean())          # nan spreads
print("nanmean       :", np.nanmean(data))     # ignores nan
print("isnan         :", np.isnan(data))
print("nan == nan    :", np.nan == np.nan)
print("without nans  :", data[~np.isnan(data)])
