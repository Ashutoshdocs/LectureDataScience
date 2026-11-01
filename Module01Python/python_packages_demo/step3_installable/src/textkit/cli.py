"""textkit.cli - command-line entry point (wired up in pyproject.toml)."""

import argparse

from . import __version__
from .core import word_count, is_palindrome, title_case


def main():
    parser = argparse.ArgumentParser(prog="textkit", description="Tiny text tools")
    parser.add_argument("action", choices=["count", "palindrome", "title"])
    parser.add_argument("text", help="text to process (quote it)")
    parser.add_argument("--version", action="version", version=__version__)
    args = parser.parse_args()

    if args.action == "count":
        print(word_count(args.text))
    elif args.action == "palindrome":
        print(is_palindrome(args.text))
    else:
        print(title_case(args.text))


if __name__ == "__main__":
    main()
