"""
LESSON 1: __init__ inside a CLASS (the constructor)
====================================================
Run:  python lesson1_class_init.py

__init__ is a special method Python calls AUTOMATICALLY
every time you create a new object from a class.
Its job: set up the object's starting data (attributes).
"""

print("=" * 50)
print("PART A: A class WITHOUT __init__")
print("=" * 50)


class EmptyStudent:
    pass


s = EmptyStudent()
s.name = "Asha"          # we must add data by hand, one by one
s.age = 20
print("Empty student:", s.name, s.age)
# Problem: easy to forget a field, and every object is set up differently.


print()
print("=" * 50)
print("PART B: A class WITH __init__")
print("=" * 50)


class Student:
    def __init__(self, name, age):
        # 'self' = the brand-new object being created
        print(f"  -> __init__ is running for {name}!")
        self.name = name        # store data ON the object
        self.age = age
        self.courses = []       # a default starting value

    def enroll(self, course):
        self.courses.append(course)

    def introduce(self):
        print(f"  Hi, I'm {self.name}, {self.age} years old. Courses: {self.courses}")


print("Creating ravi...")
ravi = Student("Ravi", 21)      # Python calls Student.__init__(ravi, "Ravi", 21)
print("Creating meera...")
meera = Student("Meera", 19)

ravi.enroll("Python")
meera.enroll("Maths")
meera.enroll("Physics")

ravi.introduce()
meera.introduce()
# Each object has its OWN data. Changing ravi doesn't affect meera.


print()
print("=" * 50)
print("PART C: Default arguments in __init__")
print("=" * 50)


class BankAccount:
    def __init__(self, owner, balance=0):   # balance is optional
        self.owner = owner
        self.balance = balance

    def __repr__(self):
        return f"BankAccount(owner={self.owner!r}, balance={self.balance})"


print(BankAccount("Kiran"))          # uses default balance=0
print(BankAccount("Divya", 5000))    # overrides it


print()
print("=" * 50)
print("PART D: Common beginner mistake")
print("=" * 50)
try:
    Student("Only a name")           # forgot the age argument
except TypeError as e:
    print("  TypeError:", e)
print("  __init__ demands every required argument, just like a normal function.")


print()
print("KEY TAKEAWAYS")
print(" 1. __init__ runs automatically when you write ClassName(...).")
print(" 2. 'self' is the new object; self.x = ... stores data on it.")
print(" 3. You never call __init__ directly yourself.")
print(" 4. __init__ should not return anything (it returns None).")
