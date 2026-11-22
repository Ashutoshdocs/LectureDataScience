"""Lecture 07: The constructor __init__: why, how, defaults, validation, kinds, gotchas."""

print("=== 1. Without a constructor: easy to forget something ===")


class NoInitStudent:
    def show(self):
        print(" ", self.name, self.marks)


a = NoInitStudent()
a.name, a.marks = "Asha", 88
a.show()
b = NoInitStudent()
b.name = "Ravi"
try:
    b.show()
except AttributeError as e:
    print("  forgot marks ->", e)

print("\n=== 2. __init__ runs automatically ===")


class Student:
    def __init__(self, name, marks):
        print(f"  __init__ running: name={name!r}, marks={marks}")
        self.name = name
        self.marks = marks

    def show(self):
        print(f"  {self.name} scored {self.marks}")


a = Student("Asha", 88)
b = Student("Ravi", 74)
a.show()
b.show()
print("  a.__dict__ =", a.__dict__)
try:
    Student("Dev")
except TypeError as e:
    print("  missing argument ->", e)

print("\n=== 3. Default & keyword arguments ===")


class Pizza:
    def __init__(self, size="medium", toppings=None, cheese=True):
        self.size = size
        self.toppings = toppings if toppings is not None else []
        self.cheese = cheese

    def describe(self):
        extra = ", ".join(self.toppings) or "plain"
        return f"{self.size} pizza, {extra}, cheese={self.cheese}"


print(" ", Pizza().describe())
print(" ", Pizza("large", ["olive", "corn"]).describe())
print(" ", Pizza(cheese=False, size="small").describe())

print("\n=== 4. The mutable-default bug ===")


class BadPizza:
    def __init__(self, toppings=[]):         # ONE list, created once, shared!
        self.toppings = toppings


p1, p2 = BadPizza(), BadPizza()
p1.toppings.append("olive")
print("  BadPizza: p2.toppings =", p2.toppings, "<- p2 got p1's olive!")
q1, q2 = Pizza(), Pizza()
q1.toppings.append("olive")
print("  Pizza   : q2.toppings =", q2.toppings)

print("\n=== 5. Validation & computed attributes ===")


class Temperature:
    def __init__(self, celsius):
        if celsius < -273.15:
            raise ValueError("below absolute zero")
        self.celsius = celsius
        self.fahrenheit = celsius * 9 / 5 + 32
        self.kelvin = celsius + 273.15
        self.label = "hot" if celsius > 30 else "pleasant"


t = Temperature(35)
print(" ", t.celsius, t.fahrenheit, t.kelvin, t.label)
try:
    bad = Temperature(-300)
except ValueError as e:
    print("  Temperature(-300) ->", e, "| 'bad' exists?", "bad" in globals())

print("\n=== 6. Kinds of constructors ===")


class Dog:                                    # default constructor (none written)
    pass


class Box:                                    # non-parameterised
    def __init__(self):
        self.size = 1


class Item:                                   # parameterised
    def __init__(self, name, qty):
        self.name = name
        self.qty = qty


print("  Dog() ok:", isinstance(Dog(), Dog), "| Box().size =", Box().size, "| Item('pen', 3).qty =", Item("pen", 3).qty)

print("\n=== 7. No overloading: the second __init__ replaces the first ===")


class Point:
    def __init__(self):
        self.x = 0

    def __init__(self, x):                    # replaces the one above
        self.x = x


print("  Point(5).x =", Point(5).x)
try:
    Point()
except TypeError as e:
    print("  Point() ->", e)


class FixedPoint:
    def __init__(self, x=0):                  # one constructor, a default argument
        self.x = x


print("  FixedPoint().x =", FixedPoint().x, "| FixedPoint(5).x =", FixedPoint(5).x)

print("\n=== 8. More gotchas ===")


class ReturnsValue:
    def __init__(self):
        return 5


try:
    ReturnsValue()
except TypeError as e:
    print("  return from __init__ ->", e)


class ForgotSelf:
    def __init__(self, name):
        name = name                           # only a local variable!


print("  forgot self. -> attributes:", ForgotSelf("Asha").__dict__)


class Typo:
    def __int__(self):                        # typo: __int__ is a different special method
        self.ready = True


print("  typo __int__ -> attributes:", Typo().__dict__, "(constructor never ran)")

print("\n=== 9. Counting objects ===")


class Ticket:
    count = 0

    def __init__(self, passenger):
        Ticket.count += 1
        self.number = Ticket.count
        self.passenger = passenger


t1, t2, t3 = Ticket("Asha"), Ticket("Ravi"), Ticket("Dev")
print(f"  {t3.passenger} has ticket {t3.number} | sold: {Ticket.count}")
