"""Lecture 08: Instance vs class vs static methods; alternative constructors; cls with subclasses."""
import datetime as dt

print("=== 1. Three kinds of method side by side ===")


class Date:
    created = 0

    def __init__(self, day, month, year):
        if not 1 <= month <= 12 or not 1 <= day <= Date.days_in_month(month, year):
            raise ValueError(f"invalid date {day}-{month}-{year}")
        self.day, self.month, self.year = day, month, year
        type(self).created += 1

    def show(self):                                   # instance method
        return f"{self.day:02d}/{self.month:02d}/{self.year}"

    @classmethod
    def from_string(cls, text):                       # alternative constructor
        d, m, y = map(int, text.split("-"))
        return cls(d, m, y)

    @classmethod
    def today(cls):
        t = dt.date.today()
        return cls(t.day, t.month, t.year)

    @classmethod
    def how_many(cls):
        return cls.created

    @staticmethod
    def is_leap(year):                                # static helper
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

    @staticmethod
    def days_in_month(month, year):
        if month == 2:
            return 29 if Date.is_leap(year) else 28
        return 30 if month in (4, 6, 9, 11) else 31


d1 = Date(13, 11, 2026)
d2 = Date.from_string("29-02-2024")
d3 = Date.today()
print("  d1:", d1.show(), "| d2:", d2.show(), "| today is a", type(d3).__name__)
print("  is_leap(2024), is_leap(2026), is_leap(1900), is_leap(2000):",
      Date.is_leap(2024), Date.is_leap(2026), Date.is_leap(1900), Date.is_leap(2000))
print("  static method via an object works too:", d1.is_leap(2028))
print("  Date.how_many():", Date.how_many())
try:
    Date.from_string("29-02-2026")
except ValueError as e:
    print("  Date.from_string('29-02-2026') -> ValueError:", e)

print("\n=== 2. cls means 'whichever class was called' ===")


class IndianDate(Date):
    MONTHS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()

    def show(self):
        return f"{self.day:02d}-{self.MONTHS[self.month - 1]}-{self.year}"


class HardCodedDate(Date):
    @classmethod
    def from_string(cls, text):
        d, m, y = map(int, text.split("-"))
        return Date(d, m, y)                          # wrong: always the parent


i = IndianDate.from_string("13-11-2026")
h = HardCodedDate.from_string("13-11-2026")
print("  IndianDate.from_string    ->", type(i).__name__, i.show())
print("  HardCodedDate.from_string ->", type(h).__name__, "(wrong type, because of Date(...) instead of cls(...))")
print("  IndianDate.how_many() reads the counter through cls:", IndianDate.how_many())

print("\n=== 3. Alternative constructors for real data ===")


class Employee:
    raise_rate = 0.05

    def __init__(self, name, dept, salary):
        if not Employee.is_valid_salary(salary):
            raise ValueError(f"bad salary {salary!r}")
        self.name, self.dept, self.salary = name, dept, salary

    @classmethod
    def from_csv(cls, line):
        name, dept, salary = (part.strip() for part in line.split(","))
        return cls(name, dept, int(salary))

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data.get("dept", "General"), data["salary"])

    @classmethod
    def set_raise_rate(cls, rate):
        cls.raise_rate = rate

    @staticmethod
    def is_valid_salary(value):
        return isinstance(value, (int, float)) and value > 0

    def apply_raise(self):
        self.salary = round(self.salary * (1 + self.raise_rate))

    def __repr__(self):
        return f"Employee({self.name!r}, {self.dept!r}, {self.salary})"


staff = [Employee("Asha", "IT", 60000),
         Employee.from_csv("Ravi, HR, 45000"),
         Employee.from_dict({"name": "Dev", "salary": 52000})]
Employee.set_raise_rate(0.10)
for e in staff:
    e.apply_raise()
print("  after a 10% company raise:", staff)
print("  Employee.is_valid_salary(-5):", Employee.is_valid_salary(-5))

print("\n=== 4. Built-in classes use the same idea ===")
print("  dict.fromkeys('abc', 0)            ->", dict.fromkeys("abc", 0))
print("  dt.date.fromisoformat('2026-11-13') ->", dt.date.fromisoformat("2026-11-13"))
print("  int.from_bytes(b'\\x01\\x00', 'big') ->", int.from_bytes(b"\x01\x00", "big"))

print("\n=== 5. Common mistakes ===")


class Oops:
    x = "class value"

    def not_a_classmethod(cls):            # forgot @classmethod
        return type(cls).__name__

    @staticmethod
    def uses_self():
        return self.x                      # noqa: F821  there is no self here


print("  without @classmethod, 'cls' is actually:", Oops().not_a_classmethod(), "object")
try:
    Oops.uses_self()
except NameError as e:
    print("  self inside @staticmethod -> NameError:", e)
