"""
Python List Lab - Answers to the 10 Student Practice Tasks.

The tasks run IN ORDER on the same list, so each step starts from the
result of the step before it.

Run:  python answers.py
"""

marks = [85, 72, 90, 65, 88]
print("Starting list:", marks)

print("\nQ1. Add 95")
marks.append(95)
print(marks)

print("\nQ2. Remove 65")
marks.remove(65)
print(marks)

print("\nQ3. Find maximum marks")
print(max(marks))

print("\nQ4. Find minimum marks")
print(min(marks))

print("\nQ5. Find total marks")
print(sum(marks))

print("\nQ6. Find number of students")
print(len(marks))

print("\nQ7. Sort marks ascending")
marks.sort()
print(marks)

print("\nQ8. Sort marks descending")
marks.sort(reverse=True)
print(marks)

print("\nQ9. Reverse the list")
marks.reverse()
print(marks)

print("\nQ10. Create a copy of the list")
marks_copy = marks.copy()
print(marks_copy)
marks_copy.append(100)
print("Copy    :", marks_copy)
print("Original:", marks)
