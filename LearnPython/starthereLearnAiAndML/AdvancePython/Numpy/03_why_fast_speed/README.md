# Lecture 03 — Why NumPy is fast: the speed race

Run: `python lecture.py`

We square **one million numbers** two ways and time them with `time.perf_counter()` (a precise stopwatch).

```
Python list : ████████████████████████████████████████  ~45 ms
NumPy array : ████                                        ~5 ms
```
(measured on a desktop; your numbers will differ — the *gap* is what matters, usually 10× to 100×)

## Why is NumPy so much faster?

### 1. The loop runs in compiled C, not in Python
The loop still happens — but inside NumPy's pre-compiled C code. Python only issues one instruction: "multiply these". The Python interpreter, which is slow per step, is no longer doing a million steps.

### 2. No type check per item
A list could hold anything, so for every `x * x` Python must ask: *what type is x? does it support `*`? what type is the result?* — a million times.
An array has **one dtype**, so NumPy checks once and then runs a tight loop.

### 3. Packed memory
Array values sit **side by side** in one block of memory. The CPU reads them in fast continuous chunks (cache-friendly) and can even process several at once using **SIMD** instructions (Single Instruction, Multiple Data).

A list stores **pointers** to separate Python objects scattered around memory — the CPU must hop from place to place.

```
list :  [ptr][ptr][ptr][ptr] ...      each ptr → a separate int object somewhere
array:  [ 0 ][ 1 ][ 2 ][ 3 ] ...      raw numbers, contiguous
```

## How to time code properly

```python
import time
t = time.perf_counter()
# ... the code you want to time ...
elapsed = time.perf_counter() - t      # seconds
```

`lecture.py` also uses the `timeit` module, which repeats a test several times and takes the best — more reliable than a single measurement.

## When is NumPy *not* faster?

- For **tiny** arrays (a handful of items), NumPy's setup overhead can make it slower than a list.
- Converting a list to an array costs time too — do it **once**, then stay in NumPy.
- Writing a Python `for` loop **over an array** is *slower* than over a list! The speed comes from vectorized operations, not from the array itself.

## Exercises

1. Change `n` to `5_000_000`. Does the gap grow?
2. Time `sum(nums)` against `arr.sum()` the same way.
3. Time a Python loop over the *array*: `[x * x for x in arr]`. Is it faster or slower than the list loop?

<details><summary>Solutions</summary>

1. Both times grow roughly 5×, the ratio stays similar or grows.
2. `arr.sum()` is typically 10–50× faster than `sum(nums)`.
3. **Slower** — each element is converted into a NumPy scalar object. Lesson: never loop over arrays when a vectorized operation exists. (The last section of `lecture.py` shows this.)
</details>

**Next →** [Lecture 04: Why it's compact](../04_why_compact_memory/)
