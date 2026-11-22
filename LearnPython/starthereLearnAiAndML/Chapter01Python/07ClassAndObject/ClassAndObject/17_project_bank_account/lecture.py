"""Lecture 17: Project: a BankAccount class that uses every kind of function."""


class BankAccount:
    # ---------------- class attributes ----------------
    bank_name = "PyBank"
    min_balance = 100
    interest_rate = 4.0
    _next_number = 1001
    _accounts = []

    # ---------------- constructor ----------------
    def __init__(self, owner, balance=0):
        self.owner = owner                                  # validated by the property setter
        if not BankAccount.valid_amount(balance, allow_zero=True):
            raise ValueError("opening balance must be a non-negative number")
        self._balance = balance
        self._history = []                                  # per-object list: created HERE
        self._account_no = BankAccount._next_number
        BankAccount._next_number += 1
        BankAccount._accounts.append(self)
        self._open = True
        self._record("open", balance)
        print(f"  [opened] #{self._account_no} for {self.owner} with {self.rupees(balance)}")

    # ---------------- properties ----------------
    @property
    def balance(self):                                      # read-only
        return self._balance

    @property
    def account_no(self):                                   # read-only
        return self._account_no

    @property
    def owner(self):
        return self._owner

    @owner.setter
    def owner(self, name):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("owner name cannot be empty")
        self._owner = name.strip().title()

    # ---------------- instance methods ----------------
    def deposit(self, amount):
        if not self.valid_amount(amount):
            raise ValueError(f"invalid deposit: {amount!r}")
        self._balance += amount
        self._record("deposit", amount)
        return self

    def withdraw(self, amount):
        if not self.valid_amount(amount):
            raise ValueError(f"invalid withdrawal: {amount!r}")
        if self._balance - amount < BankAccount.min_balance:
            print(f"  [refused] {self.owner}: withdrawing {self.rupees(amount)} would go below "
                  f"the minimum {self.rupees(BankAccount.min_balance)}")
            return False
        self._balance -= amount
        self._record("withdraw", amount)
        return True

    def transfer_to(self, other, amount):
        print(f"  [transfer] {self.owner} -> {other.owner}: {self.rupees(amount)}")
        if self.withdraw(amount):
            other.deposit(amount)
            return True
        return False

    def add_interest(self):
        interest = round(self._balance * BankAccount.interest_rate / 100, 2)
        self._balance = round(self._balance + interest, 2)
        self._record("interest", interest)

    def statement(self):
        print(f"  Statement #{self._account_no} - {self.owner}")
        for kind, amount, after in self._history:
            print(f"    {kind:<9}{self.rupees(amount):>14}  -> balance {self.rupees(after)}")

    def _record(self, kind, amount):                       # internal helper
        self._history.append((kind, amount, self._balance))

    def close(self):
        if getattr(self, "_open", False):
            self._open = False
            print(f"  [closed] #{self._account_no} ({self.owner})")

    # ---------------- class methods ----------------
    @classmethod
    def from_csv(cls, line):
        name, amount = line.split(",")
        return cls(name, float(amount))

    @classmethod
    def total_accounts(cls):
        return len(cls._accounts)

    @classmethod
    def find(cls, number):
        return next((a for a in cls._accounts if a.account_no == number), None)

    @classmethod
    def set_interest_rate(cls, rate):
        cls.interest_rate = rate

    # ---------------- static methods ----------------
    @staticmethod
    def valid_amount(x, allow_zero=False):
        return isinstance(x, (int, float)) and (x >= 0 if allow_zero else x > 0)

    @staticmethod
    def rupees(x):
        return f"Rs {x:,.2f}"

    # ---------------- special methods ----------------
    def __str__(self):
        return f"{self.owner} (#{self._account_no}): {self.rupees(self._balance)}"

    def __repr__(self):
        return f"BankAccount({self.owner!r}, {self._balance})"

    def __eq__(self, other):
        return isinstance(other, BankAccount) and self._account_no == other._account_no

    def __hash__(self):
        return hash(self._account_no)

    def __lt__(self, other):
        return self._balance < other._balance

    def __len__(self):
        return len(self._history)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()
        return False

    def __del__(self):
        self.close()


# ---------------- global function ----------------
def total_deposits(accounts):
    return sum(amount for acc in accounts for kind, amount, _ in acc._history if kind == "deposit")


def main():
    print("=== Open accounts (constructor + class method factory) ===")
    asha = BankAccount("asha", 1000)
    ravi = BankAccount("Ravi")
    dev = BankAccount.from_csv("dev,2500")

    print("\n=== Validation ===")
    for bad in [("", 100), ("Meena", -5)]:
        try:
            BankAccount(*bad)
        except ValueError as e:
            print(f"  BankAccount{bad} -> {e}")
    try:
        asha.balance = 1_000_000
    except AttributeError as e:
        print("  asha.balance = 1_000_000 ->", e)
    try:
        asha.deposit(-50)
    except ValueError as e:
        print("  asha.deposit(-50) ->", e)

    print("\n=== Transactions (instance methods) ===")
    asha.transfer_to(ravi, 300)
    ravi.transfer_to(asha, 500)
    dev.withdraw(2450)
    asha.deposit(200).deposit(50)                          # chaining: deposit returns self

    print("\n=== Class-wide operations ===")
    BankAccount.set_interest_rate(4.0)
    for acc in (asha, ravi, dev):
        acc.add_interest()
    print("  accounts at", BankAccount.bank_name, ":", BankAccount.total_accounts())
    print("  find(1002):", BankAccount.find(1002))

    print("\n=== Special methods ===")
    for acc in sorted([asha, ravi, dev]):                  # __lt__
        print("  ", acc)                                   # __str__
    print("  repr list:", [asha, ravi])                    # __repr__
    print("  transactions in asha (len):", len(asha))     # __len__
    print("  asha == find(1001):", asha == BankAccount.find(1001))   # __eq__
    print("  richest:", max([asha, ravi, dev]).owner)

    print("\n=== Statement & global report ===")
    asha.statement()
    print("  total deposits across all accounts:", BankAccount.rupees(total_deposits([asha, ravi, dev])))

    print("\n=== Context manager & destructor ===")
    with BankAccount("Temp User", 500) as temp:
        temp.deposit(100)
        print("  inside with:", temp)
    print("  after with: closed already")
    asha.close()
    print("  end of main(): remaining objects are closed when they're destroyed")


if __name__ == "__main__":
    main()
    BankAccount._accounts.clear()                          # drop the registry's references
