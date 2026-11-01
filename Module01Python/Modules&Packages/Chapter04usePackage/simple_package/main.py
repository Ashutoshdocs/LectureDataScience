# main.py
# -------
# This program USES the calculator package.
# Run it from this folder with:   python main.py

print("Step 1: importing the package...")  # Message printed before the import happens
import calculator  # Runs calculator/__init__.py (watch for "calculator package loaded")
import calculator  # Importing again does NOT run __init__.py again (Python remembers it)

print()  # Print an empty line to keep the output tidy
print("Step 2: using the package version")  # Heading for this part
print("Version:", calculator.__version__)  # Read the variable defined in __init__.py

print()  # Empty line
print("Step 3: short names (thanks to __init__.py)")  # Heading for this part
print("add(5, 3) =", calculator.add(5, 3))  # Call add() through the package -> 8
print("subtract(10, 4) =", calculator.subtract(10, 4))  # Call subtract() -> 6
print("power(2, 3) =", calculator.power(2, 3))  # Call power() -> 8
print("square_root(16) =", calculator.square_root(16))  # Call square_root() -> 4.0

print()  # Empty line
print("Step 4: other ways to import")  # Heading for this part
from calculator import add  # Import ONE function straight from the package
print("add(1, 2) =", add(1, 2))  # Now we can call it without "calculator." -> 3
from calculator.advanced import power  # Long form: package.module -> function
print("power(3, 2) =", power(3, 2))  # Works the same way -> 9
from calculator import *  # Import every name listed in __all__
print("subtract(9, 1) =", subtract(9, 1))  # subtract came in through * -> 8

print()  # Empty line
print("Step 5: handling an error")  # Heading for this part
try:  # Try code that might fail
    calculator.square_root(-9)  # This raises ValueError on purpose
except ValueError as error:  # Catch the error instead of crashing
    print("Error caught:", error)  # Show the error message
