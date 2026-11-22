"""Lecture 21: Project: library manager (ABC, inheritance, polymorphism, composition, dataclass, exceptions)."""
import datetime as dt
from abc import ABC, abstractmethod
from dataclasses import dataclass, field


# ---------- custom exceptions ----------
class LibraryError(Exception):
    """Base class for all library errors."""


class NotAvailable(LibraryError):
    pass


class LimitReached(LibraryError):
    pass


class UnpaidFines(LibraryError):
    pass


# ---------- items ----------
class Item(ABC):
    _next_id = 1

    def __init__(self, title):
        if not title:
            raise ValueError("title is required")
        self.item_id = f"{self.PREFIX}{Item._next_id:03d}"
        Item._next_id += 1
        self.title = title
        self._available = True

    @property
    def available(self):
        return self._available

    @abstractmethod
    def loan_days(self):
        ...

    @abstractmethod
    def fine_per_day(self):
        ...

    def _check_out(self):
        if not self._available:
            raise NotAvailable(f"{self.title!r} is already on loan")
        self._available = False

    def _check_in(self):
        self._available = True

    def __repr__(self):
        return f"{type(self).__name__}({self.item_id}, {self.title!r})"


class Book(Item):
    PREFIX = "B"

    def __init__(self, title, author):
        super().__init__(title)
        self.author = author

    def loan_days(self):
        return 14

    def fine_per_day(self):
        return 2


class DVD(Item):
    PREFIX = "D"

    def loan_days(self):
        return 3

    def fine_per_day(self):
        return 10


class Magazine(Item):
    PREFIX = "M"

    def loan_days(self):
        return 7

    def fine_per_day(self):
        return 1


# ---------- members ----------
class Member:
    LIMIT = 3

    def __init__(self, name):
        if not name or not name.strip():
            raise ValueError("member name is required")
        self.name = name.strip().title()
        self._loans = []
        self.fines_due = 0

    @property
    def borrowed(self):
        return [loan.item for loan in self._loans]          # a copy, not the internal list

    def fine_for(self, loan, today):
        return loan.days_late(today) * loan.item.fine_per_day()

    def can_borrow(self):
        if self.fines_due:
            raise UnpaidFines(f"{self.name} owes Rs {self.fines_due}")
        if len(self._loans) >= self.LIMIT:
            raise LimitReached(f"{self.name} already has {self.LIMIT} items")

    def pay(self, amount):
        self.fines_due = max(0, self.fines_due - amount)

    def __repr__(self):
        return f"{type(self).__name__}({self.name!r})"


class PremiumMember(Member):
    LIMIT = 6

    def fine_for(self, loan, today):
        return 0                                             # premium perk


# ---------- loan record ----------
@dataclass
class Loan:
    item: Item
    member: Member
    issued: dt.date
    returned: dt.date | None = field(default=None)

    @property
    def due(self):
        return self.issued + dt.timedelta(days=self.item.loan_days())

    def days_late(self, today):
        end = self.returned or today
        return max(0, (end - self.due).days)


# ---------- library (composition) ----------
class Library:
    def __init__(self, name):
        self.name = name
        self._items = {}
        self._members = {}
        self._loans = []

    def add_item(self, item):
        self._items[item.item_id] = item
        return item

    def join(self, member):
        self._members[member.name] = member
        return member

    def issue(self, item, member, today):
        member.can_borrow()
        item._check_out()
        loan = Loan(item, member, today)
        member._loans.append(loan)
        self._loans.append(loan)
        return loan

    def give_back(self, item, today):
        loan = next((l for l in self._loans if l.item is item and l.returned is None), None)
        if loan is None:
            raise LibraryError(f"{item.title!r} is not on loan")
        loan.returned = today
        fine = loan.member.fine_for(loan, today)
        loan.member.fines_due += fine
        loan.member._loans.remove(loan)
        item._check_in()
        return fine

    def search(self, *, text="", kind=None, available_only=False):
        return [i for i in self._items.values()
                if text.lower() in i.title.lower()
                and (kind is None or isinstance(i, kind))
                and (not available_only or i.available)]

    def __len__(self):
        return len(self._items)

    def __contains__(self, title):
        return any(i.title.lower() == title.lower() for i in self._items.values())

    def report(self, today):
        print(f"  {'ID':<5}{'Type':<9}{'Title':<24}{'Status':<26}")
        for item in self._items.values():
            loan = next((l for l in self._loans if l.item is item and l.returned is None), None)
            status = "available" if loan is None else f"{loan.member.name}, due {loan.due:%d %b}" + (
                f" (LATE {loan.days_late(today)}d)" if loan.days_late(today) else "")
            print(f"  {item.item_id:<5}{type(item).__name__:<9}{item.title:<24}{status}")


def attempt(label, func, *args, **kwargs):
    try:
        result = func(*args, **kwargs)
        print(f"  ✔ {label:<38}" + (f" fine Rs {result}" if isinstance(result, int) else ""))
    except LibraryError as e:
        print(f"  ✘ {label:<38} {type(e).__name__}: {e}")


def main():
    lib = Library("City Library")
    clean_code = lib.add_item(Book("Clean Code", "Robert Martin"))
    crash = lib.add_item(Book("Python Crash Course", "Eric Matthes"))
    ocean = lib.add_item(DVD("Ocean Life"))
    wired = lib.add_item(Magazine("Wired Nov 2026"))
    lib.add_item(Book("Fluent Python", "Luciano Ramalho"))
    asha = lib.join(Member("asha"))
    ravi = lib.join(PremiumMember("ravi"))

    day1 = dt.date(2026, 11, 1)
    print(f"=== {lib.name}: {len(lib)} items, members {list(lib._members.values())} ===")
    print("  'clean code' in lib:", "clean code" in lib)

    print("\n=== 1 Nov: borrowing ===")
    attempt("Asha borrows Clean Code", lib.issue, clean_code, asha, day1)
    attempt("Asha borrows Ocean Life", lib.issue, ocean, asha, day1)
    attempt("Ravi borrows Clean Code", lib.issue, clean_code, ravi, day1)
    attempt("Asha borrows Wired", lib.issue, wired, asha, day1)
    attempt("Asha borrows Python Crash Course", lib.issue, crash, asha, day1)
    attempt("Ravi borrows Python Crash Course", lib.issue, crash, ravi, day1)
    print("  Asha has:", asha.borrowed)

    print("\n=== Report on 10 Nov ===")
    lib.report(dt.date(2026, 11, 10))

    print("\n=== 10 Nov: returns and fines ===")
    attempt("Asha returns Ocean Life (DVD)", lib.give_back, ocean, dt.date(2026, 11, 10))
    attempt("Asha returns Wired (on time)", lib.give_back, wired, dt.date(2026, 11, 8))
    attempt("Asha borrows Ocean Life again", lib.issue, ocean, asha, dt.date(2026, 11, 10))
    print(f"  Asha owes Rs {asha.fines_due} and pays it")
    asha.pay(asha.fines_due)
    attempt("Asha borrows Ocean Life again", lib.issue, ocean, asha, dt.date(2026, 11, 10))
    attempt("Ravi (premium) returns 20 days late", lib.give_back, crash, dt.date(2026, 12, 5))
    attempt("return Fluent Python (not on loan)", lib.give_back, lib.search(text="fluent")[0], day1)

    print("\n=== Search with keyword-only filters ===")
    print("  books        :", lib.search(kind=Book))
    print("  available    :", lib.search(available_only=True))
    print("  text 'python':", lib.search(text="python"))

    print("\n=== Polymorphism: same calls, different rules ===")
    for item in (clean_code, ocean, wired):
        print(f"  {type(item).__name__:<9} loan {item.loan_days():>2} days, fine Rs {item.fine_per_day():>2}/day")
    try:
        Item("generic")
    except TypeError as e:
        print("  Item('generic') -> TypeError:", e)
    try:
        clean_code.available = True
    except AttributeError as e:
        print("  clean_code.available = True ->", e)


if __name__ == "__main__":
    main()
