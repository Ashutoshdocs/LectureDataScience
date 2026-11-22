# Python `if __name__ == "__main__"` — Two-Module Demo

This practical demonstrates the exact Python pattern:

```python
if __name__ == "__main__":
    main()
```

Both files can be:
- executed directly as Python programs; or
- imported by another Python file as modules without automatically running their demo code.

The two modules can also call functions from each other.

## 1. Project structure

```text
python_name_main_demo/
├── module_a.py
├── module_b.py
└── README.md
```

## 2. Understand the special variable `__name__`

Python automatically sets a variable named `__name__` in every module.

- When you execute a file directly, Python sets `__name__` to `"__main__"`.
- When another file imports it, Python sets `__name__` to that module's name, such as `"module_a"`.

Therefore:

```python
if __name__ == "__main__":
    main()
```

means: call `main()` only when this file is executed directly. Do not run that entry-point code merely because another file imports the module.

Important: Python still executes the module's top-level statements and function/class definitions during import. The `if` guard prevents only the code placed inside that guarded block from running on import.

## 3. File 1 — `module_a.py`

```python
def message_from_a():
    return "Hello from Module A"


def call_module_b():
    import module_b
    return module_b.message_from_b()


def main():
    print(message_from_a())
    print(call_module_b())


if __name__ == "__main__":
    main()
```

## 4. File 2 — `module_b.py`

```python
def message_from_b():
    return "Hello from Module B"


def call_module_a():
    import module_a
    return module_a.message_from_a()


def main():
    print(message_from_b())
    print(call_module_a())


if __name__ == "__main__":
    main()
```

The imports inside `call_module_a()` and `call_module_b()` are intentional. They let the two modules call each other without importing each other immediately while Python is still loading the files.

## 5. Step-by-step practical

### Step 1: Run Module A directly

From the folder containing both files:

```bash
python module_a.py
```

Expected output:

```text
Hello from Module A
Hello from Module B
```

Here `module_a.py` is the main program, so its `__name__` is `"__main__"` and its `main()` function runs.

### Step 2: Run Module B directly

```bash
python module_b.py
```

Expected output:

```text
Hello from Module B
Hello from Module A
```

Now `module_b.py` is the main program. The same rule applies.

### Step 3: Import Module A from another Python session

Start Python:

```bash
python
```

Then type:

```python
import module_a
print("Import completed")
```

Expected output:

```text
Import completed
```

Notice that the two demo messages were not printed. Importing defined the functions, but did not execute the guarded `main()` block.

Now call a function explicitly:

```python
print(module_a.message_from_a())
```

Output:

```text
Hello from Module A
```

Call Module B through Module A:

```python
print(module_a.call_module_b())
```

Output:

```text
Hello from Module B
```

Exit the Python prompt:

```python
exit()
```

### Step 4: Import Module B and call Module A

```python
import module_b

print(module_b.message_from_b())
print(module_b.call_module_a())
```

Expected output:

```text
Hello from Module B
Hello from Module A
```

## 6. Compare direct execution and import

| Action | Value of `__name__` in the file | Does guarded `main()` run automatically? |
|---|---|---|
| `python module_a.py` | `"__main__"` | Yes |
| `python module_b.py` | `"__main__"` | Yes |
| `import module_a` | `"module_a"` | No |
| `import module_b` | `"module_b"` | No |

## 7. The execution flow

```text
                    Run module_a.py
                           |
                  __name__ == "__main__"?
                           |
                          Yes
                           |
                        main()
                           |
                  call_module_b()
                           |
                      import module_b
                           |
                 call message_from_b()
```

When imported by another file:

```text
                  another_program.py
                           |
                    import module_a
                           |
             Python loads module_a definitions
                           |
              __name__ is "module_a"
                           |
                 guarded main() skipped
                           |
             caller chooses which function
                       to call
```

## 8. Teaching points and common mistakes

1. The special variable is `__name__` (two underscores before and after `name`).
2. The string is `"__main__"` (two underscores before and after `main`).
3. `main()` is an ordinary function name. Python does not require you to call your entry-point function `main`.
4. The `if` guard is not what makes a file importable. Python modules are importable by their module name; the guard controls whether the demo/entry-point code runs automatically.
5. Do not put important reusable function definitions inside the guard. If you do, those functions will not be defined when the file is imported.
6. Avoid top-level code with side effects (such as starting a server or deleting files) if the module is intended to be safely imported.

## 9. Student practice

- Add `message_from_a()` and `message_from_b()` parameters so each accepts a student's name.
- Add a third file, `student.py`, that imports both modules and calls their functions.
- Run each module directly and then import it. Observe the difference.
- Add a `print("Module A is being loaded")` statement at the top of `module_a.py`. Import it and observe that top-level statements still execute even though `main()` does not.

**Remember:** direct execution runs the guarded entry point; importing makes the module's reusable definitions available without automatically running that entry point.
