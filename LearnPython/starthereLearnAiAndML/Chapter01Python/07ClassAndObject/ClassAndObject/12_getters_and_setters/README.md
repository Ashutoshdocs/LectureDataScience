# Lecture 12: Getters & setters (and `_protected` / `__private` names)

Run: `python lecture.py`

## The problem: anyone can put bad data in an attribute

```python
class Account:
    def __init__(self, balance):
        self.balance = balance

acc = Account(1000)
acc.balance = -5000          # nothing stops this!
acc.balance = "lots"         # or this
```

The constructor can validate the **starting** value (Lecture 07), but after that any code can assign anything.

## The classic solution: getter & setter methods

- A **getter** is a method that *returns* an attribute's value: `get_balance()`.
- A **setter** is a method that *changes* it, after checking the new value: `set_balance(value)`.

The data itself is stored under a name that signals "don't touch directly" (`_balance`):

```python
class Account:
    def __init__(self, owner, balance=0):
        self._owner = owner
        self._balance = 0
        self.set_balance(balance)          # reuse the setter's validation

    def get_balance(self):                 # GETTER
        return self._balance

    def set_balance(self, value):          # SETTER
        if not isinstance(value, (int, float)):
            raise TypeError("balance must be a number")
        if value < 0:
            raise ValueError("balance cannot be negative")
        self._balance = value

    def get_owner(self):                   # read-only: getter but no setter
        return self._owner
```

## What getters/setters give you

| Benefit | Example |
|---------|---------|
| **Validation** | reject negative or non-numeric balances |
| **Read-only data** | provide `get_owner()` but no `set_owner()` |
| **Computed values** | `get_balance_in_usd()` calculated on the fly |
| **Formatting / conversion** | store paise, return rupees |
| **Logging / side effects** | record every change in a history list |
| **Freedom to change internals later** | rename `_balance` without breaking callers |

## Naming conventions: public, `_protected`, `__private`

Python has **no truly private attributes**. It relies on naming conventions:

| Name | Meaning | Enforced? |
|------|---------|-----------|
| `balance` | public: anyone can read/write | n/a |
| `_balance` | "**internal**, please use the methods" | ❌ convention only; still accessible |
| `__balance` | "**private**": Python **renames** it to `_Account__balance` (*name mangling*) | partly: `acc.__balance` fails from outside |
| `__balance__` | reserved for Python's special names | n/a, don't invent your own |

```python
class Safe:
    def __init__(self):
        self.__code = 1234      # stored as _Safe__code

s = Safe()
s.__code                        # AttributeError
s._Safe__code                   # 1234, so it is still reachable: NOT real security
```

> **Rule of thumb:** use a single underscore `_x` for internal data. Use `__x` only when you specifically want name mangling to avoid accidental clashes. Neither is a security feature.

### ⚠️ The "new attribute" trap with private names

```python
s.__code = 9999      # doesn't change the private value!
```
From outside, `s.__code` isn't mangled, so this **creates a new, unrelated attribute** literally named `__code`. The real `_Safe__code` is unchanged.

## Getter/setter methods vs properties

Explicit `get_x()` / `set_x()` methods are common in Java and C++. They work in Python, but they make calling code noisy:

```python
acc.set_balance(acc.get_balance() + 500)     # getter/setter methods
acc.balance += 500                            # with a property (next lecture)
```

The **Pythonic** way is to start with a plain public attribute, and switch to a **`@property`** only when you need validation or computation. Callers never notice the change. That's Lecture 13.

## Exercises

1. Add `deposit(amount)` and `withdraw(amount)` methods that use the setter.
2. Add `get_history()` that returns a **copy** of a `_history` list. Why a copy?
3. Make `set_balance` record every change in `_history`.
4. Show that `acc._balance = -1` still "works". Why is that allowed?

<details><summary>Solutions</summary>

2. Returning the list itself would let callers modify your internal list: `acc.get_history().clear()`.
4. `_balance` is only a convention. Python trusts programmers ("we're all consenting adults").
</details>

**Next →** [Lecture 13: `@property`](../13_property_decorator/)
