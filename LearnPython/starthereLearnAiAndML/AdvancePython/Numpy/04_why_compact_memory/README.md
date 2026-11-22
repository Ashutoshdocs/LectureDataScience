# Lecture 04 — Why NumPy is compact: memory

Run: `python lecture.py`

## How a list stores numbers

A Python list doesn't hold numbers directly. It holds **pointers** (memory addresses), and each pointer leads to a full Python `int` object with its own bookkeeping (reference count, type pointer, size, value).

```
Python list → [ ptr | ptr | ptr | … ]      8 bytes per pointer
                 ↓     ↓     ↓
               int    int   int            ~28 bytes per int object
```

## How an array stores numbers

```
NumPy array → [ 0 | 1 | 2 | 3 | … ]        8 bytes each (int64), side by side
```

Just the raw numbers, plus one small header describing shape and dtype.

## Measuring it

| Tool | Gives |
|------|-------|
| `sys.getsizeof(obj)` | bytes for one Python object (a list's size does **not** include the objects it points to) |
| `arr.nbytes` | bytes used by the array's data |
| `arr.itemsize` | bytes per element |
| `arr.size` | number of elements |

> `arr.nbytes == arr.size * arr.itemsize`

## Choosing a smaller dtype

| dtype | Bytes per item | Range |
|-------|----------------|-------|
| `int8` | 1 | −128 … 127 |
| `uint8` | 1 | 0 … 255 (images!) |
| `int16` | 2 | −32 768 … 32 767 |
| `int32` | 4 | about ±2.1 billion |
| `int64` | 8 | about ±9.2 × 10¹⁸ |
| `float32` | 4 | decimals, ~7 digits |
| `float64` | 8 | decimals, ~15 digits |

For a million values, the difference is tens of megabytes. For a billion values, it decides whether your data fits in RAM at all.

## Expected output (64-bit)

```
List of 1000 ints : 36056 bytes
Array of 1000 ints: 8000 bytes
Bytes per item    : 8
As int16          : 2000 bytes
```

## Warning: too small a dtype overflows

```python
np.arange(126, 130, dtype=np.int8)   # [ 126  127 -128 -127]
```
128 doesn't fit in `int8`, so it **wraps around** silently. Pick a dtype big enough for your values (more in Lecture 07).

## Exercises

1. Try `dtype=np.int8`. Print `np.arange(126, 130, dtype=np.int8)`. What happens above 127?
2. Compare list vs array memory for 1 000 000 items.
3. A 1920×1080 colour image has 3 channels. How many bytes as `uint8`? As `float64`?

<details><summary>Solutions</summary>

1. Wraps to −128, −127 (overflow).
2. Roughly 36 MB vs 8 MB (see the last section of `lecture.py`).
3. 1920 × 1080 × 3 = 6 220 800 bytes (~6 MB) as `uint8`; × 8 = ~50 MB as `float64`.
</details>

**Next →** [Lecture 05: Vectorization](../05_vectorization/)
