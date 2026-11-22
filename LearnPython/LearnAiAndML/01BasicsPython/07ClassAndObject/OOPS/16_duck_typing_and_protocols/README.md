# Lecture 16: Duck typing & protocols

Run: `python lecture.py`

## "If it walks like a duck and quacks like a duck…"

Python doesn't check an object's **class** before calling a method. It just **tries the call**. Any object with the right method works, even if the classes share no parent:

```python
class Duck:
    def speak(self): return "Quack"

class Robot:
    def speak(self): return "Beep"

for thing in [Duck(), Robot()]:
    print(thing.speak())       # works for both: no common base class needed
```

This is **duck typing**: what matters is **what an object can do**, not **what it is**.

## You use duck typing every day

| Function / syntax | Accepts anything that… |
|-------------------|------------------------|
| `for x in obj` | has `__iter__` (or `__getitem__`) |
| `len(obj)` | has `__len__` |
| `with obj:` | has `__enter__` and `__exit__` |
| `json.dump(data, f)` | `f` has a `.write()` method (a file, `io.StringIO`, a socket wrapper…) |
| `sorted(items)` | items support `<` |

That's why a function written for files also works with `io.StringIO` in tests: it only needs `.write()`.

## The catch: errors appear at runtime

If an object lacks the method, you only find out **when that line runs**:

```
AttributeError: 'Stone' object has no attribute 'speak'
```

### Two styles of handling it

| LBYL: "Look Before You Leap" | EAFP: "Easier to Ask Forgiveness than Permission" |
|------------------------------|---------------------------------------------------|
| `if hasattr(thing, "speak"): thing.speak()` | `try: thing.speak()` `except AttributeError: ...` |
| explicit check first | just try it; handle failure |
| can be wrong if the attribute exists but isn't callable | the most Pythonic style |

`callable(getattr(obj, "speak", None))` checks that the method exists and can be called.

## Protocols: duck typing with type hints

Since Python 3.8, `typing.Protocol` describes "anything with these methods", so **type checkers** (mypy, IDEs) can catch mistakes **before** running:

```python
from typing import Protocol

class Speaker(Protocol):
    def speak(self) -> str: ...

def announce(s: Speaker) -> None:      # mypy accepts Duck and Robot, rejects Stone
    print(s.speak())
```

- Classes **don't inherit** from the protocol. They just need to match it ("structural typing").
- Add `@runtime_checkable` to allow `isinstance(obj, Speaker)` checks. These only check that the method **names** exist, not their signatures.

## Duck typing vs inheritance vs ABCs

| | Duck typing | Inheritance | Abstract base class (Lecture 17) |
|--|-------------|-------------|----------------------------------|
| needs a common parent | ❌ | ✅ | ✅ |
| checked | at runtime, when called | n/a | when **creating** the object |
| shares code | ❌ | ✅ | ✅ |
| flexibility | highest | medium | lower, but safest |
| best for | small interfaces, third-party objects | real "is-a" families | frameworks / plugins that **must** implement certain methods |

## Exercises

1. Fix the `Stone` loop with EAFP, then with LBYL.
2. Write `save_report(lines, out)` that calls `out.write(...)`. Pass it a real file **and** an `io.StringIO`.
3. Define a `Drawable` protocol with `draw() -> str`. Write two classes that satisfy it without inheriting.
4. Use `@runtime_checkable` and test `isinstance` for three objects.

**Next →** [Lecture 17: Abstract classes](../17_abstract_classes/)
