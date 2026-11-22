"""Lecture 07: **kwargs: packing keyword arguments, ** unpacking, merging, forwarding."""

print("=== 1. **kwargs packs keyword arguments into a dict ===")


def profile(**kwargs):
    print(f"  kwargs = {kwargs} ({type(kwargs).__name__})")
    for key, value in kwargs.items():
        print(f"    {key}: {value}")


profile(name="Asha", age=25, city="Pune")
profile()

print("\n=== 2. Mixing with named parameters ===")


def create_user(username, *, admin=False, **extra):
    return {"username": username, "admin": admin, "extra": extra}


print(" ", create_user("asha", admin=True, city="Pune", theme="dark"))
print(" ", create_user("ravi"))

print("\n=== 3. ** in a CALL unpacks a dict ===")
settings = {"sep": "-", "end": "!\n"}
print("  ", end="")
print("a", "b", "c", **settings)


def describe(name, age, city):
    return f"{name} ({age}) from {city}"


person = {"name": "Asha", "age": 25, "city": "Pune"}
print(" ", describe(**person))
try:
    describe(**{**person, "country": "India"})
except TypeError as e:
    print("  extra key ->", e)

print("\n=== 4. Merging dicts ===")
defaults = {"color": "blue", "size": "M", "qty": 1}
custom = {"size": "L"}
print("  {**defaults, **custom} =", {**defaults, **custom})

print("\n=== 5. Config with validation of keys ===")
DEFAULTS = {"theme": "light", "font_size": 12, "autosave": True}


def make_config(**overrides):
    unknown = set(overrides) - set(DEFAULTS)
    if unknown:
        raise TypeError(f"unknown setting(s): {', '.join(sorted(unknown))}")
    return {**DEFAULTS, **overrides}


print(" ", make_config(theme="dark"))
try:
    make_config(thme="dark")                     # typo caught
except TypeError as e:
    print("  ", e)

print("\n=== 6. Building strings / records ===")


def build_url(base, **params):
    query = "&".join(f"{k}={v}" for k, v in params.items())
    return f"{base}?{query}" if query else base


print(" ", build_url("site.com/products", page=2, sort="asc"))
print(" ", build_url("site.com"))

print("\n=== 7. *args + **kwargs: forward everything ===")


def original(a, b, c=0, *, verbose=False):
    return f"a={a}, b={b}, c={c}, verbose={verbose}"


def wrapper(*args, **kwargs):
    print(f"  wrapper got args={args} kwargs={kwargs}")
    return original(*args, **kwargs)


print("  ->", wrapper(1, 2, c=3, verbose=True))
