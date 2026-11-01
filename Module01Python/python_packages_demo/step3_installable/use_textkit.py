"""Run this from ANY folder after `pip install -e .` - the package is now importable everywhere."""

import textkit
from textkit import is_palindrome

print("textkit version:", textkit.__version__)
print("Loaded from:   ", textkit.__file__)
print(textkit.word_count("Python packages are fun"))
print(is_palindrome("Never odd or even"))
print(textkit.title_case("modules and packages"))
