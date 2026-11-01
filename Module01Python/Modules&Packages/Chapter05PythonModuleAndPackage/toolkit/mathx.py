"""toolkit.mathx - a submodule that itself uses a built-in module."""

import math


def factorial(n):
    return math.factorial(n)


def is_prime(n):
    if n < 2:
        return False
    return all(n % i for i in range(2, math.isqrt(n) + 1))
