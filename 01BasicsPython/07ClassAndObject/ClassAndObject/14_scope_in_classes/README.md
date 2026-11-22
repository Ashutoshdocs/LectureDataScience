# Lecture 14: Scope in classes

Run: `python lecture.py`

## Two separate lookup systems

This is the single most useful fact about scope and classes:

| You write | Lookup system | Searches |
|-----------|---------------|----------|
| a **plain name**: `x` | **LEGB scopes** | Local → Enclosing → Global → Built-in |
| a **dotted name**: `obj.x` | **attribute lookup** | the object → its class → `AttributeError` |

Keep them apart and most confusion disappears.

## 1. Local variables vs `self` attributes

```python
class Cart:
    def __init__(self):
        self.total = 0                 # attribute: lives on the object

    def add(self, price, qty):         # price, qty: local (parameters)
        cost = price * qty             # cost: local, gone when add() returns
        self.total += cost             # attribute: survives between calls
```

| | Local variable | Instance attribute |
|---|---|---|
| Written as | `cost = …` (and parameters) | `self.total = …` |
| Lives in | this one method call | the object |
| Lifetime | until the method returns | as long as the object |
| Visible to other methods | ❌ | ✅ |

Common bug: writing `total = self.total + cost` (no `self.`). It creates a local and the attribute never changes.

## 2. Global variables inside methods

Methods follow the same rules as functions:
- **Reading** a global needs nothing.
- **Assigning** to a global needs `global name`. Otherwise Python makes it local and you get `UnboundLocalError`.

```python
visitors = 0

class Gate:
    def enter(self):
        global visitors
        visitors += 1
```

> Better design: keep such data on the class (`Gate.visitors`) instead of in a global.

## 3. ⚠️ Class-body names are NOT visible inside methods

```python
class Circle:
    PI = 3.14159
    label = "pi is " + str(PI)          # ✅ inside the class BODY, earlier names work

    def area(self, r):
        return PI * r * r               # ❌ NameError: name 'PI' is not defined
```

The class body is **not** part of LEGB for methods. Inside a method, reach class attributes through:
- `self.PI`: checks the object, then the class
- `Circle.PI`: goes straight to the class
- `cls.PI`: inside a `@classmethod`

And if a **global** `PI = 3` exists, the bare `PI` silently uses *that one*. That's even more dangerous than an error.

## 4. Attribute lookup order (dotted names)

```
 obj.x  →  1. obj.__dict__  →  2. type(obj).__dict__  →  3. AttributeError
```

Properties (Lecture 13) are found on the class at step 2 and take priority over the instance dict, which is how they can intercept `obj.x`.

## 5. Puzzle: the same name at every level

```python
x = "global"

class Demo:
    x = "class"

    def __init__(self):
        self.x = "instance"

    def show(self):
        x = "local"
        print(x)                 # local
        print(self.x)            # instance
        print(Demo.x)            # class
        print(globals()["x"])    # global
```

| Written as | Lives in | Created by | Lifetime |
|------------|----------|-----------|----------|
| `x` in the method | local scope of `show` | `x = "local"` | one call |
| `self.x` | the object | `__init__` | the object's life |
| `Demo.x` | the class | class body | the program |
| `x` at top level | global scope | line 1 | the program |

**The prefix decides which variable you get:** nothing = LEGB, `self.` = object (then class), `ClassName.` = class.

## 6. Scope of the three method kinds

| Inside… | can use `self.x` | can use `cls.x` | can use `ClassName.x` | can use globals |
|---------|------------------|-----------------|-----------------------|-----------------|
| instance method | ✅ | n/a (use `type(self).x`) | ✅ | ✅ |
| class method | ❌ | ✅ | ✅ | ✅ |
| static method | ❌ | ❌ | ✅ | ✅ |

## Exercises

1. Add `print(cost)` at the end of the Cart example. What error?
2. Rewrite the visitor counter as a class attribute with no `global`.
3. Add a global `PI = 3` and call `broken_area`. What does it return, and why is that dangerous?
4. In the puzzle, delete `x = "local"`. What does the first print show? Then delete `self.x = …`. What does `self.x` show?

<details><summary>Solutions</summary>

1. `NameError: name 'cost' is not defined`.
3. It silently uses 3, a wrong answer with no error.
4. "global"; then "class".
</details>

**Next →** [Lecture 15: Special (dunder) methods](../15_special_methods/)
