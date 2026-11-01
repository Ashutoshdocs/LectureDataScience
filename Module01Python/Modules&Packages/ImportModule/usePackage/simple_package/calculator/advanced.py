# calculator/advanced.py
# ----------------------
# A second MODULE inside the calculator package.
# It holds the harder math functions.

import math  # Import Python's built-in math module (gives us math.sqrt)


def power(base, exponent):  # Define a function that raises base to exponent
    return base ** exponent  # "**" means "to the power of" (2 ** 3 = 8)


def square_root(number):  # Define a function that finds a square root
    if number < 0:  # Square roots of negative numbers are not real numbers
        raise ValueError("Cannot take the square root of a negative number")  # Stop with a clear error
    return math.sqrt(number)  # Send back the square root using the math module
