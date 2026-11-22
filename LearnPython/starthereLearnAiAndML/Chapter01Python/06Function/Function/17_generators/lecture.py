"""Lecture 17: Generators: yield, laziness, memory, generator expressions, pipelines."""
import itertools
import sys

print("=== 1. A generator pauses at each yield ===")


def count_up_to(n):
    print("    (body starts)")
    i = 1
    while i <= n:
        print(f"    (about to yield {i})")
        yield i
        print(f"    (resumed after {i})")
        i += 1
    print("    (body ends)")


gen = count_up_to(2)
print("  calling count_up_to(2) gave:", type(gen).__name__, "- the body hasn't run yet")
print("  next ->", next(gen))
print("  next ->", next(gen))
try:
    next(gen)
except StopIteration:
    print("  next -> StopIteration (a for loop handles this silently)")
print("  a for loop:", [x for x in count_up_to(3)])

print("\n=== 2. Single use ===")
g = (n * n for n in range(3))
print("  first pass :", list(g))
print("  second pass:", list(g), "<- exhausted")

print("\n=== 3. Memory: list vs generator ===")
big_list = [n * n for n in range(1_000_000)]
big_gen = (n * n for n in range(1_000_000))
print(f"  list     : {sys.getsizeof(big_list):>10,} bytes")
print(f"  generator: {sys.getsizeof(big_gen):>10,} bytes")
print("  same sum :", sum(big_list) == sum(n * n for n in range(1_000_000)))
del big_list

print("\n=== 4. Infinite generators ===")


def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


def ids(prefix):
    for n in itertools.count(1):
        yield f"{prefix}-{n:04d}"


print("  first 10 fibonacci:", list(itertools.islice(fibonacci(), 10)))
id_gen = ids("EMP")
print("  next three ids    :", next(id_gen), next(id_gen), next(id_gen))

print("\n=== 5. Stopping early saves work ===")
checked = []


def numbers():
    for n in range(1, 1_000_000):
        checked.append(n)
        yield n


first_big_square = next(n for n in numbers() if n * n > 500)
print("  first n with n*n > 500:", first_big_square, "| numbers produced:", len(checked), "(not a million)")

print("\n=== 6. A pipeline of generators ===")
log_lines = [
    "2025-06-01 INFO  started",
    "2025-06-01 ERROR disk full",
    "2025-06-02 WARN  slow",
    "2025-06-02 ERROR timeout",
]


def read_lines(lines):
    for line in lines:
        print(f"    reading: {line[:22]}")
        yield line


def parse(lines):
    for line in lines:
        date, level, msg = line.split(maxsplit=2)
        yield {"date": date, "level": level, "msg": msg}


def only(level, records):
    return (r for r in records if r["level"] == level)


pipeline = only("ERROR", parse(read_lines(log_lines)))
print("  pipeline built, nothing read yet")
for rec in pipeline:
    print("  ERROR found:", rec["date"], rec["msg"])

print("\n=== 7. yield from ===")


def flatten(nested):
    for item in nested:
        if isinstance(item, list):
            yield from flatten(item)
        else:
            yield item


print("  flatten:", list(flatten([1, [2, [3, [4]]], 5])))


def evens(limit):
    yield from range(0, limit + 1, 2)


print("  evens(10):", list(evens(10)))
squares = (n * n for n in range(1, 30))
print("  squares ending in 6:", [s for s in squares if s % 10 == 6])
