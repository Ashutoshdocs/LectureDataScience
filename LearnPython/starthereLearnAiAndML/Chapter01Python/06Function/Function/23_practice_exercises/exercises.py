"""Practice exercises: fill in each function, then run:  python lecture.py exercises"""
import functools


def greet(name, greeting="Hello"):
    """Return '<greeting>, <name>!'.   greet('Asha') -> 'Hello, Asha!'   greet('Ravi', 'Hi') -> 'Hi, Ravi!'"""
    ...


def area_of_rectangle(length, width):
    """Return length * width.   area_of_rectangle(3, 4) -> 12"""
    ...


def min_max(numbers):
    """Return a tuple (smallest, largest).   min_max([4, 1, 9]) -> (1, 9)"""
    ...


def is_even(n):
    """Return True if n is even.   is_even(4) -> True"""
    ...


def count_vowels(text):
    """Count a, e, i, o, u (any case).   count_vowels('Hello World') -> 3"""
    ...


def make_counter():
    """Return a function that returns 1, 2, 3, ... on successive calls (use a closure + nonlocal)."""
    ...


def average(*numbers):
    """Average of any number of values; return 0 if none.   average(2, 4, 6) -> 4.0"""
    ...


def build_profile(name, **details):
    """Return a dict with 'name' plus all details.   build_profile('Asha', age=25) -> {'name': 'Asha', 'age': 25}"""
    ...


def safe_divide(a, b, *, default=None):
    """Return a / b, or `default` if b is 0.   safe_divide(1, 0, default=0) -> 0"""
    ...


def apply_twice(func, value):
    """Return func(func(value)).   apply_twice(lambda x: x + 3, 1) -> 7"""
    ...


def sort_by_age(people):
    """people is a list of (name, age) tuples. Return a new list sorted by age, youngest first."""
    ...


def squares_of_evens(numbers):
    """Return the squares of the even numbers, in order.   squares_of_evens([1, 2, 3, 4]) -> [4, 16]"""
    ...


def make_multiplier(n):
    """Return a function that multiplies its argument by n.   make_multiplier(3)(5) -> 15"""
    ...


def shout(func):
    """Decorator: the decorated function's string result is returned in UPPERCASE. Keep the name (functools.wraps)."""
    ...


def count_calls(func):
    """Decorator: the wrapper gets an attribute .calls counting how many times it was called."""
    ...


def repeat(times):
    """Decorator with an argument: call the function `times` times and return a list of the results."""
    ...


def factorial(n):
    """Recursive factorial.   factorial(5) -> 120, factorial(0) -> 1"""
    ...


def flatten(nested):
    """Recursively flatten nested lists.   flatten([1, [2, [3]], 4]) -> [1, 2, 3, 4]"""
    ...


def countdown(n):
    """Generator yielding n, n-1, ..., 1.   list(countdown(3)) -> [3, 2, 1]"""
    ...


def parse_age(text):
    """Return int(text) if it is a whole number from 0 to 130, else raise ValueError."""
    ...
