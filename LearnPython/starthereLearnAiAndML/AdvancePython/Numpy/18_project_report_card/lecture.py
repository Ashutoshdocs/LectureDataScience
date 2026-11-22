"""Lecture 18 — Project: a class report card with NumPy."""
import numpy as np

names = np.array(["Asha", "Ravi", "Meena", "John", "Zara"])
subjects = np.array(["Maths", "Science", "English", "CS"])
marks = np.array([[78, 85, 62, 90],
                  [92, 88, 79, 95],
                  [45, 52, 68, 40],
                  [83, 64, 90, 77],
                  [67, 73, 58, 81]])

percent = marks.mean(axis=1).round(1)
grade = np.where(percent >= 80, "A", np.where(percent >= 60, "B", "C"))

for n, p, g in zip(names, percent, grade):
    print(f"{n:<6} {p:5.1f}%  grade {g}")

print("Topper:", names[percent.argmax()])
print("Subject averages:", dict(zip(subjects.tolist(), marks.mean(axis=0).tolist())))
print("Hardest subject:", subjects[marks.mean(axis=0).argmin()])
print("Failed (<50) per subject:", (marks < 50).sum(axis=0))

print("\n--- Extensions ---")
order = np.argsort(percent)[::-1]
print("Ranking:", names[order])
print("Best subject per student:", dict(zip(names.tolist(), subjects[marks.argmax(axis=1)].tolist())))
print("Failed any subject:", names[(marks < 50).any(axis=1)])

class_avg = marks.mean(axis=0)
print("Marks vs class average per subject:")
print((marks - class_avg).round(1))

finer = np.select([percent >= 85, percent >= 75, percent >= 60], ["A+", "A", "B"], default="C")
print("Finer grades:", dict(zip(names.tolist(), finer.tolist())))

hardest = marks.mean(axis=0).argmin()
graced = marks.copy()
graced[:, hardest] = np.clip(graced[:, hardest] + 5, 0, 100)
print(f"After +5 grace in {subjects[hardest]}:", graced[:, hardest])
