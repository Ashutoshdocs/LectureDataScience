"""Lecture 18: Project: a library system with three cooperating classes."""


def print_table(rows, headers):
    """Global helper: generic, used by any class that needs a table."""
    widths = [max(len(str(x)) for x in col) for col in zip(headers, *rows)]
    line = "  " + "  ".join(f"{h:<{w}}" for h, w in zip(headers, widths))
    print(line)
    print("  " + "  ".join("-" * w for w in widths))
    for r in rows:
        print("  " + "  ".join(f"{str(x):<{w}}" for x, w in zip(r, widths)))


class Book:
    def __init__(self, isbn, title, author):
        if not Book.valid_isbn(isbn):
            raise ValueError(f"invalid ISBN: {isbn!r}")
        self._isbn = isbn
        self.title = title
        self.author = author
        self.borrowed_by = None
        self.times_borrowed = 0

    @property
    def isbn(self):                          # read-only after creation
        return self._isbn

    @property
    def available(self):                     # computed
        return self.borrowed_by is None

    @classmethod
    def from_line(cls, line):                # alternative constructor
        isbn, title, author = [part.strip() for part in line.split(",")]
        return cls(isbn, title, author)

    @staticmethod
    def valid_isbn(text):
        return len(text) == 10 and text.isdigit()

    def __eq__(self, other):
        return isinstance(other, Book) and self.isbn == other.isbn

    def __hash__(self):
        return hash(self.isbn)

    def __lt__(self, other):
        return self.title < other.title

    def __str__(self):
        return f"'{self.title}' by {self.author}"


class Member:
    max_books = 2                            # class-wide rule

    def __init__(self, member_id, name):
        self.member_id = member_id
        self.name = name
        self.books = []                      # per-member list, created in __init__

    @property
    def can_borrow(self):
        return len(self.books) < Member.max_books

    @classmethod
    def set_limit(cls, n):
        cls.max_books = n

    def __len__(self):
        return len(self.books)

    def __str__(self):
        return f"{self.name} (#{self.member_id})"


class Library:
    fine_per_day = 5

    def __init__(self, name):
        self.name = name
        self.books = {}                      # isbn -> Book
        self.members = {}                    # id -> Member

    def add_book(self, book):
        self.books[book.isbn] = book

    def add_member(self, member):
        self.members[member.member_id] = member

    def checkout(self, isbn, member_id):
        book, member = self.books[isbn], self.members[member_id]
        if not book.available:
            return f"refused: {book} is with {book.borrowed_by.name}"
        if not member.can_borrow:
            return f"refused: {member} already holds {len(member)} (limit {Member.max_books})"
        book.borrowed_by = member
        book.times_borrowed += 1
        member.books.append(book)
        return f"ok: {member.name} borrowed {book}"

    def return_book(self, isbn, member_id, days_late=0):
        book, member = self.books[isbn], self.members[member_id]
        if book not in member.books:
            return f"refused: {member.name} doesn't have {book}"
        member.books.remove(book)
        book.borrowed_by = None
        fine = Library.late_fine(days_late)
        return f"ok: {book} returned" + (f", fine Rs {fine}" if fine else "")

    def search(self, word):
        word = word.lower()
        return [b for b in self.books.values() if word in b.title.lower() or word in b.author.lower()]

    def most_popular(self):
        return max(self.books.values(), key=lambda b: b.times_borrowed)

    @staticmethod
    def late_fine(days):
        return max(0, days) * Library.fine_per_day

    def report(self):
        rows = [(b.isbn, b.title, "yes" if b.available else f"no ({b.borrowed_by.name})", b.times_borrowed)
                for b in sorted(self.books.values())]
        print_table(rows, ["ISBN", "Title", "Available", "Borrowed"])

    def __contains__(self, isbn):
        return isbn in self.books

    def __len__(self):
        return len(self.books)


def main():
    lib = Library("City Library")
    for line in ["0131103628, The C Programming Language, Kernighan",
                 "0596007124, Head First Design Patterns, Freeman",
                 "1593279280, Python Crash Course, Matthes",
                 "0132350882, Clean Code, Martin"]:
        lib.add_book(Book.from_line(line))
    for m in [Member(1, "Asha"), Member(2, "Ravi")]:
        lib.add_member(m)
    print(f"=== {lib.name}: {len(lib)} books, {len(lib.members)} members ===")

    print("\n=== Validation ===")
    try:
        Book("12AB", "Bad", "Nobody")
    except ValueError as e:
        print("  ", e)
    try:
        lib.books["1593279280"].isbn = "0000000000"
    except AttributeError as e:
        print("  ", e)

    print("\n=== Borrowing ===")
    print(" ", lib.checkout("1593279280", 1))
    print(" ", lib.checkout("0132350882", 1))
    print(" ", lib.checkout("0131103628", 1))          # over the limit
    print(" ", lib.checkout("1593279280", 2))          # already out
    Member.set_limit(3)                                 # class method: rule changes for everyone
    print("  (limit raised to 3)")
    print(" ", lib.checkout("0131103628", 1))

    print("\n=== Returning ===")
    print(" ", lib.return_book("1593279280", 2))       # Ravi doesn't have it
    print(" ", lib.return_book("1593279280", 1, days_late=3))
    print(" ", lib.checkout("1593279280", 2))

    print("\n=== Queries ===")
    print("  '0132350882' in library:", "0132350882" in lib)
    print("  search 'python':", [str(b) for b in lib.search("python")])
    print("  Asha holds", len(lib.members[1]), "books:", [b.title for b in lib.members[1].books])
    print("  most popular:", lib.most_popular())

    print("\n=== Report ===")
    lib.report()


if __name__ == "__main__":
    main()
