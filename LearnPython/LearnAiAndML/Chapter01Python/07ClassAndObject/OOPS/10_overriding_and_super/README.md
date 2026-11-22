# Lecture 10: Overriding methods & `super()`

Run: `python lecture.py`

## Overriding = the child's version wins

If a child defines a method with **the same name** as the parent, Python uses the child's version (it's found first in the lookup order).

```python
class Employee:
    def describe(self):
        return f"{self.name} earns {self.salary}"

class Intern(Employee):
    def describe(self):                       # REPLACES the parent's version
        return f"{self.name} is an intern"
```

## Replace or extend?

| Goal | How |
|------|-----|
| **Replace** the behaviour completely | just define the method; don't call the parent |
| **Extend** the behaviour: do what the parent does, plus more | call `super().method(...)` inside your version |

```python
class Manager(Employee):
    def __init__(self, name, salary, team):
        super().__init__(name, salary)        # parent sets up name & salary
        self.team = team                      # child adds its own part

    def describe(self):
        base = super().describe()             # reuse the parent's text
        return base + f" and manages {self.team} people"
```

## What `super()` does

`super()` returns a proxy that finds the **next class in the MRO** (Lecture 11). With single inheritance, that's simply the parent. `super().__init__(name, salary)` = "run my parent's setup on this same object".

### Why not write `Employee.__init__(self, name, salary)`?

It works for simple cases, but:
- it hard-codes the parent's name, so renaming the parent or changing the hierarchy breaks it;
- with multiple inheritance, it can call a class **twice** or skip one (Lecture 11 shows this).

**Always use `super()`.**

## The `__init__` rule

If the child defines `__init__`, the parent's `__init__` **does not run automatically**. Forget `super().__init__(...)` and the parent's attributes never get created:

```python
class Manager(Employee):
    def __init__(self, name, salary, team):
        self.team = team                # forgot super().__init__
m.describe()   # AttributeError: 'Manager' object has no attribute 'name'
```

If the child **doesn't** define `__init__`, the parent's is used automatically.

## Overriding rules of thumb

1. **Keep the same signature** (same parameters, compatible return). Code that works with an `Employee` should work with a `Manager` too. This is the *Liskov Substitution Principle*.
2. Call `super()` **first** in `__init__`, so the parent's attributes exist before you use them.
3. Override **special methods** too: `__str__`, `__eq__`, and so on.
4. Use a class attribute to customise behaviour without overriding a whole method (`bonus_rate = 0.2` in the child).

## Exercises

1. Add `Intern(Employee)` whose `describe()` adds " (intern)" by extending the parent's text.
2. Give `Employee` an `annual_bonus()` using a class attribute `bonus_rate`. Make `Manager` override only the rate.
3. Remove `super().__init__` from `Manager` and read the error.
4. Make `SavingsAccount(BankAccount)` override `withdraw()` to keep a minimum balance of 500, calling `super().withdraw()` for the real work.

**Next →** [Lecture 11: Inheritance types & MRO](../11_inheritance_types_and_mro/)
