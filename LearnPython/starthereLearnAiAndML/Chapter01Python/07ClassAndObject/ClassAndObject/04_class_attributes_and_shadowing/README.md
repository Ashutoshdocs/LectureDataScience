# Lecture 04: Class attributes & shadowing

Run: `python lecture.py`

## Class attributes: shared by all objects

A variable written **directly in the class body** is a **class attribute**. There's **one copy**, stored on the class and shared by every object:

```python
class Student:
    school = "City High"          # class attribute

s1 = Student(); s1.name = "Asha"  # instance attributes
s2 = Student(); s2.name = "Ravi"

print(s1.school, s2.school)       # City High City High
Student.school = "Green Valley"   # change it ONCE, through the class
print(s1.school, s2.school)       # Green Valley Green Valley
```

| | Instance attribute | Class attribute |
|---|---|---|
| Created by | `self.x = …` / `obj.x = …` | writing `x = …` in the class body |
| Copies | one **per object** | one **for the whole class** |
| Stored in | `obj.__dict__` | `ClassName.__dict__` |
| Typical use | name, marks, balance | school name, constants, counters, settings |
| Change for everyone | n/a | `ClassName.x = new_value` |

## Attribute lookup order

When you read `obj.x`, Python searches:

```
 1. the object's own __dict__   →   2. the class   →   3. AttributeError
```

That's why `s1.school` works even though `school` isn't in `s1.__dict__`. Python finds it on the class.

## ⚠️ Shadowing: assigning through an object

```python
class Counter:
    step = 1

a = Counter(); b = Counter()
a.step = 10                       # does NOT change the class!
print(a.step, b.step, Counter.step)   # 10 1 1
```

**Reading** through an object can reach the class, but **assigning** through an object always creates (or changes) an **instance** attribute on that object. The new instance attribute **shadows** (hides) the class one, for `a` only.

| Step | `a.__dict__` | `Counter.step` | `a.step` | `b.step` |
|------|--------------|----------------|----------|----------|
| start | `{}` | 1 | 1 (from class) | 1 |
| `a.step = 10` | `{'step': 10}` | 1 | **10** (own) | 1 |
| `del a.step` | `{}` | 1 | 1 (class again) | 1 |
| `Counter.step = 5` | `{}` | 5 | 5 | 5 |

### The `+=` trap

```python
b.step += 5        # means: b.step = b.step + 5
```
It **reads** the class value (1) and **writes** an instance attribute (6). The class stays at 1.

## ⚠️ Mutable class attributes are shared

```python
class Team:
    members = []                  # ONE list for every team!

red = Team(); blue = Team()
red.members.append("Asha")        # modifies the shared list (no assignment)
print(blue.members)               # ['Asha']  ← surprise!
```

`append` doesn't assign, so no instance attribute is created and both objects share the class's list. Per-object lists belong in the constructor: `self.members = []` (Lecture 07).

## Exercises

1. Add `country = "India"` to `Student` and read it from `s2`.
2. Print `s1.__dict__`. Is `school` in it?
3. Do `b.step += 5`. Print `b.step`, `Counter.step` and `b.__dict__`.
4. Fix the `Team` example so each team has its own list.

<details><summary>Solutions</summary>

2. No, only `name`.
3. `6`, `1`, `{'step': 6}`.
4. Set `self.members = []` inside `__init__`.
</details>

**Next →** [Lecture 05: Instance methods & `self`](../05_instance_methods_and_self/)
