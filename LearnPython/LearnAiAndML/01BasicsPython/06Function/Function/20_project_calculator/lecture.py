"""Lecture 20: Project: a calculator built from small functions.

Set INTERACTIVE = True to type your own expressions (type 'quit' to stop).
"""
import functools
import math

INTERACTIVE = False
HISTORY = []


# ---------- 1. Tiny pure functions ----------
def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("cannot divide by zero")
    return a / b


def factorial(n):
    if n < 0 or n != int(n):
        raise ValueError("factorial needs a non-negative whole number")
    return 1 if n == 0 else n * factorial(n - 1)


def square_root(x):
    if x < 0:
        raise ValueError("cannot take the square root of a negative number")
    return math.sqrt(x)


# ---------- 2. Dispatch tables ----------
OPERATIONS = {
    "+": add, "-": subtract, "*": multiply, "/": divide,
    "//": lambda a, b: divide(a, b) // 1,
    "%": lambda a, b: a % b,
    "**": pow,
}
UNARY = {"sqrt": square_root, "!": factorial}


# ---------- 3. A closure for consistent rounding ----------
def make_rounder(places):
    def rounder(x):
        x = round(x, places)
        return int(x) if x == int(x) else x
    return rounder


tidy = make_rounder(4)


# ---------- 4. Decorators ----------
def log_history(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if isinstance(result, (int, float)):
            HISTORY.append(result)
        return result
    return wrapper


def safe(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, ZeroDivisionError, OverflowError, RecursionError) as e:
            return f"Error: {e}"
    return wrapper


# ---------- 5. Parsing & validation ----------
def parse_number(text, last=None):
    if text == "ans":
        if last is None:
            raise ValueError("no previous answer yet")
        return last
    try:
        value = float(text)
    except ValueError:
        raise ValueError(f"{text!r} is not a number") from None
    return int(value) if value.is_integer() else value


@safe
@log_history
def calculate(expression, *, history=HISTORY):
    last = history[-1] if history else None
    parts = expression.split()
    if len(parts) == 2 and parts[0] in UNARY:              # sqrt 16
        return tidy(UNARY[parts[0]](parse_number(parts[1], last)))
    if len(parts) == 2 and parts[1] in UNARY:              # 5 !
        return tidy(UNARY[parts[1]](parse_number(parts[0], last)))
    if len(parts) != 3:
        raise ValueError("use: number operator number  (e.g. 12 * 3), 'sqrt x' or 'x !'")
    a, op, b = parts
    if op not in OPERATIONS:
        raise ValueError(f"unknown operator {op!r} (use one of {' '.join(OPERATIONS)})")
    return tidy(OPERATIONS[op](parse_number(a, last), parse_number(b, last)))


# ---------- 6. *args statistics ----------
def stats(*numbers):
    if not numbers:
        raise ValueError("stats needs at least one number")
    return {"count": len(numbers), "total": tidy(sum(numbers)), "mean": tidy(sum(numbers) / len(numbers)),
            "min": min(numbers), "max": max(numbers)}


def handle(line):
    if line.startswith("stats"):
        try:
            nums = [parse_number(t) for t in line.split()[1:]]
            s = stats(*nums)
            return "= " + ", ".join(f"{k} {v}" for k, v in s.items())
        except ValueError as e:
            return f"! Error: {e}"
    result = calculate(line)
    return f"! {result}" if isinstance(result, str) else f"= {result}"


def main():
    demo = ["12 * 3", "ans + 4", "10 / 0", "sqrt 2", "5 !", "2 ^ 3", "7 // 2", "2 ** 10",
            "ten + 1", "sqrt -9", "stats 4 8 15 16 23 42", "stats"]
    if INTERACTIVE:
        print("Calculator: type an expression, 'stats n1 n2 ...', or 'quit'")
        while (line := input("> ").strip()) != "quit":
            print(handle(line))
    else:
        for line in demo:
            print(f"> {line:<22} {handle(line)}")
    print("\nhistory:", HISTORY)
    print("operations available:", " ".join(OPERATIONS), "|", " ".join(UNARY))
    print("calculate is still called", repr(calculate.__name__), "thanks to functools.wraps")


if __name__ == "__main__":
    main()
