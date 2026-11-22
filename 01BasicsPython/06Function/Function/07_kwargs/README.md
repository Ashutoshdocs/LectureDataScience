# Lecture 07: `**kwargs`: any number of keyword arguments

Run: `python lecture.py`

## `**kwargs` collects extra keyword arguments into a dict

```python
def profile(**kwargs):
    print(kwargs, type(kwargs))
    for key, value in kwargs.items():
        print(f"{key}: {value}")

profile(name="Asha", age=25, city="Pune")
# {'name': 'Asha', 'age': 25, 'city': 'Pune'} <class 'dict'>
```

- `**` is what matters; `kwargs` ("keyword arguments") is the conventional name. `**options`, `**fields` and the like are fine too.
- Inside, it's a normal **dict**: `.get()`, `in`, `.items()`.
- Called with no keyword arguments, `kwargs` is `{}`.

## Mixing with other parameters

```python
def create_user(username, *, admin=False, **extra):
    ...
create_user("asha", admin=True, city="Pune", theme="dark")
# username="asha", admin=True, extra={'city': 'Pune', 'theme': 'dark'}
```

Named parameters take what they match; `**kwargs` gets the **leftovers**.

## Unpacking a dict at call time: `**`

```python
settings = {"sep": "-", "end": "!\n"}
print("a", "b", **settings)          # print("a", "b", sep="-", end="!\n")

def describe(name, age, city): ...
person = {"name": "Asha", "age": 25, "city": "Pune"}
describe(**person)                    # keys must match parameter names
```

| Where | `**` means |
|-------|-----------|
| definition `def f(**kwargs)` | **pack** extra keyword arguments → a dict |
| call `f(**d)` | **unpack** a dict → keyword arguments |

## Merging dicts with `**`

```python
defaults = {"color": "blue", "size": "M"}
custom = {"size": "L"}
final = {**defaults, **custom}      # {'color': 'blue', 'size': 'L'}: later keys win
```

## `*args` and `**kwargs` together: the "accept anything" signature

```python
def wrapper(*args, **kwargs):
    return original(*args, **kwargs)    # pass EVERYTHING through unchanged
```

This exact pattern is the heart of **decorators** (Lecture 14).

## When to use `**kwargs` (and when not)

| ✅ Use when | ❌ Avoid when |
|------------|--------------|
| optional settings/options whose names vary (`make_chart(title=..., color=...)`) | you know the parameters. Name them; callers get autocomplete and clear errors |
| building records/dicts from named values (`create_record(**fields)`) | it hides typos: `colr="red"` is silently accepted! |
| forwarding arguments to another function (wrappers, decorators) | |
| configuration overrides merged with defaults | |

> ⚠️ The big downside: misspelled names aren't errors. Validate the keys if it matters (`lecture.py` section 5).

## Exercises

1. Write `build_url(base, **params)` → `"site.com?page=2&sort=asc"`.
2. Write `make_config(**overrides)` that merges overrides into a defaults dict.
3. Reject unknown keys in `make_config` with a `TypeError`.
4. Call `describe(**person)` where the dict has an extra key. Read the error.

<details><summary>Solutions</summary>

```python
def build_url(base, **params):
    query = "&".join(f"{k}={v}" for k, v in params.items())
    return f"{base}?{query}" if query else base
```
4. `TypeError: describe() got an unexpected keyword argument 'country'`.
</details>

**Next →** [Lecture 08: Argument order & special parameters](../08_argument_order_and_special_params/)
