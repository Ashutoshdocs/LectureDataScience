"""Lecture 18: Errors in functions: validate, raise, try/except/else/finally, custom errors."""

print("=== 1. Validate and raise ===")


def withdraw(balance, amount):
    if not isinstance(amount, (int, float)):
        raise TypeError(f"amount must be a number, got {type(amount).__name__}")
    if amount <= 0:
        raise ValueError(f"amount must be positive, got {amount}")
    if amount > balance:
        raise ValueError(f"insufficient funds: balance {balance}, requested {amount}")
    return balance - amount


print("  withdraw(1000, 300) =", withdraw(1000, 300))
for bad in ["300", -5, 5000]:
    try:
        withdraw(1000, bad)
    except (TypeError, ValueError) as e:
        print(f"  withdraw(1000, {bad!r}) -> {type(e).__name__}: {e}")

print("\n=== 2. try / except / else / finally ===")


def safe_divide(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        print(f"    except: {a}/{b} is not allowed")
        return None
    else:
        print(f"    else: no error")
        return round(result, 2)
    finally:
        print(f"    finally: always runs")


print("  ->", safe_divide(10, 3))
print("  ->", safe_divide(10, 0))

print("\n=== 3. Return a default vs raise ===")
users = {"asha": "Pune", "ravi": "Delhi"}


def find_city(name):
    return users.get(name)                         # "not found" is normal -> None


def get_city(name):
    if name not in users:
        raise KeyError(f"no user called {name!r}")  # caller made a mistake -> raise
    return users[name]


print("  find_city('zara') ->", find_city("zara"))
try:
    get_city("zara")
except KeyError as e:
    print("  get_city('zara') -> KeyError:", e)


def safe_int(text, default=0):
    try:
        return int(text)
    except (TypeError, ValueError):
        return default


print("  safe_int:", [safe_int(x) for x in ["42", "abc", None, "7"]])

print("\n=== 4. Custom exceptions ===")


class InvalidMarks(ValueError):
    """Raised when marks are outside 0-100."""


def grade(marks):
    if not 0 <= marks <= 100:
        raise InvalidMarks(f"marks must be 0-100, got {marks}")
    return "A" if marks >= 85 else "B" if marks >= 70 else "C" if marks >= 40 else "F"


for m in [92, 55, 130]:
    try:
        print(f"  grade({m}) =", grade(m))
    except InvalidMarks as e:
        print(f"  grade({m}) -> InvalidMarks: {e} (is a ValueError too: {isinstance(e, ValueError)})")

print("\n=== 5. Collect errors instead of stopping ===")


def parse_age(text):
    try:
        age = int(text)
    except ValueError as e:
        raise ValueError(f"age must be a whole number, got {text!r}") from e
    if not 0 <= age <= 130:
        raise ValueError(f"age out of range: {age}")
    return age


ok, errors = [], []
for row, text in enumerate(["25", "abc", "-3", "61", "200"], start=1):
    try:
        ok.append(parse_age(text))
    except ValueError as e:
        errors.append(f"row {row}: {e}")
print("  valid ages:", ok)
for err in errors:
    print("  ", err)
try:
    parse_age("x")
except ValueError as e:
    print("  original cause kept via 'from':", repr(e.__cause__))

print("\n=== 6. EAFP vs LBYL ===")
stock = {"pen": 10}


def take_lbyl(item):
    if item in stock and stock[item] > 0:           # look before you leap
        stock[item] -= 1
        return True
    return False


def take_eafp(item):
    try:                                             # ask forgiveness
        if stock[item] <= 0:
            return False
        stock[item] -= 1
        return True
    except KeyError:
        return False


print("  LBYL pen/book:", take_lbyl("pen"), take_lbyl("book"), "| EAFP pen/book:", take_eafp("pen"), take_eafp("book"))

print("\n=== 7. assert is for bugs, not user input ===")


def average(items):
    assert len(items) > 0, "average() needs at least one item"
    return sum(items) / len(items)


try:
    average([])
except AssertionError as e:
    print("  AssertionError:", e, "(disabled by python -O, so don't validate input this way)")
