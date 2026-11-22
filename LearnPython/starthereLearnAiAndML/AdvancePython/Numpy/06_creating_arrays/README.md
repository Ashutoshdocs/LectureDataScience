# Lecture 06 — Creating arrays

Run: `python lecture.py`

## 1. From a list: `np.array()`

NumPy looks at the values and picks **one dtype** that fits them all.

| You give | dtype chosen | Printed as |
|----------|-------------|------------|
| Whole numbers | `int64` | `[10 20 30 40]` |
| Decimals | `float64` | `[1.5 2.5 3.5]` |
| Ints and floats mixed | `float64` | `[1.  2.5 3. ]` |
| `True`/`False` | `bool` | `[ True False  True]` |
| Any string | `<U…` (text) | `['1' '2' '3']` |

> **Upcasting:** when types are mixed, NumPy converts everything to the "bigger" type so nothing is lost: bool → int → float → string.

Force a type with `dtype=`: `np.array([1, 2, 3], dtype=float)` → `[1. 2. 3.]`.

## 2. Filled arrays: `zeros`, `ones`, `full`, `empty`

Use these when you know the **size** before you know the values.

| Function | Creates | Default dtype |
|----------|---------|---------------|
| `np.zeros(n)` | n zeros | float |
| `np.ones(n)` | n ones | float |
| `np.full(n, value)` | n copies of value | type of value |
| `np.empty(n)` | n *uninitialised* slots (fast, garbage values) | float |
| `np.zeros_like(a)` | zeros with the same shape/dtype as `a` | same as `a` |

> ⚠️ **2D needs a tuple:** `np.zeros((2, 3))` — double brackets. `np.zeros(2, 3)` is an error because the 2nd argument is the dtype.

## 3. Ranges: `arange` vs `linspace`

| | `np.arange(start, stop, step)` | `np.linspace(start, stop, count)` |
|---|---|---|
| You choose | the **step size** | **how many** values |
| `stop` | **excluded** (like `range`) | **included** |
| Best for | counting | dividing an interval into equal parts (e.g. points for a graph) |

```python
np.arange(0, 20, 5)       # [ 0  5 10 15]
np.linspace(0, 10, 5)     # [ 0.   2.5  5.   7.5 10. ]
```

> ⚠️ Float steps with `arange` can give surprising lengths due to rounding (`np.arange(0, 1, 0.1)` may or may not include ~1.0). Prefer `linspace` for decimals.

## 4. Special matrices

| Function | Gives |
|----------|-------|
| `np.eye(n)` | identity matrix (1s on the diagonal) |
| `np.diag([4, 5, 6])` | your values on the diagonal |
| `np.tri(n)` | lower-triangle of 1s |

(Random arrays get their own lecture: 17.)

## Exercises

1. Create a 3 × 3 array full of `-1`.
2. Make `np.zeros(4, dtype=bool)`. What do zeros look like as booleans?
3. Odd numbers 1 to 19 with `arange`.
4. 11 values from 0 to 1 with `linspace`.

<details><summary>Solutions</summary>

```python
np.full((3, 3), -1)
np.zeros(4, dtype=bool)        # [False False False False]
np.arange(1, 20, 2)
np.linspace(0, 1, 11)          # [0.  0.1 0.2 ... 1. ]
```
</details>

**Next →** [Lecture 07: Shape & dtype](../07_shape_and_dtype/)
