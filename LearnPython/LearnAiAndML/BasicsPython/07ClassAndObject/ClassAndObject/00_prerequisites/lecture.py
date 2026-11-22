"""Lecture 00: Prerequisites: functions, parameters, return, scope, dicts. No classes yet."""

print("=== 1. Functions, parameters, defaults, return ===")


def greet(name, greeting="Hello"):
    message = f"{greeting}, {name}!"      # local variable
    return message


print(greet("Asha"))
print(greet(greeting="Hi", name="Ravi"))
print("a function without return gives:", print("(printing inside)"))

print("\n=== 2. Scope: local vs global ===")
count = 0


def bump():
    global count
    count += 1


def show():
    print("  reading the global count:", count)


bump()
bump()
show()


def broken_bump():
    count += 1          # no 'global' -> Python treats count as local


try:
    broken_bump()
except UnboundLocalError as e:
    print("  broken_bump ->", type(e).__name__ + ":", e)


def outer():
    x = "enclosing"

    def inner():
        print("  inner sees:", x)         # E in LEGB

    inner()


outer()
print("  built-in found last in LEGB:", len("hello"))

print("\n=== 3. Dictionaries ===")
student = {"name": "Asha", "marks": 88}
student["marks"] += 5
print(student, "| age:", student.get("age", "unknown"))

print("\n=== 4. Functions are values ===")


def double(x):
    return x * 2


f = double
print("f is", f, "| f(5) =", f(5))
size = len
print("size('hello') =", size("hello"))

print("\n=== 5. try / except: how errors are shown in this course ===")
try:
    int("abc")
except ValueError as e:
    print("  ValueError:", e)
print("  ...and the program carries on.")
