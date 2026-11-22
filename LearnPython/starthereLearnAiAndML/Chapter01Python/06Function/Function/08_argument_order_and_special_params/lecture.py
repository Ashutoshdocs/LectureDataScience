"""Lecture 08: Parameter order, keyword-only (*), positional-only (/), matching rules."""

print("=== 1. Every kind of parameter in one function ===")


def f(pos_only, /, normal, default=1, *args, kw_only, kw_default=2, **kwargs):
    return dict(pos_only=pos_only, normal=normal, default=default, args=args,
                kw_only=kw_only, kw_default=kw_default, kwargs=kwargs)


for key, value in f(10, 20, 30, 40, 50, kw_only="K", extra="E").items():
    print(f"  {key:<11}= {value!r}")

print("\n=== 2. Keyword-only parameters ===")


def transfer(amount, *, from_acct, to_acct):
    return f"move {amount} from {from_acct} to {to_acct}"


print(" ", transfer(500, from_acct="A1", to_acct="B2"))
try:
    transfer(500, "A1", "B2")
except TypeError as e:
    print("  positional ->", e)


def save(data, *, overwrite=False):
    return f"saving {data!r}, overwrite={overwrite}"


print(" ", save("report", overwrite=True), "<- clearer than save('report', True)")

print("\n=== 3. Positional-only parameters ===")


def area(width, height, /):
    return width * height


print("  area(3, 4) =", area(3, 4))
try:
    area(width=3, height=4)
except TypeError as e:
    print("  keywords ->", e)
try:
    len(obj=[1, 2])
except TypeError as e:
    print("  built-ins are positional-only too: len(obj=...) ->", e)

print("\n=== 4. Matching puzzle ===")


def g(a, b=0, *args, x, **kw):
    return f"a={a}, b={b}, args={args}, x={x}, kw={kw}"


print("  g(1, 2, 3, 4, x=5, y=6) ->", g(1, 2, 3, 4, x=5, y=6))
print("  g(1, x=5)               ->", g(1, x=5))
try:
    g(1, 2)
except TypeError as e:
    print("  g(1, 2) ->", e)

print("\n=== 5. A realistic signature ===")


def connect(host, port=5432, *, timeout=10, ssl=True):
    return f"{host}:{port} timeout={timeout} ssl={ssl}"


print(" ", connect("db.local"))
print(" ", connect("db.local", 6543, ssl=False))
print(" ", connect(port=1, host="h", timeout=3))

print("\n=== 6. Calls: positional (and *seq) first, then keywords (and **dict) ===")
more = [3, 4]
options = {"x": 5, "y": 6}
print("  g(1, 2, *more, **options) ->", g(1, 2, *more, **options))
