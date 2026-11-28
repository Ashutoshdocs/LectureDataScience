import csv
from pathlib import Path
import numpy as np

# Locate the CSV file in this project's data folder.
DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "students.csv"

students = []
marks_rows = []

# Read student names and marks from CSV.
with DATA_FILE.open("r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        students.append(row["Student"])
        marks_rows.append([
            int(row["Mathematics"]),
            int(row["Science"]),
            int(row["English"])
        ])

students = np.array(students)
subjects = np.array(["Mathematics", "Science", "English"])
marks = np.array(marks_rows)

print("Student names:")
print(students)
print("\nSubjects:")
print(subjects)
print("\nMarks:")
print(marks)

# Total and average marks for each student.
total_marks = np.sum(marks, axis=1)
average_marks = np.mean(marks, axis=1)

# Average for each subject.
subject_averages = np.mean(marks, axis=0)

# Highest and lowest individual marks.
highest_mark = np.max(marks)
lowest_mark = np.min(marks)

# Student with the highest average.
top_index = np.argmax(average_marks)

# A student passes only if every subject mark is at least 40.
passed = np.all(marks >= 40, axis=1)

# Assign grades based on each student's average.
conditions = [
    average_marks >= 90,
    average_marks >= 75,
    average_marks >= 60,
    average_marks >= 40
]
choices = ["A", "B", "C", "D"]
grades = np.select(conditions, choices, default="F")

# Students whose average is below 60 need improvement.
needs_improvement = average_marks < 60

# Complete report.
print("\n========== STUDENT PERFORMANCE REPORT ==========")

for index, name in enumerate(students):
    print("\nStudent:", name)
    print("Marks:", marks[index])
    print("Total:", total_marks[index])
    print("Average:", round(average_marks[index], 2))
    print("Grade:", grades[index])
    print("Result:", "Pass" if passed[index] else "Fail")

print("\nSubject-wise average:")
for subject, average in zip(subjects, subject_averages):
    print(subject, ":", round(average, 2))

print("\nTop performer:", students[top_index])
print("Top average:", round(average_marks[top_index], 2))
print("Highest individual mark:", highest_mark)
print("Lowest individual mark:", lowest_mark)
print("Students needing improvement:", students[needs_improvement])
