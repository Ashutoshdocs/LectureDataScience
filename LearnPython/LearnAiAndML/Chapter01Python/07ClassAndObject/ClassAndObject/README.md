# Python Classes & Objects: From Zero to Confident

A hands-on course in 20 short lectures (00–19) on **classes and objects** in Python, and on **every kind of function you can put inside a class**:

| Kind | Decorator | First parameter | Lecture |
|------|-----------|-----------------|---------|
| Instance method ("normal" method) | none | `self` (the object) | 05, 06 |
| Constructor | n/a: named `__init__` | `self` | 07 |
| Destructor | n/a: named `__del__` | `self` | 08 |
| Class method | `@classmethod` | `cls` (the class) | 09 |
| Static method | `@staticmethod` | nothing automatic | 10 |
| Getter / setter methods | none | `self` | 12 |
| Properties (Pythonic getters/setters) | `@property`, `@x.setter`, `@x.deleter` | `self` | 13 |
| Special ("dunder") methods | n/a: `__str__`, `__eq__`, ... | `self` | 15 |
| Global (module-level) function | n/a: outside the class | n/a | 06, 11 |

Every lecture folder has:

| File | What it is |
|------|------------|
| `README.md` | The lesson: concepts, diagrams, step-by-step traces, tables, common mistakes, exercises (with solutions) |
| `lecture.py` | Runnable code for the lesson. Read it, run it, change it |

No libraries to install. Everything uses plain **Python 3.10+**.

## How to use this course

1. Work through the folders **in order**.
2. In each folder: read `README.md`, then run `python lecture.py` and compare the output with the README.
3. Do the exercises. Change the code, break it on purpose, and read the error messages.

Examples that are *meant* to fail are wrapped in `try/except`, so every file runs to the end and prints the error message for you to read.

## Course map

| # | Lecture | Big idea |
|---|---------|----------|
| 00 | [Prerequisites](00_prerequisites/) | Functions, parameters, return, scope (LEGB), dicts |
| 01 | [Why classes?](01_why_classes/) | Scattered variables → dicts → one class, many objects |
| 02 | [Your first class & object](02_first_class_and_object/) | `class`, instantiation, `type`, `isinstance`, `id`, vocabulary |
| 03 | [Instance attributes](03_instance_attributes/) | `obj.x = ...`, `__dict__`, `getattr` / `setattr` / `hasattr` / `delattr` |
| 04 | [Class attributes & shadowing](04_class_attributes_and_shadowing/) | Shared data, lookup order, the "assign through an object" trap |
| 05 | [Instance methods & `self`](05_instance_methods_and_self/) | What `self` really is; `obj.m()` = `Class.m(obj)`; forgetting `self` |
| 06 | [Return values, chaining & global functions](06_methods_return_values_and_chaining/) | Methods calling methods, fluent chaining, function vs method |
| 07 | [The constructor `__init__`](07_constructor_init/) | Defaults, validation, computed attributes, no overloading, gotchas |
| 08 | [The destructor `__del__`](08_destructor_del/) | Object lifetime, reference counting, safe cleanup, `with` |
| 09 | [`@classmethod` & `cls`](09_classmethod_and_cls/) | Class-wide data, counters, alternative constructors (factories) |
| 10 | [`@staticmethod`](10_staticmethod/) | Helpers that belong to the class but need no data |
| 11 | [Choosing the right function type](11_choosing_the_right_function_type/) | Decision guide; all kinds side by side |
| 12 | [Getters & setters](12_getters_and_setters/) | `get_x` / `set_x`, validation, `_protected` and `__private` names |
| 13 | [`@property`](13_property_decorator/) | Pythonic getters/setters/deleters, read-only and computed attributes |
| 14 | [Scope in classes](14_scope_in_classes/) | Local vs `self.x`, `global`, class-body scope, the same name at every level |
| 15 | [Special (dunder) methods](15_special_methods/) | `__str__`, `__repr__`, `__eq__`, `__lt__`, `__len__`, `__add__`, `__call__` … |
| 16 | [Working with objects](16_working_with_objects/) | Objects as arguments/returns, lists of objects, aliasing, copying, objects inside objects |
| 17 | [Project: bank account](17_project_bank_account/) | Every function type in one class |
| 18 | [Project: library system](18_project_library_system/) | Several classes working together |
| 19 | [Recap & cheat sheet](19_recap_cheatsheet/) | Everything on one page + self-test |

## Run everything at once

```bash
python run_all.py
```

## Scope of this course

This course covers **classes and objects**: creating them, attributes, all kinds of methods, constructors, destructors, getters/setters/properties, special methods and scope. The OOP *pillars* of inheritance and polymorphism are a separate topic and are not covered here. Getters, setters and `_private` naming are covered, because they are everyday tools for working with a single class.
