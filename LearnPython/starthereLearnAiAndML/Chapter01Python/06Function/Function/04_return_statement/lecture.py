"""Lecture 04: return: values, print vs return, None, early return, multiple values."""

print("=== 1. return hands a value back ===")


def square(n):
    return n * n


result = square(4)
print("  square(4) =", result, "| square(3) + square(4) =", square(3) + square(4))

print("\n=== 2. return vs print ===")


def add_print(a, b):
    print("  (add_print prints)", a + b)


def add_return(a, b):
    return a + b


x = add_print(2, 3)
y = add_return(2, 3)
print("  x =", x, "| y =", y, "| y * 10 =", y * 10)
try:
    x * 10
except TypeError as e:
    print("  x * 10 ->", e)

print("\n=== 3. No return -> None ===")


def nothing():
    pass


def bare():
    return


print("  nothing():", nothing(), "| bare():", bare())

print("\n=== 4. return ends the function: early returns ===")


def grade(marks):
    if marks < 0 or marks > 100:
        return "invalid"
    if marks >= 85:
        return "A"
    if marks >= 70:
        return "B"
    return "C"
    print("never runs")                          # unreachable


print("  grades:", {m: grade(m) for m in [95, 72, 40, 150]})


def first_negative(numbers):
    for n in numbers:
        if n < 0:
            return n                             # stops the loop AND the function
    return None


print("  first_negative([3, 5, -2, -9]) =", first_negative([3, 5, -2, -9]))
print("  first_negative([1, 2]) =", first_negative([1, 2]))

print("\n=== 5. Returning several values ===")


def min_max(numbers):
    return min(numbers), max(numbers)


low, high = min_max([4, 9, 1])
pair = min_max([4, 9, 1])
print("  unpacked:", low, high, "| as a tuple:", pair, type(pair).__name__)


def stats(numbers):
    total = sum(numbers)
    return {"count": len(numbers), "total": total, "mean": round(total / len(numbers), 2)}


s = stats([10, 20, 35])
print("  dict result:", s, "| use names:", s["mean"])

print("\n=== 6. Booleans and 'not found' ===")


def is_even(n):
    return n % 2 == 0


def find(names, target):
    for i, name in enumerate(names):
        if name == target:
            return i
    return None


print("  evens:", [n for n in range(10) if is_even(n)])
for target in ["Ravi", "Zara"]:
    idx = find(["Asha", "Ravi"], target)
    print(f"  find {target!r}:", "not found" if idx is None else f"index {idx}")
