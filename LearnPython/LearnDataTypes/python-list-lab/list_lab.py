"""
Python List Data Type Lab - all labs in one script.

Run:  python list_lab.py
"""


def lab(title):
    print("\n" + "=" * 50)
    print(title)
    print("=" * 50)


# ---------------- PART 1: CREATE ----------------
lab("01. Creating a list")
students = ["Rahul", "Amit", "Neha", "Priya"]
print(students)

students = []
print(students)

mixed = ["Rahul", 25, 85.5, True]
print(mixed)

# ---------------- PART 2: INDEXING ----------------
lab("02. Positive indexing")
students = ["Rahul", "Amit", "Neha", "Priya"]
print(students[0])
print(students[2])

lab("03. Negative indexing")
students = ["Rahul", "Amit", "Neha", "Priya"]
print(students[-1])
print(students[-2])

# ---------------- PART 3: SLICING ----------------
lab("04. List slicing")
students = ["Rahul", "Amit", "Neha", "Priya"]
print(students[1:3])
print(students[:2])
print(students[2:])
print(students[::-1])

# ---------------- PART 4: ADD / INSERT ----------------
lab("05. append()")
students = ["Rahul", "Amit"]
students.append("Neha")
print(students)

lab("06. insert()")
students = ["Rahul", "Amit", "Neha"]
students.insert(1, "Priya")
print(students)

lab("07. extend()")
students = ["Rahul", "Amit"]
new_students = ["Neha", "Priya"]
students.extend(new_students)
print(students)

lab("07b. append() vs extend()")
students = ["Rahul", "Amit"]
students.append(["Neha", "Priya"])
print(students)

students = ["Rahul", "Amit"]
students.extend(["Neha", "Priya"])
print(students)

# ---------------- PART 5: REMOVE ----------------
lab("08. remove()")
students = ["Rahul", "Amit", "Neha"]
students.remove("Amit")
print(students)

lab("09. pop()")
students = ["Rahul", "Amit", "Neha"]
student = students.pop(1)
print(student)
print(students)

students = ["Rahul", "Amit", "Neha"]
last = students.pop()
print(last)
print(students)

lab("10. clear()")
students = ["Rahul", "Amit", "Neha"]
students.clear()
print(students)

lab("11. del statement")
students = ["Rahul", "Amit", "Neha", "Priya"]
del students[0]
print(students)

students = ["Rahul", "Amit", "Neha", "Priya"]
del students[1:3]
print(students)

# ---------------- PART 6: SEARCH / COUNT ----------------
lab("12. index()")
students = ["Rahul", "Amit", "Neha"]
print(students.index("Amit"))

lab("13. count()")
numbers = [10, 20, 10, 30, 10]
print(numbers.count(10))

lab("14. in - membership check")
students = ["Rahul", "Amit", "Neha"]
print("Amit" in students)
print("Rohit" in students)

# ---------------- PART 7: SORT / REVERSE ----------------
lab("15. sort()")
numbers = [50, 10, 40, 20, 30]
numbers.sort()
print(numbers)

numbers.sort(reverse=True)
print(numbers)

lab("16. reverse()")
students = ["Rahul", "Amit", "Neha"]
students.reverse()
print(students)

# ---------------- PART 8: COPY ----------------
lab("17. copy()")
students = ["Rahul", "Amit", "Neha"]
new_students = students.copy()
print(new_students)

lab("18. assignment vs copy()")
students = ["Rahul", "Amit", "Neha"]
same_list = students
same_list.append("Priya")
print(students)

students = ["Rahul", "Amit", "Neha"]
copied_list = students.copy()
copied_list.append("Priya")
print(students)
print(copied_list)

# ---------------- PART 9: BUILT-IN FUNCTIONS ----------------
lab("19. len()")
students = ["Rahul", "Amit", "Neha", "Priya"]
print(len(students))

lab("20. min()")
numbers = [50, 10, 40, 20, 30]
print(min(numbers))

lab("21. max()")
numbers = [50, 10, 40, 20, 30]
print(max(numbers))

lab("22. sum()")
numbers = [10, 20, 30, 40]
print(sum(numbers))

lab("23. sorted()")
numbers = [50, 10, 30, 20]
result = sorted(numbers)
print(result)
print(numbers)

# ---------------- PART 10: MUTABILITY ----------------
lab("24. List is mutable")
students = ["Rahul", "Amit", "Neha"]
students[1] = "Rohit"
print(students)

# ---------------- REAL-WORLD PROJECT ----------------
lab("25. Real-world project: employee list")
employees = ["Rahul", "Amit", "Neha"]
employees.append("Priya")
employees.remove("Amit")
print("Neha" in employees)
print(len(employees))
print(employees)

print("\nAll labs completed successfully.")
