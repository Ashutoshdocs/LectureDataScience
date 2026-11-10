"""
SUGGESTED SOLUTIONS FOR STUDENT PRACTICE

Encourage students to attempt the exercises before reading this file.
"""


# 1. Basic function
def show_person():
    print("Name: Rahul")
    print("Age: 25")
    print("City: Patna")


show_person()


# 2. Product of two numbers
def multiply(a, b):
    return a * b


print("Product:", multiply(5, 4))


# 3. Square
def square(number):
    return number ** 2


print("Square:", square(6))


# 4. Local scope
def show_local():
    message = "I am local"
    print(message)


show_local()
# print(message)  # NameError: message is not defined in this outer scope.


# 5. Average with *args
def average(*values):
    if not values:
        return None
    return sum(values) / len(values)


print("Average:", average(10, 20, 30, 40))
print("Average with no values:", average())


# 6. Student details with **kwargs
def show_student(**details):
    for key, value in details.items():
        print(f"{key}: {value}")


show_student(name="Amit", age=22, course="Python")


# 7. Student marks and percentage
def student_result(name, *marks):
    if not marks:
        return name, 0, 0.0

    total = sum(marks)
    percentage = total / len(marks)
    return name, total, percentage


print(student_result("Priya", 80, 90, 70))


# 8. Employee details
def employee(name, *skills, **details):
    print("Name:", name)
    print("Skills:", ", ".join(skills) if skills else "None")
    print("Other details:")
    for key, value in details.items():
        print(f"{key}: {value}")


employee(
    "Riya",
    "Python",
    "Linux",
    department="Cloud",
    city="Patna"
)


# CHALLENGE: Menu-driven calculator
def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply_numbers(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        return "Cannot divide by zero"
    return a / b


def calculator():
    print("1. Add  2. Subtract  3. Multiply  4. Divide")
    choice = input("Choose 1-4: ")

    try:
        a = float(input("First number: "))
        b = float(input("Second number: "))
    except ValueError:
        print("Enter valid numbers.")
        return

    operations = {
        "1": add,
        "2": subtract,
        "3": multiply_numbers,
        "4": divide,
    }

    operation = operations.get(choice)
    if operation is None:
        print("Invalid choice.")
        return

    print("Result:", operation(a, b))


if __name__ == "__main__":
    calculator()
