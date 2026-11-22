"""Reference solutions for exercises.py."""
import functools


def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"


def area_of_rectangle(length, width):
    return length * width


def min_max(numbers):
    return min(numbers), max(numbers)


def is_even(n):
    return n % 2 == 0


def count_vowels(text):
    return sum(1 for ch in text.lower() if ch in "aeiou")


def make_counter():
    count = 0

    def counter():
        nonlocal count
        count += 1
        return count
    return counter


def average(*numbers):
    return sum(numbers) / len(numbers) if numbers else 0


def build_profile(name, **details):
    return {"name": name, **details}


def safe_divide(a, b, *, default=None):
    try:
        return a / b
    except ZeroDivisionError:
        return default


def apply_twice(func, value):
    return func(func(value))


def sort_by_age(people):
    return sorted(people, key=lambda person: person[1])


def squares_of_evens(numbers):
    return [n * n for n in numbers if n % 2 == 0]


def make_multiplier(n):
    def multiply(x):
        return x * n
    return multiply


def shout(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs).upper()
    return wrapper


def count_calls(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.calls += 1
        return func(*args, **kwargs)
    wrapper.calls = 0
    return wrapper


def repeat(times):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return [func(*args, **kwargs) for _ in range(times)]
        return wrapper
    return decorator


def factorial(n):
    return 1 if n == 0 else n * factorial(n - 1)


def flatten(nested):
    result = []
    for item in nested:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result


def countdown(n):
    while n > 0:
        yield n
        n -= 1


def parse_age(text):
    try:
        age = int(text)
    except (TypeError, ValueError):
        raise ValueError(f"not a whole number: {text!r}") from None
    if not 0 <= age <= 130:
        raise ValueError(f"age out of range: {age}")
    return age
