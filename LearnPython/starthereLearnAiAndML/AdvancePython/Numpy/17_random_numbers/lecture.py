"""Lecture 17 — Random numbers with np.random.default_rng, and a simulation."""
import numpy as np

rng = np.random.default_rng(seed=42)   # random generator, repeatable

print("dice rolls   :", rng.integers(1, 7, size=10))
print("decimals     :", rng.random(3))
print("uniform 5-10 :", rng.uniform(5, 10, size=3).round(2))
print("heights      :", rng.normal(170, 10, size=4).round(1))
print("2D grid      :\n", rng.integers(0, 10, size=(3, 4)))

print("\n--- choice, shuffle, permutation ---")
fruits = np.array(["apple", "mango", "kiwi", "banana"])
print("pick 3 (repeats ok):", rng.choice(fruits, size=3))
print("pick 3 (no repeats):", rng.choice(fruits, size=3, replace=False))
print("weighted (mango 70%):", rng.choice(fruits, size=8, p=[0.1, 0.7, 0.1, 0.1]))
print("permutation copy   :", rng.permutation(fruits))
deck = np.arange(10)
rng.shuffle(deck)
print("shuffled in place  :", deck)
print("5-card hand        :", rng.choice(52, size=5, replace=False))

print("\n--- Same seed -> same numbers ---")
r1 = np.random.default_rng(7).integers(0, 100, 5)
r2 = np.random.default_rng(7).integers(0, 100, 5)
print(r1, r2, "identical:", np.array_equal(r1, r2))

print("\n--- Coin flips ---")
flips = rng.integers(0, 2, size=20)
print(flips, "heads:", flips.sum())

print("\n--- 600 dice: count each face ---")
print("faces 1-6:", np.bincount(rng.integers(1, 7, 600), minlength=7)[1:])

print("\n--- Simulation: P(two dice total 7) ---")
n = 100_000
d1 = rng.integers(1, 7, n)
d2 = rng.integers(1, 7, n)
estimate = np.mean(d1 + d2 == 7)
print(f"simulated: {estimate:.4f} | theory: {6/36:.4f}")
