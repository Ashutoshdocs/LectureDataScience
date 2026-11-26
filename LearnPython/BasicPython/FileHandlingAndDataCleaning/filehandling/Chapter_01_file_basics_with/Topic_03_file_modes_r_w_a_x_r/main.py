# Open/use the resource in a context manager so it is closed automatically.
with open("log.txt", "w", encoding="utf-8") as f:
    # Perform this operation; the expression or method shown determines the exact action.
    f.write("line 1\n")

# Open/use the resource in a context manager so it is closed automatically.
with open("log.txt", "a", encoding="utf-8") as f:
    # Perform this operation; the expression or method shown determines the exact action.
    f.write("line 2\n")

# Start an error-handling block for operations that may fail.
try:
    # Open/use the resource in a context manager so it is closed automatically.
    with open("log.txt", "x", encoding="utf-8") as f:
        # Perform this operation; the expression or method shown determines the exact action.
        f.write("never written")
# Catch the specified exception so the program can respond safely.
except FileExistsError:
    # Display this value so we can inspect the program's result.
    print("x mode: log.txt already exists")

# Open/use the resource in a context manager so it is closed automatically.
with open("log.txt", "r+", encoding="utf-8") as f:
    # Assign the calculated or created value to old for later use.
    old = f.read()
    # Perform this operation; the expression or method shown determines the exact action.
    f.write("line 3\n")

# Open/use the resource in a context manager so it is closed automatically.
with open("log.txt", encoding="utf-8") as f:
    # Display this value so we can inspect the program's result.
    print(f.read().strip())

# Open/use the resource in a context manager so it is closed automatically.
with open("log.txt", "w", encoding="utf-8") as f:
    # Do nothing here; this placeholder keeps the block syntactically valid.
    pass

# Open/use the resource in a context manager so it is closed automatically.
with open("log.txt", encoding="utf-8") as f:
    # Display this value so we can inspect the program's result.
    print("after 'w' again:", repr(f.read()))
