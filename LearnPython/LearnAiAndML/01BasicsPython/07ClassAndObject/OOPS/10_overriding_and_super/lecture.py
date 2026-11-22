"""Lecture 10: Overriding (replace vs extend), super(), the __init__ rule, overriding by class attribute."""

print("=== 1. Replace vs extend ===")


class Employee:
    bonus_rate = 0.10

    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def describe(self):
        return f"{self.name} earns {self.salary:,}"

    def annual_bonus(self):
        return round(self.salary * 12 * self.bonus_rate)


class Intern(Employee):
    bonus_rate = 0                                   # override a class attribute only

    def describe(self):                              # REPLACE completely
        return f"{self.name} is an intern"


class Manager(Employee):
    bonus_rate = 0.20

    def __init__(self, name, salary, team):
        super().__init__(name, salary)               # parent sets name & salary
        self.team = team                             # child adds team

    def describe(self):                              # EXTEND
        return super().describe() + f" and manages {self.team} people"


class Director(Manager):
    def describe(self):
        return super().describe() + " (director)"   # extends Manager, which extends Employee


staff = [Employee("Asha", 50000), Intern("Kiran", 15000), Manager("Ravi", 90000, 5), Director("Meena", 150000, 40)]
for s in staff:
    print(f"  {type(s).__name__:<9} {s.describe():<60} bonus {s.annual_bonus():>9,}")

print("\n=== 2. Which describe() runs? ===")
for cls in (Employee, Intern, Manager, Director):
    owner = next(c.__name__ for c in cls.__mro__ if "describe" in c.__dict__)
    print(f"  {cls.__name__:<9} uses the describe() defined in {owner}")

print("\n=== 3. Forgetting super().__init__ ===")


class BrokenManager(Employee):
    def __init__(self, name, salary, team):
        self.team = team                             # parent setup never runs


bm = BrokenManager("Dev", 80000, 3)
print("  bm.__dict__:", bm.__dict__)
try:
    bm.describe()
except AttributeError as e:
    print("  bm.describe() -> AttributeError:", e)


class NoInit(Employee):
    pass                                             # no __init__ -> parent's is used


print("  child without its own __init__ uses the parent's:", NoInit("Zara", 30000).describe())

print("\n=== 4. Extending a rule: SavingsAccount ===")


class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner, self.balance = owner, balance

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("insufficient funds")
        self.balance -= amount
        return self.balance


class SavingsAccount(BankAccount):
    MIN_BALANCE = 500

    def __init__(self, owner, balance=0, rate=0.04):
        super().__init__(owner, balance)
        self.rate = rate

    def withdraw(self, amount):                      # same signature as the parent
        if self.balance - amount < self.MIN_BALANCE:
            raise ValueError(f"must keep a minimum of {self.MIN_BALANCE}")
        return super().withdraw(amount)              # the parent does the real work

    def add_interest(self):
        self.balance = round(self.balance * (1 + self.rate), 2)
        return self.balance


accounts = [BankAccount("Asha", 1000), SavingsAccount("Ravi", 1000)]
for acc in accounts:                                 # same code works for both (substitution)
    for amount in (400, 400):
        try:
            print(f"  {type(acc).__name__:<14} withdraw {amount} -> balance {acc.withdraw(amount)}")
        except ValueError as e:
            print(f"  {type(acc).__name__:<14} withdraw {amount} -> refused: {e}")
print("  Ravi after interest:", accounts[1].add_interest())

print("\n=== 5. super() vs hard-coding the parent ===")


class Base:
    def hello(self):
        return "Base"


class Middle(Base):
    def hello(self):
        return "Middle>" + super().hello()


class Leaf(Middle):
    def hello(self):
        return "Leaf>" + super().hello()


print("  Leaf().hello():", Leaf().hello(), "- each class hands on to the next with super()")
