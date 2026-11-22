# Lecture 18: Project: a library system (several classes working together)

Run: `python lecture.py`

Real programs use **several classes** whose objects hold and use each other (composition, Lecture 16). This project builds a small library with three classes.

## The classes

```
 Library ──has many──► Book
    │
    └────has many──► Member ──borrows──► Book
```

| Class | Responsibility | Highlights |
|-------|----------------|------------|
| `Book` | one title in the library | `@property` `isbn` (validated, read-only after creation); `available` computed property; `__str__`, `__eq__` on ISBN; `@classmethod from_line`; `@staticmethod valid_isbn` |
| `Member` | one library member | class-level `max_books` limit; borrowed books stored in a list created in `__init__`; `can_borrow` property; `__len__` = books held |
| `Library` | owns books & members, runs the rules | dict of books keyed by ISBN; `checkout`, `return_book`, `search`, `report`; `__contains__` for `isbn in library`; `__len__` |

Plus a global function `print_table(rows)` for neat output, used by more than one class.

## Rules

1. ISBNs must be 10 digits (`Book.valid_isbn`).
2. A member may hold at most `Member.max_books` books (class attribute: change once for everyone).
3. A book can be borrowed only if it's available.
4. Returning a book the member doesn't hold is refused.
5. Late returns cost `Library.fine_per_day` per day (class attribute), computed by a static method.

## Which function type, and why

| Function | Kind | Reason |
|----------|------|--------|
| `Book.from_line("123…,Title,Author")` | class method | alternative constructor |
| `Book.valid_isbn(text)` | static method | validation, needs no data |
| `Book.available` | property | computed from `self.borrowed_by` |
| `Member.can_borrow` | property | computed from `len(self.books)` and the class limit |
| `Member.set_limit(n)` | class method | changes the class-wide limit |
| `Library.checkout(isbn, member_id)` | instance method | uses this library's books and members |
| `Library.late_fine(days)` | static method | pure calculation from a class constant |
| `print_table(rows)` | global function | generic, not tied to one class |

## Extension exercises

1. Add a waiting list: if a book is out, `reserve(isbn, member_id)` adds the member to a list on the book.
2. Add `@classmethod Member.from_dict(cls, data)`.
3. Add `Library.most_popular()` using a per-book borrow counter.
4. Add `__lt__` to `Member` so `sorted(library.members.values())` sorts members by name (Book already has one, sorting by title).

**Next →** [Lecture 19: Recap & cheat sheet](../19_recap_cheatsheet/)
