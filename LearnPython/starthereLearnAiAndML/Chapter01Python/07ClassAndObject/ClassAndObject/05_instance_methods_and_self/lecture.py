"""Lecture 05: Instance methods and self."""

print("=== 1. Your first methods ===")


class Greeter:
    def hello(self):
        print("  Hello from a method!")

    def hello_name(self, name):
        print("  Hello,", name)


g = Greeter()
g.hello()
g.hello_name("Asha")
Greeter.hello_name(g, "Asha (called the long way)")

print("\n=== 2. self IS the object before the dot ===")


class Light:
    def turn_on(self):
        self.on = True
        print(f"  turn_on: self is the object with id {id(self)}")

    def turn_off(self):
        self.on = False

    def status(self):
        print("  on?", self.on)


kitchen = Light()
hall = Light()
print(f"  kitchen id = {id(kitchen)}")
kitchen.turn_on()
print(f"  hall id    = {id(hall)}")
Light.turn_on(hall)
hall.turn_off()
kitchen.status()
hall.status()
print("  kitchen.__dict__ =", kitchen.__dict__, "| hall.__dict__ =", hall.__dict__)

garage = Light()
try:
    garage.status()                        # turn_on never ran -> no 'on' attribute
except AttributeError as e:
    print("  garage.status() ->", e)

print("\n=== 3. What an instance method can use ===")
TAX_RATE = 0.18                            # global


def format_rupees(x):                      # global function
    return f"Rs {x:,.2f}"


class Item:
    category = "general"                   # class attribute

    def set(self, name, price):
        self.name = name
        self.price = price

    def price_with_tax(self):
        return self.price * (1 + TAX_RATE)

    def describe(self):
        total = self.price_with_tax()      # another method, via self
        label = f"{self.name} [{self.category}]"    # attribute + class attribute
        return f"{label}: {format_rupees(total)}"   # global function


lamp = Item()
lamp.set("Lamp", 1500)
print(" ", lamp.describe())

print("\n=== 4. Forgetting self ===")


class Calc:
    def add(a, b):                          # forgot self
        return a + b


print("  Calc.add(2, 3) =", Calc.add(2, 3))
try:
    Calc().add(2, 3)
except TypeError as e:
    print("  Calc().add(2, 3) ->", e)


class FixedCalc:
    def add(self, a, b):
        return a + b


print("  FixedCalc().add(2, 3) =", FixedCalc().add(2, 3))

print("\n=== 5. Bound methods remember their object ===")
say = g.hello_name
print("  type:", type(say).__name__, "| bound to:", type(say.__self__).__name__)
say("Ravi")
print("  through the class it's a plain", type(Greeter.hello_name).__name__)
