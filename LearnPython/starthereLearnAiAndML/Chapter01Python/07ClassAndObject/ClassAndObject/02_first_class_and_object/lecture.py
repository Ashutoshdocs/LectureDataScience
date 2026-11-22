"""Lecture 02: Your first class & object: syntax, instantiation, identity, vocabulary."""


class Dog:
    """A dog in our shelter."""
    pass


print("=== 1. Creating objects ===")
d1 = Dog()
d2 = Dog()
print("type(d1)          :", type(d1))
print("isinstance(d1,Dog):", isinstance(d1, Dog))
print("d1 is d2          :", d1 is d2)
print("ids differ        :", id(d1) != id(d2))
print("type(Dog)         :", type(Dog))
print("Dog.__name__      :", Dog.__name__)
print("Dog.__doc__       :", Dog.__doc__)
print("default print     :", str(d1).split(" at ")[0] + " at 0x...>")


class Cat:
    pass


print("isinstance(d1,Cat):", isinstance(d1, Cat))

print("\n=== 2. A class is a value too ===")
Blueprint = Dog              # another name for the same class
d3 = Blueprint()
print("made from Blueprint, is a Dog?", isinstance(d3, Dog))

print("\n=== 3. Vocabulary in one small class ===")


class Phone:
    brand = "Generic"                 # attribute (shared by all phones)

    def ring(self):                   # method
        print("  Ring ring! (self is the phone object:", type(self).__name__ + ")")


my_phone = Phone()                    # instantiation -> object
print("attribute:", my_phone.brand)   # dot operator: read an attribute
my_phone.ring()                       # dot operator: call a method
print("method without brackets:", type(my_phone.ring).__name__, "(a bound method, not called)")

print("\n=== 4. An empty class body is not allowed ===")
try:
    exec("class Empty:\n")
except SyntaxError as e:
    print(type(e).__name__ + ":", e.msg)
