# Lecture 13: Nested functions & closures

Run: `python lecture.py`

## Nested (inner) functions

A function can be defined **inside** another function. The inner one exists only while the outer one runs, and can't be called from outside:

```python
def process(numbers):
    def clean(n):                # helper visible only inside process()
        return max(0, n)
    return [clean(n) for n in numbers]
```

**Why?** To hide a small helper that only one function needs. It keeps the module tidy and the helper close to where it's used.

## Returning a function: function factories

The outer function can **build and return** the inner function:

```python
def make_multiplier(factor):
    def multiply(x):
        return x * factor        # uses the outer function's variable
    return multiply              # return the function itself (no brackets)

double = make_multiplier(2)
triple = make_multiplier(3)
double(5)    # 10
triple(5)    # 15
```

`make_multiplier` has **finished running**, yet `double` still knows `factor = 2`. How?

## Closures

A **closure** is an inner function that **remembers variables from the enclosing scope** even after the outer function has returned.

```
 make_multiplier(2) runs:        returns multiply + a "backpack" { factor: 2 }
 make_multiplier(3) runs:        returns multiply + a "backpack" { factor: 3 }
```

Each call creates a **separate** closure with its own remembered values. You can peek inside: `double.__closure__[0].cell_contents` → `2`.

Three conditions make a closure:
1. a nested function,
2. that uses a variable from the enclosing function,
3. and is returned (or otherwise kept alive) beyond the outer call.

## Changing remembered state: `nonlocal`

Reading an enclosing variable is automatic. **Assigning** to it needs `nonlocal` (Lecture 05):

```python
def make_counter():
    count = 0
    def counter():
        nonlocal count
        count += 1
        return count
    return counter

c1 = make_counter(); c1(); c1()   # 1, 2
c2 = make_counter(); c2()         # 1: independent state
```

## Why closures matter

| Use | Example |
|-----|---------|
| **Function factories**: configure once, use many times | `make_multiplier(3)`, `make_validator(min_len=8)`, `make_discount(10)` |
| **Private state** without a class | counters, running totals, caches |
| **Callbacks that carry data** | `button.on_click(make_handler("save"))` |
| **Decorators** (next lecture) | the wrapper is a closure that remembers the original function |

### Closure or class?

| Closure | Class |
|---------|-------|
| one behaviour + a little state | several behaviours / methods |
| very short | more structure, easier to inspect & extend |
| `counter()` | `counter.increment()`, `counter.reset()`, `counter.value` |

## ⚠️ Late binding (again)

Closures look up variables **when called**, not when created. A loop that creates closures shares the loop variable. See Lecture 11 for the `i=i` fix.

## Exercises

1. Write `make_power(n)` returning a function that raises its argument to `n`.
2. Write `make_greeting(greeting)` → `hello = make_greeting("Hello"); hello("Asha")`.
3. Write `make_accumulator()` whose function adds its argument to a running total and returns the total.
4. Write `make_password_checker(min_length, require_digit)` returning a validator function.

<details><summary>Solutions</summary>

```python
def make_power(n):
    def power(x):
        return x ** n
    return power

def make_accumulator():
    total = 0
    def add(x):
        nonlocal total
        total += x
        return total
    return add
```
</details>

**Next →** [Lecture 14: Decorators: basics](../14_decorators_basics/)
