# Lecture 16: Recursion: functions that call themselves

Run: `python lecture.py`

## The idea

A **recursive** function solves a problem by calling **itself** on a **smaller version** of the same problem, until it reaches a case so small the answer is obvious.

Every recursive function needs two parts:

| Part | Role | Factorial example |
|------|------|-------------------|
| **Base case** | the smallest problem, answered directly, with no recursive call | `0! = 1` |
| **Recursive case** | reduce the problem and call yourself | `n! = n × (n−1)!` |

```python
def factorial(n):
    if n == 0:                    # base case: STOP here
        return 1
    return n * factorial(n - 1)   # recursive case: a smaller problem
```

## What happens on the call stack

```
factorial(4)
 = 4 * factorial(3)                   ← waiting
       = 3 * factorial(2)             ← waiting
             = 2 * factorial(1)       ← waiting
                   = 1 * factorial(0) ← waiting
                         = 1          ← base case reached
                   = 1                ← results flow back up
             = 2
       = 6
 = 24
```

Each call waits on the stack (Lecture 02) until the call it made returns. `lecture.py` prints this trace.

## ⚠️ No base case = infinite recursion

Forget the base case, or make a step that doesn't get smaller, and Python stops you:

```
RecursionError: maximum recursion depth exceeded
```

Python's default limit is about **1000** nested calls (`sys.getrecursionlimit()`). So recursion is unsuitable for very deep problems, such as walking a 100,000-item list one element per call.

## Classic recursive problems

| Problem | Base case | Recursive case |
|---------|-----------|----------------|
| `factorial(n)` | `n == 0 → 1` | `n * factorial(n-1)` |
| `sum_list(items)` | empty → 0 | `items[0] + sum_list(items[1:])` |
| `power(b, e)` | `e == 0 → 1` | `b * power(b, e-1)` |
| `reverse(s)` | `len(s) <= 1 → s` | `reverse(s[1:]) + s[0]` |
| `fib(n)` | `n < 2 → n` | `fib(n-1) + fib(n-2)` |
| `binary_search` | range empty → not found | search one half |
| `flatten(nested_list)` | not a list → `[item]` | flatten each element |
| folder sizes / tree walks | a file → its size | sum of children |

## When to use recursion

| ✅ Natural fit | ❌ Prefer a loop |
|---------------|-----------------|
| **tree-shaped / nested data**: folders, JSON, org charts, nested lists | simple counting or walking a flat list |
| divide-and-conquer: binary search, merge sort, quicksort | depth could exceed ~1000 |
| problems defined recursively in maths | performance-critical code (function calls cost time) |

Anything recursive can be written with a loop (plus a stack). Choose whichever is **clearer**.

## Recursion + memoisation

Naive `fib(n)` recomputes the same values exponentially many times (`fib(30)` makes 1.6 million calls). Caching results with `@functools.lru_cache` (Lecture 15) makes it linear.

## Exercises

1. Write `count_down(n)` recursively.
2. Write `sum_digits(n)` → `sum_digits(1234) == 10`.
3. Write `is_palindrome(s)` recursively.
4. Write `flatten([1, [2, [3, 4]], 5])` → `[1, 2, 3, 4, 5]`.
5. Count the calls made by `fib(20)` with and without `lru_cache`.

<details><summary>Solutions</summary>

```python
def sum_digits(n):
    return n if n < 10 else n % 10 + sum_digits(n // 10)

def is_palindrome(s):
    return len(s) <= 1 or (s[0] == s[-1] and is_palindrome(s[1:-1]))
```
</details>

**Next →** [Lecture 17: Generators](../17_generators/)
