"""Lecture 18: Composition vs inheritance: has-a, delegation, swappable parts, DI, aggregation."""

print("=== 1. Composition: a Car HAS an engine, gearbox and roof ===")


class PetrolEngine:
    def start(self):
        return "petrol engine roars"


class ElectricEngine:
    def start(self):
        return "electric motor hums"


class Manual:
    def shift(self):
        return "you change gears"


class Automatic:
    def shift(self):
        return "gears change themselves"


class Sunroof:
    def describe(self):
        return "with sunroof"


class NoRoof:
    def describe(self):
        return "fixed roof"


class Car:
    def __init__(self, brand, engine, gearbox, roof=None):
        self.brand = brand
        self.engine = engine            # parts are passed in (dependency injection)
        self.gearbox = gearbox
        self.roof = roof or NoRoof()

    def drive(self):                    # delegation
        return f"{self.brand}: {self.engine.start()}, {self.gearbox.shift()}, {self.roof.describe()}"


cars = [Car("Tata", ElectricEngine(), Automatic(), Sunroof()),
        Car("Maruti", PetrolEngine(), Manual())]
for car in cars:
    print("  ", car.drive())
cars[1].engine = ElectricEngine()       # swap a part at runtime
print("   after swapping the engine:", cars[1].drive())
print("   2 engines x 2 gearboxes x 2 roofs = 8 combinations from 6 small classes")

print("\n=== 2. Wrong inheritance: Stack(list) exposes too much ===")


class BadStack(list):
    def push(self, item):
        self.append(item)


bs = BadStack()
bs.push(1)
bs.push(2)
bs.insert(0, 99)                        # a stack shouldn't allow this!
bs.sort()
print("  BadStack after insert/sort:", bs, "<- inherited methods break the stack's rules")


class Stack:
    def __init__(self):
        self._items = []                # composition: HAS a list

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if not self._items:
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self):
        return self._items[-1] if self._items else None

    def __len__(self):
        return len(self._items)

    def __repr__(self):
        return f"Stack({self._items})"


s = Stack()
for n in (1, 2, 3):
    s.push(n)
print("  Stack:", s, "| pop:", s.pop(), "| peek:", s.peek(), "| len:", len(s))
print("  has insert?", hasattr(s, "insert"), "| has sort?", hasattr(s, "sort"))

print("\n=== 3. Dependency injection makes testing easy ===")


class EmailSender:
    def send(self, to, msg):
        return f"(would really email {to})"


class FakeSender:
    def __init__(self):
        self.sent = []

    def send(self, to, msg):
        self.sent.append((to, msg))
        return "(recorded)"


class OrderService:
    def __init__(self, notifier):
        self.notifier = notifier

    def place(self, customer, item):
        return self.notifier.send(customer, f"Your {item} is confirmed")


print("  production:", OrderService(EmailSender()).place("asha@mail.com", "book"))
fake = FakeSender()
OrderService(fake).place("ravi@mail.com", "pen")
assert fake.sent == [("ravi@mail.com", "Your pen is confirmed")]
print("  test with FakeSender passed; it recorded:", fake.sent)

print("\n=== 4. Composition vs aggregation ===")


class OrderLine:
    def __init__(self, item, qty, price):
        self.item, self.qty, self.price = item, qty, price


class Order:
    def __init__(self):
        self.lines = []                 # composition: Order creates and owns its lines

    def add(self, item, qty, price):
        self.lines.append(OrderLine(item, qty, price))

    def total(self):
        return sum(line.qty * line.price for line in self.lines)


class Player:
    def __init__(self, name):
        self.name = name


class Team:
    def __init__(self, name, players):
        self.name = name
        self.players = players          # aggregation: players exist independently


order = Order()
order.add("pen", 3, 20)
order.add("bag", 1, 900)
print("  order total:", order.total(), "(lines were created inside the order)")
asha, ravi = Player("Asha"), Player("Ravi")
team = Team("Red", [asha, ravi])
del team
print("  team deleted, players still exist:", asha.name, ravi.name)

print("\n=== 5. Delegating everything with __getattr__ ===")


class LoggedList:
    def __init__(self):
        self._items = []
        self.log = []

    def __getattr__(self, name):        # forward unknown attributes to the inner list
        attr = getattr(self._items, name)
        if callable(attr):
            def wrapper(*args):
                self.log.append(f"{name}{args}")
                return attr(*args)
            return wrapper
        return attr


ll = LoggedList()
ll.append(3)
ll.append(1)
ll.sort()
print("  items:", ll._items, "| log:", ll.log)
