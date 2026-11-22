# Lecture 02: Calling functions: flow & the call stack

Run: `python lecture.py`

## What happens on a call

```python
def say_hi(name):
    print("Hi", name)

print("start")
say_hi("Asha")      # ← jump into the function
print("end")        # ← come back here afterwards
```

| Step | Line running | What happens |
|------|--------------|--------------|
| 1 | `def say_hi` | the function is stored; body skipped |
| 2 | `print("start")` | prints `start` |
| 3 | `say_hi("Asha")` | Python **pauses here**, creates `name = "Asha"`, jumps into the body |
| 4 | `print("Hi", name)` | prints `Hi Asha` |
| 5 | end of body | the local `name` is discarded; Python **returns** to step 3's line |
| 6 | `print("end")` | prints `end` |

## Functions calling functions: the call stack

Python keeps a **stack** of active calls. Each call is a **frame** with its own local variables. The newest frame is on top; when it finishes, it's removed and execution continues in the frame below.

```python
def c(): print("in c")
def b(): print("in b"); c(); print("back in b")
def a(): print("in a"); b(); print("back in a")
a()
```

```
 call a()            call b()            call c()            c returns        b returns
 ┌────────┐          ┌────────┐          ┌────────┐          ┌────────┐       ┌────────┐
 │        │          │        │          │   c    │          │        │       │        │
 │        │          │   b    │          │   b    │          │   b    │       │        │
 │   a    │          │   a    │          │   a    │          │   a    │       │   a    │
 │ <main> │          │ <main> │          │ <main> │          │ <main> │       │ <main> │
 └────────┘          └────────┘          └────────┘          └────────┘       └────────┘
```

When an error happens, the **traceback** prints this stack, which tells you exactly which call chain led to the problem. Read tracebacks **bottom-up**: the last line is the error, and the lines above it show how you got there.

## Order of definition matters (at call time)

A function must be **defined before it's called**, but only before the **call actually runs**:

```python
def main():
    helper()        # fine: helper exists by the time main() is called

def helper():
    print("helping")

main()              # ✅ both defined now
```

Calling `helper()` at the top of the file, before its `def`, gives `NameError`.

## Ways to call

| Call | Meaning |
|------|---------|
| `f()` | call with no arguments |
| `f(1, 2)` | positional arguments |
| `f(x=1, y=2)` | keyword arguments (Lecture 03) |
| `result = f(3)` | keep the returned value (Lecture 04) |
| `print(f(3))` | use the result directly |
| `f(g(3))` | call `g` first, pass its result to `f` |
| `f` (no brackets) | **doesn't call**: refers to the function object |

> ⚠️ Forgetting the brackets is a classic bug: `if is_ready:` is always true, because a function object is truthy. You meant `if is_ready():`.

## The `main()` pattern

Real scripts put their top-level steps in a `main()` function and call it at the bottom:

```python
def main():
    data = load()
    result = process(data)
    show(result)

if __name__ == "__main__":     # run main() only when this file is run directly
    main()
```

`__name__` is `"__main__"` when you run the file, but the module's name when another file **imports** it. So importing doesn't trigger `main()`.

## Exercises

1. Add a function `d()` called from `c()`. Draw the stack at its deepest point.
2. Call a function before its `def` and read the error.
3. Write `if is_weekend:` (no brackets) and see that it's always true.

<details><summary>Solutions</summary>

1. `<main> → a → b → c → d`.
2. `NameError: name '...' is not defined`.
</details>

**Next →** [Lecture 03: Parameters & arguments](../03_parameters_arguments/)
