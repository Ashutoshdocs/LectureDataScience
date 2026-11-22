"""Lecture 06: Encapsulation: public, _protected, __private, name mangling, public interface."""

print("=== 1. Three access levels ===")


class Account:
    def __init__(self, owner, pin):
        self.owner = owner          # public
        self._branch = "Pune"       # protected (convention)
        self.__pin = pin            # private (name-mangled)
        self.__attempts = 0

    def check_pin(self, guess):
        if self.__attempts >= 3:
            return "LOCKED"
        ok = guess == self.__pin
        self.__attempts = 0 if ok else self.__attempts + 1
        return ok

    def change_pin(self, old, new):
        if self.check_pin(old) is not True:
            raise PermissionError("old PIN is wrong")
        if not (isinstance(new, int) and 1000 <= new <= 9999):
            raise ValueError("new PIN must be 4 digits")
        self.__pin = new


acc = Account("Ravi", 4321)
print("  acc.owner  :", acc.owner)
print("  acc._branch:", acc._branch, "(readable - underscore is only a 'please don't')")
try:
    print(acc.__pin)
except AttributeError as e:
    print("  acc.__pin  -> AttributeError:", e)
print("  acc.__dict__:", acc.__dict__)
print("  acc._Account__pin:", acc._Account__pin, "(possible, but you shouldn't)")

print("\n=== 2. Use the public interface ===")
print("  check_pin(1111), check_pin(4321):", acc.check_pin(1111), acc.check_pin(4321))
acc.change_pin(4321, 5555)
print("  after change_pin, check_pin(5555):", acc.check_pin(5555))
for args in [(1111, 2222), (5555, 12)]:
    try:
        acc.change_pin(*args)
    except (PermissionError, ValueError) as e:
        print(f"  change_pin{args} -> {type(e).__name__}: {e}")
print("  three wrong guesses:", [acc.check_pin(0) for _ in range(4)])

print("\n=== 3. Why name mangling exists: no clashes in subclasses ===")


class Parent:
    def __init__(self):
        self.__secret = "parent's"
        self._shared = "parent's"

    def parent_secret(self):
        return self.__secret


class Child(Parent):
    def __init__(self):
        super().__init__()
        self.__secret = "child's"     # becomes _Child__secret: no clash
        self._shared = "child's"      # overwrites the parent's value


c = Child()
print("  c.__dict__:", c.__dict__)
print("  parent's method still sees its own secret:", c.parent_secret())
print("  _shared was overwritten (single underscore = no protection):", c._shared)

print("\n=== 4. Dunder names (__init__) are NOT mangled ===")
print("  '__init__' in Account.__dict__:", "__init__" in Account.__dict__)
print("  '_Account__init__' in Account.__dict__:", "_Account__init__" in Account.__dict__)

print("\n=== 5. Hide internals, return copies ===")


class Wallet:
    def __init__(self):
        self._transactions = []
        self._balance = 0

    def add(self, amount):
        self._validate(amount)
        self._transactions.append(amount)
        self._balance += amount

    def history(self):
        return list(self._transactions)        # a copy: callers can't tamper

    def balance(self):
        return self._balance

    def _validate(self, amount):
        if amount <= 0:
            raise ValueError("amount must be positive")


w = Wallet()
w.add(100)
w.add(50)
h = w.history()
h.append(1_000_000)                             # changes only the copy
print("  tampered copy:", h)
print("  real history :", w.history(), "| balance:", w.balance())
public = [n for n in dir(w) if not n.startswith("_")]
print("  public interface of Wallet:", public)
