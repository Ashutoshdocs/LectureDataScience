# Lecture 06: `*args`: any number of positional arguments

Run: `python lecture.py`

## The problem

```python
def add(a, b): return a + b
add(1, 2, 3)       # TypeError: add() takes 2 positional arguments but 3 were given
```

You could accept a list (`add([1, 2, 3])`), but built-ins like `print(1, 2, 3)` and `max(4, 9, 2)` take **any number** of separate arguments. How?

## `*args` collects extra positional arguments into a tuple

```python
def add(*args):
    print(args, type(args))     # (1, 2, 3) <class 'tuple'>
    return sum(args)

add()            # 0       args = ()
add(5)           # 5       args = (5,)
add(1, 2, 3)     # 6       args = (1, 2, 3)
```

- The `*` is what matters; `args` is just a conventional name (`*numbers`, `*names` are clearer when they fit).
- Inside, `args` is a normal **tuple**: loop over it, `len()` it, index it.

## Mixing with normal parameters

Normal (required) parameters come **first** and take the first arguments; `*args` gets the rest:

```python
def report(title, *scores):
    print(title, "→", scores)

report("Maths", 78, 92, 45)     # title="Maths", scores=(78, 92, 45)
```

Parameters **after** `*args` can only be passed **by keyword** (keyword-only):

```python
def join(*words, sep=" "):
    return sep.join(words)

join("a", "b", "c", sep="-")    # 'a-b-c'
```

## Unpacking at call time: `*` on the other side

`*` in a **call** does the opposite: it spreads a list/tuple into separate positional arguments:

```python
nums = [4, 9, 2]
max(*nums)            # same as max(4, 9, 2)
add(*nums, 10)        # add(4, 9, 2, 10)

point = (3, 4)
distance(*point)      # distance(3, 4)
```

| Where | `*` means |
|-------|-----------|
| in a **definition** `def f(*args)` | **pack** many arguments → one tuple |
| in a **call** `f(*items)` | **unpack** one iterable → many arguments |

## When to use `*args` (and when not)

| ✅ Use when | ❌ Avoid when |
|------------|--------------|
| the number of similar inputs truly varies (`add(1, 2, 3)`, `log("a", "b")`) | the arguments have **different meanings**. Use named parameters |
| writing **wrappers/decorators** that pass arguments through unchanged (Lecture 14) | the caller naturally already has a list. Just accept a list parameter |
| mimicking built-ins (`print`, `max`) | it would hide what the function needs |

## Exercises

1. Write `average(*nums)` that returns 0 when called with no arguments.
2. Write `longest(*words)` returning the longest word.
3. Write `tag(name, *classes)` that returns `"<name class='a b c'>"`.
4. Call `average` with a list using `*`.

<details><summary>Solutions</summary>

```python
def average(*nums):
    return sum(nums) / len(nums) if nums else 0

def longest(*words):
    return max(words, key=len)

def tag(name, *classes):
    return f"<{name} class='{' '.join(classes)}'>"

average(*[1, 2, 3])
```
</details>

**Next →** [Lecture 07: `**kwargs`](../07_kwargs/)
