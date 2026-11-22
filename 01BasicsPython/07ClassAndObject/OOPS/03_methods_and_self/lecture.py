"""Lecture 03: Methods & self: obj.m() == Class.m(obj), queries vs commands, chaining, bound methods."""

print("=== 1. Methods work on whichever object is self ===")


class Counter:
    def __init__(self, name):
        self.name = name
        self.count = 0

    def increment(self, by=1):
        self.count += by

    def decrement(self, by=1):
        self.count = max(0, self.count - by)

    def reset(self):
        self.count = 0

    def show(self):
        print(f"    {self.name}: count = {self.count}")


a, b = Counter("a"), Counter("b")
a.increment()
b.increment(10)
b.decrement(3)
a.show()
b.show()

print("\n=== 2. obj.method(x) is Class.method(obj, x) ===")
a.increment(5)
Counter.increment(a, 5)
a.show()
print("  a.increment       :", a.increment)
print("  Counter.increment :", Counter.increment)

print("\n=== 3. Queries, commands and helpers ===")


class Cart:
    def __init__(self):
        self.items = []
        self.history = []

    def add(self, item, price, qty=1):             # command (returns self for chaining)
        if price < 0 or qty < 1:
            raise ValueError("price must be >= 0 and qty >= 1")
        self.items.append({"item": item, "price": price, "qty": qty})
        self._log(f"added {qty} x {item}")
        return self

    def remove(self, item):                        # command
        before = len(self.items)
        self.items = [i for i in self.items if i["item"] != item]
        self._log(f"removed {item}" if len(self.items) < before else f"{item} not in cart")
        return self

    def total(self):                               # query
        return sum(i["price"] * i["qty"] for i in self.items)

    def is_empty(self):                            # query
        return not self.items

    def summary(self):                             # query that uses other queries
        return f"{len(self.items)} line(s), total Rs {self.total():,}"

    def _log(self, msg):                           # internal helper
        self.history.append(msg)


cart = Cart()
cart.add("pen", 20, 3).add("notebook", 60, 2).add("bag", 900).remove("pen").remove("laptop")
print("  summary :", cart.summary())
print("  empty?  :", cart.is_empty())
print("  history :", cart.history)

print("\n=== 4. Bound methods can be stored and called later ===")
c = Counter("clicks")
click = c.increment
for _ in range(4):
    click()
c.show()
actions = {"up": c.increment, "down": c.decrement, "reset": c.reset}
for cmd in ["up", "up", "down", "up"]:
    actions[cmd]()
c.show()

print("\n=== 5. Common mistakes ===")


class NoSelf:
    def show():
        print("hi")


class ForgotSelfDot:
    def __init__(self):
        self.count = 0

    def increment(self):
        count += 1          # noqa: F821  forgot self.


class ForgotSelfCall:
    def run(self):
        return helper()     # noqa: F821  forgot self.

    def helper(self):
        return "ok"


for label, call in [("def show() without self", lambda: NoSelf().show()),
                    ("count += 1 without self.", lambda: ForgotSelfDot().increment()),
                    ("helper() without self.", lambda: ForgotSelfCall().run())]:
    try:
        call()
    except (TypeError, NameError, UnboundLocalError) as e:
        print(f"  {label:<26} -> {type(e).__name__}: {e}")
print("  c.show (no brackets) just gives:", type(c.show).__name__, "- nothing runs")
