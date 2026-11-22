# Lecture 07 — Shape & dtype

Run: `python lecture.py`

## Dimensions (axes)

| Name | Looks like | Example shape |
|------|-----------|---------------|
| 1D · vector | a row of values | `(5,)` |
| 2D · matrix | a table: rows × columns | `(2, 3)` |
| 3D · tensor | a stack of tables | `(2, 2, 2)` |

> **Trick:** count the opening brackets at the start of the printout. `[` = 1D, `[[` = 2D, `[[[` = 3D.

Read a 2D shape `(2, 3)` as **(rows, columns)**. A 1D shape `(5,)` has a trailing comma because it's a one-item tuple.

> ⚠️ Every row must be the same length. `np.array([[1, 2], [3]])` raises `ValueError` — the shape would be "ragged".

Real-world shapes:
- Greyscale photo: `(height, width)`
- Colour photo: `(height, width, 3)` — red, green, blue
- 32 colour photos in a batch: `(32, height, width, 3)`

## Array attributes (no brackets!)

| Attribute | Meaning | For `[[1,2,3],[4,5,6]]` |
|-----------|---------|-------------------------|
| `.ndim` | number of dimensions | 2 |
| `.shape` | size along each dimension | (2, 3) |
| `.size` | total elements | 6 |
| `.dtype` | element type | int64 |
| `.itemsize` | bytes per element | 8 |
| `.nbytes` | total bytes = size × itemsize | 48 |
| `len(m)` | length of the **first** axis only | 2 |

> ⚠️ `m.shape()` → `TypeError: 'tuple' object is not callable`. Attributes are stored values, not functions.

## Converting type: `.astype()`

Because every element shares one dtype, changing type means converting the **whole** array. `.astype()` returns a **new** array.

| Conversion | What happens |
|------------|--------------|
| float → int | decimals are **cut off** toward zero (1.7 → 1, −3.9 → −3) |
| text → int/float | works if every string looks like a number |
| number → bool | 0 → `False`, anything else → `True` |
| bool → int | `False` → 0, `True` → 1 |

Round first if you want the nearest integer: `a.round().astype(int)`.

Text arrays have dtypes like `<U2` = Unicode text, up to 2 characters each.

## Overflow — the silent bug

Python ints never overflow. NumPy ints have a **fixed size**:

```python
tiny = np.array([126, 127], dtype=np.int8)
tiny + 1      # [ 127 -128]   ← 127 + 1 wrapped around!
```

No error, no warning. Choose a dtype large enough for your values (the default `int64` is safe for nearly everything).

## Exercises

1. Make a 4 × 2 array and check its shape.
2. Check every property of `np.zeros((3, 4, 5))`.
3. Predict `nbytes` of a 100 × 100 `float32` array, then check.
4. `np.array(["1.5", "2"]).astype(float)` — what do you get?
5. Change `np.int8` to `np.int16` in the overflow example.

<details><summary>Solutions</summary>

1. `np.arange(8).reshape(4, 2).shape` → `(4, 2)`
2. ndim 3, shape (3, 4, 5), size 60, dtype float64, itemsize 8, nbytes 480
3. 100 × 100 × 4 = 40 000
4. `[1.5 2. ]`
5. `[127 128]` — no overflow, int16 goes up to 32 767.
</details>

**Next →** [Lecture 08: Indexing & slicing](../08_indexing_and_slicing/)
