"""Lecture 21 — Recap: why NumPy wins, in one runnable file."""
import numpy as np

data = list(range(1, 11))
arr = np.array(data)

# 1. Concise: maths reads like the formula
print("Squares:", arr ** 2)

# 2. Powerful: filter, aggregate, reshape in one line each
print("Even:", arr[arr % 2 == 0])
print("Mean:", arr.mean(), " Std:", arr.std().round(2))
print(arr.reshape(2, 5))

# 3. Compact: raw numbers, one type
print("Bytes:", arr.nbytes, "for", arr.size, "values of", arr.dtype)

# 4. Compatible: back to Python whenever you like
print(arr.tolist() == data)

print("\n--- Quick self-test: predict each line before running ---")
m = np.arange(1, 13).reshape(3, 4)
print("m =\n", m)
print("1. m[1, 2]            ->", m[1, 2])
print("2. m[:, 0]            ->", m[:, 0])
print("3. m.sum(axis=0)      ->", m.sum(axis=0))
print("4. m.mean(axis=1)     ->", m.mean(axis=1))
print("5. m[m > 6]           ->", m[m > 6])
print("6. (m % 3 == 0).sum() ->", (m % 3 == 0).sum())
print("7. m.T.shape          ->", m.T.shape)
print("8. m * [1, 0, 1, 0]   ->\n", m * np.array([1, 0, 1, 0]))
print("9. np.where(m > 6, 1, 0) ->\n", np.where(m > 6, 1, 0))
print("10. m.argmax()        ->", m.argmax(), "(position in the flattened array)")
