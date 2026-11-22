"""Lecture 16: Duck typing, EAFP vs LBYL, file-like objects, typing.Protocol."""
import io
import pathlib
import tempfile
from typing import Protocol, runtime_checkable

print("=== 1. No common parent needed ===")


class Duck:
    def speak(self):
        return "Quack"


class Robot:
    def speak(self):
        return "Beep boop"


class Person:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return f"Hi, I'm {self.name}"


class Stone:
    pass


class Statue:
    speak = "I am not callable"        # has the name, but it's not a method


for thing in [Duck(), Robot(), Person("Asha")]:
    print(f"  {type(thing).__name__:<7} -> {thing.speak()}")
try:
    Stone().speak()
except AttributeError as e:
    print("  Stone   -> AttributeError:", e, "(found only at runtime)")

print("\n=== 2. EAFP vs LBYL ===")
things = [Duck(), Stone(), Robot(), Statue()]


def speak_eafp(thing):
    try:
        return thing.speak()
    except (AttributeError, TypeError):
        return "(silent)"


def speak_lbyl(thing):
    if hasattr(thing, "speak"):
        try:
            return thing.speak()
        except TypeError as e:
            return f"CRASH: {e}"
    return "(silent)"


def speak_safe(thing):
    method = getattr(thing, "speak", None)
    return method() if callable(method) else "(silent)"


print("  EAFP:", [speak_eafp(t) for t in things])
print("  LBYL (hasattr only):", [speak_lbyl(t) for t in things], "<- hasattr passed for Statue, but the call failed")
print("  callable(getattr()):", [speak_safe(t) for t in things])

print("\n=== 3. File-like objects: anything with .write() ===")


def save_report(lines, out):
    for line in lines:
        out.write(line + "\n")


lines = ["Report", "sales: 120", "returns: 4"]
buffer = io.StringIO()
save_report(lines, buffer)
print("  to StringIO :", repr(buffer.getvalue()))
with tempfile.TemporaryDirectory() as tmp:
    path = pathlib.Path(tmp) / "report.txt"
    with open(path, "w") as f:
        save_report(lines, f)
    print("  to real file:", repr(path.read_text()))


class Shouter:
    def __init__(self):
        self.parts = []

    def write(self, text):
        self.parts.append(text.upper())


s = Shouter()
save_report(lines, s)
print("  to our own class:", s.parts)

print("\n=== 4. Built-ins use duck typing too ===")


class Countdown:
    def __init__(self, start):
        self.start = start

    def __iter__(self):
        return iter(range(self.start, 0, -1))

    def __len__(self):
        return self.start


cd = Countdown(5)
print("  for/list/len/sum work on our class:", list(cd), len(cd), sum(cd))

print("\n=== 5. typing.Protocol: duck typing that tools can check ===")


@runtime_checkable
class Speaker(Protocol):
    def speak(self) -> str: ...


def announce(s: Speaker) -> str:
    return f"announcing: {s.speak()}"


print("  ", announce(Duck()), "|", announce(Robot()))
for obj in [Duck(), Robot(), Stone(), Statue()]:
    print(f"  isinstance({type(obj).__name__}(), Speaker) = {isinstance(obj, Speaker)}")
print("  note: Duck never inherits from Speaker:", Speaker in Duck.__mro__)
print("  note: runtime checks only look for the NAME, so Statue passes even though speak isn't callable")


class Drawable(Protocol):
    def draw(self) -> str: ...


class Box:
    def draw(self):
        return "[ ]"


class Star:
    def draw(self):
        return "*"


def render(items: list[Drawable]) -> str:
    return " ".join(i.draw() for i in items)


print("  render(Box, Star, Box):", render([Box(), Star(), Box()]))
