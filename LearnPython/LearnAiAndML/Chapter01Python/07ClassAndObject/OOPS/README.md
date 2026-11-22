# Python Object-Oriented Programming: a complete course

From "why do we even need classes?" to the four pillars of OOP, with projects, auto-checked exercises and a revision sheet.

Each folder is one lecture:

- `README.md` teaches the lecture: what you need first, **why** the feature exists, **when** to use it, **how** to use it, common mistakes, and exercises with solutions.
- `lecture.py` is a runnable demo. Run it with `python lecture.py` and compare the output with the README. Errors that are part of the lesson are caught and printed, so every file runs to the end.

```bash
python run_all.py        # runs every lecture and reports "25 of 25 scripts ran successfully"
```

Requires Python 3.10+ and the standard library only.

## Course map

| # | Lecture | You will learn |
|---|---------|----------------|
| **Part 1: Classes & objects** | | |
| 00 | [Prerequisites & why OOP](00_prerequisites_why_oop/) | what you need first; the problems OOP solves (procedural vs OOP) |
| 01 | [Classes & objects](01_classes_and_objects/) | blueprint vs instance, `type`, `isinstance`, identity |
| 02 | [`__init__` & attributes](02_init_and_attributes/) | constructors, `self`, defaults, `__dict__`, validation in `__init__` |
| 03 | [Methods & `self`](03_methods_and_self/) | instance methods, `obj.m()` = `Class.m(obj)`, methods calling methods, method chaining |
| 04 | [Class vs instance attributes](04_class_vs_instance_attributes/) | shared data, lookup order, shadowing, the mutable class attribute trap |
| 05 | [Project: bank account](05_project_bank_account/) | data + rules together, transaction history |
| **Part 2: Encapsulation** | | |
| 06 | [Access levels](06_encapsulation_access_levels/) | public, `_protected`, `__private`, name mangling |
| 07 | [Properties: getters & setters](07_properties_getters_setters/) | `@property`, setters with validation, read-only and computed attributes, deleters |
| 08 | [Class methods & static methods](08_classmethod_staticmethod/) | `cls`, alternative constructors, factory methods, helpers |
| **Part 3: Inheritance** | | |
| 09 | [Inheritance basics](09_inheritance_basics/) | parent/child, "is-a", method lookup, `isinstance` / `issubclass`, `object` |
| 10 | [Overriding & `super()`](10_overriding_and_super/) | replace vs extend behaviour, `super().__init__`, common mistakes |
| 11 | [Inheritance types & MRO](11_inheritance_types_and_mro/) | single, multilevel, hierarchical, multiple, the diamond, `__mro__` |
| 12 | [Mixins](12_mixins/) | small reusable abilities added through multiple inheritance |
| **Part 4: Polymorphism** | | |
| 13 | [Polymorphism basics](13_polymorphism_basics/) | one interface with many forms; replacing `if/elif` type checks |
| 14 | [Magic (dunder) methods](14_magic_methods/) | `__str__`, `__repr__`, `__len__`, `__bool__`, `__getitem__`, `__iter__`, `__contains__`, `__call__` |
| 15 | [Operator overloading](15_operator_overloading/) | `+ - * == <`, `NotImplemented`, `total_ordering`, `__hash__` |
| 16 | [Duck typing & protocols](16_duck_typing_and_protocols/) | "can it quack?", EAFP, `hasattr`, `typing.Protocol` |
| **Part 5: Abstraction & design** | | |
| 17 | [Abstract classes](17_abstract_classes/) | `ABC`, `@abstractmethod`, abstract properties, the template method pattern |
| 18 | [Composition vs inheritance](18_composition_vs_inheritance/) | "has-a", delegation, swappable parts, aggregation |
| 19 | [Dataclasses](19_dataclasses/) | `@dataclass`, defaults, `field`, `frozen`, `order`, `__post_init__` |
| **Part 6: Putting it together** | | |
| 20 | [The four pillars together](20_four_pillars_together/) | one example using every pillar; SOLID in plain words |
| 21 | [Project: library manager](21_project_library_manager/) | abstract items, members (composition), loans, fines |
| 22 | [Project: payment system](22_project_payment_system/) | ABC + polymorphism + mixins + custom exceptions |
| 23 | [Practice exercises](23_practice_exercises/) | 20 auto-checked exercises with solutions |
| 24 | [Quick revision](24_quick_revision/) | the whole course on one page, plus a self-test |

## How to study

1. Read the lecture's README from top to bottom.
2. Run `lecture.py` and match each printed section to the README.
3. Change the code and break it on purpose. Read the error messages.
4. Do the exercises at the end of each README before opening the solutions.
