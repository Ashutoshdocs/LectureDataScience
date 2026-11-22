"""Lecture 04: Class attributes (shared) vs instance attributes, lookup order, shadowing."""

print("=== 1. A class attribute is shared ===")


class Student:
    school = "City High"
    country = "India"


s1 = Student()
s2 = Student()
s1.name = "Asha"
s2.name = "Ravi"
print(s1.name, s1.school)
print(s2.name, s2.school, s2.country)
Student.school = "Green Valley"            # change once, through the class
print("after change:", s1.school, s2.school)
print("s1.__dict__ =", s1.__dict__, "(school is not here)")
print("'school' in Student.__dict__ ?", "school" in Student.__dict__)

print("\n=== 2. Shadowing: assigning through an object ===")


class Counter:
    step = 1


a = Counter()
b = Counter()
a.step = 10
print("a.step, b.step, Counter.step =", a.step, b.step, Counter.step)
print("a.__dict__ =", a.__dict__, "| b.__dict__ =", b.__dict__)
del a.step
print("after del a.step -> a.step =", a.step, "(class value shows through)")
Counter.step = 5
print("after Counter.step = 5 ->", a.step, b.step)

print("\n=== 3. The += trap ===")
print("before: b.__dict__ =", b.__dict__, "| Counter.step =", Counter.step)
b.step += 5          # means b.step = b.step + 5: READS the class value 5, WRITES 10 onto b
print("after : b.step =", b.step, "| Counter.step =", Counter.step, "(unchanged) | b.__dict__ =", b.__dict__)

print("\n=== 4. Mutable class attribute: shared by accident ===")


class Team:
    members = []                          # one list for ALL teams


red = Team()
blue = Team()
red.members.append("Asha")
print("blue.members =", blue.members, "<- blue 'has' Asha too!")
print("same list object?", red.members is blue.members is Team.members)


class FixedTeam:
    def __init__(self):
        self.members = []                 # a new list for each team


red = FixedTeam()
blue = FixedTeam()
red.members.append("Asha")
print("fixed:", red.members, blue.members)

print("\n=== 5. Good uses of class attributes ===")


class Circle:
    PI = 3.14159                          # constant
    count = 0                             # counter shared by all circles
    unit = "cm"                           # shared setting


Circle.count += 1
Circle.count += 1
print("Circle.PI =", Circle.PI, "| circles made =", Circle.count, "| unit =", Circle.unit)
