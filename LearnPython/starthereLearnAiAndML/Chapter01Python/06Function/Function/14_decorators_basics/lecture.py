"""Lecture 14: Decorators: the wrapper pattern, @ syntax, functools.wraps, common mistakes."""
import functools
import time

print("=== 1. Step by step, without @ ===")


def log_calls(func):
    def wrapper(*args, **kwargs):
        print(f"  -> calling {func.__name__} with args={args} kwargs={kwargs}")
        result = func(*args, **kwargs)
        print(f"  <- {func.__name__} returned {result!r}")
        return result
    return wrapper


def add(a, b):
    return a + b


print("  before decorating:", add(2, 3))
add = log_calls(add)                       # wrap it
print("  after decorating :", add(2, 3))

print("\n=== 2. The @ syntax does the same thing ===")


@log_calls
def greet(name, punctuation="!"):
    return f"Hello, {name}{punctuation}"


greet("Asha")
greet("Ravi", punctuation="?")

print("\n=== 3. Decoration happens once, at definition time ===")


def announce(func):
    print(f"  [decorating {func.__name__} NOW]")
    return func


@announce
def later():
    return "called"


print("  ...later() is only called now:", later())

print("\n=== 4. Why functools.wraps matters ===")


def no_wraps(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


def with_wraps(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


@no_wraps
def area(w, h):
    """Return the area of a rectangle."""
    return w * h


@with_wraps
def volume(w, h, d):
    """Return the volume of a box."""
    return w * h * d


print(f"  no wraps  : __name__={area.__name__!r:<10} __doc__={area.__doc__!r}")
print(f"  with wraps: __name__={volume.__name__!r:<10} __doc__={volume.__doc__!r}")
print("  original still reachable:", volume.__wrapped__.__name__, volume.__wrapped__(1, 2, 3))

print("\n=== 5. Useful beginner decorators ===")


def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        print(f"  [timer] {func.__name__} took {(time.perf_counter() - start) * 1000:.1f} ms")
        return result
    return wrapper


def count_calls(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.calls += 1
        return func(*args, **kwargs)
    wrapper.calls = 0
    return wrapper


def shout(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs).upper()
    return wrapper


@timer
def slow_sum(n):
    return sum(range(n))


@count_calls
def ping():
    return "pong"


@shout
def welcome(name):
    return f"welcome, {name}"


print("  slow_sum:", slow_sum(2_000_000))
for _ in range(3):
    ping()
print("  ping was called", ping.calls, "times")
print(" ", welcome("asha"))

print("\n=== 6. Common mistakes ===")


def forgot_result(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)                  # result thrown away!
    return wrapper


def forgot_return_wrapper(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    # no 'return wrapper'


def no_args_wrapper(func):
    def wrapper():                             # can't accept arguments
        return func()
    return wrapper


@forgot_result
def five():
    return 5


print("  forgot 'return result' -> five() =", five())

@forgot_return_wrapper
def six():
    return 6


try:
    six()
except TypeError as e:
    print("  forgot 'return wrapper' ->", e)


@no_args_wrapper
def double(x):
    return 2 * x


try:
    double(4)
except TypeError as e:
    print("  wrapper without *args/**kwargs ->", e)
