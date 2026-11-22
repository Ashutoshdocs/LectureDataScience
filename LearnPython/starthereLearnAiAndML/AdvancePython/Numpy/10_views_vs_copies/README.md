# Lecture 10 — Views vs copies (a common trap)

Run: `python lecture.py`

This surprises almost everyone coming from lists.

| | List slice | Array slice |
|---|---|---|
| Creates | a **new list** (copy) | a **view** — a window onto the *same* memory |
| Changing it | leaves the original alone | **changes the original** |

```python
a = np.array([1, 2, 3, 4, 5])
part = a[1:4]     # a VIEW
part[0] = 100
print(a)          # [  1 100   3   4   5]   ← a changed!
```

## Why does NumPy do this?

Copying is slow and uses memory. With a 2 GB array, making a copy on every slice would be a disaster. So NumPy avoids copying unless you ask. That's part of why it is fast — you just need to know about it.

## Step-through

| Line | What happens | `a` |
|------|--------------|-----|
| `a = np.array([1,2,3,4,5])` | original | `[1 2 3 4 5]` |
| `part = a[1:4]` | view of elements 1–3, no new data | `[1 2 3 4 5]` |
| `part[0] = 100` | writes into `a[1]` | `[1 100 3 4 5]` |
| `safe = a[1:4].copy()` | separate data | `[1 100 3 4 5]` |
| `safe[0] = -1` | only `safe` changes | `[1 100 3 4 5]` |

## The rules

| Operation | View or copy? |
|-----------|---------------|
| Basic slice `a[1:4]`, `m[:, 0]` | **view** |
| `.reshape()`, `.T` (usually) | **view** |
| `.copy()` | **copy** |
| Boolean mask `a[a > 2]` | **copy** |
| Fancy index `a[[0, 2]]` | **copy** |
| Arithmetic `a * 2` | new array (copy) |
| `b = a` | **neither** — same object, two names |

Check with `np.shares_memory(a, b)`.

## When to use `.copy()`

When you take a piece of an array and plan to **modify** it while keeping the original intact — e.g. cleaning data, trying "what if" scenarios.

## Exercises

1. Check `np.shares_memory(a, part)` and `np.shares_memory(a, safe)`.
2. Does `b = a` make a copy? Change `b[0]` and print `a`.
3. Is `a[a > 2]` a view? Modify it and check `a`.

<details><summary>Solutions</summary>

1. `True`, `False`.
2. No — `b` is the same array. `a` changes too.
3. No, it's a copy — `a` is unchanged. (But `a[a > 2] = 0` written directly *does* modify `a`, because that's assignment into `a`.)
</details>

**Next →** [Lecture 11: Element-wise maths & ufuncs](../11_elementwise_math_ufuncs/)
