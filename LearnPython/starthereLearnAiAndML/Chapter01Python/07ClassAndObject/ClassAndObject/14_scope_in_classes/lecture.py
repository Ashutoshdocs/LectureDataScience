"""Lecture 14: Scope in classes: local vs self, global, class-body scope, lookup order."""

print("=== 1. Local variables vs self attributes ===")


class Cart:
    def __init__(self):
        self.total = 0

    def add(self, price, qty):
        cost = price * qty                   # local
        self.total += cost                   # attribute
        print(f"  added {cost} -> locals in add(): {sorted(locals())}")

    def broken_add(self, price):
        total = self.total + price           # local! attribute unchanged
        return total


c = Cart()
c.add(50, 2)
c.add(30, 1)
print("  total:", c.total, "| has 'cost' attribute?", hasattr(c, "cost"))
print("  broken_add returned", c.broken_add(100), "but c.total is still", c.total)

print("\n=== 2. Globals inside methods ===")
visitors = 0
GREETING = "Welcome"


class Gate:
    count = 0                                # the better design

    def __init__(self, name):
        self.name = name

    def enter(self):
        global visitors
        visitors += 1
        Gate.count += 1
        print(f"  {GREETING} {self.name} - visitor no. {visitors}")

    def broken_enter(self):
        visitors += 1                        # noqa: F823


Gate("Asha").enter()
Gate("Ravi").enter()
print("  global visitors =", visitors, "| Gate.count =", Gate.count)
try:
    Gate("Dev").broken_enter()
except UnboundLocalError as e:
    print("  broken_enter ->", e)

print("\n=== 3. Class-body names are NOT visible in methods ===")


class Circle:
    PI = 3.14159
    unit = "cm"
    label = "radius in " + unit              # works in the class BODY

    def __init__(self, r):
        self.r = r

    def area(self):
        return self.PI * self.r ** 2

    def area_v2(self):
        return Circle.PI * self.r ** 2

    @classmethod
    def describe(cls):
        return f"circles use PI = {cls.PI}"

    @staticmethod
    def area_of(r):
        return Circle.PI * r ** 2

    def broken_area(self):
        return PI * self.r ** 2              # noqa: F821


circ = Circle(2)
print("  label:", Circle.label)
print("  self.PI / Circle.PI / static:", round(circ.area(), 2), round(circ.area_v2(), 2), round(Circle.area_of(2), 2))
print("  classmethod:", Circle.describe())
try:
    circ.broken_area()
except NameError as e:
    print("  broken_area ->", e)
PI = 3                                       # now a GLOBAL PI exists...
print("  with a global PI = 3, broken_area silently returns", circ.broken_area(), "(WRONG, no error!)")
del PI

print("\n=== 4. Attribute lookup order ===")


class Config:
    theme = "light"
    lang = "en"

    def __init__(self):
        self.theme = "dark"

    def show(self):
        print("  self.theme  :", self.theme, "(found on the object)")
        print("  self.lang   :", self.lang, "(not on the object -> found on the class)")
        print("  Config.theme:", Config.theme, "(read straight from the class)")


cfg = Config()
cfg.show()
print("  cfg.__dict__:", cfg.__dict__)
try:
    cfg.font
except AttributeError as e:
    print("  cfg.font ->", e)
print("  getattr with default:", getattr(cfg, "font", "Arial"))

print("\n=== 5. Puzzle: the same name at every level ===")
x = "global"


class Demo:
    x = "class"

    def __init__(self):
        self.x = "instance"

    def show(self):
        x = "local"
        print("  x            ->", x)
        print("  self.x       ->", self.x)
        print("  Demo.x       ->", Demo.x)
        print("  globals()[x] ->", globals()["x"])


Demo().show()

print("\n=== 6. What each method kind can reach ===")


class Scope:
    shared = "class data"

    def __init__(self):
        self.mine = "object data"

    def inst(self):
        return self.mine, self.shared, Scope.shared, GREETING

    @classmethod
    def klass(cls):
        return cls.shared, GREETING

    @staticmethod
    def stat():
        return Scope.shared, GREETING


s = Scope()
print("  instance method:", s.inst())
print("  class method   :", Scope.klass())
print("  static method  :", Scope.stat())
