# Lecture 16: Working with objects

Run: `python lecture.py`

## 1. Objects as arguments: functions get the SAME object

Python passes a **reference** to the object, not a copy. A function that changes an attribute changes the caller's object:

```python
def pay(wallet, amount):
    wallet.money -= amount       # modifies the original

a = Wallet("Asha", 500)
pay(a, 250)
a.money                          # 250
```

But **reassigning** the parameter inside the function doesn't affect the caller:

```python
def replace(wallet):
    wallet = Wallet("New", 0)    # only the local name now points elsewhere
```

## 2. Objects as return values

Functions and methods can return existing objects or create new ones:

```python
def richer(w1, w2):
    return w1 if w1.money >= w2.money else w2     # returns one of the EXISTING objects

def make_wallet(name):
    return Wallet(name, 0)                        # returns a NEW object
```

## 3. A list of objects: the backbone of real programs

```python
staff = [Employee("Asha", "IT", 60000), Employee("Ravi", "HR", 45000), ...]

for e in staff:                                   # each e is a full object
    print(e.name, e.salary)

it_names = [e.name for e in staff if e.dept == "IT"]       # filter
payroll  = sum(e.salary for e in staff)                     # aggregate
top      = max(staff, key=lambda e: e.salary)               # best by one attribute
by_name  = sorted(staff, key=lambda e: e.name)              # sort
by_dept  = {}                                                # group
for e in staff:
    by_dept.setdefault(e.dept, []).append(e)
```

A **dict of objects** gives fast lookup by a key: `employees_by_id[101]`.

## 4. Identity, equality & aliasing

| | `is` | `==` |
|---|---|---|
| Asks | same object in memory? | equal values? |
| Your classes, by default | identity | **falls back to identity** (until you define `__eq__`) |

```python
a = Coin(5); b = Coin(5); c = a
a == b      # False by default (different objects)
a is c      # True: c is an ALIAS, another name for the same object
c.value = 10
a.value     # 10: changed through the alias
```

**Assignment never copies an object.**

## 5. Copying: shallow vs deep

```python
import copy
b = copy.copy(a)        # SHALLOW: new object, but attributes that are lists/objects are SHARED
c = copy.deepcopy(a)    # DEEP: new object AND new copies of everything inside it
```

| | `b = a` | `copy.copy(a)` | `copy.deepcopy(a)` |
|---|---|---|---|
| New outer object | ❌ | ✅ | ✅ |
| New inner lists / objects | ❌ | ❌ shared | ✅ |

## 6. Objects inside objects (composition)

An attribute can hold another object. This is how real systems are built:

```python
class Address:
    def __init__(self, city, pin): ...

class Customer:
    def __init__(self, name, address):
        self.name = name
        self.address = address          # a Customer HAS an Address

cust.address.city                       # chained dots
```

Composition ("has-a") lets small, simple classes combine into bigger ones. Lecture 18's library project is built this way.

## Exercises

1. Turn the global `pay` function into a method `Wallet.pay(self, amount)`.
2. Print the average salary, and give every IT employee a 10% raise.
3. Use `copy.copy` on an object containing a list, append to the copy's list, and check the original.
4. Add a `Customer.move(city)` method that changes the nested address.

<details><summary>Solutions</summary>

3. The original's list changes too, because a shallow copy shares inner objects. Use `deepcopy` to avoid this.
</details>

**Next →** [Lecture 17: Project: bank account](../17_project_bank_account/)
