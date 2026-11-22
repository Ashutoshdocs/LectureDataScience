"""Lecture 01: Classes & objects: blueprint vs instance, type, isinstance, identity."""

print("=== 1. The simplest class ===")


class Dog:
    pass


a = Dog()
b = Dog()
print("  a          :", a)
print("  type(a)    :", type(a))
print("  isinstance :", isinstance(a, Dog), isinstance(5, Dog))

print("\n=== 2. Every call makes a new, separate object ===")
print("  a is b :", a is b)
print("  a == b :", a == b, "(by default == means 'same object')")
print("  a is a :", a is a)
print("  id(a) != id(b):", id(a) != id(b))
c = a
print("  c = a  -> c is a:", c is a, "(two names, ONE object)")

print("\n=== 3. Attaching attributes from outside (not the proper way) ===")
a.name = "Bruno"
print("  a.name :", a.name)
try:
    print(b.name)
except AttributeError as e:
    print("  b.name -> AttributeError:", e)
print("  a.__dict__:", a.__dict__, "| b.__dict__:", b.__dict__)

print("\n=== 4. Class vs object: brackets matter ===")
x = Dog
y = Dog()
print("  x = Dog   ->", x, "(the class)")
print("  y = Dog() ->", y, "(an instance)")
print("  x() makes a new Dog too:", isinstance(x(), Dog))

print("\n=== 5. Classes are objects (of type 'type') ===")
print("  type(Dog) :", type(Dog))
print("  type(str) :", type(str), "<- built-in types are classes too")
print("  Dog.__name__:", Dog.__name__)


class Cat:
    pass


kinds = [Dog, Cat, list, str]
things = [k() for k in kinds]
print("  objects made from a list of classes:", [type(t).__name__ for t in things])

print("\n=== 6. Many objects in a collection ===")
cats = [Cat() for _ in range(3)]
for i, cat in enumerate(cats, start=1):
    cat.name = f"Cat{i}"
print("  names:", [cat.name for cat in cats])
print("  all different objects:", len({id(cat) for cat in cats}) == 3)
