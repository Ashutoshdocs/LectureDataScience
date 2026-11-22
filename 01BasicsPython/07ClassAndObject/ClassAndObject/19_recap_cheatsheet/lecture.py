"""Lecture 19: Recap. The full template class, then a self-test. Predict, then run."""

TAX = 0.18


def with_tax(x):
    return x * (1 + TAX)


class Product:
    """One product in the shop."""

    count = 0

    def __init__(self, name, price=0):
        self.name = name
        self.price = price
        self._history = []
        Product.count += 1
        self._counted = True

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError("price cannot be negative")
        self._price = value

    @property
    def price_with_tax(self):
        return round(with_tax(self.price), 2)

    def discount(self, percent):
        self.price = round(self.price * (100 - percent) / 100, 2)
        return self

    @classmethod
    def from_csv(cls, line):
        name, price = line.split(",")
        return cls(name.strip(), float(price))

    @classmethod
    def how_many(cls):
        return cls.count

    @staticmethod
    def rupees(x):
        return f"Rs {x:,.2f}"

    def __str__(self):
        return f"{self.name}: {self.rupees(self.price)}"

    def __repr__(self):
        return f"Product({self.name!r}, {self.price})"

    def __eq__(self, other):
        return isinstance(other, Product) and (self.name, self.price) == (other.name, other.price)

    def __hash__(self):
        return hash((self.name, self.price))

    def __del__(self):
        if getattr(self, "_counted", False):
            Product.count -= 1


lamp = Product("Lamp", 500)
fan = Product.from_csv("Fan, 1500")


class Counter:
    step = 1


c1, c2 = Counter(), Counter()
c1.step = 10

questions = [
    ("What does print(lamp) show?", lambda: str(lamp)),
    ("What does repr(fan) show?", lambda: repr(fan)),
    ("Product.how_many() after creating 2 products?", lambda: Product.how_many()),
    ("lamp.price_with_tax (a property, no brackets)?", lambda: lamp.price_with_tax),
    ("fan.discount(10).price (chained)?", lambda: fan.discount(10).price),
    ("Product.rupees(1234.5) (static, no object needed)?", lambda: Product.rupees(1234.5)),
    ("Product('Lamp', 500) == lamp?", lambda: Product("Lamp", 500) == lamp),
    ("Product('Lamp', 500) is lamp?", lambda: Product("Lamp", 500) is lamp),
    ("c1.step, c2.step, Counter.step after c1.step = 10?", lambda: (c1.step, c2.step, Counter.step)),
    ("Is 'step' in c2.__dict__?", lambda: "step" in c2.__dict__),
    ("type(lamp.discount).__name__ (through an object)?", lambda: type(lamp.discount).__name__),
    ("type(Product.discount).__name__ (through the class)?", lambda: type(Product.discount).__name__),
    ("What is cls inside lamp.how_many()?", lambda: Product.how_many.__self__.__name__),
]


def error_of(fn):
    try:
        fn()
        return "no error"
    except Exception as e:
        return f"{type(e).__name__}: {e}"


questions += [
    ("lamp.price = -5 ?", lambda: error_of(lambda: setattr(lamp, "price", -5))),
    ("lamp.price_with_tax = 0 ?", lambda: error_of(lambda: setattr(lamp, "price_with_tax", 0))),
    ("Product() with no name?", lambda: error_of(lambda: Product())),
    ("A set of two equal products has how many items?", lambda: len({Product("Pen", 10), Product("Pen", 10)})),
]

for i, (q, answer) in enumerate(questions, start=1):
    print(f"Q{i:02}. {q}")
    print(f"     -> {answer()}\n")

print("If every answer matched your prediction, you've mastered classes & objects. Well done!")
