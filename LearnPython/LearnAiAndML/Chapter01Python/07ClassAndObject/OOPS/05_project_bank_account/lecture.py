"""Lecture 05: Project: a bank account that enforces its own rules and keeps a history."""
import datetime as dt


class BankAccount:
    bank_name = "Python Bank"
    MIN_BALANCE = 0
    DAILY_LIMIT = 25_000
    _next_number = 1001

    def __init__(self, owner, opening_balance=0):
        if not owner:
            raise ValueError("owner is required")
        self.number = f"ACC-{BankAccount._next_number}"
        BankAccount._next_number += 1
        self.owner = owner
        self.balance = 0
        self.transactions = []
        if opening_balance:
            self.deposit(opening_balance, note="opening balance")

    # ---------- helpers ----------
    def _check_amount(self, amount):
        if not isinstance(amount, (int, float)) or isinstance(amount, bool):
            raise ValueError(f"amount must be a number, got {amount!r}")
        if amount <= 0:
            raise ValueError(f"amount must be positive, got {amount}")

    def _record(self, kind, amount, note=""):
        self.transactions.append({"date": dt.date.today(), "kind": kind, "amount": amount,
                                  "balance": self.balance, "note": note})

    # ---------- queries ----------
    def withdrawn_today(self):
        today = dt.date.today()
        return sum(t["amount"] for t in self.transactions
                   if t["kind"] == "withdraw" and t["date"] == today)

    def statement(self):
        lines = [f"  {self.bank_name} | {self.number} | {self.owner}"]
        for t in self.transactions:
            sign = "+" if t["kind"] == "deposit" else "-"
            lines.append(f"    {t['kind']:<9}{sign}{t['amount']:>9,}  bal {t['balance']:>9,}  {t['note']}")
        lines.append(f"    {'balance':<9}{self.balance:>10,}")
        return "\n".join(lines)

    # ---------- commands ----------
    def deposit(self, amount, note=""):
        self._check_amount(amount)
        self.balance += amount
        self._record("deposit", amount, note)
        return self.balance

    def withdraw(self, amount, note=""):
        self._check_amount(amount)
        if self.balance - amount < self.MIN_BALANCE:
            raise ValueError(f"insufficient funds: balance {self.balance:,}, requested {amount:,}")
        if self.withdrawn_today() + amount > self.DAILY_LIMIT:
            left = self.DAILY_LIMIT - self.withdrawn_today()
            raise ValueError(f"daily limit {self.DAILY_LIMIT:,} reached; you can withdraw {left:,} more today")
        self.balance -= amount
        self._record("withdraw", amount, note)
        return self.balance

    def transfer(self, to, amount):
        if not isinstance(to, BankAccount) or to is self:
            raise ValueError("transfer needs a different BankAccount")
        self.withdraw(amount, note=f"to {to.number}")        # if this fails, nothing moves
        to.deposit(amount, note=f"from {self.number}")


def attempt(label, func, *args):
    try:
        result = func(*args)
        print(f"  ✔ {label:<32} -> balance {result:,}" if isinstance(result, (int, float)) else f"  ✔ {label}")
    except ValueError as e:
        print(f"  ✘ {label:<32} -> {e}")


def main():
    asha = BankAccount("Asha", 10_000)
    ravi = BankAccount("Ravi")
    print(f"=== Opened {asha.number} (Asha) and {ravi.number} (Ravi) at {BankAccount.bank_name} ===")

    print("\n=== Transactions with rules enforced ===")
    attempt("Asha deposits 5,000", asha.deposit, 5_000)
    attempt("Asha deposits -50", asha.deposit, -50)
    attempt("Asha deposits '100'", asha.deposit, "100")
    attempt("Asha withdraws 20,000", asha.withdraw, 20_000)
    attempt("Asha withdraws 12,000", asha.withdraw, 12_000)
    attempt("Ravi deposits 40,000", ravi.deposit, 40_000)
    attempt("Ravi withdraws 20,000", ravi.withdraw, 20_000)
    attempt("Ravi withdraws 8,000 (limit)", ravi.withdraw, 8_000)
    attempt("Asha -> Ravi transfer 2,000", asha.transfer, ravi, 2_000)
    attempt("Asha -> Ravi transfer 9,000", asha.transfer, ravi, 9_000)
    attempt("Asha -> Asha transfer", asha.transfer, asha, 10)

    print("\n=== Statements ===")
    print(asha.statement())
    print(ravi.statement())

    print("\n=== Shared vs per-account data ===")
    print("  class attrs :", BankAccount.bank_name, "| DAILY_LIMIT", BankAccount.DAILY_LIMIT,
          "| next number", BankAccount._next_number)
    print("  asha attrs  :", sorted(vars(asha)))


if __name__ == "__main__":
    main()
