"""Lecture 10: Functions are objects: assign, store, pass, return; dispatch tables; callbacks."""

print("=== 1. A function is a value ===")


def shout(text):
    """Make text loud."""
    return text.upper() + "!"


yell = shout
print("  yell('hi') =", yell("hi"), "| shout is yell:", shout is yell)
print("  name:", yell.__name__, "| doc:", yell.__doc__, "| type:", type(yell).__name__)
shout.calls = 0                                   # functions can even carry attributes
shout.calls += 1
print("  custom attribute:", shout.calls)

print("\n=== 2. Store functions in a list / dict ===")
for f in [len, str.upper, sorted, shout]:
    print(f"  {f.__name__:<6}('banana') -> {f('banana')!r}")

print("\n=== 3. Pass functions as arguments (higher-order functions) ===")


def apply_to_all(func, items):
    return [func(x) for x in items]


print("  apply_to_all(str.upper, ...):", apply_to_all(str.upper, ["a", "b"]))
print("  apply_to_all(len, ...)      :", apply_to_all(len, ["hi", "hello"]))
print("  apply_to_all(shout, ...)    :", apply_to_all(shout, ["go", "win"]))


def get_marks(pair):
    return pair[1]


students = [("Asha", 88), ("Ravi", 74), ("Dev", 91)]
print("  sorted by marks:", sorted(students, key=get_marks))
print("  top student    :", max(students, key=get_marks))
try:
    sorted(students, key=get_marks(students[0]))   # called it instead of passing it
except TypeError as e:
    print("  key=get_marks(...) (called by mistake) ->", e)

print("\n=== 4. Dispatch table instead of if/elif ===")


def add(a, b):
    return a + b


def sub(a, b):
    return a - b


def div(a, b):
    if b == 0:
        raise ZeroDivisionError("cannot divide by zero")
    return a / b


OPERATIONS = {"+": add, "-": sub, "*": lambda a, b: a * b, "/": div, "**": pow}


def calculate(a, op, b):
    func = OPERATIONS.get(op)
    if func is None:
        raise ValueError(f"unknown operator {op!r}")
    return func(a, b)


for expr in [(6, "+", 3), (6, "-", 3), (6, "*", 3), (6, "/", 3), (2, "**", 10), (6, "/", 0), (6, "%", 3)]:
    try:
        print(f"  {expr[0]} {expr[1]} {expr[2]} = {calculate(*expr)}")
    except (ZeroDivisionError, ValueError) as e:
        print(f"  {expr[0]} {expr[1]} {expr[2]} -> {type(e).__name__}: {e}")
print("  supported operators:", list(OPERATIONS))

print("\n=== 5. Callbacks ===")


def download(url, on_done, on_error=None):
    if url.startswith("bad"):
        if on_error:
            on_error(f"could not reach {url}")
        return
    on_done(f"<contents of {url}>")


download("site.com", on_done=lambda data: print("  got:", data))
download("bad.site", on_done=print, on_error=lambda msg: print("  error callback:", msg))

print("\n=== 6. retry: a higher-order helper ===")
attempts = {"n": 0}


def flaky():
    attempts["n"] += 1
    return attempts["n"] >= 3                       # succeeds on the 3rd try


def retry(func, times):
    for i in range(1, times + 1):
        if func():
            return i
    return None


print("  flaky() succeeded on attempt:", retry(flaky, 5))
