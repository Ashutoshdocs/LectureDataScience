"""Lecture 03: Instance attributes: per-object data, __dict__, getattr/setattr/hasattr/delattr."""


class Car:
    pass


print("=== 1. Each object has its own attributes ===")
a = Car()
b = Car()
a.color = "red"
a.speed = 120
b.color = "blue"
print(a.color, a.speed)
print(b.color)
print("a.__dict__ =", a.__dict__)
print("b.__dict__ =", b.__dict__)
try:
    print(b.speed)
except AttributeError as e:
    print("b.speed ->", type(e).__name__ + ":", e)

print("\n=== 2. Read, update, check, delete ===")


class Book:
    pass


bk = Book()
bk.title = "Python 101"
bk.pages = 250
bk.pages = 300                                    # update
print("pages:", bk.pages)
print("hasattr title/author:", hasattr(bk, "title"), hasattr(bk, "author"))
print("getattr with default:", getattr(bk, "author", "Unknown"))
setattr(bk, "author", "Guido")
print("after setattr:", bk.author)
field = "title"                                   # attribute name chosen at runtime
print(f"getattr(bk, {field!r}):", getattr(bk, field))
del bk.pages
print("after del, hasattr pages:", hasattr(bk, "pages"))
try:
    bk.pages
except AttributeError as e:
    print("reading deleted attribute ->", e)
delattr(bk, "author")
print("vars(bk) =", vars(bk))

print("\n=== 3. Loop over attribute names ===")
for name in ["title", "author", "price"]:
    print(f"  {name:<7} = {getattr(bk, name, '-')}")

print("\n=== 4. Build an object from a dictionary ===")
data = {"title": "Clean Code", "pages": 464, "author": "R. Martin"}
book2 = Book()
for key, value in data.items():
    setattr(book2, key, value)
print(book2.__dict__)

print("\n=== 5. __dict__ IS the storage ===")
book2.__dict__["year"] = 2008
print("added via __dict__, read via dot:", book2.year)
