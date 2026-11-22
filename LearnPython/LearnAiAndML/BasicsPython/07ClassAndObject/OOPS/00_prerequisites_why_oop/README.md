# Lecture 00: Prerequisites & why OOP exists

Run: `python lecture.py`

## What you should know before starting

OOP is built **on top of** ordinary Python. If any of these feel shaky, revise them first:

| Topic | You should be able to… |
|-------|------------------------|
| Variables & types | explain that `x = 5` makes the name `x` refer to an int object |
| Lists & dicts | create, index, loop over, and modify them |
| Functions | write `def f(a, b=1): return ...`, call it, understand parameters and `return` |
| Scope | know that variables created inside a function are local |
| Loops & conditions | `for`, `while`, `if/elif/else` |
| Errors | read a traceback; know what `try/except` does |

One idea matters most: **everything in Python is already an object**. `5`, `"hi"`, `[1, 2]` and even functions are objects. Each has a **type** (its class), **data**, and **methods**:

```python
name = "asha"
type(name)          # <class 'str'>     ← its class
name.upper()        # 'ASHA'            ← a method: an action the object can do
[1, 2].append(3)    # list objects have methods too
```

In this course you learn to make **your own** types.

## The problem OOP solves

Imagine a program that manages bank accounts using only dicts and functions (procedural style):

```python
acc1 = {"owner": "Asha", "balance": 1000}
acc2 = {"owner": "Ravi", "balance": 500}

def deposit(acc, amount):
    acc["balance"] += amount

def withdraw(acc, amount):
    if amount > acc["balance"]:
        print("Insufficient funds")
        return
    acc["balance"] -= amount
```

It works until the program grows. Then these problems appear:

| Problem | What goes wrong |
|---------|-----------------|
| **Nothing protects the data** | any code can write `acc1["balance"] = -99999` and skip the rules in `withdraw` |
| **Typos are silent** | `acc1["balence"] = 0` creates a new key; no error |
| **Data and behaviour are separate** | `deposit` lives far from the dict it changes, and you must pass `acc` to every function |
| **No clear "shape"** | nothing says which keys an account must have |
| **Name clashes** | `withdraw` for accounts vs. `withdraw` for a wallet means two different names or `if type == ...` everywhere |
| **Hard to extend** | a savings account with interest means copying and editing every function |

## The OOP answer

A **class** bundles the data **and** the functions that work on it into one unit:

```python
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

acc1 = BankAccount("Asha", 1000)
acc1.deposit(500)          # the account does its own work
```

## OOP vocabulary

| Word | Meaning | Real-world analogy |
|------|---------|--------------------|
| **Class** | a blueprint / type | the design drawing of a car |
| **Object / instance** | one thing built from the class | your actual car |
| **Attribute** | data stored on an object | its colour, mileage |
| **Method** | a function that belongs to the class | `drive()`, `brake()` |
| **Constructor** (`__init__`) | sets up a new object | the factory assembling the car |
| **`self`** | "this particular object" | "my car" (not cars in general) |

## The four pillars

| Pillar | One-line idea | Lectures |
|--------|---------------|----------|
| **Encapsulation** | bundle data with methods; hide internal details | 06–08 |
| **Inheritance** | build new classes from existing ones | 09–12 |
| **Polymorphism** | one interface, many forms: the same call does the right thing for each type | 13–16 |
| **Abstraction** | show *what* something does and hide *how* | 17–18 |

## When to use OOP (and when not to)

| ✅ Use classes when… | ❌ Plain functions are fine when… |
|----------------------|----------------------------------|
| several pieces of data belong together **and** have rules (account, student, order) | you transform input to output with no lasting state (`celsius_to_f`) |
| you'll create **many** similar things | it's a short script |
| behaviour must stay consistent with the data | a dict or tuple is enough (just reading a config) |
| you want several variations of one idea (types of payment, shapes) | |

> Python lets you mix both styles freely. OOP is a tool, not a religion.

## Exercises

1. In `lecture.py`, find the line where the procedural version lets the balance go negative. Why can't the class version be broken the same way so easily?
2. List three objects from a school system. For each, write two attributes and two methods.
3. Run `dir("hello")` and find three methods you've never used.

**Next →** [Lecture 01: Classes & objects](../01_classes_and_objects/)
