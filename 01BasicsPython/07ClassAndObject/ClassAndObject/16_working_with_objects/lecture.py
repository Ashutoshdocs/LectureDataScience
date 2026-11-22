"""Lecture 16: Objects as arguments/returns, lists of objects, aliasing, copying, composition."""
import copy

print("=== 1. Objects as arguments ===")


class Wallet:
    def __init__(self, owner, money):
        self.owner = owner
        self.money = money

    def __repr__(self):
        return f"Wallet({self.owner!r}, {self.money})"


def pay(wallet, amount):
    wallet.money -= amount            # changes the caller's object


def replace(wallet):
    wallet = Wallet("Someone", 0)     # only rebinds the local name
    return wallet


a = Wallet("Asha", 500)
b = Wallet("Ravi", 300)
pay(a, 250)
print("  after pay(a, 250):", a)
replace(a)
print("  after replace(a):", a, "(unchanged)")

print("\n=== 2. Objects as return values ===")


def richer(w1, w2):
    return w1 if w1.money >= w2.money else w2


def make_wallet(name):
    return Wallet(name, 0)


winner = richer(a, b)
print("  richer:", winner.owner, "| winner is b:", winner is b)
new = make_wallet("Dev")
print("  make_wallet:", new)

print("\n=== 3. A list of objects ===")


class Employee:
    def __init__(self, emp_id, name, dept, salary):
        self.emp_id, self.name, self.dept, self.salary = emp_id, name, dept, salary

    def raise_salary(self, percent):
        self.salary = round(self.salary * (1 + percent / 100))

    def __repr__(self):
        return f"{self.name}({self.dept}, {self.salary})"


staff = [
    Employee(101, "Asha", "IT", 60000),
    Employee(102, "Ravi", "HR", 45000),
    Employee(103, "Dev", "IT", 70000),
    Employee(104, "Meena", "Sales", 52000),
]
for e in staff:
    print(f"  {e.name:<6}{e.dept:<6}{e.salary:>7}")
print("  IT team :", [e.name for e in staff if e.dept == "IT"])
print("  payroll :", sum(e.salary for e in staff), "| average:", sum(e.salary for e in staff) / len(staff))
print("  top     :", max(staff, key=lambda e: e.salary).name)
print("  by name :", sorted(staff, key=lambda e: e.name))
by_dept = {}
for e in staff:
    by_dept.setdefault(e.dept, []).append(e.name)
print("  grouped :", by_dept)
by_id = {e.emp_id: e for e in staff}
print("  lookup 103:", by_id[103])
for e in staff:
    if e.dept == "IT":
        e.raise_salary(10)
print("  after 10% IT raise, payroll:", sum(e.salary for e in staff))

print("\n=== 4. Identity, equality, aliasing ===")


class Coin:
    def __init__(self, value):
        self.value = value


c1, c2 = Coin(5), Coin(5)
c3 = c1
print("  c1 == c2:", c1 == c2, "| c1 is c2:", c1 is c2, "| c1 is c3:", c1 is c3)
c3.value = 10
print("  changed through the alias c3 -> c1.value =", c1.value)
print("  compare data instead:", c1.value == c2.value)

print("\n=== 5. Shallow vs deep copy ===")


class Basket:
    def __init__(self, owner, items):
        self.owner = owner
        self.items = items


orig = Basket("Asha", ["pen", "book"])
shallow = copy.copy(orig)
deep = copy.deepcopy(orig)
shallow.owner = "Ravi"                 # outer attribute: independent
shallow.items.append("lamp")           # inner list: SHARED with orig!
deep.items.append("desk")              # fully independent
print("  orig   :", orig.owner, orig.items)
print("  shallow:", shallow.owner, shallow.items, "| shares list with orig:", shallow.items is orig.items)
print("  deep   :", deep.owner, deep.items, "| shares list with orig:", deep.items is orig.items)

print("\n=== 6. Objects inside objects (composition) ===")


class Address:
    def __init__(self, city, pin):
        self.city, self.pin = city, pin

    def __repr__(self):
        return f"{self.city} - {self.pin}"


class Customer:
    def __init__(self, name, address):
        self.name = name
        self.address = address

    def move(self, city, pin):
        self.address = Address(city, pin)

    def __repr__(self):
        return f"Customer({self.name}, {self.address})"


cust = Customer("Asha", Address("Pune", "411001"))
print("  chained dots:", cust.address.city)
cust.move("Delhi", "110001")
print("  after move  :", cust)
