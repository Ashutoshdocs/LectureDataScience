"""Lecture 16: Recursion: base case, call stack trace, limits, classic problems, memoisation."""
import functools
import sys

print("=== 1. Factorial, with a trace ===")


def factorial(n, depth=0):
    pad = "    " * depth
    print(f"  {pad}factorial({n}) called")
    if n == 0:
        print(f"  {pad}base case -> 1")
        return 1
    result = n * factorial(n - 1, depth + 1)
    print(f"  {pad}factorial({n}) returns {result}")
    return result


factorial(4)

print("\n=== 2. No base case -> RecursionError ===")


def forever(n):
    return forever(n + 1)


print("  recursion limit:", sys.getrecursionlimit())
try:
    forever(0)
except RecursionError as e:
    print("  RecursionError:", e)

print("\n=== 3. Classic recursive functions ===")


def sum_list(items):
    return 0 if not items else items[0] + sum_list(items[1:])


def power(base, exp):
    return 1 if exp == 0 else base * power(base, exp - 1)


def reverse(s):
    return s if len(s) <= 1 else reverse(s[1:]) + s[0]


def sum_digits(n):
    return n if n < 10 else n % 10 + sum_digits(n // 10)


def is_palindrome(s):
    return len(s) <= 1 or (s[0] == s[-1] and is_palindrome(s[1:-1]))


def count_down(n):
    if n == 0:
        print("liftoff!")
        return
    print(n, end=" ")
    count_down(n - 1)


print("  sum_list([3, 4, 5]) =", sum_list([3, 4, 5]))
print("  power(2, 10) =", power(2, 10))
print("  reverse('python') =", reverse("python"))
print("  sum_digits(1234) =", sum_digits(1234))
print("  is_palindrome:", {w: is_palindrome(w) for w in ["level", "radar", "python"]})
print("  count_down(5): ", end="")
count_down(5)

print("\n=== 4. Where recursion shines: nested data ===")


def flatten(item):
    if not isinstance(item, list):
        return [item]
    result = []
    for sub in item:
        result.extend(flatten(sub))
    return result


print("  flatten([1, [2, [3, 4]], 5]) =", flatten([1, [2, [3, 4]], 5]))

folder = {"name": "root", "size": 0, "children": [
    {"name": "docs", "size": 0, "children": [
        {"name": "cv.pdf", "size": 120, "children": []},
        {"name": "notes.txt", "size": 5, "children": []}]},
    {"name": "photo.jpg", "size": 900, "children": []}]}


def total_size(node):
    return node["size"] + sum(total_size(child) for child in node["children"])


def show_tree(node, depth=0):
    print("  " + "  " * depth + f"{node['name']} ({total_size(node)} KB)")
    for child in node["children"]:
        show_tree(child, depth + 1)


show_tree(folder)


def binary_search(items, target, lo=0, hi=None):
    if hi is None:
        hi = len(items) - 1
    if lo > hi:
        return -1
    mid = (lo + hi) // 2
    if items[mid] == target:
        return mid
    if items[mid] < target:
        return binary_search(items, target, mid + 1, hi)
    return binary_search(items, target, lo, mid - 1)


nums = list(range(0, 100, 3))
print("  binary_search for 42:", binary_search(nums, 42), "| for 43:", binary_search(nums, 43))

print("\n=== 5. Recursion vs loop ===")


def factorial_loop(n):
    result = 1
    for k in range(2, n + 1):
        result *= k
    return result


def factorial_quiet(n):
    return 1 if n == 0 else n * factorial_quiet(n - 1)


print("  factorial_loop(10) =", factorial_loop(10), "| recursive =", factorial_quiet(10),
      "| same:", factorial_loop(10) == factorial_quiet(10))
try:
    sum_list(list(range(5000)))
except RecursionError:
    print("  sum_list on 5000 items -> RecursionError (too deep); the loop/sum() handles it:", sum(range(5000)))

print("\n=== 6. Memoisation makes naive recursion fast ===")
calls = {"plain": 0, "cached": 0}


def fib(n):
    calls["plain"] += 1
    return n if n < 2 else fib(n - 1) + fib(n - 2)


@functools.lru_cache(maxsize=None)
def fib_cached(n):
    calls["cached"] += 1
    return n if n < 2 else fib_cached(n - 1) + fib_cached(n - 2)


print("  fib(20) =", fib(20), "with", f"{calls['plain']:,}", "calls")
print("  fib_cached(20) =", fib_cached(20), "with", calls["cached"], "calls")
