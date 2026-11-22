"""Lecture 02: Calling functions: flow, the call stack, tracebacks, main()."""
import traceback

print("=== 1. Flow of a call ===")


def say_hi(name):
    print("  Hi", name)


print("  start")
say_hi("Asha")
print("  end")

print("\n=== 2. Functions calling functions (watch the indentation = stack depth) ===")
depth = 0


def show(msg):
    print("  " + "    " * depth + msg)


def c():
    global depth
    depth += 1
    show("in c (top of the stack)")
    depth -= 1


def b():
    global depth
    depth += 1
    show("in b -> calling c")
    c()
    show("back in b")
    depth -= 1


def a():
    global depth
    depth += 1
    show("in a -> calling b")
    b()
    show("back in a")
    depth -= 1


a()

print("\n=== 3. A traceback shows the call stack ===")


def level3():
    return int("not a number")


def level2():
    return level3()


def level1():
    return level2()


try:
    level1()
except ValueError:
    frames = traceback.extract_tb(__import__("sys").exc_info()[2])
    print("  call chain:", " -> ".join(f.name for f in frames))
    print("  error     :", traceback.format_exc().strip().splitlines()[-1])

print("\n=== 4. Defined before the call RUNS ===")


def main_demo():
    helper()                        # helper defined below, but before main_demo() runs


def helper():
    print("  helper ran")


main_demo()
try:
    not_defined_yet()               # noqa: F821
except NameError as e:
    print("  calling before def ->", e)

print("\n=== 5. Forgetting the brackets ===")


def is_weekend():
    return False


print("  is_weekend   ->", is_weekend.__name__, "(the function object, which is truthy)")
print("  is_weekend() ->", is_weekend())
if is_weekend:
    print("  'if is_weekend:' is True even though it's not the weekend!")

print("\n=== 6. Nested calls: inner first ===")


def double(x):
    return x * 2


def add_one(x):
    return x + 1


print("  add_one(double(5)) =", add_one(double(5)), "(double runs first)")

print("\n=== 7. The main() pattern ===")


def main():
    print("  main() running, __name__ =", __name__)


if __name__ == "__main__":
    main()
