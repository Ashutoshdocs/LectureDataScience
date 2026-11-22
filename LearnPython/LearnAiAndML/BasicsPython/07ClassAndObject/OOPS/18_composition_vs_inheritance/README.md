# Lecture 18: Composition vs inheritance

Run: `python lecture.py`

## Two ways to reuse code

| | Inheritance | Composition |
|--|-------------|-------------|
| relationship | **is-a**: a Dog *is an* Animal | **has-a**: a Car *has an* Engine |
| code | `class Dog(Animal):` | `self.engine = Engine()` |
| coupling | tight: the child depends on the parent's internals | loose: the object only uses the part's public methods |
| change at runtime? | no, the parent is fixed | yes, swap the part |
| risk | deep hierarchies, the "fragile base class" problem | a little more code to forward calls |

## Composition: building objects from parts

```python
class Engine:
    def start(self): return "engine roars"

class Car:
    def __init__(self, brand, engine):
        self.brand = brand
        self.engine = engine          # Car HAS an Engine

    def drive(self):
        return f"{self.brand}: {self.engine.start()}"   # DELEGATE part of the job
```

**Delegation** means the outer object passes work to the inner object.

## Why "prefer composition over inheritance"?

Imagine features combined by inheritance: `ElectricCar`, `PetrolCar`, `ElectricAutomaticCar`, `PetrolManualCar`, `HybridAutomaticSunroofCar`… The number of classes **explodes**: 3 engines × 2 gearboxes × 2 roofs = 12 classes.

With composition, you write **3 + 2 + 2 = 7 small parts** and combine them freely:

```python
Car("Tata", engine=ElectricEngine(), gearbox=Automatic(), roof=Sunroof())
```

You can even **swap a part at runtime**: `car.engine = PetrolEngine()`.

This is also **dependency injection**: pass the parts in, rather than creating them inside. Tests can then pass fake parts (a `FakeEmailSender` that just records messages).

## Composition vs aggregation

| Kind | Lifetime | Example |
|------|----------|---------|
| **Composition** (strong) | the part is created and owned by the whole; it dies with it | `Order` creates its `OrderLine`s |
| **Aggregation** (weak) | the part exists independently; the whole only references it | a `Team` holds existing `Player`s; deleting the team doesn't delete the players |

In Python both look like `self.part = ...`. The difference is **who creates and owns** the part.

## Choosing

```
Is "Child is a Parent" true, and will it stay true?
  ├─ yes, and the child can be used anywhere the parent is → inheritance
  └─ no / "has a" / "uses a" / you'd like to swap it → composition
```

Signs that inheritance is wrong:
- the child overrides methods to make them **do nothing** or raise errors
- you inherit just to reuse **one** helper method
- `class Stack(list)` exposes `insert` and `sort`, which a stack shouldn't have

## Exercises

1. Add a `Wheel` class and give each `Car` a list of four wheels (composition).
2. Write `Hybrid` with both an electric and a petrol engine, choosing one by speed.
3. Build `Stack` using composition (`self._items = []`) with only `push`, `pop`, `peek` and `__len__`.
4. Make `OrderService` take a `notifier` parameter. Pass in a fake notifier in a test and check what it received.

**Next →** [Lecture 19: Dataclasses](../19_dataclasses/)
