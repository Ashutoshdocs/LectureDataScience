"""Lecture 01: Why classes? Scattered variables -> dictionaries -> a class."""

print("=== 1. Scattered variables ===")
name1, marks1 = "Asha", 88
name2, marks2 = "Ravi", 74


def show(name, marks):
    print(" ", name, "scored", marks)


show(name1, marks1)
show(name2, marks1)          # BUG: wrong marks, and nothing warns us

print("\n=== 2. Dictionaries: better, but only halfway ===")
asha = {"name": "Asha", "marks": 88}
ravi = {"name": "Ravi", "marks": 74}


def show_dict(student):
    print(" ", student["name"], "scored", student["marks"])


def add_bonus_dict(student, bonus):
    student["marks"] += bonus


add_bonus_dict(ravi, 5)
show_dict(asha)
show_dict(ravi)
typo = {"nmae": "Dev", "marks": 90}          # accepted without complaint...
try:
    show_dict(typo)                          # ...and crashes only later
except KeyError as e:
    print("  typo found too late -> KeyError:", e)

print("\n=== 3. A class: data + behaviour together ===")


class Student:
    def __init__(self, name, marks):
        self.name = name
        self.marks = marks

    def show(self):
        print(" ", self.name, "scored", self.marks)

    def add_bonus(self, bonus):
        self.marks += bonus

    def has_passed(self):
        return self.marks >= 40


asha = Student("Asha", 88)
ravi = Student("Ravi", 74)
ravi.add_bonus(5)
asha.show()
ravi.show()
print("  Ravi passed?", ravi.has_passed())

try:
    Student("Dev")                           # missing marks: caught IMMEDIATELY
except TypeError as e:
    print("  missing data caught at creation -> TypeError:", e)

print("\n=== 4. One class, many objects ===")
class_list = [Student("Asha", 88), Student("Ravi", 74), Student("Meena", 35)]
for s in class_list:
    s.show()
print("  passed:", [s.name for s in class_list if s.has_passed()])
