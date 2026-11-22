# Lecture 11: Lambda: anonymous one-line functions

Run: `python lecture.py`

## Syntax

```python
lambda parameters: expression
```

A **lambda** is a small function **without a name**, written in one expression. Its value is returned automatically (no `return` keyword).

```python
square = lambda x: x * x          # same as:  def square(x): return x * x
add = lambda a, b: a + b
greet = lambda name="you": f"Hi {name}"
```

## Where lambdas shine: short throw-away functions passed to other functions

```python
students = [("Asha", 88), ("Ravi", 74), ("Dev", 91)]

sorted(students, key=lambda s: s[1])                 # sort by marks
max(students, key=lambda s: s[1])                    # top student
sorted(words, key=lambda w: (len(w), w))             # by length, then alphabetically
list(filter(lambda n: n % 2 == 0, nums))             # keep evens
list(map(lambda c: c * 9 / 5 + 32, celsius))         # convert each
OPS = {"+": lambda a, b: a + b, "-": lambda a, b: a - b}
```

## Limits of lambda

| Lambda can | Lambda cannot |
|-----------|---------------|
| take any parameters (defaults, `*args`, `**kwargs`) | contain statements: no `if:` blocks, loops, `return`, assignments (`=`) |
| contain **one expression** | have a docstring |
| use a conditional **expression**: `lambda m: "pass" if m >= 40 else "fail"` | span several lines of logic |

## lambda vs def

| Use `lambda` when… | Use `def` when… |
|-------------------|-----------------|
| it's tiny (one short expression) | there's more than one step |
| it's used **once**, inline (`key=`, `map`, `filter`) | it's reused or needs a meaningful name |
| the meaning is obvious from context | it needs a docstring, type hints or tests |
| | you'd write `name = lambda ...` → **use `def` instead** (PEP 8) |

```python
# ❌ assigning a lambda to a name: you lose a readable name in tracebacks
square = lambda x: x * x      # traceback shows "<lambda>"
# ✅
def square(x):
    return x * x
```

## ⚠️ The late-binding trap

Lambdas (and all nested functions) look up variables **when they're called**, not when they're created:

```python
funcs = [lambda: i for i in range(3)]
[f() for f in funcs]                    # [2, 2, 2]  ← all see the final i!

funcs = [lambda i=i: i for i in range(3)]
[f() for f in funcs]                    # [0, 1, 2]  ← default argument captures the value now
```

## Alternatives that are often clearer

| Instead of | Consider |
|------------|----------|
| `map(lambda x: x * 2, nums)` | `[x * 2 for x in nums]` |
| `filter(lambda x: x > 0, nums)` | `[x for x in nums if x > 0]` |
| `key=lambda s: s[1]` | `key=operator.itemgetter(1)` |
| `key=lambda p: p.age` | `key=operator.attrgetter("age")` |

## Exercises

1. Sort a list of words by their last letter with a lambda.
2. Write a lambda `is_adult` with a conditional expression returning "adult"/"minor".
3. Sort `[{"name": "Asha", "age": 25}, ...]` by age, then by name.
4. Reproduce the late-binding trap and fix it.

<details><summary>Solutions</summary>

```python
sorted(words, key=lambda w: w[-1])
is_adult = lambda age: "adult" if age >= 18 else "minor"   # (as a def in real code!)
sorted(people, key=lambda p: (p["age"], p["name"]))
```
</details>

**Next →** [Lecture 12: map, filter, reduce & built-ins](../12_map_filter_reduce_builtins/)
