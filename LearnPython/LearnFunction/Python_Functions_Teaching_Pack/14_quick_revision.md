# Python Functions – Quick Revision Sheet

## Function basics
```python
def greet():
    print("Hello")

greet()
```

## Parameters and arguments
```python
def greet(name):       # name = parameter
    print(name)

greet("Rahul")         # "Rahul" = argument
```

## Default and keyword arguments
```python
def student(name, city="Pune"):
    print(name, city)

student("Amit")
student(name="Riya", city="Patna")
```

## Scope
```python
x = 100                 # global

def demo():
    y = 50              # local
    print(x, y)
```

- `global x`: rebind the module-level `x` inside a function.
- `nonlocal x`: rebind a name in an enclosing function scope.
- LEGB: Local, Enclosing, Global, Built-in.

## Return
```python
def add(a, b):
    return a + b

answer = add(10, 20)
```

- `print()` displays.
- `return` sends a value back.
- No explicit return means `None`.
- `return` exits the function.

## *args
```python
def show(*args):
    print(args)         # tuple

show(10, 20, 30)
```

## **kwargs
```python
def show(**kwargs):
    print(kwargs)       # dictionary

show(name="Amit", age=25)
```

## Unpacking
```python
numbers = [1, 2, 3]
def add(a, b, c):
    return a + b + c
print(add(*numbers))

details = {"name": "Amit", "age": 25}
def profile(name, age):
    print(name, age)
profile(**details)
```

## Remember
- `*args` = extra positional arguments = tuple.
- `**kwargs` = extra keyword arguments = dictionary.
- The names `args` and `kwargs` are conventions, not reserved keywords.
