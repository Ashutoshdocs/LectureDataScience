"""
MODULE 8: COMBINING ARGUMENT TYPES

General function-definition order:
1. Positional / required parameters
2. *args (if needed)
3. Keyword-only parameters
4. **kwargs (if needed)
"""


def example(a, b=10, *args, city="Pune", **kwargs):
    print("a:", a)
    print("b:", b)
    print("args:", args)
    print("city:", city)
    print("kwargs:", kwargs)


example(10, 20, 30, 40, city="Delhi", age=25)


# A simpler example with *args and **kwargs together.
def demo(*args, **kwargs):
    print("Positional values:", args)
    print("Keyword values:", kwargs)


demo(10, 20, 30, name="Rahul", age=25)
