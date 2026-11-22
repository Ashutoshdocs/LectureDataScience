# Lecture 00: Prerequisites, what you need before classes

Run: `python lecture.py`

A class is a bundle of **data** plus **functions**. So before classes you need to be comfortable with functions and with how Python finds variables (scope).

## Checklist

| Skill | You should be able to… | Why classes need it |
|-------|------------------------|---------------------|
| Variables & types | use `int`, `float`, `str`, `bool`, `list`, `dict` | Objects store these as attributes |
| **Defining functions** | `def area(w, h): return w * h` | Every method is a function |
| **Parameters & arguments** | positional, keyword, defaults `def f(x, y=2)` | Constructors and methods use all of them |
| **`return` vs `print`** | know that `return` hands a value back | Methods should usually return results |
| **Scope (LEGB)** | know local vs global, and the `global` keyword | Lecture 14 builds on it |
| Dictionaries | `d["key"]`, `d.get("key", default)` | Every object stores its attributes in a dict |
| Lists & loops | loop over a list, use comprehensions | Programs hold many objects in lists |
| `try / except` | catch an error and print it | Used to show errors safely in the lectures |
| f-strings | `f"{name} scored {marks}"` | Printing objects nicely |

## 1. Functions in one minute

```python
def greet(name, greeting="Hello"):     # name: required, greeting: has a default
    message = f"{greeting}, {name}!"   # message is a LOCAL variable
    return message                     # hand the result back

text = greet("Asha")                   # positional argument
text2 = greet(greeting="Hi", name="Ravi")   # keyword arguments, any order
```

- **Parameters** are the names in the `def` line; **arguments** are the values you pass.
- A function without `return` returns `None`.
- Functions are **values**: you can store them in variables and pass them around.

## 2. Scope: where Python looks for a name (LEGB)

When you use a plain name like `x`, Python searches in this order:

```
 L  Local      inside the current function
 E  Enclosing  inside any outer function (nested functions)
 G  Global     at the top level of the file
 B  Built-in   print, len, sum, ...
```

```python
count = 0                 # global

def bump():
    global count          # needed to ASSIGN to a global
    count += 1

def show():
    print(count)          # READING a global needs no keyword
```

Without `global`, assigning inside a function creates a **new local** variable. Reading it first gives `UnboundLocalError`.

## 3. Dictionaries: the hidden storage of objects

```python
student = {"name": "Asha", "marks": 88}
student["marks"] += 5
student.get("age", "unknown")
```

You'll see in Lecture 03 that every object keeps its attributes in a dictionary called `__dict__`.

## 4. Functions as values

```python
def double(x): return x * 2
f = double            # no brackets: the function itself
f(5)                  # 10
```

This matters in Lecture 06: `obj.method` without brackets is a **bound method**, a function value that remembers its object.

## Exercises

1. Write `def bmi(weight, height=1.7)` that returns weight / height².
2. Write a counter function that uses `global` correctly, then remove `global` and read the error.
3. Store `len` in a variable `size` and call `size("hello")`.

<details><summary>Solutions</summary>

```python
def bmi(weight, height=1.7):
    return weight / height ** 2

size = len
size("hello")      # 5
```
Removing `global` gives `UnboundLocalError: cannot access local variable 'count' ...`.
</details>

**Next →** [Lecture 01: Why classes?](../01_why_classes/)
