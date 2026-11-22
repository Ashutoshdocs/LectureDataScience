"""Lecture 09: Type hints & docstrings."""
import doctest
from collections.abc import Callable

print("=== 1. Type hints ===")


def total_price(price: float, qty: int = 1, discount: float = 0.0) -> float:
    """Return price x qty after a fractional discount."""
    return price * qty * (1 - discount)


print("  total_price(100, 3, 0.1) =", total_price(100, 3, 0.1))
print("  annotations:", total_price.__annotations__)
def double(n: int) -> int:
    return n * 2


print("  NOT enforced: double('5') =", repr(double("5")), "<- wrong type, wrong answer, no error!")
print("  (a type checker such as mypy would flag double('5') before the program runs)")

print("\n=== 2. Hints for collections, optional values, functions ===")


def average(marks: list[float]) -> float:
    return sum(marks) / len(marks)


def find_user(users: list[dict[str, str]], name: str) -> dict[str, str] | None:
    for u in users:
        if u["name"] == name:
            return u
    return None


def apply_twice(func: Callable[[int], int], value: int) -> int:
    return func(func(value))


def total(*amounts: float, **labels: str) -> str:
    return f"{sum(amounts)} {labels}"


users = [{"name": "Asha", "city": "Pune"}]
print("  average:", average([70, 80.5]))
print("  find_user Asha:", find_user(users, "Asha"), "| Zara:", find_user(users, "Zara"))
print("  apply_twice(lambda x: x * 3, 2) =", apply_twice(lambda x: x * 3, 2))
print("  total(1, 2.5, unit='kg') =", total(1, 2.5, unit="kg"))

print("\n=== 3. A full docstring ===")


def bmi(weight_kg: float, height_m: float) -> float:
    """Calculate Body Mass Index.

    Args:
        weight_kg: Weight in kilograms (must be > 0).
        height_m: Height in metres (must be > 0).

    Returns:
        The BMI rounded to 1 decimal place.

    Raises:
        ValueError: If weight or height is not positive.

    Example:
        >>> bmi(70, 1.75)
        22.9
        >>> bmi(0, 1.75)
        Traceback (most recent call last):
        ...
        ValueError: weight and height must be positive
    """
    if weight_kg <= 0 or height_m <= 0:
        raise ValueError("weight and height must be positive")
    return round(weight_kg / height_m ** 2, 1)


print("  first docstring line:", bmi.__doc__.splitlines()[0])
print("  bmi(70, 1.75) =", bmi(70, 1.75))

print("\n=== 4. help() output (first lines) ===")
import io
import contextlib

buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    help(bmi)
for line in buf.getvalue().splitlines()[:6]:
    print("  |", line)

print("\n=== 5. doctest runs the >>> examples ===")
results = doctest.testmod(verbose=False)
print(f"  {results.attempted} examples run, {results.failed} failed")
