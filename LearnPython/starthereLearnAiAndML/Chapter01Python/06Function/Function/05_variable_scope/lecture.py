"""Lecture 05: Scope: local, global, LEGB, shadowing, global, nonlocal."""

print("=== 1. Local vs global ===")
rate = 0.18


def tax(amount):
    result = amount * rate
    print(f"  inside tax(): locals = {sorted(locals())}")
    return result


print("  tax(100) =", tax(100))
try:
    print(result)                                     # noqa: F821
except NameError as e:
    print("  outside ->", e)

print("\n=== 2. LEGB in action ===")
level = "global"


def outer():
    level = "enclosing"

    def inner():
        level = "local"
        print("  L:", level)

    def inner_no_local():
        print("  E:", level)                         # found in the enclosing function

    inner()
    inner_no_local()


def only_global():
    print("  G:", level)


outer()
only_global()
print("  B:", len("builtin"), "(len found in built-ins)")

print("\n=== 3. Shadowing ===")
x = "global"


def shadow():
    x = "local"
    print("  inside:", x)


shadow()
print("  outside:", x)
sum = 0                                                # shadows the built-in sum!
try:
    sum([1, 2])
except TypeError as e:
    print("  after 'sum = 0', sum([1, 2]) ->", e)
del sum                                                # remove the shadow
print("  after del sum:", sum([1, 2]))

print("\n=== 4. global ===")
count = 0


def increment():
    global count
    count += 1


def broken():
    count += 1                                         # noqa: F823


increment()
increment()
print("  count =", count)
try:
    broken()
except UnboundLocalError as e:
    print("  broken() ->", e)


def increment_pure(value):                             # the better design
    return value + 1


c = 0
c = increment_pure(c)
c = increment_pure(c)
print("  without global:", c)

print("\n=== 5. nonlocal ===")


def make_counter():
    n = 0

    def step():
        nonlocal n
        n += 1
        return n

    return step


counter = make_counter()
print("  counter calls:", counter(), counter(), counter())


def no_nonlocal():
    n = 0

    def step():
        n = 99                                         # new local, outer n untouched
        return n

    step()
    return n


print("  without nonlocal the outer n stays:", no_nonlocal())

print("\n=== 6. Loops don't create a scope; comprehensions do ===")
for i in range(3):
    last = i
print("  after the loop: i =", i, "| last =", last)
squares = [k * k for k in range(3)]
print("  'k' exists after the comprehension?", "k" in globals())
