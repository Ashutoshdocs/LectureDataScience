"""Lecture 04: Class vs instance attributes: sharing, lookup order, shadowing, mutable trap."""

print("=== 1. Shared class data vs per-object instance data ===")


class Car:
    wheels = 4
    count = 0

    def __init__(self, brand):
        self.brand = brand
        Car.count += 1


a, b = Car("Tata"), Car("Honda")
print("  a.brand, a.wheels:", a.brand, a.wheels)
print("  b.brand, b.wheels:", b.brand, b.wheels)
print("  Car.count        :", Car.count)
print("  a.__dict__       :", a.__dict__, "<- no 'wheels' here")
print("  'wheels' in Car.__dict__:", "wheels" in Car.__dict__)

print("\n=== 2. Writing through an object SHADOWS the class value ===")
b.wheels = 3
print("  after b.wheels = 3 -> a:", a.wheels, "| b:", b.wheels, "| Car:", Car.wheels)
print("  b.__dict__:", b.__dict__)
del b.wheels
print("  after del b.wheels -> b:", b.wheels, "(back to the class value)")
Car.wheels = 6
print("  after Car.wheels = 6 -> a:", a.wheels, "| b:", b.wheels, "(changing the class affects all)")
Car.wheels = 4

print("\n=== 3. Counter: Car.count += 1 vs self.count += 1 ===")


class WrongCounter:
    count = 0

    def __init__(self):
        self.count += 1          # creates an instance attribute!


class RightCounter:
    count = 0

    def __init__(self):
        type(self).count += 1    # same as RightCounter.count += 1


w = [WrongCounter() for _ in range(3)]
r = [RightCounter() for _ in range(3)]
print("  WrongCounter.count:", WrongCounter.count, "| each object has", w[0].count)
print("  RightCounter.count:", RightCounter.count)

print("\n=== 4. The mutable class attribute trap ===")


class BadTeam:
    members = []

    def __init__(self, name):
        self.name = name

    def add(self, person):
        self.members.append(person)


class GoodTeam:
    def __init__(self, name):
        self.name = name
        self.members = []

    def add(self, person):
        self.members.append(person)


red, blue = BadTeam("red"), BadTeam("blue")
red.add("Asha")
blue.add("Ravi")
print("  BadTeam  red :", red.members, "| blue:", blue.members, "<- shared list!")
red, blue = GoodTeam("red"), GoodTeam("blue")
red.add("Asha")
blue.add("Ravi")
print("  GoodTeam red :", red.members, "| blue:", blue.members)

print("\n=== 5. Good uses: constants, overridable defaults, registry ===")


class Employee:
    raise_rate = 0.05                 # default for everyone
    COMPANY = "Acme Ltd"              # constant
    registry = {}                     # deliberately shared: look up by id

    def __init__(self, emp_id, name, salary):
        self.emp_id, self.name, self.salary = emp_id, name, salary
        Employee.registry[emp_id] = self

    def apply_raise(self):
        self.salary = round(self.salary * (1 + self.raise_rate))


e1 = Employee(1, "Asha", 50000)
e2 = Employee(2, "Ravi", 50000)
e2.raise_rate = 0.10                  # special rate for Ravi only
e1.apply_raise()
e2.apply_raise()
print(f"  {e1.name}: {e1.salary} (rate {e1.raise_rate}) | {e2.name}: {e2.salary} (rate {e2.raise_rate})")
Employee.raise_rate = 0.08            # company-wide change
print("  after company change -> Asha's rate:", e1.raise_rate, "| Ravi keeps his own:", e2.raise_rate)
print("  registry lookup 2 ->", Employee.registry[2].name, "| company:", e1.COMPANY)

print("\n=== 6. Lookup order summary ===")
try:
    a.colour
except AttributeError as e:
    print("  a.colour -> not on the object, not on the class -> AttributeError:", e)
