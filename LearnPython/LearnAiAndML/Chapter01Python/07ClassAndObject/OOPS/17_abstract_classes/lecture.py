"""Lecture 17: Abstraction with ABCs: abstractmethod, abstract properties, template method, collections.abc."""
import collections.abc
import json
from abc import ABC, abstractmethod

print("=== 1. NotImplementedError fails late ===")


class LoosePayment:
    def pay(self, amount):
        raise NotImplementedError


class LooseWallet(LoosePayment):
    pass


w = LooseWallet()
print("  LooseWallet() created without complaint...")
try:
    w.pay(100)
except NotImplementedError:
    print("  ...and only failed when pay() was called: NotImplementedError")

print("\n=== 2. ABC fails early, at creation ===")


class Payment(ABC):
    def __init__(self, owner):
        self.owner = owner

    @property
    @abstractmethod
    def fee_percent(self):
        ...

    @abstractmethod
    def pay(self, amount):
        ...

    def total_with_fee(self, amount):              # concrete, shared
        return round(amount * (1 + self.fee_percent / 100), 2)

    def receipt(self, amount):
        total = self.total_with_fee(amount)
        return f"{self.owner}: {self.pay(total)} (incl. {self.fee_percent}% fee)"


class UPI(Payment):
    fee_percent = 0

    def pay(self, amount):
        return f"paid Rs {amount} via UPI"


class Card(Payment):
    @property
    def fee_percent(self):
        return 1.5

    def pay(self, amount):
        return f"paid Rs {amount} by card"


class Wallet(Payment):
    fee_percent = 0.5                              # forgot pay()


for method in [UPI("Asha"), Card("Ravi")]:
    print("  ", method.receipt(1000))
for cls in (Payment, Wallet):
    try:
        cls("Dev")
    except TypeError as e:
        print(f"  {cls.__name__}('Dev') -> TypeError: {e}")
print("  abstract methods of Payment:", sorted(Payment.__abstractmethods__))
print("  isinstance(UPI('x'), Payment):", isinstance(UPI("x"), Payment))

print("\n=== 3. Template method pattern ===")


class DataExporter(ABC):
    def export(self, rows):                        # fixed steps
        self.validate(rows)
        return self.header() + self.format(rows) + self.footer()

    def validate(self, rows):
        if not rows:
            raise ValueError("nothing to export")

    @abstractmethod
    def format(self, rows):
        ...

    def header(self):                              # optional hooks
        return ""

    def footer(self):
        return ""


class CsvExporter(DataExporter):
    def header(self):
        return "name,marks\n"

    def format(self, rows):
        return "\n".join(f"{r['name']},{r['marks']}" for r in rows)


class JsonExporter(DataExporter):
    def format(self, rows):
        return json.dumps(rows)


class HtmlExporter(DataExporter):
    def header(self):
        return "<table>"

    def format(self, rows):
        return "".join(f"<tr><td>{r['name']}</td><td>{r['marks']}</td></tr>" for r in rows)

    def footer(self):
        return "</table>"


rows = [{"name": "Asha", "marks": 92}, {"name": "Ravi", "marks": 78}]
for exporter in [CsvExporter(), JsonExporter(), HtmlExporter()]:
    print(f"  {type(exporter).__name__:<12} -> {exporter.export(rows)!r}")
try:
    CsvExporter().export([])
except ValueError as e:
    print("  shared validation from the parent ->", e)

print("\n=== 4. Abstract method with a default body (reached via super) ===")


class Notifier(ABC):
    @abstractmethod
    def send(self, msg):
        return f"[log] {msg}"                      # default behaviour


class EmailNotifier(Notifier):
    def send(self, msg):
        return super().send(msg) + " -> emailed"


print("  ", EmailNotifier().send("Order shipped"))

print("\n=== 5. Built-in ABCs in collections.abc ===")
for value in [[1, 2], "abc", {"a": 1}, 42, (x for x in range(3))]:
    print(f"  {type(value).__name__:<9} Iterable={isinstance(value, collections.abc.Iterable)!s:<5} "
          f"Sized={isinstance(value, collections.abc.Sized)!s:<5} "
          f"Mapping={isinstance(value, collections.abc.Mapping)}")
