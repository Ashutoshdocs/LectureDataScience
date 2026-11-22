# Lecture 10: `@staticmethod`: helpers inside a class

Run: `python lecture.py`

## What is a static method?

A plain function that **lives inside a class**. It receives **no `self` and no `cls`**, only the arguments you pass:

```python
class MathTools:
    @staticmethod
    def is_even(n):
        return n % 2 == 0

MathTools.is_even(10)      # True: no object needed
```

| | Instance method | Class method | **Static method** |
|---|---|---|---|
| Decorator | none | `@classmethod` | **`@staticmethod`** |
| Gets automatically | `self` | `cls` | **nothing** |
| Can read object data | ✅ | ❌ | ❌ |
| Can read class data | ✅ | ✅ | only by writing `ClassName.x` |
| Typical job | behaviour of one object | class-wide data, factories | **utility / helper** |

## Why not just write a global function?

Because it **belongs with the class**:

- **Organisation:** `Account.valid_pin` says clearly "this is part of how accounts work". It's easy to find and auto-complete.
- **The class itself can use it**, for example to validate in `__init__`.
- **Namespacing:** two classes can each have their own `validate` without a name clash.
- **Callable without an object:** check a PIN before creating an account.

```python
class Account:
    def __init__(self, pin):
        if not Account.valid_pin(pin):          # the class uses its own helper
            raise ValueError("PIN must be 4 digits")
        self.pin = pin

    @staticmethod
    def valid_pin(pin):
        return len(pin) == 4 and pin.isdigit()

Account.valid_pin("12a4")     # False, without creating an account
```

Inside the class you can call it as `Account.valid_pin(...)` or `self.valid_pin(...)`. Both work.

## Common use cases

| Use case | Example |
|----------|---------|
| **Validation** | `Account.valid_pin("1234")`, `User.is_valid_email(text)` |
| **Unit conversion** | `Temperature.c_to_f(30)` |
| **Formatting** | `Product.rupees(1770)` → `"Rs 1,770.00"` |
| **Pure calculations** | `Geometry.distance(p1, p2)` |
| **Parsing helpers** used by factories | `Date.parse_parts("10-11-2026")` |

## Static method vs global function: a guide

| Use a static method when… | Use a global function when… |
|---------------------------|-----------------------------|
| the logic is about this class's domain | the logic is general (used by many unrelated classes/scripts) |
| it doesn't need object or class data | it works with several unrelated objects |
| you want it grouped and discoverable with the class | it's a small script and there's no class |

## ⚠️ Mistakes

- **Using `self` inside a static method** → `NameError`. If you need the object, make it an instance method.
- **Needing class data** but writing `MyClass.x` inside a static method works, but a `@classmethod` with `cls.x` is cleaner.
- **Forgetting the decorator** and leaving out `self`: works through the class but fails through an object (Lecture 05).

## Exercises

1. Add `MathTools.cube(n)` and `MathTools.is_prime(n)`.
2. Add `Temperature.f_to_c(f)` and use it in a class method `from_fahrenheit(cls, f)`.
3. Try `Account("12")` and read the error.

<details><summary>Solutions</summary>

```python
@staticmethod
def f_to_c(f):
    return (f - 32) * 5 / 9

@classmethod
def from_fahrenheit(cls, f):
    return cls(cls.f_to_c(f))
```
</details>

**Next →** [Lecture 11: Choosing the right function type](../11_choosing_the_right_function_type/)
