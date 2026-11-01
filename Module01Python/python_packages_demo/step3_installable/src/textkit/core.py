"""textkit.core - the actual logic."""


def word_count(text):
    return len(text.split())


def is_palindrome(text):
    cleaned = "".join(ch.lower() for ch in text if ch.isalnum())
    return cleaned == cleaned[::-1]


def title_case(text):
    return " ".join(word.capitalize() for word in text.split())
