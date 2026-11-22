"""Lecture 11: Single, multilevel, hierarchical, multiple, diamond inheritance; the MRO; cooperative super()."""


def mro(cls):
    return " -> ".join(c.__name__ for c in cls.__mro__)


print("=== 1. Multilevel and hierarchical ===")


class Vehicle:
    def info(self):
        return "I move"


class Car(Vehicle):
    def wheels(self):
        return 4


class ElectricCar(Car):
    def charge(self):
        return "Charging..."


class Bike(Vehicle):
    def wheels(self):
        return 2


class Truck(Vehicle):
    def wheels(self):
        return 6


e = ElectricCar()
print("  ElectricCar has all three levels:", e.info(), e.wheels(), e.charge())
print("  MRO:", mro(ElectricCar))
print("  hierarchical (siblings):", {c.__name__: c().wheels() for c in (Car, Bike, Truck)})

print("\n=== 2. Multiple inheritance ===")


class Camera:
    def snap(self):
        return "Click!"

    def info(self):
        return "I take photos"


class SmartCar(ElectricCar, Camera):
    pass


class CameraFirst(Camera, ElectricCar):
    pass


s = SmartCar()
print("  SmartCar abilities:", s.info(), s.wheels(), s.charge(), s.snap())
print("  SmartCar MRO   :", mro(SmartCar))
print("  CameraFirst().info():", CameraFirst().info(), "| MRO:", mro(CameraFirst))

print("\n=== 3. The diamond: calling parents by name ===")
calls = []


class A1:
    def __init__(self):
        calls.append("A")


class B1(A1):
    def __init__(self):
        calls.append("B")
        A1.__init__(self)


class C1(A1):
    def __init__(self):
        calls.append("C")
        A1.__init__(self)


class D1(B1, C1):
    def __init__(self):
        calls.append("D")
        B1.__init__(self)
        C1.__init__(self)


D1()
print("  init order by name:", calls, "<- A runs TWICE")

print("\n=== 4. The diamond with cooperative super() ===")
calls = []


class A:
    def __init__(self, **kwargs):
        calls.append("A")
        super().__init__(**kwargs)


class B(A):
    def __init__(self, b=None, **kwargs):
        calls.append("B")
        self.b = b
        super().__init__(**kwargs)


class C(A):
    def __init__(self, c=None, **kwargs):
        calls.append("C")
        self.c = c
        super().__init__(**kwargs)


class D(B, C):
    def __init__(self, d=None, **kwargs):
        calls.append("D")
        self.d = d
        super().__init__(**kwargs)


obj = D(b=1, c=2, d=3)
print("  init order with super():", calls, "<- each exactly once")
print("  MRO:", mro(D))
print("  every class got its argument via **kwargs:", vars(obj))
print("  inside B, super() pointed to:", D.__mro__[D.__mro__.index(B) + 1].__name__, "(not A!)")

print("\n=== 5. Same method in two parents: first in the MRO wins ===")


class Flyer:
    def move(self):
        return "flies"


class Swimmer:
    def move(self):
        return "swims"


class Duck(Flyer, Swimmer):
    pass


class Penguin(Swimmer, Flyer):
    pass


print("  Duck().move():", Duck().move(), "| Penguin().move():", Penguin().move())

print("\n=== 6. An impossible MRO ===")


class X(Flyer, Swimmer):
    pass


class Y(Swimmer, Flyer):
    pass


try:
    class Z(X, Y):
        pass
except TypeError as err:
    print("  TypeError:", err)
