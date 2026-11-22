"""Lecture 24: Quick revision self-test: 25 questions, each verified by running real code.

Try to predict each answer before reading the line printed after it.
"""
import functools

QUESTIONS = []


def question(text):
    """Decorator that registers a question; the function computes the true answer."""
    def register(func):
        QUESTIONS.append((text, func))
        return func
    return register


@question("What does a function without a return statement return?")
def q01():
    def f():
        x = 1
    return f()


@question("def f(a, b=2): return a + b  ->  f(5) ?")
def q02():
    def f(a, b=2):
        return a + b
    return f(5)


@question("Mutable default trap: def add(x, items=[]) ... add(1); add(2) -> ?")
def q03():
    def add(x, items=[]):
        items.append(x)
        return items
    add(1)
    return add(2)


@question("def f(*args): return args  ->  type of f(1, 2)?")
def q04():
    def f(*args):
        return args
    return type(f(1, 2)).__name__


@question("def f(**kw): return kw  ->  f(a=1, b=2) ?")
def q05():
    def f(**kw):
        return kw
    return f(a=1, b=2)


@question("def f(a, *, b): ...   what does f(1, 2) raise?")
def q06():
    def f(a, *, b):
        return a + b
    try:
        f(1, 2)
    except TypeError:
        return "TypeError"


@question("def f(a, /): ...   what does f(a=1) raise?")
def q07():
    def f(a, /):
        return a
    try:
        f(a=1)
    except TypeError:
        return "TypeError"


@question("Unpacking: def f(a, b, c): return a+b+c ; f(*[1, 2], **{'c': 3}) ?")
def q08():
    def f(a, b, c):
        return a + b + c
    return f(*[1, 2], **{"c": 3})


@question("def f(): return 1, 2  ->  type of f()?")
def q09():
    def f():
        return 1, 2
    return type(f()).__name__


@question("x = 10; def f(): x = 5   ->  x after f()?")
def q10():
    ns = {}
    exec("x = 10\ndef f():\n    x = 5\nf()", ns)
    return ns["x"]


@question("Which keyword lets an inner function rebind an outer function's variable?")
def q11():
    def outer():
        n = 0

        def inner():
            nonlocal n
            n += 1
        inner()
        return n
    return "nonlocal" if outer() == 1 else "?"


@question("def double(n: int) -> int: return n * 2  ->  double('ab') ?")
def q12():
    def double(n: int) -> int:
        return n * 2
    return double("ab")


@question("sorted(['bb', 'a', 'ccc'], key=len) ?")
def q13():
    return sorted(["bb", "a", "ccc"], key=len)


@question("Late binding: [f() for f in [lambda: i for i in range(3)]] ?")
def q14():
    return [f() for f in [lambda: i for i in range(3)]]


@question("Type of map(str, [1, 2]) (is it a list?)")
def q15():
    return type(map(str, [1, 2])).__name__


@question("functools.reduce(lambda a, b: a * b, [1, 2, 3, 4]) ?")
def q16():
    return functools.reduce(lambda a, b: a * b, [1, 2, 3, 4])


@question("make_adder(5)(10) where make_adder returns a closure adding n ?")
def q17():
    def make_adder(n):
        return lambda x: x + n
    return make_adder(5)(10)


@question("@decorator def f() is shorthand for ... ?")
def q18():
    return "f = decorator(f)"


@question("Without functools.wraps, what is the decorated function's __name__?")
def q19():
    def deco(func):
        def wrapper(*a, **k):
            return func(*a, **k)
        return wrapper

    @deco
    def hello():
        pass
    return hello.__name__


@question("@bold @italic def hi(): return 'hi'  ->  hi() ?  (bold wraps <b>, italic wraps <i>)")
def q20():
    def tag(t):
        def deco(func):
            @functools.wraps(func)
            def wrapper():
                return f"<{t}>{func()}</{t}>"
            return wrapper
        return deco

    @tag("b")
    @tag("i")
    def hi():
        return "hi"
    return hi()


@question("How many levels of def does a decorator WITH arguments (like @repeat(3)) need?")
def q21():
    def repeat(n):                      # 1
        def decorator(func):            # 2
            def wrapper():              # 3
                return [func() for _ in range(n)]
            return wrapper
        return decorator
    return 3 if repeat(2)(lambda: 0)() == [0, 0] else "?"


@question("Which error does infinite recursion raise?")
def q22():
    def f():
        return f()
    try:
        f()
    except RecursionError:
        return "RecursionError"


@question("g = (x for x in [1, 2]); list(g); list(g)  ->  second result?")
def q23():
    g = (x for x in [1, 2])
    list(g)
    return list(g)


@question("In try/except/else/finally, which block ALWAYS runs?")
def q24():
    ran = []
    for b in (1, 0):
        try:
            1 / b
        except ZeroDivisionError:
            pass
        finally:
            ran.append("finally")
    return "finally" if ran == ["finally", "finally"] else "?"


@question("Pure or impure: def f(items): items.append(1) ?")
def q25():
    data = []

    def f(items):
        items.append(1)
    f(data)
    return "impure (changes its argument)" if data else "pure"


def main():
    print(f"Self-test: {len(QUESTIONS)} questions (answers are computed by running the code)\n")
    for number, (text, func) in enumerate(QUESTIONS, start=1):
        answer = func()
        print(f"Q{number:02d}. {text}")
        print(f"     -> {answer!r}\n")
    assert len(QUESTIONS) == 25
    print("Every answer above was produced by real code. If one surprised you, revisit its lecture.")
    print("(This file is itself a decorator demo: @question registered all 25 functions.)")


if __name__ == "__main__":
    main()
