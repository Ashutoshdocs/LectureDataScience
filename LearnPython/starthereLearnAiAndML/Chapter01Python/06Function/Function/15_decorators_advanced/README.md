# Lecture 15: Decorators: advanced & real-world

Run: `python lecture.py`

## 1. Decorators with arguments

`@repeat(3)` needs **one more layer**: a function that takes the arguments and *returns a decorator*:

```python
def repeat(times):                     # 1. takes the decorator's arguments
    def decorator(func):               # 2. the real decorator
        @functools.wraps(func)
        def wrapper(*args, **kwargs):  # 3. the wrapper
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)                             # repeat(3) runs first → returns decorator
def hello(): print("hi")              # then: hello = decorator(hello)
```

```
 @repeat(3)  ≡  hello = repeat(3)(hello)
                       └──┬───┘
                     a decorator
```

| Form | Layers | Example |
|------|--------|---------|
| `@deco` | 2: `deco(func)` → wrapper | `@timer` |
| `@deco(args)` | 3: `deco(args)` → decorator → wrapper | `@repeat(3)`, `@retry(times=5)`, `@require_role("admin")` |

## 2. Stacking decorators

```python
@bold
@italic
def text(): return "hi"
```

is `text = bold(italic(text))`. Decorators are **applied bottom-up** (closest to the function first), but at call time the **outermost runs first**:

```
 call text() → bold's wrapper → italic's wrapper → original → back out: "<b><i>hi</i></b>"
```

Order matters: `@timer` above `@cache` times cache hits too; below it, timing happens only on real calls.

## 3. Real-world decorators (all in `lecture.py`)

| Decorator | What it does | Where you'd use it |
|-----------|--------------|--------------------|
| `@timer` | measure how long a call takes | finding slow code |
| `@log_calls` | record arguments, results, errors | debugging, audit trails |
| `@retry(times, delay)` | call again if an exception occurs | network / API calls |
| `@validate_positive` | check arguments before running | protecting calculations |
| `@require_role("admin")` | stop unauthorised users | web apps, admin actions |
| `@memoize` / `@functools.lru_cache` | remember results of previous calls | expensive pure functions, recursion |
| `@register` | add the function to a registry dict | plugins, command menus, URL routes |
| `@deprecated("use x")` | warn when old functions are called | evolving libraries |

## 4. Built-in & standard-library decorators

| Decorator | From | Purpose |
|-----------|------|---------|
| `@functools.wraps(func)` | functools | keep metadata in your own decorators |
| `@functools.lru_cache(maxsize=…)` / `@functools.cache` | functools | memoisation |
| `@property`, `@x.setter` | built-in | getter/setter methods in classes |
| `@classmethod`, `@staticmethod` | built-in | method types in classes |
| `@dataclasses.dataclass` | dataclasses | decorates a **class**: auto `__init__`, `__repr__`… |
| `@contextlib.contextmanager` | contextlib | turn a generator into a `with` context manager |
| `@app.route("/")` | Flask (3rd party) | register a web route |
| `@pytest.fixture` | pytest (3rd party) | test setup |

## 5. Memoisation with `lru_cache`

```python
@functools.lru_cache(maxsize=None)
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)

fib(80)               # instant; without the cache it would take ages
fib.cache_info()      # hits, misses, size
```

Only cache **pure** functions (same inputs → same output, no side effects), and only with **hashable** arguments (no lists or dicts).

## 6. Class-based decorators

A class with `__call__` can be a decorator. Useful when the decorator needs rich state:

```python
class CountCalls:
    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func, self.calls = func, 0
    def __call__(self, *args, **kwargs):
        self.calls += 1
        return self.func(*args, **kwargs)
```

## 7. When NOT to use decorators

- When the extra logic matters for understanding the function. Hiding it in a decorator surprises readers.
- When only one function needs it.
- When it changes the function's arguments or return type in non-obvious ways.

## Exercises

1. Write `@repeat(n)` and use it on a function that prints.
2. Write `@retry(times=3)` and test it on a function that fails twice, then succeeds.
3. Stack `@bold` and `@italic` both ways and compare the output.
4. Time `fib(30)` with and without `@lru_cache`.
5. Build a command menu using a `@register("name")` decorator and a dict.

<details><summary>Solutions</summary>

All five are implemented in `lecture.py`; compare after trying yourself.
</details>

**Next →** [Lecture 16: Recursion](../16_recursion/)
