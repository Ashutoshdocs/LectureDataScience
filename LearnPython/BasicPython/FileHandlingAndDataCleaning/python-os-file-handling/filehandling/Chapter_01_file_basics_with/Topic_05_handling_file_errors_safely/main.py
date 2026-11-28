# Import the module or specific tools needed for this lesson.
from pathlib import Path

# Call the relevant Python function/method to perform this file or data operation.
Path("data").mkdir()
# Call the relevant Python function/method to perform this file or data operation.
Path("image.bin").write_bytes(b"\xff\xfe\x00\x89")

# Define a reusable function; parameters let the caller provide input.
def read_safely(name):
    # Start an error-handling block for operations that may fail.
    try:
        # Open/use the resource in a context manager so it is closed automatically.
        with open(name, encoding="utf-8") as f:
            # Send this result back to the caller and finish the function.
            return f.read()
    # Catch the specified exception so the program can respond safely.
    except FileNotFoundError:
        # Send this result back to the caller and finish the function.
        return f"[missing: {name}]"
    # Catch the specified exception so the program can respond safely.
    except IsADirectoryError:
        # Send this result back to the caller and finish the function.
        return f"[{name} is a folder]"
    # Catch the specified exception so the program can respond safely.
    except UnicodeDecodeError:
        # Send this result back to the caller and finish the function.
        return f"[not UTF-8 text: {name}]"

# Display this value so we can inspect the program's result.
print(read_safely("diary.txt")[:24])
# Display this value so we can inspect the program's result.
print(read_safely("nope.txt"))
# Display this value so we can inspect the program's result.
print(read_safely("data"))
# Display this value so we can inspect the program's result.
print(read_safely("image.bin"))
