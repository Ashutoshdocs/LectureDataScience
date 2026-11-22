"""OOP practice: write each class below, then run:  python lecture.py exercises

Each docstring says exactly what the checker tests. Replace `pass` with your code.
"""
import functools
from abc import ABC, abstractmethod
from dataclasses import dataclass, field


class Rectangle:
    """01. Rectangle(width, height) with methods area() and perimeter().
    Rectangle(3, 4).area() -> 12, .perimeter() -> 14"""
    pass


class Counter:
    """02. Counter() starts with attribute count = 0.
    increment(by=1) adds to count; reset() sets it back to 0."""
    pass


class Student:
    """03. Student(name). Class attribute `count` counts how many students were created
    (shared by all students). Each student stores its own `name`."""
    pass


class Temperature:
    """04. Temperature(celsius). `celsius` is a property whose setter raises ValueError below -273.15
    (also when creating the object). `fahrenheit` is a READ-ONLY property: celsius * 9 / 5 + 32."""
    pass


class BankAccount:
    """05. BankAccount(owner, balance=0). deposit(amount) and withdraw(amount) return the new balance.
    Both raise ValueError for amounts <= 0; withdraw raises ValueError if amount > balance.
    `balance` is a read-only property."""
    pass


class Point:
    """06. Point(x, y). Class method from_string('3,4') returns a Point built with cls(...)
    (so subclasses get their own type). Static method distance(p, q) returns the straight-line distance."""
    pass


class Animal:
    """07. Animal(name). speak() raises NotImplementedError.
    Dog(Animal).speak() -> '<name> says Woof'; Cat(Animal).speak() -> '<name> says Meow'."""
    pass


class Dog(Animal):
    pass


class Cat(Animal):
    pass


class Employee:
    """08. Employee(name, salary) with describe() -> '<name> earns <salary>'.
    Manager(Employee): Manager(name, salary, team) must call super().__init__;
    describe() -> parent's text + ' and manages <team> people'."""
    pass


class Manager(Employee):
    pass


class Shape:
    """09. Make Shape an abstract class (ABC) with an abstract method area().
    Circle(r).area() -> 3.14159 * r * r ; Square(side).area() -> side * side.
    Shape() itself must raise TypeError."""
    pass


class Circle(Shape):
    pass


class Square(Shape):
    pass


class Book:
    """10. Book(title, pages). str(book) -> "Python (320 pages)" ; repr(book) -> "Book('Python', 320)"."""
    pass


class Playlist:
    """11. Playlist(songs) where songs is a list. Support len(p), p[0] and 'song' in p."""
    pass


class Vector:
    """12. Vector(x, y). Support v + w, v == w, v * 3 and 3 * v. repr -> 'Vector(x, y)'."""
    pass


class Version:
    """13. Version('1.10.2'). Compare by the numbers, not the text: Version('1.10') > Version('1.9').
    Support ==, <, >, <=, >= (hint: functools.total_ordering) so sorted() works."""
    pass


class Coordinate:
    """14. Coordinate(lat, lon). Equal coordinates must be == AND hash the same, so
    len({Coordinate(1, 2), Coordinate(1, 2)}) == 1."""
    pass


class Stack:
    """15. Stack using COMPOSITION (keep a list inside; don't inherit from list).
    push(x), pop() (IndexError if empty), peek() (None if empty), len(stack)."""
    pass


class JsonMixin:
    """16. Mixin with to_json() that returns json.dumps of the object's __dict__.
    Then User(JsonMixin) with User(name, email): User('A', 'a@b').to_json() -> '{"name": "A", "email": "a@b"}'"""
    pass


class User(JsonMixin):
    pass


class Multiplier:
    """17. Multiplier(n) objects are callable: Multiplier(3)(5) -> 15. Attribute `calls` counts calls."""
    pass


class Product:
    """18. Make this a @dataclass with fields name: str, price: float, qty: int = 1
    and a property total -> price * qty."""
    pass


class Tracker:
    """19. A context manager. Tracker() has attribute events = [].
    Entering a `with` block appends 'enter'; leaving appends 'exit' (even after an error).
    `with Tracker() as t:` must give back the tracker itself."""
    pass


class Countdown:
    """20. Countdown(n) is iterable: list(Countdown(3)) -> [3, 2, 1]. It can be looped over more than once."""
    pass
