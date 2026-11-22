# Lecture 10: Functions as objects (first-class functions)

Run: `python lecture.py`

In Python, functions are **objects**, values just like numbers and strings. ("First-class functions.") That means you can:

| You can… | Example |
|----------|---------|
| assign a function to a variable | `say = print` |
| store functions in lists / dicts | `ops = {"+": add, "-": sub}` |
| pass a function as an argument | `sorted(words, key=len)` |
| return a function from a function | `make_multiplier(3)` (Lecture 13) |
| give it attributes / inspect it | `f.__name__`, `f.__doc__` |

```python
def shout(text):
    return text.upper() + "!"

yell = shout          # NO brackets: refer to the function itself
yell("hi")            # 'HI!': same function, another name
shout is yell         # True
```

> `shout` = the function object. `shout()` = **calling** it and getting its result.

## Higher-order functions

A **higher-order function** takes a function as an argument or returns one.

```python
def apply_to_all(func, items):
    return [func(x) for x in items]

apply_to_all(str.upper, ["a", "b"])        # ['A', 'B']
apply_to_all(len, ["hi", "hello"])         # [2, 5]
```

**Why?** The *what to do* (the passed-in function) is separated from the *how to repeat it* (the loop). One loop serves many jobs.

### Built-in higher-order functions you already use

| Function | The function argument decides… |
|----------|--------------------------------|
| `sorted(items, key=f)` | what to sort by |
| `max(items, key=f)` / `min(...)` | what to compare |
| `map(f, items)` | how to transform each item |
| `filter(f, items)` | which items to keep |

```python
students = [("Asha", 88), ("Ravi", 74), ("Dev", 91)]
sorted(students, key=get_marks)          # pass the function, don't call it!
```

## Dispatch tables: replacing long `if/elif` chains

```python
def add(a, b): return a + b
def sub(a, b): return a - b

OPERATIONS = {"+": add, "-": sub, "*": lambda a, b: a * b}

def calculate(a, op, b):
    func = OPERATIONS.get(op)
    if func is None:
        raise ValueError(f"unknown operator {op!r}")
    return func(a, b)
```

| `if/elif` chain | Dispatch dict |
|-----------------|---------------|
| grows with every new case | add one dict entry |
| logic and mapping mixed together | the mapping is **data**; you can list it, test it, extend it |

## Callbacks

A **callback** is a function you hand to other code to be called **later**, when something happens:

```python
def download(url, on_done):
    data = f"<contents of {url}>"
    on_done(data)                # call back the caller's function

download("site.com", on_done=print)
```

GUIs (button clicks), web frameworks and event systems all work this way.

## Exercises

1. Store `len`, `str.upper` and `sorted` in a list and apply each to `"banana"`.
2. Sort `[("Asha", 88), ("Ravi", 74)]` by marks with a named `key` function.
3. Add `/` and `**` to the dispatch table, with division-by-zero handling.
4. Write `retry(func, times)` that calls `func` up to `times` times until it returns truthy.

<details><summary>Solutions</summary>

```python
for f in [len, str.upper, sorted]:
    print(f("banana"))

def by_marks(pair): return pair[1]
sorted(data, key=by_marks)
```
</details>

**Next →** [Lecture 11: Lambda](../11_lambda/)
