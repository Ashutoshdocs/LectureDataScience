"""Lecture 16 — Reshape, sort, join and unique."""
import numpy as np

print("=== 1. reshape, flatten, transpose ===")
a = np.arange(1, 13)
print(a)
print(a.reshape(3, 4))
print(a.reshape(2, -1))          # -1 = "work it out"

m = a.reshape(3, 4)
print(m.T)                       # transpose: rows <-> columns
print(m.T.shape)
print(m.flatten())               # back to 1D
print(a.reshape(2, 3, 2).shape)  # 3D

try:
    a.reshape(5, 2)              # 12 values can't make 5 x 2
except ValueError as e:
    print("Error:", e)

print("\n=== 2. sort and argsort ===")
scores = np.array([72, 95, 58, 88, 64])
names = np.array(["Asha", "Ravi", "Meena", "John", "Zara"])

print(np.sort(scores))             # new sorted array
print(np.sort(scores)[::-1])       # descending
print(scores)                      # original unchanged

order = np.argsort(scores)[::-1]   # positions, best first
print(order)
print(names[order])                # names ranked by score
print("Top 3:", names[order][:3])
print(np.sort(names))              # alphabetical

scores.sort()                      # sorts IN PLACE
print(scores)

print("\n=== 3. Joining arrays ===")
week1 = np.array([5, 7, 6])
week2 = np.array([8, 4, 9])

print(np.concatenate([week1, week2]))    # one long 1D array
print(np.vstack([week1, week2]))         # stack as rows
print(np.hstack([week1, week2]))         # side by side
print(np.column_stack([week1, week2]))   # as columns

table = np.vstack([week1, week2])
extra = np.array([[1, 1, 1]])
print(np.concatenate([table, extra], axis=0))   # add a row
print(np.hstack([table, np.array([[0], [0]])])) # add a column

print("\n=== 4. unique and counting ===")
votes = np.array(["tea", "coffee", "tea", "juice", "tea", "coffee"])
print(np.unique(votes))
kinds, counts = np.unique(votes, return_counts=True)
print(kinds)
print(counts)
print("Winner:", kinds[counts.argmax()], "| Least popular:", kinds[counts.argmin()])

dice = np.array([3, 6, 1, 6, 6, 2, 3])
print(np.bincount(dice))      # how many 0s, 1s, 2s, ... 6s
