# Lecture 12: Mixins: small, reusable abilities

Run: `python lecture.py`

## The problem

Several unrelated classes need the same extra ability: `User`, `Order` and `Product` should all convert to JSON. `Order` and `Invoice` should both log their actions. These classes don't share an "is-a" parent, so a common base class would be wrong.

## A mixin

A **mixin** is a small class that provides **one ability**, designed to be **mixed into** other classes through multiple inheritance. It is not meant to be used on its own.

```python
class JsonMixin:
    def to_json(self):
        return json.dumps(self.__dict__)

class ReprMixin:
    def __repr__(self):
        fields = ", ".join(f"{k}={v!r}" for k, v in vars(self).items())
        return f"{type(self).__name__}({fields})"

class User(JsonMixin, ReprMixin):          # User gains both abilities
    def __init__(self, name, email):
        self.name, self.email = name, email
```

## Rules for good mixins

| Rule | Why |
|------|-----|
| name it `...Mixin` | readers instantly know it's an add-on |
| **one** focused ability | easy to reason about and reuse |
| **no `__init__`** (or a cooperative one that calls `super().__init__(**kwargs)`) | avoids fighting over constructor arguments |
| rely only on obvious things (`self.__dict__`, a documented method) | works with many classes |
| list mixins **before** the main base class: `class Admin(LoggingMixin, User)` | so the mixin's methods come first in the MRO and can call `super()` into the base |

## Mixins that wrap behaviour with `super()`

A mixin can **extend** a method of whatever class comes after it in the MRO:

```python
class TimestampMixin:
    def save(self):
        self.saved_at = datetime.now()
        return super().save()        # continue to the "real" save
```

`class Document(TimestampMixin, Model)` → `Document().save()` runs the mixin's code first, then `Model.save`. The same mixin works with any class that has a `save()`.

## Mixins in the real world

- Django: `LoginRequiredMixin`, `PermissionRequiredMixin` for views
- `socketserver.ThreadingMixIn` in the standard library
- `collections.abc.Mapping` behaves like a mixin: write `__getitem__`, `__len__` and `__iter__`, and you get `get`, `keys`, `items`, `__contains__` and more for free

## Mixin or composition?

| Mixin | Composition (Lecture 18) |
|-------|--------------------------|
| adds methods **directly** to the class (`user.to_json()`) | the object **holds** a helper (`user.serializer.dump(user)`) |
| fixed when the class is defined | can be swapped at runtime |
| great for small, stable abilities | better for big or replaceable parts |

## Exercises

1. Write `ComparableMixin` that provides `__lt__`, `__le__`, `__gt__` and `__ge__` from a `sort_key()` method.
2. Add `LoggingMixin.log(msg)` that stores messages in `self._log` (create it lazily).
3. Write a `ValidateMixin` whose `save()` calls `self.validate()` before `super().save()`.
4. Subclass `collections.abc.Mapping` for a read-only config object and use `.get()` and `in` for free.

**Next →** [Lecture 13: Polymorphism basics](../13_polymorphism_basics/)
