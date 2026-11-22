# Lecture 02 — List vs array: maths behaves differently

Run: `python lecture.py`

This is the first "aha" moment with NumPy: **the same operator means something completely different** for a list and an array.

## The comparison

| Expression | Python list | NumPy array |
|------------|-------------|-------------|
| `x * 2` | Repeats the list twice | Multiplies **every value** by 2 |
| `x + 5` | `TypeError` (can only join lists) | Adds 5 to **every value** |
| `x + y` | Joins them end to end | Adds **matching** values |
| `x > 100` | `TypeError` | One `True`/`False` per value |
| `sum(x) / len(x)` | Works | Works — but `x.mean()` is easier |

## Why?

- **Lists are general-purpose containers.** They can hold text, numbers, other lists. So `+` and `*` were designed for *container* jobs: joining and repeating.
- **Arrays are built for numbers.** Every element is a number of the same type, so operators do *maths* on every element.

```python
prices = [100, 250, 80]
arr = np.array(prices)

prices * 2   # [100, 250, 80, 100, 250, 80]
arr * 2      # [200 500 160]
```

## Introducing vectorization

> **Vectorization** means writing one operation for the whole array instead of a loop over the items.

```python
# list way  (a loop, hidden in a comprehension)
[p * 2 for p in prices]
# NumPy way (no loop in your code)
arr * 2
```

It is the core NumPy habit — and the reason NumPy code is short. Lecture 05 goes deep on it.

## Converting back and forth

```python
arr = np.array(prices)   # list  -> array
back = arr.tolist()      # array -> list (plain Python ints)
```

## Expected output (first part)

```
[100, 250, 80, 100, 250, 80]
[200 500 160]
[100, 250, 80, 5]
[105 255  85]
[200, 500, 160]
```

## Exercises

1. Try `prices + 5`. Read the error — why does Python refuse?
2. Print `arr / 10` and `arr ** 2`.
3. Make `a = np.array([1, 2, 3])` and `b = np.array([10, 20, 30])`. Compute `a + b`, `a * b`, `b / a`.

<details><summary>Solutions</summary>

1. `TypeError: can only concatenate list (not "int") to list` — for lists `+` means *join*, and you can't join a number.
2. `[10. 25.  8.]` and `[10000 62500  6400]`.
3. `[11 22 33]`, `[10 40 90]`, `[10. 10. 10.]`.
</details>

**Next →** [Lecture 03: Why it's fast](../03_why_fast_speed/)
