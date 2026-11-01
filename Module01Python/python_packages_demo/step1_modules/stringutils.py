"""stringutils.py - a second module, used to show different import styles."""

__all__ = ["shout", "reverse"]  # controls what `from stringutils import *` exports


def shout(text):
    return text.upper() + "!"


def reverse(text):
    return text[::-1]


def whisper(text):
    # Not listed in __all__, so `import *` will skip it
    # (but `from stringutils import whisper` still works).
    return text.lower() + "..."
