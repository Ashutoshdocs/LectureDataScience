# Lecture 05: Instance methods & `self`

Run: `python lecture.py`

## What is an instance method?

The "normal" kind of method: a function defined inside a class whose **first parameter is `self`**.

```python
class Greeter:
    def hello(self):
        print("Hello from a method!")

    def hello_name(self, name):
        print("Hello,", name)

g = Greeter()
g.hello()               # no arguments
g.hello_name("Asha")    # one argument
```

You **never pass `self` yourself**. Python fills it in with the object before the dot:

| You write | Python actually runs |
|-----------|----------------------|
| `g.hello()` | `Greeter.hello(g)` |
| `g.hello_name("Asha")` | `Greeter.hello_name(g, "Asha")` |

So a method declared with 2 parameters (`self, name`) is called with **1** argument.

## What `self` really is

`self` is just a parameter holding **the object the method is working on**. Through `self` a method can read and create that object's attributes:

```python
class Light:
    def turn_on(self):
        self.on = True            # store on THIS object

    def status(self):
        print("on?", self.on)     # read from THIS object

kitchen = Light()
hall = Light()
kitchen.turn_on()                 # self is kitchen
Light.turn_on(hall)               # the long way: self is hall
```

One method definition serves **every** object. While `kitchen.turn_on()` runs, `self` *is* `kitchen`; while `hall`'s runs, `self` *is* `hall`. You can check this: `id(self) == id(kitchen)`.

> `self` is a **convention**, not a keyword. Python would accept any name, but every Python programmer expects `self`. Use it.

## Instance methods can use everything

| Inside an instance method you can use… | How |
|----------------------------------------|-----|
| the object's attributes | `self.name` |
| other methods of the object | `self.other_method()` |
| class attributes | `self.PI` or `ClassName.PI` |
| parameters & local variables | `name`, `total` |
| global variables & functions | `TAX_RATE`, `helper()` |

That makes them the **most common** kind of method: use one whenever the code needs **this object's data**.

## ⚠️ Forgetting `self`

```python
class Calc:
    def add(a, b):              # forgot self!
        return a + b

Calc.add(2, 3)                  # works: 5 (no object involved)
Calc().add(2, 3)                # TypeError: Calc.add() takes 2 positional arguments but 3 were given
```

Through an object, Python inserts the object as the first argument, so it calls `Calc.add(obj, 2, 3)`: three arguments for two parameters.

> `TypeError: … takes N positional arguments but N+1 were given` almost always means **you forgot `self`**.

If a method really doesn't need the object, make it a **`@staticmethod`** (Lecture 10) instead of leaving `self` out.

## Bound methods

`g.hello` without brackets is a **bound method**: the function plus the object it's attached to. You can store it and call it later; it remembers its object:

```python
say = g.hello_name
say("Ravi")          # still uses g as self
```

## Exercises

1. Add a `turn_off` method to `Light` and call it on `hall` only.
2. Create a third light and call `status()` before `turn_on()`. What breaks, and why?
3. Fix `Calc.add` by adding `self`. Then how do you call it through the class?

<details><summary>Solutions</summary>

2. `AttributeError: 'Light' object has no attribute 'on'`. The attribute is only created by `turn_on`. (Lecture 07's constructor fixes this by setting `self.on = False` at creation.)
3. `Calc.add(Calc(), 2, 3)`, or better, `Calc().add(2, 3)`.
</details>

**Next →** [Lecture 06: Return values, chaining & global functions](../06_methods_return_values_and_chaining/)
