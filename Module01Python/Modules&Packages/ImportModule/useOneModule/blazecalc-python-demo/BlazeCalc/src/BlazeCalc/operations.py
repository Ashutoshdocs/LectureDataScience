"""Basic math operations. Each one validates its inputs first."""

from numbers import Real


def _check_numbers(*values):
    for v in values:
        # bool is a subclass of int, so reject it explicitly
        if isinstance(v, bool) or not isinstance(v, Real):
            raise TypeError(f"BlazeCalc: expected a number, got {v!r}")


def add(a, b):
    _check_numbers(a, b)
    return a + b


def subtract(a, b):
    _check_numbers(a, b)
    return a - b


def multiply(a, b):
    _check_numbers(a, b)
    return a * b


def divide(a, b):
    _check_numbers(a, b)
    if b == 0:
        raise ZeroDivisionError("BlazeCalc: cannot divide by zero")
    return a / b


def percent(value, pct):
    _check_numbers(value, pct)
    return value * pct / 100


def power(base, exponent):
    _check_numbers(base, exponent)
    return base ** exponent


def sqrt(n):
    _check_numbers(n)
    if n < 0:
        raise ValueError("BlazeCalc: cannot take the square root of a negative number")
    return n ** 0.5
