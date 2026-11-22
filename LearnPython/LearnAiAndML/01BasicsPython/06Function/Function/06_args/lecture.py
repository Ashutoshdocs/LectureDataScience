"""Lecture 06: *args: packing extra positional arguments, and * unpacking at call time."""

print("=== 1. The problem ===")


def add2(a, b):
    return a + b


try:
    add2(1, 2, 3)
except TypeError as e:
    print("  add2(1, 2, 3) ->", e)

print("\n=== 2. *args packs arguments into a tuple ===")


def add(*args):
    print(f"  args = {args!r} ({type(args).__name__}, {len(args)} items)")
    return sum(args)


print("  ->", add())
print("  ->", add(5))
print("  ->", add(1, 2, 3))

print("\n=== 3. Normal parameters first, then *args ===")


def report(title, *scores):
    avg = sum(scores) / len(scores) if scores else 0
    print(f"  {title}: scores={scores}, average={avg:.1f}")


report("Maths", 78, 92, 45)
report("Art")
try:
    report()
except TypeError as e:
    print("  report() ->", e)

print("\n=== 4. Keyword-only parameters after *args ===")


def join(*words, sep=" "):
    return sep.join(words)


print("  join('a','b','c')          ->", repr(join("a", "b", "c")))
print("  join('a','b','c', sep='-') ->", repr(join("a", "b", "c", sep="-")))
print("  join('a','b','-')          ->", repr(join("a", "b", "-")), "<- '-' became a word, not sep")

print("\n=== 5. * in a CALL unpacks ===")
nums = [4, 9, 2]
print("  max(*nums) =", max(*nums), "| add(*nums, 10) ->", add(*nums, 10))


def distance(x, y):
    return (x ** 2 + y ** 2) ** 0.5


point = (3, 4)
print("  distance(*point) =", distance(*point))
print("  print(*['a', 'b', 'c']) -> ", end="")
print(*["a", "b", "c"])

print("\n=== 6. Practical examples ===")


def average(*nums):
    return sum(nums) / len(nums) if nums else 0


def longest(*words):
    return max(words, key=len)


def tag(name, *classes):
    return f"<{name} class='{' '.join(classes)}'>"


print("  average(*[1, 2, 3]) =", average(*[1, 2, 3]), "| average() =", average())
print("  longest:", longest("pen", "notebook", "bag"))
print("  tag:", tag("div", "card", "shadow", "rounded"))


def log(level, *messages):
    print(f"  [{level.upper()}]", " | ".join(str(m) for m in messages))


log("info", "server started", "port", 8080)
