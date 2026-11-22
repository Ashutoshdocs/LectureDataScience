"""Lecture 12: Getter & setter methods, validation, read-only data, _protected and __private."""

print("=== 1. The problem: no protection ===")


class OpenAccount:
    def __init__(self, balance):
        self.balance = balance


acc = OpenAccount(1000)
acc.balance = -5000
print("  balance set to", acc.balance, "-> nothing stopped it")

print("\n=== 2. Getters & setters ===")


class Account:
    def __init__(self, owner, balance=0):
        self._owner = owner
        self._balance = 0
        self._history = []
        self.set_balance(balance)           # constructor reuses the setter's checks

    # ---- getters ----
    def get_balance(self):
        return self._balance

    def get_owner(self):                    # read-only: no set_owner
        return self._owner

    def get_balance_usd(self, rate=84.0):   # computed getter
        return round(self._balance / rate, 2)

    def get_history(self):
        return list(self._history)          # a COPY protects the internal list

    # ---- setter ----
    def set_balance(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("balance must be a number")
        if value < 0:
            raise ValueError("balance cannot be negative")
        self._history.append((self._balance, value))
        self._balance = value

    # ---- normal methods built on the setter ----
    def deposit(self, amount):
        self.set_balance(self._balance + amount)

    def withdraw(self, amount):
        self.set_balance(self._balance - amount)


a = Account("Asha", 1000)
a.deposit(500)
a.withdraw(200)
print("  owner:", a.get_owner(), "| balance:", a.get_balance(), "| in USD:", a.get_balance_usd())
for bad in [-50, "lots"]:
    try:
        a.set_balance(bad)
    except (ValueError, TypeError) as e:
        print(f"  set_balance({bad!r}) -> {type(e).__name__}: {e}")
try:
    a.withdraw(5000)
except ValueError as e:
    print("  withdraw(5000) ->", e)
print("  history (old, new):", a.get_history())
copy = a.get_history()
copy.clear()
print("  clearing the returned copy doesn't touch the real history:", len(a.get_history()), "entries")
print("  no setter for owner:", hasattr(a, "set_owner"))

print("\n=== 3. _protected is only a convention ===")
a._balance = -1                                # allowed, but you broke the rules
print("  a._balance =", a._balance, "-> possible, but you bypassed the validation")

print("\n=== 4. __private and name mangling ===")


class Safe:
    def __init__(self, code):
        self.__code = code                     # stored as _Safe__code

    def check(self, guess):
        return guess == self.__code            # inside the class, __code works normally


s = Safe(1234)
print("  s.__dict__ =", s.__dict__)
try:
    s.__code
except AttributeError as e:
    print("  s.__code ->", e)
print("  s._Safe__code =", s._Safe__code, "(still reachable: not real security)")
print("  s.check(1234) =", s.check(1234))
s.__code = 9999                                # creates a NEW unrelated attribute
print("  after s.__code = 9999 ->", s.__dict__, "| check(1234) still:", s.check(1234))

print("\n=== 5. Getter/setter methods make calling code noisy ===")
b = Account("Ravi", 300)
b.set_balance(b.get_balance() + 500)
print("  b.set_balance(b.get_balance() + 500) ->", b.get_balance())
print("  Lecture 13: @property lets you write b.balance += 500 with the same validation.")
