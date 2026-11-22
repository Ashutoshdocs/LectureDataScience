"""Lecture 15: Special (dunder) methods: text, comparison, arithmetic, containers, call."""

print("=== 1. Default text ===")


class Plain:
    pass


print("  print(Plain()) ->", str(Plain()).split(" at ")[0] + " at 0x...>")

print("\n=== 2. __str__ and __repr__ ===")


class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return f"Point(x={self.x}, y={self.y})"

    def __eq__(self, other):
        if not isinstance(other, Point):
            return NotImplemented
        return (self.x, self.y) == (other.x, other.y)

    def __hash__(self):
        return hash((self.x, self.y))

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, n):
        return Point(self.x * n, self.y * n)


p = Point(3, 4)
print("  print(p)       ->", p)
print("  f-string       ->", f"point is {p}")
print("  repr(p)        ->", repr(p))
print("  list of points ->", [Point(0, 0), Point(1, 2)], "(lists use __repr__)")

print("\n=== 3. __eq__ and __hash__ ===")
a, b = Point(1, 2), Point(1, 2)
print("  a == b:", a == b, "| a is b:", a is b, "| a != b:", a != b)
print("  a == 'text':", a == "text", "(NotImplemented -> False)")
print("  set of points:", {a, b, Point(5, 5)}, "(duplicates removed thanks to __hash__)")


class NoHash:
    def __init__(self, v):
        self.v = v

    def __eq__(self, other):
        return self.v == other.v


try:
    {NoHash(1)}
except TypeError as e:
    print("  __eq__ without __hash__ ->", e)

print("\n=== 4. Arithmetic ===")
print("  Point(1,2) + Point(3,4) =", Point(1, 2) + Point(3, 4))
print("  Point(5,5) - Point(1,2) =", Point(5, 5) - Point(1, 2))
print("  Point(1,2) * 3          =", Point(1, 2) * 3)

print("\n=== 5. Ordering with __lt__ ===")


class Money:
    def __init__(self, amount):
        self.amount = amount

    def __repr__(self):
        return f"Rs{self.amount}"

    def __eq__(self, other):
        return isinstance(other, Money) and self.amount == other.amount

    def __lt__(self, other):
        return self.amount < other.amount

    def __hash__(self):
        return hash(self.amount)

    def __add__(self, other):
        return Money(self.amount + other.amount)


wallet = [Money(500), Money(20), Money(150)]
print("  sorted:", sorted(wallet), "| min:", min(wallet), "| max:", max(wallet))
print("  Money(20) < Money(500):", Money(20) < Money(500), "| > also works:", Money(500) > Money(20))
total = Money(0)
for m in wallet:
    total += m                       # no __iadd__, so Python uses __add__
print("  total with += :", total)

print("\n=== 6. Container behaviour ===")


class Cart:
    def __init__(self):
        self._items = []

    def add(self, item):
        self._items.append(item)
        return self

    def __len__(self):
        return len(self._items)

    def __getitem__(self, i):
        return self._items[i]

    def __contains__(self, item):
        return item in self._items

    def __iter__(self):
        return iter(self._items)

    def __repr__(self):
        return f"Cart({self._items})"


cart = Cart().add("pen").add("book").add("lamp")
print("  len(cart):", len(cart), "| cart[0]:", cart[0], "| cart[-1]:", cart[-1], "| cart[0:2]:", cart[0:2])
print("  'book' in cart:", "book" in cart, "| 'desk' in cart:", "desk" in cart)
print("  loop:", [item.upper() for item in cart])
print("  empty cart is falsy:", not Cart(), "| full cart is truthy:", bool(cart))

print("\n=== 7. Callable objects with __call__ ===")


class Multiplier:
    def __init__(self, n):
        self.n = n
        self.calls = 0

    def __call__(self, x):
        self.calls += 1
        return x * self.n


triple = Multiplier(3)
print("  triple(10) =", triple(10), "| list(map(triple, [1,2,3])) =", list(map(triple, [1, 2, 3])))
print("  it remembers state: called", triple.calls, "times")

print("\n=== 8. Use the syntax, not the dunder ===")
print("  str(p) == p.__str__():", str(p) == p.__str__(), "-> but always write str(p)")
