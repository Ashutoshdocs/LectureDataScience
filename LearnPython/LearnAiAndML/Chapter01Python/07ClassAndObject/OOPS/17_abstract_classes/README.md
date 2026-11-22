# Lecture 17: Abstraction & abstract classes

Run: `python lecture.py`

## What is abstraction?

**Abstraction** means showing **what** something does and hiding **how** it does it. You press "Pay" in an app without knowing whether it uses UPI, a card network or a wallet API. The *what* (pay this amount) is the same; the *how* is hidden in different classes.

In code, abstraction means defining a **contract**: "every payment method **must** have `pay(amount)`". The code that uses payments depends only on that contract.

## The problem with "just remember to override it"

```python
class Payment:
    def pay(self, amount):
        raise NotImplementedError

class Wallet(Payment):
    pass                 # forgot pay()!

w = Wallet()             # created fine...
w.pay(100)               # ...fails much later, maybe in production
```

## Abstract Base Classes (ABCs)

```python
from abc import ABC, abstractmethod

class Payment(ABC):                      # 1. inherit from ABC
    @abstractmethod                      # 2. mark what children MUST implement
    def pay(self, amount): ...

    def receipt(self, amount):           # 3. normal methods can use the abstract ones
        return f"Receipt: {self.pay(amount)}"

class UPI(Payment):
    def pay(self, amount):
        return f"Paid Rs {amount} via UPI"
```

| Action | Result |
|--------|--------|
| `Payment()` | ❌ `TypeError: Can't instantiate abstract class Payment ...`: the template can't be used on its own |
| `Wallet()` where `Wallet` doesn't implement `pay` | ❌ `TypeError` **at creation time**, which is early and clear |
| `UPI()` | ✅ every abstract method is implemented |

## What an ABC can contain

| Element | Purpose |
|---------|---------|
| `@abstractmethod` methods | the contract: children must write them |
| abstract **properties** (`@property` + `@abstractmethod`) | children must provide an attribute such as `fee_percent` |
| normal (concrete) methods | shared code written **once** that relies on the abstract parts |
| `__init__`, class attributes | shared setup |
| an abstract method **with a body** | default behaviour that children can call with `super()` |

## The template method pattern

The parent defines the **steps** of an algorithm in a concrete method. Children fill in the details:

```python
class DataExporter(ABC):
    def export(self, rows):                  # the template: fixed order of steps
        data = self.format(rows)             # ← abstract (each child differs)
        return self.header() + data          # ← hook with a default

    @abstractmethod
    def format(self, rows): ...

    def header(self):                        # optional hook: children MAY override
        return ""
```

`CsvExporter`, `JsonExporter` and `HtmlExporter` then only write `format()`.

## ABC vs `NotImplementedError` vs Protocol

| | `raise NotImplementedError` | `ABC` + `@abstractmethod` | `typing.Protocol` |
|--|------------------------------|---------------------------|-------------------|
| error appears | when the method is **called** | when the object is **created** | in the **type checker**, before running |
| needs inheritance | yes | yes | no |
| shares code | yes | yes | no |
| use when | a quick, informal contract | frameworks and plugin systems; a family of classes | interfaces for code you don't control |

## Built-in ABCs

`collections.abc` defines abstract classes such as `Iterable`, `Sized`, `Sequence`, `Mapping` and `MutableMapping`. Use them in `isinstance` checks (`isinstance(x, Iterable)`) or as bases that give you free methods (Lecture 12).

## Exercises

1. Add `Cash(Payment)` and `NetBanking(Payment)` classes.
2. Add an abstract property `fee_percent`, and a concrete method `total_with_fee(amount)` that uses it.
3. Create a `Wallet` subclass that forgets `pay` and read the error.
4. Add an `HtmlExporter` to the template-method example that overrides `header()`.

**Next →** [Lecture 18: Composition vs inheritance](../18_composition_vs_inheritance/)
