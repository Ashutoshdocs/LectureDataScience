"""Lecture 11: Every function type side by side, plus a decision exercise."""

TAX = 0.18


def with_tax(amount):                          # 1. global function
    return amount * (1 + TAX)


def total_value(products):                     # global function over many objects
    return sum(p.price for p in products)


class Product:
    count = 0
    tax_note = "incl. 18% GST"

    def __init__(self, name, price):           # 2. constructor
        if not Product.is_valid_name(name):
            raise ValueError(f"bad product name: {name!r}")
        self.name = name
        self.price = price
        Product.count += 1
        self._counted = True                   # remember that this object was counted

    def price_with_tax(self):                  # 3. instance method
        return with_tax(self.price)

    def apply_discount(self, percent):         # instance method: changes THIS object
        self.price = round(self.price * (100 - percent) / 100, 2)
        return self

    @classmethod
    def how_many(cls):                         # 4. class method
        return cls.count

    @classmethod
    def from_csv(cls, line):                   # 4b. class method as factory
        name, price = line.split(",")
        return cls(name.strip(), float(price))

    @classmethod
    def set_tax_note(cls, text):               # class method: class-wide setting
        cls.tax_note = text

    @staticmethod
    def rupees(x):                             # 5. static method
        return f"Rs {x:,.2f}"

    @staticmethod
    def is_valid_name(text):                   # static method: validation
        return text.replace(" ", "").isalpha() and 2 <= len(text) <= 30

    @staticmethod
    def cheapest(products):                    # static method over a list
        return min(products, key=lambda p: p.price)

    def __str__(self):                         # 6. special method
        return f"{self.name} ({self.rupees(self.price)})"

    def __del__(self):                         # 7. destructor
        if getattr(self, "_counted", False):   # __del__ also runs if __init__ FAILED!
            Product.count -= 1


print("=== 1. Each kind in action ===")
lamp = Product("Lamp", 500)
fan = Product("Fan", 1500)
desk = Product.from_csv("Desk, 4500")
print("global function        :", Product.rupees(with_tax(fan.price)))
print("instance method        :", Product.rupees(lamp.price_with_tax()))
print("class method           :", Product.how_many(), "products")
print("factory (class method) :", desk)
print("static method          :", Product.rupees(1234.5))
print("special method __str__ :", lamp)

print("\n=== 2. What Python passes ===")
print("lamp.price_with_tax() == Product.price_with_tax(lamp):",
      lamp.price_with_tax() == Product.price_with_tax(lamp))
print("lamp.how_many() == Product.how_many():", lamp.how_many() == Product.how_many())
print("lamp.rupees(5) == Product.rupees(5):", lamp.rupees(5) == Product.rupees(5))

print("\n=== 3. Types of what you get back ===")
for label, obj in [("with_tax", with_tax), ("lamp.price_with_tax", lamp.price_with_tax),
                   ("Product.how_many", Product.how_many), ("Product.rupees", Product.rupees)]:
    bound_to = getattr(obj, "__self__", None)
    who = "nothing" if bound_to is None else (bound_to.__name__ if isinstance(bound_to, type) else "an object")
    print(f"  {label:<22} {type(obj).__name__:<9} bound to {who}")

print("\n=== 4. The exercise answers ===")
items = [lamp, fan, desk]
print("cheapest (static)      :", Product.cheapest(items))
print("apply_discount (inst.) :", fan.apply_discount(10))
Product.set_tax_note("incl. 12% GST")
print("set_tax_note (class)   :", lamp.tax_note, "/", desk.tax_note)
print("is_valid_name (static) :", Product.is_valid_name("Table Lamp"), Product.is_valid_name("X1"))
print("total_value (global)   :", Product.rupees(total_value(items)))
try:
    Product("#$", 10)
except ValueError as e:
    print("constructor + static validation ->", e)

print("\n=== 5. Destructor keeps the count honest ===")
print("before del:", Product.how_many())
del desk
items.pop()                                     # the list also referred to desk
print("after del :", Product.how_many())

print("\n=== 6. Gotcha: __del__ runs even when __init__ raised ===")


class Naive:
    count = 0

    def __init__(self, ok):
        if not ok:
            raise ValueError("bad input")
        Naive.count += 1

    def __del__(self):
        Naive.count -= 1                        # no guard


Naive(True)                                      # counted, then immediately destroyed
keep = Naive(True)
print("Naive.count with one living object:", Naive.count)
try:
    Naive(False)                                 # __init__ fails BEFORE counting...
except ValueError:
    pass
print("after a FAILED creation:", Naive.count, "<- wrong! __del__ still ran on the half-built object")
print("Product avoids this with the _counted flag:", Product.how_many(), "(stayed correct)")
