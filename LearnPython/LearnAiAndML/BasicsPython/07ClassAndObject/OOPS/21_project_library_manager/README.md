# Lecture 21: Project: library manager

Run: `python lecture.py`

A small library system. Members borrow books, DVDs and magazines, items have different loan periods and late fines, and the library produces reports.

## Class design

```
            Item (ABC)                         Library ──has many──▶ Item
     ┌──────────┼───────────┐                    │
   Book        DVD       Magazine                ├──has many──▶ Member ──has many──▶ Loan
  14 days     3 days      7 days                 └──has many──▶ Loan
  Rs 2/day   Rs 10/day   Rs 1/day                                  └──refers to──▶ Item, Member
```

| Class | Responsibility | OOP features |
|-------|----------------|--------------|
| `Item` (ABC) | common data (`item_id`, `title`), availability, the fine formula | abstraction (`loan_days`, `fine_per_day` abstract), encapsulation (`_available` + read-only property), class-level ID counter |
| `Book`, `DVD`, `Magazine` | their own loan rules | inheritance, polymorphism (`loan_days()` differs), `super().__init__` for extra fields |
| `Member` | name, limit, current loans | encapsulation (a `borrowed` property that returns a copy), validation |
| `PremiumMember(Member)` | higher limit, no fines | overriding a class attribute and a method |
| `Loan` (dataclass) | item + member + dates; `due`, `days_late`, `fine` | `@dataclass`, computed properties |
| `Library` | catalogue, members, issuing and returns, reports | composition, custom exceptions, `__len__`, `__contains__`, `search` with keyword-only filters |
| `LibraryError` and subclasses | clear, catchable errors | custom exception hierarchy |

## Business rules

1. An item can be on loan to only one member at a time.
2. Members have a loan limit (normal 3, premium 6).
3. A member with unpaid fines can't borrow.
4. Fine = days late × the item's fine per day (premium members pay nothing).
5. Returning an item records the fine on the member's account.

## What to look for in the code

- `Library.issue()` never checks `isinstance(item, Book)`. It asks the item `item.loan_days()`: **polymorphism**.
- `PremiumMember` changes behaviour only by overriding `LIMIT` and `fine_for()`: **minimal overriding**.
- Dates are passed in (`today=`), so the demo is repeatable and testable: **dependency injection**.

## Extension exercises

1. Add `EBook(Item)` that can be borrowed by several members at once (override `_available` logic).
2. Add reservations: a queue of members waiting for an item.
3. Save and load the library to JSON with `asdict` and alternative constructors.
4. Add `Library.overdue_report(today)`.

**Next →** [Lecture 22: Project: payment system](../22_project_payment_system/)
