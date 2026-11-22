# Lecture 05: Variable scope: LEGB, `global`, `nonlocal`

Run: `python lecture.py`

**Scope** = the region of code where a name is visible.

## Local vs global

```python
rate = 0.18                      # GLOBAL: defined at the top level of the file

def tax(amount):
    result = amount * rate       # amount, result: LOCAL to this call
    return result

tax(100)
print(result)                    # NameError: result only existed inside the call
```

| | Local | Global |
|---|---|---|
| Defined | inside a function (incl. parameters) | at the top level of the file |
| Visible | only inside that function call | everywhere in the file |
| Lifetime | created on call, destroyed on return | until the program ends |

Each call gets a **fresh** set of local variables. Two calls never share locals.

## The LEGB rule

When Python sees a plain name, it searches four scopes in order and uses the **first** match:

```
 L  Local       the current function
 E  Enclosing   any outer function(s), when functions are nested
 G  Global      the module (file) level
 B  Built-in    print, len, sum, max, ...
```

## Shadowing

A local variable with the same name as a global **hides** (shadows) it inside the function. The global is untouched:

```python
x = "global"
def f():
    x = "local"      # a NEW local x; the global x is unchanged
    print(x)         # local
```

> ⚠️ Shadowing built-ins is a common bug: `list = [1, 2]` or `sum = 0` breaks later calls to `list()` / `sum()`.

## `global`: assigning to a global from inside a function

**Reading** a global needs nothing. **Assigning** to it needs `global`; otherwise Python treats the name as local for the **whole** function:

```python
count = 0
def increment():
    global count
    count += 1

def broken():
    count += 1       # UnboundLocalError: count is "local" but has no value yet
```

> **When to use `global`:** rarely. Prefer passing values in and **returning** results. Globals make functions harder to test and reason about, because any function might change them. Global **constants** (`TAX_RATE = 0.18`, uppercase) that you only read are fine.

## `nonlocal`: assigning to an enclosing function's variable

For nested functions (Lecture 13):

```python
def counter():
    count = 0
    def increment():
        nonlocal count       # the count in counter(), not a new local
        count += 1
        return count
    return increment
```

| Keyword | Lets you assign to… |
|---------|---------------------|
| (none) | a new local variable |
| `global x` | the module-level `x` |
| `nonlocal x` | the nearest enclosing function's `x` |

## Loops and `if` blocks do NOT create a scope

Unlike some languages, a variable created in a `for` loop or `if` block is still visible after it, within the same function:

```python
for i in range(3):
    last = i
print(i, last)       # 2 2: still visible
```

Comprehension variables **are** local to the comprehension: `[n for n in range(3)]` leaves no `n` behind.

## Exercises

1. Print a local variable outside its function. What error?
2. Write a counter with `global`, then rewrite it without `global` (pass and return the value).
3. Shadow the built-in `sum`, then try `sum([1, 2])`. Fix it with `del sum`.
4. In a nested function, change the outer variable without `nonlocal`. What happens?

<details><summary>Solutions</summary>

1. `NameError`.
3. `TypeError: 'int' object is not callable`.
4. Assigning creates a new local in the inner function (or `UnboundLocalError` with `+=`).
</details>

**Next →** [Lecture 06: `*args`](../06_args/)
