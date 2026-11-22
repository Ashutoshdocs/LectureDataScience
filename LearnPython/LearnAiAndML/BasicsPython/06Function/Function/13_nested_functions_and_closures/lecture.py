"""Lecture 13: Nested functions, function factories, closures, nonlocal state."""

print("=== 1. A nested helper ===")


def process(numbers):
    def clean(n):
        return max(0, n)
    return [clean(n) for n in numbers]


print("  process([-3, 5, -1, 8]) =", process([-3, 5, -1, 8]))
try:
    clean(5)                                      # noqa: F821
except NameError as e:
    print("  clean() from outside ->", e)

print("\n=== 2. Function factories ===")


def make_multiplier(factor):
    def multiply(x):
        return x * factor
    return multiply


double = make_multiplier(2)
triple = make_multiplier(3)
print("  double(5) =", double(5), "| triple(5) =", triple(5))
print("  double is a", type(double).__name__, "named", double.__name__)

print("\n=== 3. Peeking inside the closure ===")
print("  double remembers:", double.__code__.co_freevars, "=", double.__closure__[0].cell_contents)
print("  triple remembers:", triple.__code__.co_freevars, "=", triple.__closure__[0].cell_contents)

print("\n=== 4. Closures with state: nonlocal ===")


def make_counter():
    count = 0

    def counter():
        nonlocal count
        count += 1
        return count

    return counter


c1 = make_counter()
c2 = make_counter()
print("  c1:", c1(), c1(), c1(), "| c2:", c2(), "(independent)")


def make_accumulator():
    total = 0

    def add(x):
        nonlocal total
        total += x
        return total

    return add


acc = make_accumulator()
print("  running totals:", [acc(x) for x in [10, 5, 20]])

print("\n=== 5. Practical factories ===")


def make_power(n):
    return lambda x: x ** n


def make_greeting(greeting):
    def greet(name):
        return f"{greeting}, {name}!"
    return greet


def make_password_checker(min_length=8, require_digit=True):
    def check(password):
        if len(password) < min_length:
            return f"too short (min {min_length})"
        if require_digit and not any(ch.isdigit() for ch in password):
            return "needs a digit"
        return "ok"
    return check


square, cube = make_power(2), make_power(3)
print("  square(4), cube(2):", square(4), cube(2))
hello, namaste = make_greeting("Hello"), make_greeting("Namaste")
print(" ", hello("Asha"), "|", namaste("Ravi"))
strict = make_password_checker(10, True)
relaxed = make_password_checker(4, False)
for pw in ["abc", "abcdefghijk", "abcdefghij9"]:
    print(f"  {pw!r:<15} strict: {strict(pw):<20} relaxed: {relaxed(pw)}")

print("\n=== 6. Closures as callbacks that carry data ===")
handlers = {action: make_greeting(f"Clicked {action}") for action in ["save", "open"]}
print(" ", handlers["save"]("user"), "|", handlers["open"]("user"))

print("\n=== 7. Same idea as a class (for comparison) ===")


class Counter:
    def __init__(self):
        self.count = 0

    def __call__(self):
        self.count += 1
        return self.count


k = Counter()
print("  class-based counter:", k(), k(), "| state visible as k.count =", k.count)
