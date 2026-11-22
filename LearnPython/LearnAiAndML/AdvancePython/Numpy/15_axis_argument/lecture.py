"""Lecture 15 — The axis argument: rows vs columns."""
import numpy as np

subjects = np.array(["Maths", "Science", "English"])
# rows = students, columns = subjects
marks = np.array([[78, 85, 62],
                  [92, 88, 79],
                  [55, 70, 81],
                  [83, 64, 90]])

print("Overall mean     :", marks.mean())
print("Subject averages :", marks.mean(axis=0))
print("Student totals   :", marks.sum(axis=1))
print("Best in subject  :", marks.max(axis=0))
print("Topper (row)     :", marks.sum(axis=1).argmax())

print("\n--- Shapes: the named axis disappears ---")
print("marks          :", marks.shape)
print("mean(axis=0)   :", marks.mean(axis=0).shape)
print("mean(axis=1)   :", marks.mean(axis=1).shape)

print("\n--- More axis questions ---")
print("Lowest per student   :", marks.min(axis=1))
print("Best average subject :", subjects[marks.mean(axis=0).argmax()])
print("Above 80 per subject :", (marks > 80).sum(axis=0))
print("Anyone failed (<60)? :", (marks < 60).any(axis=1))

print("\n--- keepdims for broadcasting back ---")
row_means = marks.mean(axis=1, keepdims=True)
print("row_means shape:", row_means.shape)
print((marks - row_means).round(1))

print("\n--- 3D ---")
cube = np.arange(24).reshape(2, 3, 4)
for ax in (0, 1, 2, -1):
    print(f"sum(axis={ax:2}) shape -> {cube.sum(axis=ax).shape}")
