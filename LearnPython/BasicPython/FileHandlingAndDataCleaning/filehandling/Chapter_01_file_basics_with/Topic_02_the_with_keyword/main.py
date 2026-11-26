# Open/use the resource in a context manager so it is closed automatically.
with open("diary.txt", encoding="utf-8") as f:
    # Assign the calculated or created value to first for later use.
    first = f.readline()
    # Display this value so we can inspect the program's result.
    print("inside the block, closed?", f.closed)

# Display this value so we can inspect the program's result.
print("after the block, closed? ", f.closed)
# Display this value so we can inspect the program's result.
print(first.strip())

# Start an error-handling block for operations that may fail.
try:
    # Open/use the resource in a context manager so it is closed automatically.
    with open("diary.txt", encoding="utf-8") as f:
        # Perform this operation; the expression or method shown determines the exact action.
        f.read()
        # Raise an exception deliberately to signal an error condition.
        raise ValueError("something went wrong")
# Catch the specified exception so the program can respond safely.
except ValueError as e:
    # Display this value so we can inspect the program's result.
    print("error:", e)

# Display this value so we can inspect the program's result.
print("closed even after the error?", f.closed)
