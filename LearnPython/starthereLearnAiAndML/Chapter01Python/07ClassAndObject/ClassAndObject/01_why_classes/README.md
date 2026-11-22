# Lecture 01: Why classes?

Run: `python lecture.py`

## The problem: scattered data

A program about students. Each student has a **name** and **marks**:

```python
name1 = "Asha"
marks1 = 88
name2 = "Ravi"
marks2 = 74

def show(name, marks):
    print(name, "scored", marks)

show(name1, marks1)
show(name2, marks1)      # BUG: Ravi with Asha's marks. Python doesn't notice!
```

- **Data is scattered.** A student's name and marks live in unrelated variables.
- **Easy to mismatch.** Nothing links `name2` to `marks2`.
- **Doesn't scale.** 40 students × 6 fields = 240 variables.

## Halfway there: dictionaries

```python
asha = {"name": "Asha", "marks": 88}

def show(student):
    print(student["name"], "scored", student["marks"])

def add_bonus(student, bonus):
    student["marks"] += bonus
```

Better: one value per student. But two problems remain:

1. **Data and behaviour are separate.** `show` and `add_bonus` are loose functions. Nothing says they belong to students.
2. **No guaranteed shape.** A typo like `{"nmae": "Dev"}` is accepted, and crashes only later inside `show`.

| | dict | class |
|---|---|---|
| Groups data | ✅ | ✅ |
| Functions live with the data | ❌ outside | ✅ inside (methods) |
| Every object set up the same way | ❌ | ✅ the constructor guarantees it |
| Nice printing, comparison, validation | manual | built in via special methods & properties |

## The fix: one class, many objects

```python
class Student:
    def __init__(self, name, marks):     # constructor: runs on creation
        self.name = name                 # data stored ON the object
        self.marks = marks

    def show(self):                      # method: a function that belongs to Student
        print(self.name, "scored", self.marks)

    def add_bonus(self, bonus):
        self.marks += bonus

asha = Student("Asha", 88)               # create objects from the class
ravi = Student("Ravi", 74)
ravi.add_bonus(5)
asha.show()                              # Asha scored 88
ravi.show()                              # Ravi scored 79
```

### The vocabulary, with an analogy

| Term | Analogy | In the code |
|------|---------|-------------|
| **Class** | a cookie cutter, a blueprint | `Student` |
| **Object / instance** | a cookie, a house built from the blueprint | `asha`, `ravi` |
| **Attribute** | what the object *has* | `name`, `marks` |
| **Method** | what the object *can do* | `show()`, `add_bonus()` |

You make the cutter **once** and stamp out as many cookies as you like. Each one has its own decoration (its own name and marks).

## Step-through: what Python does

| Step | Line | What happens |
|------|------|--------------|
| 1 | `class Student:` | Python stores the blueprint. Nothing inside runs yet |
| 2 | `asha = Student("Asha", 88)` | creates an empty object, then calls `__init__(obj, "Asha", 88)` |
| 3 | `self.name = name` | stores `"Asha"` on that object |
| 4 | back to step 2 | the finished object is stored in `asha` |
| 5 | `ravi.add_bonus(5)` | inside the method, `self` *is* ravi → `self.marks` becomes 79 |
| 6 | `asha.show()` | inside the method, `self` *is* asha → prints her own data |

## Exercises

1. Add a third student and call `show()` on it.
2. Add a method `has_passed(self)` that returns `True` if marks ≥ 40.
3. In the dict version, write `has_passed(student)`. Notice it lives *outside* the data.

<details><summary>Solutions</summary>

```python
def has_passed(self):
    return self.marks >= 40
```
</details>

**Next →** [Lecture 02: Your first class & object](../02_first_class_and_object/)
