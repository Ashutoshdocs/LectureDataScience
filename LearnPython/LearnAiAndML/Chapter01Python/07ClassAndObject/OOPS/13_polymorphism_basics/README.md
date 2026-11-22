# Lecture 13: Polymorphism: one interface, many forms

Run: `python lecture.py`

## The idea

**Polymorphism** (Greek: "many forms") means **the same call does the right thing for each type of object**.

You already use it:

```python
len("hello")      # 5   string length
len([1, 2, 3])    # 3   list length
len({"a": 1})     # 1   dict size
1 + 2             # 3   number addition
"a" + "b"         # 'ab' string joining
```

One name (`len`, `+`) has many behaviours, depending on the object.

## Polymorphism with your own classes

```python
class Circle:
    def __init__(self, r): self.r = r
    def area(self): return 3.14159 * self.r ** 2

class Square:
    def __init__(self, s): self.s = s
    def area(self): return self.s ** 2

for shape in [Circle(1), Square(3)]:
    print(shape.area())        # each object answers in its own way
```

The loop doesn't know or care which class `shape` is. It only relies on the shared method name: the **interface**.

## Why it matters: getting rid of type checks

### ❌ Without polymorphism

```python
def area(shape):
    if shape["type"] == "circle":
        return 3.14 * shape["r"] ** 2
    elif shape["type"] == "square":
        return shape["s"] ** 2
    elif shape["type"] == "triangle":      # edit this function for EVERY new shape
        ...
```

### ✅ With polymorphism

Each class knows its own area. **Adding a `Triangle` class requires no change** to any code that uses shapes.

This is the **Open/Closed Principle**: code should be *open for extension* (add new classes) but *closed for modification* (don't edit working code).

## Two ways to get polymorphism in Python

| Way | How | Lecture |
|-----|-----|---------|
| **Inheritance + overriding** | children override a parent's method (`Shape.area` → `Circle.area`) | 09–10, 17 |
| **Duck typing** | unrelated classes just have the same method name | 16 |

Inheritance adds a shared parent, which gives you `isinstance` checks, shared code and (with ABCs) enforcement. Duck typing needs nothing but matching names.

## Polymorphic functions

A function written against an interface works with any object that provides it:

```python
def print_report(items):
    for item in items:
        print(item.describe())        # Employee, Manager, Product, ... anything with describe()
```

## Method overloading? Not in Python

Some languages let you define `add(int, int)` and `add(str, str)` separately. In Python a later `def` with the same name **replaces** the earlier one. Instead, use:
- default / optional arguments: `def area(self, unit="cm")`
- `*args` / `**kwargs`
- `functools.singledispatch` / `singledispatchmethod` to choose an implementation by **argument type**

## Exercises

1. Add `Triangle(base, height)` and include it in the shapes list without touching the loop.
2. Write `total_area(shapes)` and `largest(shapes)` that work with any shape.
3. Create `Notifier` classes `Email`, `SMS` and `Push`, each with `send(msg)`. Send one message through all of them.
4. Use `functools.singledispatch` to write `describe(x)` with different output for `int`, `str` and `list`.

**Next →** [Lecture 14: Magic (dunder) methods](../14_magic_methods/)
