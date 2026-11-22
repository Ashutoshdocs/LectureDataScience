# Lecture 11: Choosing the right function type

Run: `python lecture.py`

You now know every kind of function that can live in or around a class. This lecture puts them **side by side** and gives you a decision guide.

## All of them in one program

```python
TAX = 0.18                                 # global constant

def with_tax(amount):                      # 1. GLOBAL function
    return amount * (1 + TAX)

class Product:
    count = 0                              # class attribute

    def __init__(self, name, price):       # 2. CONSTRUCTOR
        self.name = name
        self.price = price
        Product.count += 1

    def price_with_tax(self):              # 3. INSTANCE method
        return with_tax(self.price)

    @classmethod
    def how_many(cls):                     # 4. CLASS method
        return cls.count

    @classmethod
    def from_csv(cls, line):               # 4b. CLASS method as factory
        name, price = line.split(",")
        return cls(name, float(price))

    @staticmethod
    def rupees(x):                         # 5. STATIC method
        return f"Rs {x:,.2f}"

    def __str__(self):                     # 6. SPECIAL method
        return f"{self.name} ({self.rupees(self.price)})"

    def __del__(self):                     # 7. DESTRUCTOR
        Product.count -= 1
```

> ⚠️ `lecture.py` guards the destructor with a `_counted` flag. If `__init__` raises (e.g. a bad name), Python **still calls `__del__`** on the half-built object, and an unguarded counter would go down for an object that was never counted. Section 6 of `lecture.py` shows the bug.

| Function | Kind | Why that kind |
|----------|------|---------------|
| `with_tax` | global function | a general tax rule any code can use |
| `__init__` | constructor | sets up each new product |
| `price_with_tax` | instance method | needs **this** product's price (`self`) |
| `how_many` | class method | reports class-wide data (`cls.count`) |
| `from_csv` | class method (factory) | builds a new object from other input |
| `rupees` | static method | formatting helper; needs no data, but belongs with products |
| `__str__` | special method | Python calls it for `print(obj)` |
| `__del__` | destructor | cleanup when an object disappears |

## The decision guide

```
Does the function need THIS object's data (self.x)?
├── yes → INSTANCE METHOD                            def f(self, ...)
└── no
    ├── needs class-wide data, or creates objects? → CLASS METHOD    @classmethod  def f(cls, ...)
    └── no
        ├── logically part of this class?          → STATIC METHOD   @staticmethod def f(...)
        └── general / used by many things?         → GLOBAL FUNCTION def f(...)   (outside the class)

Special moments:
  object created   → __init__       object destroyed → __del__
  print / str()    → __str__        ==, <, +, len()  → __eq__, __lt__, __add__, __len__  (Lecture 15)
  get/set an attribute with checks  → @property (Lecture 13)
```

## Comparison table

| | Global | Instance | Class | Static |
|---|---|---|---|---|
| Where | outside the class | inside | inside | inside |
| Decorator | n/a | none | `@classmethod` | `@staticmethod` |
| First parameter | n/a | `self` | `cls` | none |
| Access object data | via argument | ✅ `self.x` | ❌ | ❌ |
| Access class data | `ClassName.x` | ✅ | ✅ `cls.x` | `ClassName.x` |
| Call as | `f(obj)` | `obj.f()` | `Class.f()` / `obj.f()` | `Class.f()` / `obj.f()` |
| Needs an object to call | n/a | ✅ | ❌ | ❌ |
| Typical uses | utilities, functions over many objects | behaviour of one object | counters, settings, factories | validation, conversion, formatting |

## What Python passes, call by call

| You write | Python passes |
|-----------|---------------|
| `p.price_with_tax()` | `Product.price_with_tax(p)` |
| `Product.how_many()` / `p.how_many()` | `how_many(Product)` |
| `Product.rupees(5)` / `p.rupees(5)` | `rupees(5)` |
| `Product("Lamp", 500)` | `__init__(new_obj, "Lamp", 500)` |
| `print(p)` | `print(Product.__str__(p))` |

## Exercises

For each, decide the kind and write it:
1. `Product.cheapest(products)`: returns the cheapest of a list of products.
2. `p.apply_discount(percent)`: reduces this product's price.
3. `Product.set_tax(rate)`: changes the tax rate for every product.
4. `Product.is_valid_name(text)`: True if the name is 2–30 letters.
5. `total_value(products)`: sum of prices, used by a reporting script.

<details><summary>Solutions</summary>

1. static method or global function (works on a list; needs no class data). Static if you want it grouped with Product.
2. instance method (needs self.price).
3. class method (changes class-wide data).
4. static method (validation helper).
5. global function (a general report over many objects).

See section 4 of `lecture.py`.
</details>

**Next →** [Lecture 12: Getters & setters](../12_getters_and_setters/)
