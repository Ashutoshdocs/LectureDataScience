"""Lecture 03: Parameters & arguments: positional, keyword, defaults, mutable traps."""

print("=== 1. Positional arguments ===")


def describe(name, age, city):
    print(f"  {name} is {age} and lives in {city}")


describe("Asha", 25, "Pune")
describe(25, "Asha", "Pune")              # runs, but the values are in the wrong places

print("\n=== 2. Keyword arguments ===")
describe(city="Pune", name="Asha", age=25)
describe("Ravi", city="Delhi", age=31)

for bad_call in [
    lambda: describe("Asha", 25),
    lambda: describe("Asha", 25, "Pune", "India"),
    lambda: describe("Asha", 25, ciyt="Pune"),
    lambda: describe("Asha", name="Ravi", age=1, city="X"),
]:
    try:
        bad_call()
    except TypeError as e:
        print("  TypeError:", e)
try:
    compile('describe(name="A", 25, "Pune")', "<test>", "exec")
except SyntaxError as e:
    print("  SyntaxError:", e.msg)

print("\n=== 3. Default values ===")


def power(base, exponent=2):
    return base ** exponent


print("  power(5) =", power(5), "| power(5, 3) =", power(5, 3), "| power(5, exponent=0) =", power(5, exponent=0))


def make_email(first, last, domain="company.com"):
    return f"{first.lower()}.{last.lower()}@{domain}"


print(" ", make_email("Asha", "Rao"), "|", make_email("Ravi", "Kumar", domain="gmail.com"))
try:
    compile("def f(a=1, b): pass", "<test>", "exec")
except SyntaxError as e:
    print("  def f(a=1, b) ->", e.msg)

print("\n=== 4. The mutable-default trap ===")


def add_item_bad(item, basket=[]):
    basket.append(item)
    return basket


first = list(add_item_bad("pen"))         # snapshot after call 1
second = list(add_item_bad("book"))       # snapshot after call 2
print("  bad : call 1 ->", first, "| call 2 ->", second, "<- the list remembers old calls")
print("  the default lives on the function:", add_item_bad.__defaults__)


def add_item(item, basket=None):
    if basket is None:
        basket = []
    basket.append(item)
    return basket


print("  good:", add_item("pen"), add_item("book"))

print("\n=== 5. Mutable vs immutable arguments ===")


def add_bonus(marks):
    marks.append(5)                       # in-place: caller sees it


def reset(n):
    n = 0                                 # rebinding a local: caller doesn't


def remove_negatives(numbers):
    return [x for x in numbers if x >= 0] # new list: caller's list untouched


my_marks = [80, 90]
add_bonus(my_marks)
print("  list after add_bonus:", my_marks)
score = 99
reset(score)
print("  int after reset     :", score)
data = [3, -1, 4, -5]
print("  remove_negatives    :", remove_negatives(data), "| original:", data)
