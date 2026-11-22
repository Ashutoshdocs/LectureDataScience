"""Lecture 12: Mixins: small reusable abilities via multiple inheritance."""
import collections.abc
import datetime as dt
import json

print("=== 1. Ability mixins ===")


class JsonMixin:
    def to_json(self):
        return json.dumps({k: v for k, v in vars(self).items() if not k.startswith("_")}, default=str)


class ReprMixin:
    def __repr__(self):
        fields = ", ".join(f"{k}={v!r}" for k, v in vars(self).items() if not k.startswith("_"))
        return f"{type(self).__name__}({fields})"


class LoggingMixin:
    def log(self, msg):
        if not hasattr(self, "_log"):          # created lazily: no __init__ needed
            self._log = []
        self._log.append(f"{type(self).__name__}: {msg}")

    def history(self):
        return list(getattr(self, "_log", []))


class User(JsonMixin, ReprMixin):
    def __init__(self, name, email):
        self.name, self.email = name, email


class Order(JsonMixin, ReprMixin, LoggingMixin):
    def __init__(self, order_id, amount):
        self.order_id, self.amount = order_id, amount
        self.log("created")

    def pay(self):
        self.log(f"paid {self.amount}")


u = User("Asha", "asha@mail.com")
o = Order(101, 499)
o.pay()
print("  repr(User):", repr(u))
print("  User JSON :", u.to_json())
print("  Order JSON:", o.to_json(), "(private _log hidden)")
print("  Order log :", o.history())
print("  User has a log() method?", hasattr(u, "log"), "(it didn't mix in LoggingMixin)")

print("\n=== 2. A mixin that extends a method with super() ===")


class Model:
    def save(self):
        return f"saved {type(self).__name__} to database"


class TimestampMixin:
    def save(self):
        self.saved_at = dt.datetime(2026, 11, 22, 10, 30)    # fixed time so output is stable
        return "[timestamp set] " + super().save()


class ValidateMixin:
    def save(self):
        self.validate()
        return "[validated] " + super().save()


class Document(ValidateMixin, TimestampMixin, Model):
    def __init__(self, title):
        self.title = title

    def validate(self):
        if not self.title:
            raise ValueError("title is required")


doc = Document("Report")
print("  doc.save():", doc.save())
print("  MRO:", " -> ".join(c.__name__ for c in Document.__mro__))
try:
    Document("").save()
except ValueError as e:
    print("  Document('').save() -> ValueError:", e)

print("\n=== 3. ComparableMixin: four operators from one method ===")


class ComparableMixin:
    def __lt__(self, other):
        return self.sort_key() < other.sort_key()

    def __le__(self, other):
        return self.sort_key() <= other.sort_key()

    def __gt__(self, other):
        return self.sort_key() > other.sort_key()

    def __ge__(self, other):
        return self.sort_key() >= other.sort_key()


class Student(ComparableMixin, ReprMixin):
    def __init__(self, name, marks):
        self.name, self.marks = name, marks

    def sort_key(self):
        return self.marks


class Parcel(ComparableMixin, ReprMixin):
    def __init__(self, label, kg):
        self.label, self.kg = label, kg

    def sort_key(self):
        return self.kg


students = [Student("Asha", 92), Student("Ravi", 78), Student("Dev", 85)]
print("  sorted students:", sorted(students))
print("  max student    :", max(students).name, "| Asha >= Dev:", students[0] >= students[2])
print("  same mixin, different class:", sorted([Parcel("A", 5), Parcel("B", 1.5)]))

print("\n=== 4. The standard library's mixin-style ABC ===")


class Config(collections.abc.Mapping, ReprMixin):
    def __init__(self, **settings):
        self._data = dict(settings)

    def __getitem__(self, key):
        return self._data[key]

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return iter(self._data)


cfg = Config(debug=True, port=8080)
print("  we wrote 3 methods; got for free -> get:", cfg.get("port"), "| in:", "debug" in cfg,
      "| keys:", list(cfg.keys()), "| items:", list(cfg.items()))
try:
    cfg["port"] = 1
except TypeError as e:
    print("  read-only:", e)
