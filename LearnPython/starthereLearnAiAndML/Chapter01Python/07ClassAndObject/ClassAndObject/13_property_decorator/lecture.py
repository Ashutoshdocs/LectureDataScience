"""Lecture 13: @property: getters, setters, deleters, read-only and computed properties."""

print("=== 1. A property with getter, setter and deleter ===")


class Account:
    def __init__(self, owner, balance=0):
        self._owner = owner
        self.balance = balance                 # goes through the setter

    @property
    def balance(self):
        print("    (getter called)")
        return self._balance

    @balance.setter
    def balance(self, value):
        print(f"    (setter called with {value!r})")
        if not isinstance(value, (int, float)):
            raise TypeError("balance must be a number")
        if value < 0:
            raise ValueError("balance cannot be negative")
        self._balance = value

    @balance.deleter
    def balance(self):
        print("    (deleter called) closing balance")
        del self._balance

    @property
    def owner(self):                           # read-only
        return self._owner


print("  create:")
acc = Account("Asha", 1000)
print("  read:")
print("  ->", acc.balance)
print("  assign:")
acc.balance = 1500
print("  += (getter then setter):")
acc.balance += 500
print("  invalid values:")
for bad in [-1, "lots"]:
    try:
        acc.balance = bad
    except (ValueError, TypeError) as e:
        print(f"  -> {type(e).__name__}: {e}")
try:
    Account("Ravi", -10)
except ValueError as e:
    print("  -> constructor got the same validation:", e)
print("  read-only owner:", acc.owner)
try:
    acc.owner = "Someone else"
except AttributeError as e:
    print("  ->", e)
print("  delete:")
del acc.balance
print("  hasattr(acc, '_balance'):", hasattr(acc, "_balance"))

print("\n=== 2. Computed properties never go stale ===")


class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.stored_area = width * height      # stored once: goes stale

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        if value <= 0:
            raise ValueError("width must be positive")
        self._width = value

    @property
    def area(self):                            # computed every time
        return self.width * self.height


r = Rectangle(4, 3)
r.width = 10
print("  computed area:", r.area, "| stored area:", r.stored_area, "<- stale")
try:
    r.width = 0
except ValueError as e:
    print("  r.width = 0 ->", e)

print("\n=== 3. Two linked properties: Celsius & Fahrenheit ===")


class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius

    @property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("below absolute zero")
        self._celsius = value

    @property
    def fahrenheit(self):
        return round(self.celsius * 9 / 5 + 32, 2)

    @fahrenheit.setter
    def fahrenheit(self, f):
        self.celsius = round((f - 32) * 5 / 9, 2)   # reuses celsius validation


t = Temperature(25)
print("  25 C ->", t.fahrenheit, "F")
t.fahrenheit = 212
print("  set 212 F ->", t.celsius, "C")
try:
    t.fahrenheit = -1000
except ValueError as e:
    print("  set -1000 F ->", e)

print("\n=== 4. Adding a property later doesn't break callers ===")


class ProductV1:
    def __init__(self, price):
        self.price = price                     # plain attribute


class ProductV2:
    def __init__(self, price):
        self.price = price                     # now validated, same caller code

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError("price cannot be negative")
        self._price = round(value, 2)


for cls in (ProductV1, ProductV2):
    p = cls(99.999)
    p.price = p.price + 1                      # identical caller code for both versions
    print(f"  {cls.__name__}: price = {p.price}")

print("\n=== 5. The recursion trap ===")


class Broken:
    @property
    def value(self):
        return self.value                      # calls itself forever


try:
    Broken().value
except RecursionError as e:
    print("  RecursionError:", str(e)[:45], "...")

print("\n=== 6. The older property() function ===")


class Temp:
    def __init__(self, c):
        self._c = c

    def _get(self):
        return self._c

    def _set(self, v):
        self._c = v

    celsius = property(_get, _set, doc="temperature in C")


tp = Temp(30)
tp.celsius = 31
print("  Temp.celsius via property():", tp.celsius, "| doc:", Temp.celsius.__doc__)
print("  type(Account.__dict__['balance']):", type(Account.__dict__["balance"]).__name__)
