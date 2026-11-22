"""Lecture 06: Return values, methods calling methods, chaining, global function vs method."""

print("=== 1. Parameters & return values ===")


class Rectangle:
    def set_size(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)

    def is_square(self):
        return self.width == self.height

    def scale(self, factor):
        self.width *= factor
        self.height *= factor
        return self                        # enables chaining


r = Rectangle()
result = r.set_size(4, 3)
print("set_size returned:", result)
a = r.area()
print("Area:", a, "| Perimeter:", r.perimeter(), "| Double area:", r.area() * 2)
print("Square?", r.is_square())
print("scale(2).area() =", r.scale(2).area())

print("\n=== 2. Methods calling methods (with a trace) ===")


class Order:
    def __init__(self, prices):
        self.prices = prices

    def subtotal(self):
        print("    subtotal() called")
        return sum(self.prices)

    def tax(self):
        print("    tax() called -> needs subtotal")
        return self.subtotal() * 0.1

    def total(self):
        print("    total() called")
        return self.subtotal() + self.tax()


o = Order([100, 50])
print("Total:", o.total())


def broken_tax(self):
    return subtotal() * 0.1               # bare name: NOT visible


try:
    broken_tax(o)
except NameError as e:
    print("bare subtotal() ->", e)

print("\n=== 3. Method chaining ===")


class Query:
    def __init__(self, table):
        self.table = table
        self.conditions = []
        self.n = None

    def where(self, cond):
        self.conditions.append(cond)
        return self

    def limit(self, n):
        self.n = n
        return self

    def sql(self):
        text = f"SELECT * FROM {self.table}"
        if self.conditions:
            text += " WHERE " + " AND ".join(self.conditions)
        if self.n:
            text += f" LIMIT {self.n}"
        return text


print(Query("users").where("age > 18").where("city = 'Pune'").limit(10).sql())

print("\n=== 4. Global function vs method ===")


def area_of(rect):
    return rect.width * rect.height


def bigger(r1, r2):                       # works with TWO objects: a good global function
    return r1 if r1.area() >= r2.area() else r2


class Rect:
    def __init__(self, w, h):
        self.width, self.height = w, h

    def area(self):
        return self.width * self.height


r1, r2 = Rect(5, 2), Rect(3, 3)
print("area_of(r1) =", area_of(r1), "| r1.area() =", r1.area())
print("bigger:", bigger(r1, r2).area())
print("type(area_of)  :", type(area_of).__name__)
print("type(r1.area)  :", type(r1.area).__name__)
print("type(Rect.area):", type(Rect.area).__name__)
m = r1.area
r1.width = 10
print("stored bound method m() after width change:", m(), "(it remembers r1)")
