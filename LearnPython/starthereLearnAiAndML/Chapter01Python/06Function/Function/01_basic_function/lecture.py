"""Lecture 01: Your first function: def, call, docstring, DRY."""

print("=== 1. Define once, call many times ===")


def greet():
    """Print a welcome message."""
    print("  Welcome to Python!")


greet()
greet()

print("\n=== 2. The copy-paste problem, solved ===")


def average(numbers):
    """Return the average of a list of numbers."""
    total = 0
    for n in numbers:
        total += n
    return total / len(numbers)


for name, marks in [("A", [78, 92, 45, 83]), ("B", [67, 71, 88]), ("C", [95, 59, 73, 64, 80])]:
    print(f"  Class {name} average: {average(marks):.2f}")
print("  One definition, three calls, and no copy can go out of sync.")

print("\n=== 3. Defining is not running ===")


def boom():
    print(1 / 0)


print("  boom() defined without any error")
try:
    boom()
except ZeroDivisionError as e:
    print("  calling boom() ->", type(e).__name__ + ":", e)

print("\n=== 4. Docstrings ===")


def area(width, height):
    """Return the area of a rectangle."""
    return width * height


print("  area.__doc__ :", area.__doc__)
print("  area.__name__:", area.__name__)

print("\n=== 5. A placeholder function ===")


def todo_later():
    pass


print("  todo_later() returns:", todo_later())

print("\n=== 6. A function is a value ===")
print("  type(greet):", type(greet).__name__)
print("  greet without () is the function itself:", greet.__name__)
