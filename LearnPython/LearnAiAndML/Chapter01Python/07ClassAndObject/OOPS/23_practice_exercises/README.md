# Lecture 23: Practice exercises (20, auto-checked)

| File | What it is |
|------|------------|
| `exercises.py` | **Your work.** 20 class stubs. Each docstring says exactly what will be tested. |
| `solutions.py` | Reference solutions. Try first! |
| `lecture.py` | The checker. `python lecture.py` tests `solutions.py`; `python lecture.py exercises` tests **your** file. |

```
python lecture.py exercises
  ✔ 01 Rectangle
  ✘ 05 BankAccount                 withdraw(1000): returned 100, expected ValueError
  …
  Score: 7 / 20
```

## The exercises

| # | Class | Concept | Lecture |
|---|-------|---------|---------|
| 01 | `Rectangle` | `__init__`, methods | 02–03 |
| 02 | `Counter` | instance state, default args | 03 |
| 03 | `Student.count` | class attribute shared by all | 04 |
| 04 | `Temperature` | property with setter validation; read-only property | 07 |
| 05 | `BankAccount` | encapsulation, read-only `balance`, raising errors | 05–07 |
| 06 | `Point` | `@classmethod` alternative constructor with `cls`; `@staticmethod` | 08 |
| 07 | `Animal` / `Dog` / `Cat` | inheritance + overriding | 09–10 |
| 08 | `Employee` / `Manager` | `super().__init__` and extending a method | 10 |
| 09 | `Shape` / `Circle` / `Square` | `ABC` + `@abstractmethod` | 17 |
| 10 | `Book` | `__str__` vs `__repr__` | 14 |
| 11 | `Playlist` | `__len__`, `__getitem__`, `__contains__` | 14 |
| 12 | `Vector` | `__add__`, `__mul__`, `__rmul__`, `__eq__` | 15 |
| 13 | `Version` | comparisons, `total_ordering`, `sorted()` | 15 |
| 14 | `Coordinate` | `__eq__` + `__hash__` for sets and dicts | 15 |
| 15 | `Stack` | composition instead of inheritance | 18 |
| 16 | `JsonMixin` / `User` | mixins | 12 |
| 17 | `Multiplier` | `__call__` with state | 14 |
| 18 | `Product` | `@dataclass` + property | 19 |
| 19 | `Tracker` | context manager `__enter__` / `__exit__` | 14 |
| 20 | `Countdown` | `__iter__` (re-iterable) | 14, 16 |

## How to practise

1. Do them in order. Later ones assume earlier skills.
2. Run the checker after each one. Failure messages show the call, what you returned and what was expected.
3. When you reach 20 / 20, compare with `solutions.py`. Is yours shorter? Clearer?
4. Extra challenge: add `__repr__` to every class you wrote.

**Next →** [Lecture 24: Quick revision](../24_quick_revision/)
