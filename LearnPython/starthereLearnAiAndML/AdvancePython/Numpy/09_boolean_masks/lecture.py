"""Lecture 09 — Boolean masks: filtering arrays with conditions."""
import numpy as np

marks = np.array([45, 82, 67, 91, 38, 74])
names = np.array(["Asha", "Ravi", "Meena", "John", "Zara", "Ali"])

passed = marks >= 50
print(passed)

print(marks[passed])                 # keep only True positions
print(marks[marks > 80])             # in one line
print("Passed:", passed.sum(), "of", marks.size)

print(marks[(marks > 60) & (marks < 80)])   # AND: use &
graced = marks.copy()
graced[graced < 50] = 50             # raise fails to 50 (grace)
print(graced)

print("\n--- More mask tricks ---")
print("below 40 OR above 90:", marks[(marks < 40) | (marks > 90)])
print("NOT passed          :", marks[~passed])
print("even marks count    :", (marks % 2 == 0).sum())
print("pass percentage     :", round(passed.mean() * 100, 2), "%")
print("positions over 80   :", np.where(marks > 80)[0])
print("names over 70       :", names[marks > 70])
print("names who failed    :", names[~passed])

print("\n--- The 'and' trap ---")
try:
    marks[(marks > 60) and (marks < 80)]
except ValueError as e:
    print("using 'and' fails ->", str(e)[:60], "...")
