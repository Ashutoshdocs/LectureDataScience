"""Lecture 09: Inheritance basics: reuse, is-a, method lookup, isinstance/issubclass, object."""

print("=== 1. Without inheritance: copy-paste ===")


class DogNoInherit:
    def __init__(self, name):
        self.name = name

    def eat(self):
        return f"{self.name} is eating"


class CatNoInherit:
    def __init__(self, name):          # same code again...
        self.name = name

    def eat(self):                     # ...and again
        return f"{self.name} is eating"


print("  two classes, duplicated __init__ and eat():", DogNoInherit("A").eat(), "|", CatNoInherit("B").eat())

print("\n=== 2. With inheritance: write shared code once ===")


class Animal:
    legs = 4

    def __init__(self, name, age=1):
        self.name = name
        self.age = age

    def eat(self):
        return f"{self.name} is eating"

    def sleep(self):
        return f"{self.name} is sleeping"

    def describe(self):
        return f"{type(self).__name__} {self.name}, {self.age} yr, {self.legs} legs"


class Dog(Animal):
    def bark(self):
        return f"{self.name} says Woof!"


class Cat(Animal):
    def meow(self):
        return f"{self.name} says Meow"


class Bird(Animal):
    legs = 2                               # child changes a class attribute

    def fly(self):
        return f"{self.name} flies"


pets = [Dog("Bruno", 3), Cat("Kitty"), Bird("Tweety", 2)]
for pet in pets:
    print("  ", pet.describe(), "|", pet.eat(), "|", pet.sleep())
print("  ", pets[0].bark(), "|", pets[1].meow(), "|", pets[2].fly())

print("\n=== 3. How Python finds a method ===")
d = pets[0]
for name in ["bark", "eat", "__str__"]:
    owner = next(cls.__name__ for cls in type(d).__mro__ if name in cls.__dict__)
    print(f"  d.{name:<8} found in {owner}")
print("  Dog.__mro__ :", [c.__name__ for c in Dog.__mro__])
print("  Dog.__bases__:", Dog.__bases__)

print("\n=== 4. isinstance / issubclass / type ===")
print("  isinstance(d, Dog), isinstance(d, Animal), isinstance(d, Cat):",
      isinstance(d, Dog), isinstance(d, Animal), isinstance(d, Cat))
print("  issubclass(Dog, Animal), issubclass(Animal, Dog):", issubclass(Dog, Animal), issubclass(Animal, Dog))
print("  type(d) is Animal:", type(d) is Animal, "<- type() ignores inheritance; prefer isinstance")
print("  every class inherits from object:", all(issubclass(c, object) for c in (Dog, Animal, int, str)))

print("\n=== 5. Inheritance goes one way only ===")
generic = Animal("Generic")
try:
    generic.bark()
except AttributeError as e:
    print("  Animal('Generic').bark() -> AttributeError:", e)

print("\n=== 6. Hierarchy of vehicles ===")


class Vehicle:
    def __init__(self, brand):
        self.brand = brand
        self.running = False

    def start(self):
        self.running = True
        return f"{self.brand} {type(self).__name__} started"

    def stop(self):
        self.running = False
        return f"{self.brand} stopped"


class Car(Vehicle):
    def open_boot(self):
        return f"{self.brand} boot open"


class Bike(Vehicle):
    def wheelie(self):
        return f"{self.brand} does a wheelie" if self.running else "start the bike first"


car, bike = Car("Tata"), Bike("Bajaj")
print("  ", car.start(), "|", car.open_boot(), "|", car.stop())
print("  ", bike.wheelie(), "|", bike.start(), "|", bike.wheelie())
print("  both are Vehicles:", all(isinstance(v, Vehicle) for v in (car, bike)))
