# Open/use the resource in a context manager so it is closed automatically.
with open("diary.txt", encoding="utf-8") as f:
    # Display this value so we can inspect the program's result.
    print(repr(f.read(5)))
    # Display this value so we can inspect the program's result.
    print("position:", f.tell())
    # Display this value so we can inspect the program's result.
    print(repr(f.readline()))
    # Assign the calculated or created value to rest for later use.
    rest = f.readlines()
    # Display this value so we can inspect the program's result.
    print(rest)
    # Display this value so we can inspect the program's result.
    print("at the end:", repr(f.read()))

    # Perform this operation; the expression or method shown determines the exact action.
    f.seek(0)
    # Loop through each item so the same operation is applied repeatedly.
    for number, line in enumerate(f, start=1):
        # Display this value so we can inspect the program's result.
        print(number, line.rstrip("\n"))
