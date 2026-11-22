# Lecture 20: The four pillars together (+ SOLID in plain words)

Run: `python lecture.py`

## One example, all four pillars

`lecture.py` builds a small **shape and canvas** program. Every pillar has a clear role:

| Pillar | Big idea | In the code |
|--------|----------|-------------|
| **Encapsulation** | bundle data + methods; hide internals | `Shape` stores dimensions in `_private` attributes behind validated properties; `Canvas` keeps `_shapes` private |
| **Inheritance** | reuse a parent's code | `Square(Rectangle)` reuses everything with `super().__init__(side, side)` |
| **Polymorphism** | same call, different behaviour | `Canvas.total_area()` calls `shape.area()` on any shape; `sorted(shapes)` works through `__lt__` |
| **Abstraction** | show *what*, hide *how* | `Shape(ABC)` declares `area()` and `perimeter()` as abstract; `Canvas` only knows the `Shape` contract |

Plus the supporting tools: properties (07), class methods as alternative constructors (08), magic methods (14–15) and composition (`Canvas` *has* shapes, 18).

## How the pillars relate

```
              Abstraction  ── defines the contract (what)
                   │
   Inheritance ────┼──── classes fulfil the contract (how)
                   │
              Polymorphism ── code uses any class through the contract
                   │
             Encapsulation ── each class protects its own data
```

## SOLID: five design principles in plain words

| Letter | Principle | Plain words | Where you saw it |
|--------|-----------|-------------|------------------|
| **S** | Single Responsibility | one class, one job | `Exporter` formats; `Account` holds money |
| **O** | Open/Closed | add features by **adding classes**, not editing working code | new `Triangle` shape → no change to `Canvas` (13) |
| **L** | Liskov Substitution | a child must work anywhere the parent works | `SavingsAccount.withdraw` keeps the same signature (10) |
| **I** | Interface Segregation | small, focused interfaces beat one huge one | mixins and protocols with one or two methods (12, 16) |
| **D** | Dependency Inversion | depend on abstractions; pass parts in | `OrderService(notifier)` (18), `Checkout(payment: Payment)` (22) |

## OOP design checklist

1. Identify the **nouns** (likely classes) and **verbs** (likely methods) in the problem.
2. Decide what each class **knows** (attributes) and **does** (methods).
3. Make attributes internal (`_x`) and expose a small public interface.
4. Use **inheritance** only for true "is-a" relationships; use **composition** for "has-a".
5. Put shared contracts in an **ABC** (or a Protocol).
6. Add `__repr__` to every class. Debugging becomes much easier.
7. Validate in `__init__` / setters so invalid objects can't exist.

## Exercises

1. Add `Circle(Shape)` and an `Ellipse`. Does any existing code need to change?
2. Add `Canvas.largest(n=2)` using `sorted()` on the shapes.
3. Try to create `Shape()` and a subclass that forgets `perimeter()`.
4. For each SOLID letter, find one more example in Lectures 05–19.

**Next →** [Lecture 21: Project: library manager](../21_project_library_manager/)
