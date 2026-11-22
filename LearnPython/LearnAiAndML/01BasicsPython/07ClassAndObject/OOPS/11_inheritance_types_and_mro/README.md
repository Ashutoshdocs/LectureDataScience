# Lecture 11: Types of inheritance & the MRO

Run: `python lecture.py`

## Five shapes of inheritance

| Type | Shape | Example |
|------|-------|---------|
| **Single** | one parent → one child | `Car(Vehicle)` |
| **Multilevel** | a chain: grandparent → parent → child | `Vehicle → Car → ElectricCar` |
| **Hierarchical** | one parent, many children | `Car(Vehicle)`, `Bike(Vehicle)`, `Truck(Vehicle)` |
| **Multiple** | one child, several parents | `SmartCar(ElectricCar, Camera)` |
| **Hybrid** | a mix, often a diamond | `D(B, C)` where `B(A)` and `C(A)` |

```
 Multilevel        Hierarchical          Multiple            Diamond
   Vehicle           Vehicle          ElectricCar Camera        A
     │              ┌──┼──┐               └───┬───┘           ┌─┴─┐
    Car           Car Bike Truck           SmartCar           B   C
     │                                                        └─┬─┘
 ElectricCar                                                    D
```

## Method Resolution Order (MRO)

When you call `obj.method()`, Python searches classes in a fixed order: the **MRO**. See it with `ClassName.__mro__` or `ClassName.mro()`.

Python builds it with the **C3 linearization** algorithm. You don't need the algorithm, just its rules:

1. A child comes **before** its parents.
2. Parents keep the **left-to-right order** you wrote: `class D(B, C)` → B before C.
3. Every class appears **exactly once**, even in a diamond, and `object` comes last.

```python
class A: ...
class B(A): ...
class C(A): ...
class D(B, C): ...
D.__mro__  # D → B → C → A → object
```

## The diamond problem, and how `super()` solves it

In the diamond, `B` and `C` both inherit from `A`. If each calls its parent **by name** (`A.__init__(self)`), then `A.__init__` runs **twice**.

With `super()`, each class calls the **next class in the MRO**, not necessarily its own parent:

```
D.__init__ → super() → B.__init__ → super() → C.__init__ → super() → A.__init__
```

Each `__init__` runs **once**, in MRO order. This is called **cooperative multiple inheritance**. For it to work, every class in the chain must call `super()`, and they usually pass extra arguments along with `**kwargs`.

> Inside `B`, `super()` means "next after B **in the MRO of the actual object**". For a `D` object that's `C`, even though `B` doesn't inherit from `C`!

## When two parents have the same method

The one that comes **first in the MRO** wins: usually the parent listed first. Swap the order in `class X(First, Second)` to change it.

## Impossible hierarchies

Some orders contradict each other, for example `class X(A, B)` together with `class Y(B, A)` and then `class Z(X, Y)`. Python refuses with `TypeError: Cannot create a consistent method resolution order (MRO)`.

## Guidance

| ✅ | ❌ |
|----|----|
| keep hierarchies shallow (2–3 levels) | 6-level chains nobody can follow |
| use multiple inheritance mainly for small **mixins** (Lecture 12) | two big parents with overlapping methods |
| always use `super()` with multiple inheritance | calling `Parent.method(self)` by name |
| check `__mro__` when confused | guessing |

## Exercises

1. Build `Vehicle → Car → ElectricCar` and print each class's MRO.
2. Give `Camera` an `info()` method too. Which `info()` does `SmartCar` use? Swap the parents and check again.
3. Recreate the diamond with name-based calls and count how often `A.__init__` runs. Then switch to `super()`.
4. Try to create an inconsistent MRO and read the error.

**Next →** [Lecture 12: Mixins](../12_mixins/)
