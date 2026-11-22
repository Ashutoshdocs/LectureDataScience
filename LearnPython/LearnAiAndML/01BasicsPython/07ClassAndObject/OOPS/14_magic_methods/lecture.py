"""Lecture 14: Magic methods: __str__/__repr__, container protocol, __call__, context managers, __getattr__."""
import time

print("=== 1. __str__ vs __repr__ ===")


class Plain:
    def __init__(self, title):
        self.title = title


class Book:
    def __init__(self, title, pages):
        self.title, self.pages = title, pages

    def __str__(self):
        return f"'{self.title}' ({self.pages} pages)"

    def __repr__(self):
        return f"Book({self.title!r}, {self.pages})"


class OnlyRepr:
    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return f"OnlyRepr({self.title!r})"


b = Book("Python Basics", 320)
print("  no dunders : print ->", Plain("x"))
print("  print(b)   ->", b)
print("  [b]        ->", [b])
print("  f'{b!r}'   ->", f"{b!r}")
print("  only __repr__, print uses it as fallback ->", OnlyRepr("x"))

print("\n=== 2. A playlist that behaves like a built-in container ===")


class Playlist:
    def __init__(self, name, songs=None):
        self.name = name
        self._songs = list(songs or [])

    def __repr__(self):
        return f"Playlist({self.name!r}, {len(self)} songs)"

    def __len__(self):
        return len(self._songs)

    def __getitem__(self, index):                      # p[0], p[-1], p[1:3]
        result = self._songs[index]
        return Playlist(f"{self.name} (slice)", result) if isinstance(index, slice) else result

    def __setitem__(self, index, song):
        self._songs[index] = song

    def __delitem__(self, index):
        del self._songs[index]

    def __contains__(self, song):
        return song.lower() in (s.lower() for s in self._songs)

    def __iter__(self):                                # generator = easy iterator
        for song in self._songs:
            yield song

    def __bool__(self):
        return bool(self._songs)


p = Playlist("Road trip", ["Kesariya", "Believer", "Shape of You", "Tum Hi Ho"])
print("  repr      :", repr(p))
print("  len(p)    :", len(p))
print("  p[0], p[-1]:", p[0], "|", p[-1])
print("  p[1:3]    :", p[1:3], list(p[1:3]))
print("  'believer' in p:", "believer" in p)
p[1] = "Thunder"
del p[0]
print("  after set/del :", list(p))
print("  for loop      :", " / ".join(song for song in p))
print("  sorted(p)     :", sorted(p), "<- works because p is iterable")
print("  bool(empty)   :", bool(Playlist("empty")), "| bool(p):", bool(p))

print("\n=== 3. __call__: objects that act like functions (with memory) ===")


class Multiplier:
    def __init__(self, n):
        self.n = n
        self.calls = 0

    def __call__(self, x):
        self.calls += 1
        return x * self.n


triple = Multiplier(3)
print("  triple(5), triple(10):", triple(5), triple(10), "| calls so far:", triple.calls)
print("  callable(triple):", callable(triple), "| list(map(triple, [1, 2, 3])):", list(map(triple, [1, 2, 3])))

print("\n=== 4. Context manager: __enter__ / __exit__ ===")


class Timer:
    def __init__(self, label):
        self.label = label

    def __enter__(self):
        self.start = time.perf_counter()
        print(f"  [{self.label}] start")
        return self

    def __exit__(self, exc_type, exc, tb):
        ms = (time.perf_counter() - self.start) * 1000
        status = f"failed with {exc_type.__name__}" if exc_type else "ok"
        print(f"  [{self.label}] end ({status}) - cleanup always runs")
        self.ms = ms
        return False                                   # don't swallow exceptions


with Timer("sum"):
    total = sum(range(100_000))
try:
    with Timer("boom"):
        1 / 0
except ZeroDivisionError:
    print("  the error still reached us after cleanup")

print("\n=== 5. __getattr__: runs only when normal lookup fails ===")


class Settings:
    defaults = {"theme": "light", "language": "en"}

    def __init__(self, **custom):
        self.custom = custom

    def __getattr__(self, name):
        if name in self.custom:
            return self.custom[name]
        if name in self.defaults:
            return self.defaults[name]
        raise AttributeError(f"no setting {name!r}")


s = Settings(theme="dark")
print("  s.theme, s.language:", s.theme, s.language, "| s.custom found normally:", s.custom)
try:
    s.font
except AttributeError as e:
    print("  s.font ->", e)

print("\n=== 6. Mistakes ===")


class BadStr:
    def __str__(self):
        return 42


class BadIter:
    def __iter__(self):
        return [1, 2, 3]


for label, action in [("__str__ returns int", lambda: str(BadStr())),
                      ("__iter__ returns list", lambda: list(BadIter()))]:
    try:
        action()
    except TypeError as e:
        print(f"  {label:<22} -> TypeError: {e}")
