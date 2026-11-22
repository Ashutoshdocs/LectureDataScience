# Lecture 17: Project: a bank account using every function type

Run: `python lecture.py`

One class, `BankAccount`, that uses **everything** from this course, with each function placed in the kind that fits the data it needs.

## Design

| Feature | Kind | Why |
|---------|------|-----|
| `bank_name`, `min_balance`, `interest_rate`, `_next_number`, `_accounts` | **class attributes** | shared by every account |
| `__init__(owner, balance=0)` | **constructor** | validates owner & opening balance, assigns an account number, registers the account |
| `balance` | **read-only `@property`** | readable by anyone, changed only through deposit/withdraw |
| `owner` | **`@property` + setter** | can be corrected, but must be a non-empty name |
| `account_no` | **read-only property** | never changes after creation |
| `deposit`, `withdraw`, `statement` | **instance methods** | work on *this* account's data |
| `transfer_to(other, amount)` | **instance method** with another object | moves money between two accounts |
| `_record(kind, amount)` | **"internal" instance method** (leading `_`) | helper used only inside the class |
| `from_csv(line)` | **class method (factory)** | builds an account from `"Dev,2500"` |
| `total_accounts()`, `find(number)`, `set_interest_rate(r)` | **class methods** | class-wide data |
| `valid_amount(x)`, `rupees(x)` | **static methods** | validation & formatting helpers |
| `__str__`, `__repr__`, `__eq__`, `__lt__`, `__len__` | **special methods** | printing, comparing by balance, `len()` = number of transactions |
| `__enter__`, `__exit__`, `close()`, `__del__` | **context manager + destructor** | safe closing |
| `total_deposits(accounts)` | **global function** | a report over many accounts |

## Rules the class enforces

1. Opening balance can't be negative; owner can't be empty.
2. Every amount must be a positive number (static `valid_amount`).
3. A withdrawal can't take the balance below `min_balance`.
4. `balance` can't be assigned directly, only changed via `deposit` / `withdraw`.
5. Every change is recorded in a per-account `_history` list (created in `__init__`, never in the class body).

## Follow the money

```
Asha opens with 1000, Ravi with 0, Dev via from_csv("Dev,2500")
Asha → Ravi  300      ✅  Asha 700,  Ravi 300
Ravi → Asha  500      ❌  would leave Ravi below min_balance (100)
Dev withdraws 2450    ❌  same rule
interest added at 4%  →   each balance grows by 4%
```

## Extension exercises

1. Add a daily withdrawal limit stored as a class attribute.
2. Add `@classmethod richest(cls)` that returns the account with the highest balance.
3. Make `statement()` print dates (`datetime.now()`) for each transaction.
4. Add `__add__` so `acc1 + acc2` returns the combined balance.

**Next →** [Lecture 18: Project: library system](../18_project_library_system/)
