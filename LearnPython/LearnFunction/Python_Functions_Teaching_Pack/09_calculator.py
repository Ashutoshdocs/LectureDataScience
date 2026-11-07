"""
PROJECT 1: CALCULATOR USING FUNCTIONS

Concepts: function definition, parameters, return, conditional logic.
"""


def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        return "Cannot divide by zero"
    return a / b


def main():
    print("PYTHON FUNCTION CALCULATOR")
    print("1. Addition")
    print("2. Subtraction")
    print("3. Multiplication")
    print("4. Division")

    choice = input("Choose an operation (1-4): ")

    try:
        first = float(input("Enter first number: "))
        second = float(input("Enter second number: "))
    except ValueError:
        print("Please enter valid numbers.")
        return

    if choice == "1":
        result = add(first, second)
    elif choice == "2":
        result = subtract(first, second)
    elif choice == "3":
        result = multiply(first, second)
    elif choice == "4":
        result = divide(first, second)
    else:
        print("Invalid choice.")
        return

    print("Result:", result)


if __name__ == "__main__":
    main()
