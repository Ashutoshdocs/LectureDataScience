# Lecture 05: Project: bank account

Run: `python lecture.py`

**Goal:** model a bank account that keeps its own rules (no overdraft, positive amounts only, daily withdrawal limit) and records every transaction. It uses everything from Lectures 01–04.

## Design first: data and behaviour

| Kind | Name | Notes |
|------|------|-------|
| class attributes | `bank_name`, `MIN_BALANCE`, `DAILY_LIMIT`, `_next_number` | shared rules and an account-number counter |
| instance attributes | `number`, `owner`, `balance`, `transactions` | per-account data |
| commands | `deposit(amount)`, `withdraw(amount)`, `transfer(to, amount)` | change the balance; enforce rules |
| queries | `statement()`, `withdrawn_today()` | read-only |
| helpers | `_check_amount(amount)`, `_record(kind, amount)` | internal, used by commands |

## Rules (all enforced inside the class)

1. Amounts must be positive numbers.
2. A withdrawal may not take the balance below `MIN_BALANCE` (0).
3. Total withdrawals per day are capped at `DAILY_LIMIT` (25,000).
4. A transfer is a withdrawal from one account plus a deposit to another. If the withdrawal fails, nothing moves.
5. Every successful operation is recorded with a running balance.

Errors are reported by **raising exceptions** (`ValueError`), not by printing. The caller decides how to show them. That keeps the class reusable in a web app, a CLI or a test.

## Why this is better than dicts + functions (Lecture 00)

- Code outside the class never touches `balance` directly. It asks the account to `withdraw`, and the account enforces the rules.
- `transfer` reuses `withdraw` and `deposit`, so the rules can't be bypassed.
- Each account carries its own history.

## Extension exercises

1. Add `SavingsAccount` behaviour: `add_interest(rate)` (Lecture 09 does this properly with inheritance).
2. Make `balance` read-only with `@property` (Lecture 07).
3. Add `__str__` so `print(acc)` shows `ACC-1001 Asha: Rs 1,200` (Lecture 14).
4. Add a `freeze()` command that blocks all withdrawals.

**Next →** [Lecture 06: Encapsulation & access levels](../06_encapsulation_access_levels/)
