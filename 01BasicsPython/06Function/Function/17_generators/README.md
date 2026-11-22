# Lecture 17: Generators: functions that `yield`

Run: `python lecture.py`

## The idea

A normal function **returns once** and is done. A **generator function** contains `yield`. It produces values **one at a time**, pausing after each one and resuming where it left off when the next value is requested.

```python
def count_up_to(n):
    i = 1
    while i <= n:
        yield i          # hand out one value, then PAUSE here
        i += 1

for x in count_up_to(3):
    print(x)             # 1, 2, 3
```

Calling `count_up_to(3)` **doesn't run the body**. It returns a **generator object**. The body runs bit by bit as you ask for values (`for`, `next()`, `list()`).

```
 gen = count_up_to(3)    → nothing runs yet
 next(gen)  → runs until the 1st yield → 1   (paused)
 next(gen)  → resumes, runs to next yield → 2
 next(gen)  → 3
 next(gen)  → body ends → StopIteration (a for loop handles this for you)
```

## `return` vs `yield`

| `return` | `yield` |
|----------|---------|
| gives back **one** value and ends | gives back **many** values over time |
| function state is thrown away | state (local variables, position) is **kept** between values |
| builds the whole result in memory | produces values **lazily**, on demand |

## Why generators? Memory & laziness

```python
squares_list = [n * n for n in range(10_000_000)]   # ~80+ MB in memory, computed up front
squares_gen  = (n * n for n in range(10_000_000))   # ~200 bytes; computes as you go
```

| ✅ Use a generator when… | ❌ Use a list when… |
|--------------------------|--------------------|
| the data is huge or **infinite** (sensor readings, IDs, log lines) | you need `len()`, indexing `[i]`, or slicing |
| you process items one by one (a pipeline) | you need to loop over the data **several times** |
| you may stop early (first match) | the data is small anyway |
| reading big files line by line | |

> A generator can be consumed **only once**. After it's exhausted, it yields nothing more.

## Generator expressions

Like a list comprehension, but with **round brackets**: lazy, no list built:

```python
total = sum(n * n for n in range(1_000_000))       # no list in memory
any(line.startswith("ERROR") for line in log)      # stops at the first match
```

## Pipelines: chaining generators

Each stage pulls one item at a time from the previous stage, like water through pipes:

```python
lines   = read_lines(path)                     # yields raw lines
records = (parse(l) for l in lines)            # yields dicts
errors  = (r for r in records if r["level"] == "ERROR")
for e in errors: ...                           # only now does anything run, one line at a time
```

## `yield from`

Delegate to another iterable or generator:

```python
def flatten(nested):
    for item in nested:
        if isinstance(item, list):
            yield from flatten(item)     # yield everything the inner generator yields
        else:
            yield item
```

## Exercises

1. Write `evens(limit)` that yields even numbers up to `limit`.
2. Write an infinite `fibonacci()` generator and take the first 10 values with `itertools.islice`.
3. Compare `sys.getsizeof` of a list vs a generator of a million squares.
4. Build a 3-stage pipeline: numbers → squares → only those ending in 6.

<details><summary>Solutions</summary>

```python
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

list(itertools.islice(fibonacci(), 10))
```
</details>

**Next →** [Lecture 18: Errors in functions](../18_errors_in_functions/)
