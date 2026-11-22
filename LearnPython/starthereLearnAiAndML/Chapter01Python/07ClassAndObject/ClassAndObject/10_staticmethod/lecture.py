"""Lecture 10: @staticmethod: helpers that belong to a class but need no object/class data."""

print("=== 1. A class of helpers ===")


class MathTools:
    @staticmethod
    def is_even(n):
        return n % 2 == 0

    @staticmethod
    def square(n):
        return n * n

    @staticmethod
    def cube(n):
        return n ** 3

    @staticmethod
    def is_prime(n):
        return n > 1 and all(n % d for d in range(2, int(n ** 0.5) + 1))


print("  is_even(10):", MathTools.is_even(10), "| square(7):", MathTools.square(7),
      "| cube(3):", MathTools.cube(3))
print("  primes < 30:", [n for n in range(30) if MathTools.is_prime(n)])

print("\n=== 2. The class uses its own static method ===")


class Account:
    def __init__(self, owner, pin):
        if not Account.valid_pin(pin):
            raise ValueError("PIN must be 4 digits")
        self.owner = owner
        self.pin = pin

    @staticmethod
    def valid_pin(pin):
        return len(pin) == 4 and pin.isdigit()

    def change_pin(self, new_pin):
        if not self.valid_pin(new_pin):       # via self works too
            return "rejected"
        self.pin = new_pin
        return "changed"


print("  valid_pin('12a4') without any account:", Account.valid_pin("12a4"))
acc = Account("Asha", "4321")
print("  created account for", acc.owner)
print("  change to 'abcd':", acc.change_pin("abcd"), "| change to '9999':", acc.change_pin("9999"))
try:
    Account("Ravi", "12")
except ValueError as e:
    print("  Account('Ravi', '12') ->", e)

print("\n=== 3. Unit conversion + a class method that uses it ===")


class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius

    @staticmethod
    def c_to_f(c):
        return c * 9 / 5 + 32

    @staticmethod
    def f_to_c(f):
        return (f - 32) * 5 / 9

    @classmethod
    def from_fahrenheit(cls, f):
        return cls(round(cls.f_to_c(f), 2))

    def show(self):
        return f"{self.celsius} C = {self.c_to_f(self.celsius)} F"


print(" ", Temperature(30).show())
print(" ", Temperature.from_fahrenheit(98.6).show())

print("\n=== 4. Formatting helper ===")


class Product:
    def __init__(self, name, price):
        self.name, self.price = name, price

    @staticmethod
    def rupees(x):
        return f"Rs {x:,.2f}"

    def label(self):
        return f"{self.name}: {self.rupees(self.price)}"


print(" ", Product("Desk", 12500).label(), "| helper on its own:", Product.rupees(99))

print("\n=== 5. Mistakes ===")


class Wrong:
    @staticmethod
    def show():
        return self.name                          # noqa: F821


try:
    Wrong.show()
except NameError as e:
    print("  self in a static method ->", e)
print("  static method type through class :", type(MathTools.__dict__["square"]).__name__)
print("  ...and when you access it        :", type(MathTools.square).__name__, "(just a plain function)")
