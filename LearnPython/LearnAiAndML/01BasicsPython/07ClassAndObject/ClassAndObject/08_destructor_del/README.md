# Lecture 08: The destructor `__del__`

Run: `python lecture.py`

## What is a destructor?

The opposite of a constructor. Python calls **`__del__`** just before an object is destroyed, giving it a last chance to clean up: close a file, release a connection, log a message.

| | `__init__` (constructor) | `__del__` (destructor) |
|---|---|---|
| Runs when | the object is **created** | the object is about to be **destroyed** |
| Job | set up attributes | clean up resources |
| Parameters | `self` + any arguments | **only `self`** |
| Called by | `ClassName(...)` | Python, when the last reference disappears |

```python
class File:
    def __init__(self, name):
        self.name = name
        print("Opened", name)

    def __del__(self):
        print("Closed", self.name)

f = File("notes.txt")      # Opened notes.txt
del f                      # Closed notes.txt
```

## When exactly is it called? Reference counting

`del f` deletes a **name**, not an object. Python (CPython) keeps a **reference count** for every object, meaning how many names, lists, attributes and so on point to it. The destructor runs when that count drops to **zero**.

| Situation | Destroyed? |
|-----------|-----------|
| `b = a` then `del a` | ❌ `b` still refers to it |
| …then `del b` | ✅ last reference gone |
| `c = Res("C")` then `c = Res("D")` | ✅ C dies when `c` is rebound |
| object stored only in a list, then `list.clear()` | ✅ |
| object created in a function's **local** variable | ✅ when the function returns |
| object stored in a **global** variable | at `del` or when the program ends |
| object **returned** from a function and stored | ❌ still referenced by the caller |
| two objects referring to **each other** (a cycle) | later, by the garbage collector |

```
 create (__init__)  →  use (methods)  →  last reference gone  →  destroy (__del__)
```

> The exact timing is a CPython detail. Objects caught in reference cycles are cleaned up later by the garbage collector (`gc.collect()`). **Never rely on precisely *when* `__del__` runs.**

## Using destructors safely

1. **Give the class an explicit cleanup method** (`close()`) and call it yourself.
2. Let `__del__` be only a **safety net** that calls the same cleanup.
3. Make cleanup **safe to run twice** (track a flag like `self.open`).
4. Keep `__del__` **short**. Exceptions inside it are printed as warnings and otherwise ignored.
5. **`__del__` runs even if `__init__` raised an error**, on a half-built object. Don't assume every attribute exists; use `getattr(self, "x", default)` (Lecture 11 shows a counter that goes wrong without this).

```python
class Conn:
    def __init__(self, name):
        self.name, self.open = name, True

    def close(self):
        if self.open:
            self.open = False
            print("disconnect", self.name)

    def __del__(self):
        self.close()          # safety net
```

## The better tool: `with` (context managers)

For guaranteed cleanup at a precise moment, Python's answer is the `with` statement. A class becomes usable with `with` by defining two more special methods:

```python
class Conn:
    def __enter__(self):
        return self                       # value bound by "as"
    def __exit__(self, exc_type, exc, tb):
        self.close()                      # ALWAYS runs, even after an error

with Conn("db") as c:
    ...                                   # closed right here, guaranteed
```

`with open("file.txt") as f:` works exactly this way.

## Exercises

1. Move `del f` to after the last print and watch the order change.
2. Make `work()` **return** its local object and store it: `x = work()`. Does the object still die at the end of the function?
3. Remove the explicit `close()` call. Who closes the connection now?
4. Use the `Conn` class in a `with` block that raises an error inside. Is it still closed?

<details><summary>Solutions</summary>

2. No. The caller's `x` keeps it alive.
3. The destructor's safety net, when the object is destroyed.
4. Yes. `__exit__` runs even when an exception happens (section 5 of `lecture.py`).
</details>

**Next →** [Lecture 09: `@classmethod` & `cls`](../09_classmethod_and_cls/)
