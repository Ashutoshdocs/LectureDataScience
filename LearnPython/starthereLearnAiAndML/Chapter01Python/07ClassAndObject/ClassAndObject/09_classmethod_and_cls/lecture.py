"""Lecture 09: @classmethod and cls: class-wide data, counters, alternative constructors."""
import datetime

print("=== 1. Three kinds of methods ===")


class Demo:
    def instance_method(self):
        print("  instance method: self is a", type(self).__name__, "object")

    @classmethod
    def class_method(cls):
        print("  class method   : cls is the class", cls.__name__)

    @staticmethod
    def static_method():
        print("  static method  : no self, no cls")


d = Demo()
d.instance_method()
Demo.class_method()
d.class_method()                       # through an object: cls is STILL the class
Demo.static_method()
try:
    Demo.instance_method()             # no object -> no self
except TypeError as e:
    print("  Demo.instance_method() ->", e)

print("\n=== 2. Changing class-wide data ===")


class Shop:
    discount = 0

    def __init__(self, item, price):
        self.item = item
        self.price = price

    def final_price(self):
        return self.price * (100 - self.discount) / 100

    @classmethod
    def set_discount(cls, percent):
        cls.discount = percent

    @classmethod
    def reset_discount(cls):
        cls.discount = 0


pen, bag = Shop("pen", 50), Shop("bag", 800)
print("  before:", pen.final_price(), bag.final_price())
Shop.set_discount(10)
print("  after Shop.set_discount(10):", pen.final_price(), bag.final_price())
pen.set_discount(20)                   # via an object: still changes the CLASS
print("  after pen.set_discount(20):", Shop.discount, "| bag sees it:", bag.final_price())
Shop.reset_discount()


class BadShop:
    price = 0

    @classmethod
    def show_price(cls):
        return self.price               # noqa: F821  (no self in a class method)


try:
    BadShop.show_price()
except NameError as e:
    print("  self inside a classmethod ->", e)

print("\n=== 3. Counting & tracking objects ===")


class Student:
    count = 0
    all_students = []

    def __init__(self, name):
        self.name = name
        Student.count += 1
        Student.all_students.append(self)

    @classmethod
    def total(cls):
        return cls.count

    @classmethod
    def names(cls):
        return sorted(s.name for s in cls.all_students)


for n in ["Ravi", "Asha", "Meena"]:
    Student(n)
print("  total:", Student.total(), "| names:", Student.names())

print("\n=== 4. Alternative constructors (factories) ===")


class Date:
    def __init__(self, day, month, year):
        self.day, self.month, self.year = day, month, year

    @classmethod
    def from_string(cls, text):
        d, m, y = text.split("-")
        return cls(int(d), int(m), int(y))

    @classmethod
    def from_dict(cls, data):
        return cls(data["day"], data["month"], data["year"])

    @classmethod
    def from_tuple(cls, t):
        return cls(*t)

    @classmethod
    def today(cls):
        t = datetime.date.today()
        return cls(t.day, t.month, t.year)

    def show(self):
        return f"{self.day:02d}/{self.month:02d}/{self.year}"


dates = {
    "Date(5, 11, 2026)": Date(5, 11, 2026),
    "from_string('10-11-2026')": Date.from_string("10-11-2026"),
    "from_dict({...})": Date.from_dict({"day": 1, "month": 1, "year": 2027}),
    "from_tuple((25, 12, 2026))": Date.from_tuple((25, 12, 2026)),
}
for how, obj in dates.items():
    print(f"  {how:<28} -> {obj.show()} ({type(obj).__name__})")
print("  today() returns a", type(Date.today()).__name__, "object")

print("\n=== 5. Python's own alternative constructors ===")
print("  dict.fromkeys(['a', 'b'], 0) =", dict.fromkeys(["a", "b"], 0))
print("  datetime.date.fromisoformat('2026-11-22') =", datetime.date.fromisoformat("2026-11-22"))
print("  int.from_bytes(b'\\x01\\x00', 'big') =", int.from_bytes(b"\x01\x00", "big"))

print("\n=== 6. Class-level configuration ===")


class Price:
    currency = "Rs"
    tax_rate = 0.18

    def __init__(self, amount):
        self.amount = amount

    def show(self):
        return f"{self.currency} {self.amount * (1 + self.tax_rate):,.2f}"

    @classmethod
    def configure(cls, currency=None, tax_rate=None):
        if currency is not None:
            cls.currency = currency
        if tax_rate is not None:
            cls.tax_rate = tax_rate


p = Price(1000)
print("  default   :", p.show())
Price.configure(currency="USD", tax_rate=0.07)
print("  configured:", p.show())
