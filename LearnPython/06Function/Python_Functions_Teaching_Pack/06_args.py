"""
MODULE 6: *args

*args collects extra positional arguments into a tuple.
The name `args` is a convention; another valid name could be used.
"""


# A. See what *args collects
def show_values(*args):
    print("Collected values:", args)
    print("Type:", type(args))


show_values(10, 20)
show_values(10, 20, 30, 40)


# B. Add any number of values
def add_all(*args):
    total = 0
    for number in args:
        total += number
    return total


print("Sum 1:", add_all(10, 20))
print("Sum 2:", add_all(10, 20, 30))
print("Sum 3:", add_all(10, 20, 30, 40, 50))


# C. A normal parameter before *args
def show_students(course, *students):
    print("Course:", course)
    for student in students:
        print("Student:", student)


show_students("Python", "Rahul", "Amit", "Priya")


# D. Unpacking a list with *
def add_three(a, b, c):
    return a + b + c


numbers = [10, 20, 30]
print("Unpacked list result:", add_three(*numbers))

# The * operator unpacks the list into separate positional arguments.
