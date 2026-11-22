"""Lecture 19: Pure vs impure functions, refactoring into small functions, testing with assert."""
import functools

print("=== 1. Pure vs impure ===")


def add_tax(price, rate):                       # pure
    return round(price * (1 + rate), 2)


total = 0


def add_to_total(x):                            # impure: changes a global
    global total
    total += x
    return total


def add_bonus_impure(marks):                    # impure: modifies its argument
    marks.append(5)
    return marks


def add_bonus_pure(marks):                      # pure: returns a new list
    return marks + [5]


print("  add_tax(100, 0.1) twice:", add_tax(100, 0.1), add_tax(100, 0.1), "(always the same)")
print("  add_to_total(10) twice :", add_to_total(10), add_to_total(10), "(depends on hidden state)")
m = [80, 90]
add_bonus_pure(m)
print("  after add_bonus_pure  :", m, "(unchanged)")
add_bonus_impure(m)
print("  after add_bonus_impure:", m, "(changed!)")

print("\n=== 2. Before: one function doing everything ===")
RAW = "Asha:88,Ravi:35,Dev:91,Meena:62"


def report_everything(raw):
    students = []
    for part in raw.split(","):
        name, mark = part.split(":")
        students.append((name, int(mark)))
    total_marks = 0
    for _, mark in students:
        total_marks += mark
    avg = total_marks / len(students)
    passed = []
    for name, mark in students:
        if mark >= 40:
            passed.append(name)
    print(f"  Average: {avg:.1f}")
    print(f"  Passed : {', '.join(passed)}")
    print(f"  Failed : {len(students) - len(passed)}")


report_everything(RAW)

print("\n=== 3. After: small functions, mostly pure ===")


def parse_students(raw):                        # pure
    return [(name, int(mark)) for name, mark in (p.split(":") for p in raw.split(","))]


def average_mark(students):                     # pure
    return sum(mark for _, mark in students) / len(students)


def passed_names(students, pass_mark=40):       # pure
    return [name for name, mark in students if mark >= pass_mark]


def print_report(avg, passed, failed_count):    # impure: output is its only job
    print(f"  Average: {avg:.1f}")
    print(f"  Passed : {', '.join(passed)}")
    print(f"  Failed : {failed_count}")


students = parse_students(RAW)
passed = passed_names(students)
print_report(average_mark(students), passed, len(students) - len(passed))
print("  reusable: who scored 90+?", passed_names(students, pass_mark=90))

print("\n=== 4. Testing pure functions with assert ===")


def test_parse_students():
    assert parse_students("A:1,B:2") == [("A", 1), ("B", 2)]


def test_average_mark():
    assert average_mark([("A", 50), ("B", 100)]) == 75


def test_passed_names():
    assert passed_names([("A", 39), ("B", 40)]) == ["B"]
    assert passed_names([("A", 95)], pass_mark=90) == ["A"]


def test_add_tax():
    assert add_tax(100, 0.1) == 110
    assert add_tax(0, 0.5) == 0


tests = [test_parse_students, test_average_mark, test_passed_names, test_add_tax]
for t in tests:
    t()
    print(f"  {t.__name__:<22} passed")

print("\n=== 5. Pure functions are safe to cache ===")


@functools.lru_cache(maxsize=None)
def slow_square(n):
    return n * n


print("  cached results:", [slow_square(n) for n in [4, 4, 4]], slow_square.cache_info())

print("\n=== 6. Readable names and guard clauses ===")


def is_valid_email(text):
    if "@" not in text:
        return False
    user, _, domain = text.partition("@")
    if not user or "." not in domain:
        return False
    return True


print("  is_valid_email:", {e: is_valid_email(e) for e in ["a@b.com", "ab.com", "@b.com", "a@b"]})
