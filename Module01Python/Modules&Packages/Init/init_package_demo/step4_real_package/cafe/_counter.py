"""cafe/_counter.py — internal helper. Not exposed in cafe/__init__.py."""

_last = 0


def next_number():
    global _last
    _last += 1
    return _last
