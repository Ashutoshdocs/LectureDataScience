# Folder 5 – Introduce `if __name__ == "__main__"`

A Python file can be:
- run directly, for example `python3 program1.py`
- imported by another Python file

The condition:

```python
if __name__ == "__main__":
    main()
```

runs `main()` only when that file is executed directly. It does not run when the file is imported as a module.

In this folder:
- `program1.py` and `program2.py` each define a `main()` function.
- `common.py` contains reusable functions.
- Running `common.py` directly also runs its small test block, but importing it does not.

Try these commands from this folder:

```bash
python3 program1.py
python3 program2.py
python3 common.py
```

## Important distinction

`__name__` is a special Python variable:
- Direct execution: `__name__` is set to `"__main__"`.
- Imported module: `__name__` is set to the module's name (for example, `"common"`).
