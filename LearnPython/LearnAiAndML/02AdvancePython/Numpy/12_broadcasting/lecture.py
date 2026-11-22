"""Lecture 12 — Broadcasting: combining arrays of different shapes."""
import numpy as np

print("=== 1. Array with a single number ===")
celsius = np.array([0, 18.5, 25, 37, 100])
fahrenheit = celsius * 9 / 5 + 32
print(fahrenheit)

prices = np.array([499, 1299, 250])
print(prices * 0.8)            # 20% sale
print(prices - 50)             # Rs 50 off each
print(prices > 400)            # compare every price

print("\n=== 2. Rows and columns ===")
# 3 shops x 4 products: units sold
sold = np.array([[10,  5,  0,  8],
                 [ 3, 12,  7,  1],
                 [ 6,  6,  6,  6]])

price = np.array([20, 50, 100, 10])     # one price per product: (4,)

revenue = sold * price                  # (3,4) * (4,) works!
print(revenue)
print("Per shop:", revenue.sum(axis=1))

bonus = np.array([[1], [2], [3]])       # one value per shop: (3,1)
print(sold + bonus)

try:
    sold + np.array([1, 2, 3])          # (3,4) + (3,) -> error
except ValueError as e:
    print("Error:", e)

print("\n=== 3. Making a column ===")
b = np.array([1, 2, 3])
print(b.shape, b[:, np.newaxis].shape, b.reshape(-1, 1).shape)
print(sold + b[:, np.newaxis])          # the fix

print("\n=== 4. (3,1) with (1,4) -> (3,4) ===")
print(np.arange(1, 6)[:, None] * np.arange(1, 6))   # times table

print("\n=== 5. Normalise each column ===")
data = np.array([[150, 50], [160, 60], [170, 70], [180, 80]], dtype=float)
z = (data - data.mean(axis=0)) / data.std(axis=0)
print(z.round(2))
