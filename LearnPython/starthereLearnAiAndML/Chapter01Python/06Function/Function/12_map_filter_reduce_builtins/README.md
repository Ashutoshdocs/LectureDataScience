# Lecture 12: map, filter, reduce & the function-friendly built-ins

Run: `python lecture.py`

## `map(func, iterable)`: transform every item

```python
list(map(str.upper, ["a", "b"]))           # ['A', 'B']
list(map(int, ["1", "2", "3"]))            # [1, 2, 3]: common for parsing input
list(map(lambda a, b: a + b, [1, 2], [10, 20]))   # [11, 22]: several iterables
```

## `filter(func, iterable)`: keep items where func is truthy

```python
list(filter(str.isdigit, ["12", "ab", "7"]))      # ['12', '7']
list(filter(None, [0, 1, "", "x", None]))         # [1, 'x']: None means "keep truthy"
```

## `functools.reduce(func, iterable, start)`: combine everything into one value

```python
from functools import reduce
reduce(lambda acc, x: acc + x, [1, 2, 3, 4], 0)   # ((((0+1)+2)+3)+4) = 10
```

```
 acc=0 ─(+1)→ 1 ─(+2)→ 3 ─(+3)→ 6 ─(+4)→ 10
```

> Most reductions already have a built-in: `sum`, `max`, `min`, `any`, `all`, `math.prod`, `"".join`. Use `reduce` only when none fits.

## They're lazy

`map` and `filter` return **iterators**: nothing is computed until you loop over them (or call `list()`), and they can be consumed only **once**.

```python
m = map(str.upper, ["a", "b"])
list(m)    # ['A', 'B']
list(m)    # []  ← already used up
```

## map/filter vs list comprehensions

```python
[x * 2 for x in nums if x > 0]               # comprehension: usually clearer
list(map(lambda x: x * 2, filter(lambda x: x > 0, nums)))   # same result, harder to read
```

| Prefer a comprehension when… | Prefer map/filter when… |
|------------------------------|-------------------------|
| you'd need a `lambda` | you already have a **named** function: `map(int, parts)`, `filter(str.isdigit, s)` |
| you combine transform + condition | you want lazy processing of a huge stream |

## Function-friendly built-ins

| Built-in | Does | Example |
|----------|------|---------|
| `sorted(it, key=, reverse=)` | new sorted list | `sorted(students, key=lambda s: s[1], reverse=True)` |
| `max(it, key=)`, `min(it, key=)` | best item by a rule | `max(words, key=len)` |
| `sum(it, start)` | total | `sum(p.price for p in cart)` |
| `any(it)` | at least one truthy? | `any(m < 40 for m in marks)` |
| `all(it)` | all truthy? | `all(isinstance(x, int) for x in data)` |
| `zip(a, b, …)` | pair up items | `dict(zip(names, marks))` |
| `enumerate(it, start=0)` | (index, item) pairs | `for i, name in enumerate(names, 1):` |
| `reversed(seq)` | iterate backwards | `list(reversed(nums))` |
| `len`, `abs`, `round`, `isinstance`, `callable` | everyday helpers | `callable(print)` → True |

`any` and `all` **short-circuit**: they stop as soon as the answer is known.

## Exercises

1. Convert `"3 8 1 9"` into a list of ints using `split` and `map`.
2. Keep only valid emails (containing `@`) with `filter`.
3. Use `reduce` to find the product of `[1, 2, 3, 4, 5]`, then do it with `math.prod`.
4. Build `{name: marks}` from two lists with `zip`, and print a numbered list with `enumerate`.
5. Check whether any student failed and whether all passed.

<details><summary>Solutions</summary>

```python
list(map(int, "3 8 1 9".split()))
list(filter(lambda e: "@" in e, emails))
reduce(lambda a, b: a * b, [1, 2, 3, 4, 5]); math.prod([1, 2, 3, 4, 5])
```
</details>

**Next →** [Lecture 13: Nested functions & closures](../13_nested_functions_and_closures/)
