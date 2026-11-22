"""Lecture 00: Why OOP? Everything is an object; procedural vs OOP side by side."""

print("=== 1. Everything in Python is already an object ===")
for value in [5, 3.14, "hi", [1, 2], {"a": 1}, len]:
    print(f"  {value!r:<12} type={type(value).__name__:<22} has {len(dir(value))} attributes/methods")
name = "asha"
print("  'asha'.upper() ->", name.upper(), "| 'asha'.title() ->", name.title())
nums = [3, 1, 2]
nums.sort()
print("  list method .sort() changed the list itself:", nums)

print("\n=== 2. Procedural version: dicts + functions ===")
acc1 = {"owner": "Asha", "balance": 1000}


def deposit(acc, amount):
    acc["balance"] += amount


def withdraw(acc, amount):
    if amount > acc["balance"]:
        print("  Insufficient funds")
        return
    acc["balance"] -= amount


deposit(acc1, 500)
withdraw(acc1, 5000)
print("  after deposit/withdraw:", acc1)
acc1["balance"] = -99999                     # nothing stops this
acc1["balence"] = 0                          # typo -> silently adds a new key
print("  rules bypassed + typo  :", acc1)

print("\n=== 3. OOP version: data + behaviour + rules together ===")


class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self._balance = balance

    @property
    def balance(self):                       # read-only from outside (Lecture 07)
        return self._balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("deposit must be positive")
        self._balance += amount

    def withdraw(self, amount):
        if amount > self._balance:
            print("  Insufficient funds")
            return
        self._balance -= amount

    def __repr__(self):
        return f"BankAccount({self.owner!r}, balance={self._balance})"


acc = BankAccount("Asha", 1000)
acc.deposit(500)
acc.withdraw(5000)
print("  after deposit/withdraw:", acc)
try:
    acc.balance = -99999
except AttributeError as e:
    print("  acc.balance = -99999 ->", type(e).__name__, ":", e)
try:
    acc.deposit(-10)
except ValueError as e:
    print("  acc.deposit(-10)      -> ValueError:", e)

print("\n=== 4. Many objects, one blueprint ===")
accounts = [BankAccount("Asha", 100), BankAccount("Ravi", 250), BankAccount("Dev")]
for a in accounts:
    a.deposit(50)
print("  ", accounts)
print("  each object is separate:", accounts[0] is not accounts[1])

print("\n=== 5. Your class is a type, just like str or list ===")
print("  type(acc)     :", type(acc))
print("  type(acc).__name__ == 'BankAccount':", type(acc).__name__ == "BankAccount")
print("  isinstance(acc, BankAccount):", isinstance(acc, BankAccount))
print("  isinstance('hi', str)       :", isinstance("hi", str))
