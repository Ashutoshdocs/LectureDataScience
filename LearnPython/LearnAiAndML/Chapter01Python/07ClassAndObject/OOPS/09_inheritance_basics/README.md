# Lecture 09: Inheritance basics

Run: `python lecture.py`

## Why inheritance?

Suppose you have `Dog`, `Cat` and `Cow` classes. Each has `name`, `age`, `eat()` and `sleep()`, and only the sound differs. Copying the same code into three classes means three places to fix every bug.

**Inheritance** lets a new class (the **child**) **reuse everything** from an existing class (the **parent**) and then **add** or **change** only what's different.

```python
class Animal:                       # parent / base / superclass
    def __init__(self, name):
        self.name = name

    def eat(self):
        print(self.name, "is eating")

class Dog(Animal):                  # child / derived / subclass
    def bark(self):                 # extra ability
        print(self.name, "says Woof!")

d = Dog("Bruno")    # uses Animal.__init__
d.eat()             # inherited
d.bark()            # Dog's own
```

## The "is-a" test

Use inheritance only when **"Child is a Parent"** is true:

| Relationship | "is-a"? | Inheritance? |
|--------------|---------|--------------|
| Dog → Animal | a Dog **is an** Animal ✅ | yes |
| SavingsAccount → BankAccount | ✅ | yes |
| Manager → Employee | ✅ | yes |
| Car → Engine | a Car **has an** Engine ❌ | no → **composition** (Lecture 18) |
| Stack → list | a stack is *not* every kind of list ❌ | usually no |

## How Python finds a method

```
d.eat()  →  look in Dog     → not found
         →  look in Animal  → found → run Animal.eat with self = d
         →  (else look in object, the root of every class)
         →  (else AttributeError)
```

The child **overrides** a method simply by defining one with the same name (Lecture 10).

## Useful tools

| Tool | Meaning |
|------|---------|
| `isinstance(d, Dog)` / `isinstance(d, Animal)` | both `True`: a Dog is also an Animal |
| `issubclass(Dog, Animal)` | `True` |
| `Dog.__bases__` | the direct parents: `(Animal,)` |
| `Dog.__mro__` | the full lookup order: `Dog → Animal → object` |
| `type(d) is Animal` | `False`: `type()` ignores inheritance, so prefer `isinstance` |

## Every class inherits from `object`

`class Animal:` is the same as `class Animal(object):`. `object` provides defaults such as `__init__`, `__str__`, `__eq__` (identity) and `__dict__`. That's why even an empty class can be printed and compared.

## Inheritance is one-directional

The child gets the parent's abilities, **not the other way round**: `Animal("x").bark()` raises `AttributeError`.

## What to put in the parent

Put things that are **common to every child** in the parent. Put anything specific in the child. If you find yourself writing `if isinstance(self, Dog)` in the parent, that code belongs in `Dog`.

## Exercises

1. Add `Cat(Animal)` with `meow()` and `Cow(Animal)` with `moo()`. Loop over all three and call `eat()`.
2. Add `sleep()` to `Animal` once, and show every child can use it.
3. Print `Cat.__mro__`.
4. Write `Vehicle` → `Car` and `Bike` sharing `brand`, `start()`, `stop()`.

**Next →** [Lecture 10: Overriding & `super()`](../10_overriding_and_super/)
