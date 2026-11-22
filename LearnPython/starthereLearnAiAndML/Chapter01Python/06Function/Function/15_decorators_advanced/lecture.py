"""Lecture 15: Decorators with arguments, stacking, real-world decorators, lru_cache, classes."""
import functools
import time
import warnings

print("=== 1. Decorator with arguments: @repeat(n) ===")


def repeat(times):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = None
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator


@repeat(3)
def hello(name):
    print("  hi", name)


hello("Asha")
print("  hello.__name__ is still", repr(hello.__name__))

print("\n=== 2. Stacking: applied bottom-up, run outside-in ===")


def bold(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return f"<b>{func(*args, **kwargs)}</b>"
    return wrapper


def italic(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return f"<i>{func(*args, **kwargs)}</i>"
    return wrapper


@bold
@italic
def text_a():
    return "hi"


@italic
@bold
def text_b():
    return "hi"


print("  @bold @italic ->", text_a())
print("  @italic @bold ->", text_b())

print("\n=== 3. Real-world decorators ===")


def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            print(f"  [timer] {func.__name__}: {(time.perf_counter() - start) * 1000:.2f} ms")
    return wrapper


def retry(times=3, delay=0.0, exceptions=(Exception,)):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    print(f"  [retry] attempt {attempt} failed: {e}")
                    if attempt == times:
                        raise
                    time.sleep(delay)
        return wrapper
    return decorator


def validate_positive(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        for value in list(args) + list(kwargs.values()):
            if isinstance(value, (int, float)) and value <= 0:
                raise ValueError(f"{func.__name__}: arguments must be positive, got {value}")
        return func(*args, **kwargs)
    return wrapper


CURRENT_USER = {"name": "ravi", "role": "viewer"}


def require_role(role):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if CURRENT_USER["role"] != role:
                raise PermissionError(f"{CURRENT_USER['name']} needs role {role!r} for {func.__name__}")
            return func(*args, **kwargs)
        return wrapper
    return decorator


def deprecated(advice):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            warnings.warn(f"{func.__name__} is deprecated: {advice}", DeprecationWarning, stacklevel=2)
            return func(*args, **kwargs)
        return wrapper
    return decorator


calls = {"n": 0}


@retry(times=3)
def flaky_api():
    calls["n"] += 1
    if calls["n"] < 3:
        raise ConnectionError("server busy")
    return "data received"


@timer
@validate_positive
def area(w, h):
    return w * h


@require_role("admin")
def delete_all():
    return "everything deleted"


@deprecated("use new_total() instead")
def old_total(items):
    return sum(items)


print("  flaky_api ->", flaky_api())
print("  area(3, 4) ->", area(3, 4))
try:
    area(3, -4)
except ValueError as e:
    print("  area(3, -4) ->", e)
try:
    delete_all()
except PermissionError as e:
    print("  delete_all() as viewer ->", e)
CURRENT_USER["role"] = "admin"
print("  delete_all() as admin ->", delete_all())
with warnings.catch_warnings(record=True) as caught:
    warnings.simplefilter("always")
    print("  old_total ->", old_total([1, 2, 3]), "| warning:", caught[0].message)

print("\n=== 4. Memoisation: hand-made vs lru_cache ===")


def memoize(func):
    cache = {}

    @functools.wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    wrapper.cache = cache
    return wrapper


def fib_plain(n):
    return n if n < 2 else fib_plain(n - 1) + fib_plain(n - 2)


@memoize
def fib_memo(n):
    return n if n < 2 else fib_memo(n - 1) + fib_memo(n - 2)


@functools.lru_cache(maxsize=None)
def fib_lru(n):
    return n if n < 2 else fib_lru(n - 1) + fib_lru(n - 2)


for label, f in [("no cache", fib_plain), ("@memoize", fib_memo), ("@lru_cache", fib_lru)]:
    t = time.perf_counter()
    value = f(27)
    print(f"  fib(27) {label:<11} = {value} in {(time.perf_counter() - t) * 1000:8.2f} ms")
print("  fib_lru(90) =", fib_lru(90), "| cache_info:", fib_lru.cache_info())

print("\n=== 5. A registry decorator: build a command menu ===")
COMMANDS = {}


def register(name):
    def decorator(func):
        COMMANDS[name] = func
        return func                       # no wrapper needed: just record it
    return decorator


@register("greet")
def cmd_greet(user):
    return f"Hello {user}"


@register("bye")
def cmd_bye(user):
    return f"Goodbye {user}"


print("  menu:", list(COMMANDS))
for name in ["greet", "bye"]:
    print(f"  run {name!r}:", COMMANDS[name]("Asha"))

print("\n=== 6. A class-based decorator ===")


class CountCalls:
    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func = func
        self.calls = 0

    def __call__(self, *args, **kwargs):
        self.calls += 1
        return self.func(*args, **kwargs)


@CountCalls
def square(x):
    """Square a number."""
    return x * x


print("  ", [square(i) for i in range(4)], "| calls:", square.calls, "| name:", square.__name__)
