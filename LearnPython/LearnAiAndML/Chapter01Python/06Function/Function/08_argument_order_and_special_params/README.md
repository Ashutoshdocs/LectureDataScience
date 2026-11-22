# Lecture 08: Argument order & special parameters (`/` and `*`)

Run: `python lecture.py`

## The full parameter order

When a function uses several kinds of parameters, they **must** appear in this order:

```python
def f(pos_only, /, normal, default=1, *args, kw_only, kw_default=2, **kwargs):
       │         │    │        │          │      │         │            │
       │         │    │        │          │      │         │            └ 6. **kwargs (extra keyword args)
       │         │    │        │          │      └─────────┴──────────── 5. keyword-only (after * or *args)
       │         │    │        │          └──────────────────────────── 4. *args (extra positional args)
       │         │    └────────┴─────────────────────────────────────── 2-3. normal, then with defaults
       │         └─────────────────────────────────────────────────── the / marker
       └───────────────────────────────────────────────────────────── 1. positional-only
```

Short version to memorise: **positional-only → normal → defaults → `*args` → keyword-only → `**kwargs`**.

## Keyword-only parameters: the bare `*`

A bare `*` (or `*args`) in the signature means: **everything after must be passed by keyword**.

```python
def transfer(amount, *, from_acct, to_acct):
    ...

transfer(500, from_acct="A1", to_acct="B2")     # ✅ clear
transfer(500, "A1", "B2")                        # ❌ TypeError
```

**Why?** To prevent mix-ups of similar arguments, and to make calls self-documenting. Especially useful for **boolean flags**: `save(data, overwrite=True)` instead of the mysterious `save(data, True)`.

## Positional-only parameters: `/`

Everything **before** `/` must be passed **by position**. Keywords aren't allowed:

```python
def area(width, height, /):
    return width * height

area(3, 4)                  # ✅
area(width=3, height=4)     # ❌ TypeError
```

**Why?**
- The parameter names are **implementation details** you want freedom to rename later.
- The names wouldn't be meaningful to callers (`len(obj)`, `pow(x, y)`).
- It leaves those names free for `**kwargs`.

Many built-ins are positional-only. `help(len)` shows `len(obj, /)`.

## Arguments in a call

In a **call**: positional arguments (and `*iterable`) first, then keyword arguments (and `**dict`):

```python
f(1, 2, *more, key=3, **options)
```

## How Python matches arguments to parameters

1. Positional arguments fill parameters left to right.
2. Extra positional arguments go into `*args` (or `TypeError` if there's none).
3. Keyword arguments fill parameters by name.
4. Extra keyword arguments go into `**kwargs` (or `TypeError`).
5. Unfilled parameters use their defaults (or `TypeError: missing ... argument`).

## Quick reference

| Syntax | Meaning |
|--------|---------|
| `def f(a, b)` | normal: by position or keyword |
| `def f(a, b=2)` | `b` optional |
| `def f(a, /, b)` | `a` positional-only |
| `def f(a, *, b)` | `b` keyword-only |
| `def f(*args)` | any number of positional → tuple |
| `def f(**kwargs)` | any number of keyword → dict |
| `f(*seq)` | unpack a sequence into positional arguments |
| `f(**mapping)` | unpack a dict into keyword arguments |

## Exercises

1. Write `connect(host, port=5432, *, timeout=10, ssl=True)` and call it several ways.
2. Make `divide(a, b, /)` positional-only and try calling it with keywords.
3. Predict which parameter gets which value in `f(1, 2, 3, 4, x=5, y=6)` for `def f(a, b=0, *args, x, **kw)`.

<details><summary>Solutions</summary>

3. `a=1, b=2, args=(3, 4), x=5, kw={'y': 6}`.
</details>

**Next →** [Lecture 09: Type hints & docstrings](../09_type_hints_and_docstrings/)
