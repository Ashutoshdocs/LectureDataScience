"""Lecture 02: __init__ & attributes: constructor, self, defaults, validation, __dict__."""

print("=== 1. __init__ runs automatically ===")


class Student:
    def __init__(self, name, marks):
        print(f"    __init__ running: self={type(self).__name__} object, name={name!r}, marks={marks}")
        self.name = name
        self.marks = marks


s1 = Student("Asha", 92)
s2 = Student("Ravi", 78)
print("  s1:", s1.name, s1.marks, "| s2:", s2.name, s2.marks)
print("  s1.__dict__:", s1.__dict__)
print("  Student.__init__(s1, ...) is what Python really calls; self IS s1")

print("\n=== 2. self.x = x vs x = x ===")


class Broken:
    def __init__(self, name):
        name = name              # local variable only


class Fixed:
    def __init__(self, name):
        self.name = name         # stored on the object


print("  Broken('A').__dict__:", Broken("A").__dict__)
print("  Fixed('A').__dict__ :", Fixed("A").__dict__)

print("\n=== 3. Defaults, validation and derived attributes ===")


class Pupil:
    def __init__(self, name, marks=0, subjects=None):
        if not name or not name.strip():
            raise ValueError("name is required")
        if not 0 <= marks <= 100:
            raise ValueError(f"marks must be 0-100, got {marks}")
        self.name = name.strip().title()
        self.marks = marks
        self.subjects = subjects if subjects is not None else []
        self.result = "PASS" if marks >= 40 else "FAIL"


p = Pupil("  meera iyer ", 65, ["Maths"])
q = Pupil("dev")
print("  p:", vars(p))
print("  q:", vars(q))
for bad in [("", 50), ("Zara", 150)]:
    try:
        Pupil(*bad)
    except ValueError as e:
        print(f"  Pupil{bad} -> ValueError: {e}")

print("\n=== 4. The mutable default trap ===")


class BadPupil:
    def __init__(self, name, subjects=[]):
        self.name = name
        self.subjects = subjects


x, y = BadPupil("X"), BadPupil("Y")
x.subjects.append("Art")
print("  BadPupil: y.subjects =", y.subjects, "<- Y got X's subject! (one shared list)")
x2, y2 = Pupil("X"), Pupil("Y")
x2.subjects.append("Art")
print("  Pupil   : y.subjects =", y2.subjects, "<- separate lists")

print("\n=== 5. Working with attributes by name ===")
print("  getattr(p, 'name')             :", getattr(p, "name"))
print("  getattr(p, 'email', 'unknown') :", getattr(p, "email", "unknown"))
setattr(p, "email", "meera@school.in")
print("  after setattr, hasattr email   :", hasattr(p, "email"))
del p.email
print("  after del, hasattr email       :", hasattr(p, "email"))
for field in ["name", "marks", "result"]:
    print(f"    {field:<7} = {getattr(p, field)}")

print("\n=== 6. Common errors ===")


class NoSelf:
    def __init__(name):
        pass


class Typo:
    def __int__(self, name):     # typo: __int__ instead of __init__
        self.name = name


class ReturnsSelf:
    def __init__(self):
        return self


try:
    NoSelf("A")
except TypeError as e:
    print("  missing self   ->", e)
try:
    Student("Asha")
except TypeError as e:
    print("  missing arg    ->", e)
try:
    Typo("A")
except TypeError as e:
    print("  __int__ typo   ->", e, "(no __init__ accepted the argument)")
try:
    ReturnsSelf()
except TypeError as e:
    print("  return in init ->", e)
