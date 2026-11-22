"""Lecture 08: The destructor __del__: lifetime, reference counting, safe cleanup, with."""
import gc
import sys

print("=== 1. __init__ on creation, __del__ on destruction ===")


class File:
    def __init__(self, name):
        self.name = name
        print("  Opened", name)

    def __del__(self):
        print("  Closed", self.name)


f = File("notes.txt")
print("  Working with", f.name)
del f
print("  After del")

print("\n=== 2. del removes a NAME; the object dies at zero references ===")


class Res:
    def __init__(self, name):
        self.name = name
        print("  create", name)

    def __del__(self):
        print("  destroy", self.name)


a = Res("A")
b = a
print("  references to A (getrefcount adds 1 for its own argument):", sys.getrefcount(a) - 1)
del a
print("  a deleted, but b still points to it")
del b
print("  ---")
c = Res("C")
c = Res("D")              # rebinding c drops the last reference to C
print("  ---")
items = [Res("E")]
items.clear()
del c

print("\n=== 3. Lifetime follows scope ===")


def work():
    print("  work() starts")
    t = Res("local")
    print("  work() ends")


work()
print("  back in main")


def make():
    return Res("returned")


x = make()
print("  the returned object is still alive in x:", x.name)
del x

print("\n=== 4. Cycles are cleaned up later by the garbage collector ===")
p = Res("P")
q = Res("Q")
p.partner, q.partner = q, p      # they refer to each other
del p, q
print("  names deleted, but the cycle keeps both alive...")
gc.collect()
print("  ...until gc.collect() ran")

print("\n=== 5. Safe cleanup: explicit close() + __del__ as a safety net + with ===")


class Conn:
    def __init__(self, name):
        self.name = name
        self.open = True
        print("  connect", name)

    def close(self):
        if self.open:
            self.open = False
            print("  disconnect", self.name)

    def __del__(self):
        self.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()
        return False                     # don't hide errors


c1 = Conn("db1")
c1.close()                               # explicit
del c1                                   # destructor runs, but nothing left to close
print("  'disconnect db1' appeared only once")

c2 = Conn("db2")
del c2                                   # forgot close(): the safety net does it

try:
    with Conn("db3") as c3:
        print("  using", c3.name)
        raise RuntimeError("something failed inside the with block")
except RuntimeError as e:
    print("  error:", e, "| still closed?", not c3.open)
del c3
print("  done")
