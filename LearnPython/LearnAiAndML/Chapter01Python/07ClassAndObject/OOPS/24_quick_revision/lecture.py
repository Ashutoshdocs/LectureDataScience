"""Lecture 24: OOP self-test: 25 questions, each answer computed by running real code.

Try to predict each answer before reading the line printed after it.
"""
import dataclasses
import functools
from abc import ABC, abstractmethod

QUESTIONS = []


def question(text):
    def register(func):
        QUESTIONS.append((text, func))
        return func
    return register


@question("class Dog: pass  ->  Dog() == Dog() ?")
def q01():
    class Dog:
        pass
    return Dog() == Dog()


@question("Inside a method, what is self in the call c.increment(5)?")
def q02():
    class Counter:
        def who(self):
            return self
    c = Counter()
    return "the object c" if c.who() is c else "?"


@question("__init__ returns ... ?")
def q03():
    class A:
        def __init__(self):
            pass
    return A.__init__(object.__new__(A))


@question("class Car: wheels = 4 ; b = Car(); b.wheels = 3  ->  Car.wheels ?")
def q04():
    class Car:
        wheels = 4
    b = Car()
    b.wheels = 3
    return Car.wheels


@question("class T: members = [] ; T().members.append('x')  ->  T().members ?")
def q05():
    class T:
        members = []
    T().members.append("x")
    return T().members


@question("self.__pin = 1 inside class Account is stored under which name?")
def q06():
    class Account:
        def __init__(self):
            self.__pin = 1
    return list(vars(Account()))[0]


@question("A @property with no setter: what does assigning to it raise?")
def q07():
    class A:
        @property
        def x(self):
            return 1
    try:
        A().x = 5
    except AttributeError:
        return "AttributeError"


@question("@classmethod from_string returns cls(...). Child.from_string() returns which type?")
def q08():
    class Parent:
        @classmethod
        def make(cls):
            return cls()

    class Child(Parent):
        pass
    return type(Child.make()).__name__


@question("Which method kind receives neither self nor cls?")
def q09():
    class A:
        @staticmethod
        def f(*args):
            return len(args)
    return "staticmethod" if A.f() == 0 else "?"


@question("class Dog(Animal) without __init__: whose __init__ runs on Dog('Rex')?")
def q10():
    class Animal:
        def __init__(self, name):
            self.made_by = "Animal"

    class Dog(Animal):
        pass
    return Dog("Rex").made_by


@question("Child defines __init__ but forgets super().__init__(). Do the parent's attributes exist?")
def q11():
    class P:
        def __init__(self):
            self.x = 1

    class C(P):
        def __init__(self):
            self.y = 2
    return hasattr(C(), "x")


@question("isinstance(Dog(), Animal) where Dog(Animal) ?")
def q12():
    class Animal:
        pass

    class Dog(Animal):
        pass
    return isinstance(Dog(), Animal)


@question("Diamond D(B, C), B(A), C(A): MRO ?")
def q13():
    class A: ...
    class B(A): ...
    class C(A): ...
    class D(B, C): ...
    return [k.__name__ for k in D.__mro__]


@question("class Duck(Flyer, Swimmer): both define move(). Duck().move() uses ... ?")
def q14():
    class Flyer:
        def move(self):
            return "Flyer.move"

    class Swimmer:
        def move(self):
            return "Swimmer.move"

    class Duck(Flyer, Swimmer):
        pass
    return Duck().move()


@question("print(obj) uses __str__. A list [obj] shows each item using ... ?")
def q15():
    class B:
        def __str__(self):
            return "STR"

        def __repr__(self):
            return "REPR"
    return str([B()])


@question("Class with only __len__ returning 0: bool(obj) ?")
def q16():
    class Empty:
        def __len__(self):
            return 0
    return bool(Empty())


@question("3 * v needs which magic method on v?")
def q17():
    class V:
        def __rmul__(self, k):
            return "__rmul__"
    return 3 * V()


@question("Define __eq__ but not __hash__: can the objects go in a set?")
def q18():
    class P:
        def __eq__(self, other):
            return True
    try:
        {P()}
        return True
    except TypeError:
        return False


@question("@total_ordering with __eq__ and __lt__: does >= work?")
def q19():
    @functools.total_ordering
    class N:
        def __init__(self, v):
            self.v = v

        def __eq__(self, o):
            return self.v == o.v

        def __lt__(self, o):
            return self.v < o.v
    return N(5) >= N(3)


@question("Duck typing: does a function calling x.speak() care about x's class?")
def q20():
    class Robot:
        def speak(self):
            return "beep"

    def talk(x):
        return x.speak()
    return "no, only that speak() exists" if talk(Robot()) == "beep" else "?"


@question("Creating an object of an ABC subclass that hasn't implemented every @abstractmethod raises ... ?")
def q21():
    class Base(ABC):
        @abstractmethod
        def run(self): ...

    class Half(Base):
        pass
    try:
        Half()
    except TypeError:
        return "TypeError"


@question("A Car HAS an Engine. Inheritance or composition?")
def q22():
    class Engine:
        def start(self):
            return "vroom"

    class Car:
        def __init__(self):
            self.engine = Engine()
    return "composition" if Car().engine.start() == "vroom" else "?"


@question("@dataclass class P: x: int; y: int = 0  ->  repr(P(1)) ?")
def q23():
    @dataclasses.dataclass
    class P:
        x: int
        y: int = 0
    return repr(P(1)).split(".")[-1]


@question("@dataclass(frozen=True): what happens on p.x = 5 ?")
def q24():
    @dataclasses.dataclass(frozen=True)
    class P:
        x: int
    try:
        P(1).x = 5
    except dataclasses.FrozenInstanceError:
        return "FrozenInstanceError"


@question("A __exit__ that returns False: is an exception inside the with block re-raised?")
def q25():
    class CM:
        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return False
    try:
        with CM():
            raise ValueError
    except ValueError:
        return True
    return False


def main():
    print(f"OOP self-test: {len(QUESTIONS)} questions (answers computed by running the code)\n")
    for number, (text, func) in enumerate(QUESTIONS, start=1):
        print(f"Q{number:02d}. {text}")
        print(f"     -> {func()!r}\n")
    assert len(QUESTIONS) == 25
    print("If an answer surprised you, revisit the lecture listed in the README's sections.")


if __name__ == "__main__":
    main()
