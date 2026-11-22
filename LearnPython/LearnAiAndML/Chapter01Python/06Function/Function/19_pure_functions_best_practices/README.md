# Lecture 19: Pure functions & best practices

Run: `python lecture.py`

## Pure vs impure functions

A **pure function**:
1. returns a result that depends **only on its arguments** (same input → same output, every time), and
2. has **no side effects**: it doesn't change anything outside itself (no globals, no modifying arguments, no printing, no files).

```python
def add_tax(price, rate):           # PURE
    return price * (1 + rate)

total = 0
def add_to_total(x):                # IMPURE: changes a global
    global total
    total += x

def add_bonus(marks):               # IMPURE: modifies its argument
    marks.append(5)
```

| Pure | Impure |
|------|--------|
| easy to **test**: call it, check the result | must set up and inspect outside state |
| easy to **reason about**: no hidden effects | anything it touches might change |
| safe to **cache** (`lru_cache`) and run in parallel | caching may return stale results |
| e.g. `len`, `sorted`, `max`, maths | e.g. `print`, `list.append`, `random.random`, file I/O |

Programs **need** side effects (printing, saving, network). The skill is to **keep most logic pure** and push side effects to the edges:

```
 read input (impure) → calculate (PURE, most of the code) → write output (impure)
```

## Best practices checklist

| # | Practice | Example |
|---|----------|---------|
| 1 | **One job per function** (single responsibility) | `load_data`, `clean_data`, `summarise`, not `do_everything` |
| 2 | **Clear verb names** | `calculate_total`, `is_valid_email`, not `process`, `data2`, `f` |
| 3 | **Short**: fits on a screen (~20–30 lines) | split long functions into helpers |
| 4 | **Few parameters** (≤ 4-ish); group the rest | pass a dict / object, or use keyword-only arguments |
| 5 | **Return values, don't print** (unless output is the job) | `return total` |
| 6 | **Avoid globals**; pass inputs, return outputs | `def f(data): return ...` |
| 7 | **Don't modify arguments** unexpectedly | return a new list, or name it clearly: `sort_in_place` |
| 8 | **No mutable defaults** | `items=None` |
| 9 | **Validate early, fail loudly** | guard clauses + clear exceptions |
| 10 | **Consistent return types** | don't return a number *or* a string *or* `None` at random |
| 11 | **Docstrings + type hints** for anything non-trivial | Lecture 09 |
| 12 | **Test** with small checks | `assert add_tax(100, 0.1) == 110` |
| 13 | **DRY**, but don't over-abstract | wait for the 3rd repetition before generalising |
| 14 | **Prefer built-ins** | `sum`, `max(key=)`, `sorted`, `any`, `all` |

## Refactoring example

`lecture.py` takes one 25-line function that reads data, calculates, formats and prints all at once, and splits it into four small functions: three pure, one for output. Same result, but each piece can now be tested and reused.

## Testing functions with `assert`

```python
def test_add_tax():
    assert add_tax(100, 0.1) == 110
    assert add_tax(0, 0.5) == 0

test_add_tax()      # silent if everything is right; AssertionError if not
```

Real projects use **pytest**, which finds and runs `test_*` functions automatically. The idea is identical.

## Exercises

1. Make `add_bonus(marks)` pure: return a new list instead of modifying the argument.
2. Split a "do-everything" function from your own code into 3+ functions.
3. Write three `assert` tests for a function from an earlier lecture.
4. Identify which built-ins in Lecture 12 are pure.

**Next →** [Lecture 20: Project: calculator](../20_project_calculator/)
