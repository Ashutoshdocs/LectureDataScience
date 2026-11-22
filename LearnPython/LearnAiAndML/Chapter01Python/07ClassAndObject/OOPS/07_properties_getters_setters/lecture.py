"""Lecture 07: @property: getters, setters, deleters, read-only & computed attributes, cached_property."""
import functools
import time

print("=== 1. The problem with plain attributes ===")


class PlainTemp:
    def __init__(self, celsius):
        self.celsius = celsius


p = PlainTemp(25)
p.celsius = -500
print("  PlainTemp accepted -500 C without complaint:", p.celsius)

print("\n=== 2. Property with getter, setter and computed values ===")


class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius                  # uses the setter -> validated

    @property
    def celsius(self):
        print("    (getter runs)")
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        print(f"    (setter runs with {value})")
        if not isinstance(value, (int, float)):
            raise TypeError("temperature must be a number")
        if value < -273.15:
            raise ValueError("below absolute zero!")
        self._celsius = value

    @celsius.deleter
    def celsius(self):
        print("    (deleter runs)")
        del self._celsius

    @property
    def fahrenheit(self):
        return round(self._celsius * 9 / 5 + 32, 2)

    @property
    def kelvin(self):
        return round(self._celsius + 273.15, 2)


t = Temperature(25)
print("  t.celsius ->", t.celsius)
t.celsius = 100
print("  F and K (computed, always in sync):", t.fahrenheit, t.kelvin)
for bad in [-300, "hot"]:
    try:
        t.celsius = bad
    except (ValueError, TypeError) as e:
        print(f"  t.celsius = {bad!r} -> {type(e).__name__}: {e}")
try:
    Temperature(-1000)
except ValueError as e:
    print("  Temperature(-1000) -> ValueError:", e, "(even __init__ is validated)")
try:
    t.fahrenheit = 50
except AttributeError as e:
    print("  t.fahrenheit = 50 ->", e)
try:
    t.fahrenheit()
except TypeError as e:
    print("  t.fahrenheit() ->", e, "(properties are not called)")
del t.celsius
print("  after del, hasattr(t, '_celsius'):", hasattr(t, "_celsius"))

print("\n=== 3. Getter/setter that manages several attributes ===")


class Person:
    def __init__(self, first, last):
        self.first, self.last = first, last

    @property
    def full_name(self):
        return f"{self.first} {self.last}"

    @full_name.setter
    def full_name(self, text):
        parts = text.strip().split(" ", 1)
        if len(parts) != 2:
            raise ValueError("full name needs a first and last name")
        self.first, self.last = (s.title() for s in parts)

    @property
    def initials(self):
        return f"{self.first[0]}.{self.last[0]}."


person = Person("Asha", "Rao")
person.full_name = "meera iyer"
print("  after setting full_name:", person.first, "|", person.last, "| initials:", person.initials)

print("\n=== 4. Adding validation later doesn't break callers ===")


class ProductV1:
    def __init__(self, name, price):
        self.name, self.price = name, price


class ProductV2:
    def __init__(self, name, price):
        self.name, self.price = name, price

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError("price can't be negative")
        self._price = round(value, 2)


for cls in (ProductV1, ProductV2):
    item = cls("pen", 10.456)          # identical calling code for both versions
    item.price = 12.999
    print(f"  {cls.__name__}: item.price = {item.price}")
try:
    ProductV2("pen", -1)
except ValueError as e:
    print("  ProductV2('pen', -1) -> ValueError:", e)

print("\n=== 5. Read-only view of private data ===")


class Account:
    def __init__(self, balance):
        self._balance = balance

    @property
    def balance(self):
        return self._balance

    def deposit(self, amount):
        self._balance += amount


a = Account(100)
a.deposit(50)
print("  a.balance:", a.balance)
try:
    a.balance = 1_000_000
except AttributeError as e:
    print("  a.balance = 1_000_000 ->", e)

print("\n=== 6. cached_property: compute once, then reuse ===")


class Report:
    def __init__(self, rows):
        self.rows = rows

    @functools.cached_property
    def summary(self):
        time.sleep(0.2)               # pretend this is slow
        return {"rows": len(self.rows), "total": sum(self.rows)}


r = Report([5, 10, 15])
for attempt in (1, 2):
    start = time.perf_counter()
    s = r.summary
    print(f"  access {attempt}: {s} in {(time.perf_counter() - start) * 1000:.1f} ms")

print("\n=== 7. Common mistake: getter returning itself ===")


class Recursive:
    @property
    def value(self):
        return self.value             # calls the property again, forever


try:
    Recursive().value
except RecursionError:
    print("  RecursionError: store the data under a different name like self._value")
