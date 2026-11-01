# =============================================================
# LESSON 12 - HANDLING FILE ERRORS
# =============================================================
# Things go wrong: files go missing, have bad data, etc.
# try / except stops your program from crashing.
#
#   try:      code that might fail
#   except:   what to do if it fails
#   else:     runs only if there was NO error
#   finally:  runs ALWAYS

import json
import os

# Changes the working directory to the folder containing this script to avoid path errors.
os.chdir(os.path.dirname(os.path.abspath(__file__)))


print("===== 1. FileNotFoundError =====")
# Starts a guarded code block where potential file-system exceptions could occur.
try:
    # Attempts to open a non-existent file for reading.
    with open("missing.txt", encoding="utf-8") as f:
        print(f.read())
# Intercepts a FileNotFoundError if it gets thrown inside the try block, preventing a crash.
except FileNotFoundError:
    # Executes alternative fallback logic to handle the missing file issue gracefully.
    print("Sorry, missing.txt was not found.")


print("\n===== 2. Getting the error message with 'as' =====")
try:
    open("missing.txt", encoding="utf-8")
# Captures the exception object into a variable named 'error' to inspect its internal metadata.
except FileNotFoundError as error:
    # Extracts and prints the string name of the specific exception class.
    print("Error type   :", type(error).__name__)
    # Prints the descriptive system error string explaining what went wrong.
    print("Error message:", error)


print("\n===== 3. try / except / else / finally =====")
# Defines a reusable file reading workflow utilizing full exception lifecycle keywords.
def read_file(name):
    try:
        # Attempts to open the target file path.
        f = open(name, encoding="utf-8")
    except FileNotFoundError:
        # Runs only if a FileNotFoundError occurs during the open() attempt.
        print(f"  except : {name} not found")
    else:
        # Runs only if the try block executed successfully without throwing any errors.
        # Wraps the pre-opened file handler in a context manager to ensure safe closing.
        with f:
            print(f"  else   : {name} has {len(f.readlines())} lines")
    finally:
        # Executes unconditionally at the end of the block, regardless of errors or successes.
        print(f"  finally: finished with {name}")

# Tests the function with a file that exists.
read_file("notes.txt")
# Tests the function with a file that does not exist.
read_file("ghost.txt")


print("\n===== 4. Bad data inside a file =====")
with open("shopping.txt", encoding="utf-8") as f:
    lines = f.readlines()
# Manually appends a corrupt string value to simulate an input error in data formats.
lines.append("chocolate many\n")          # a broken line, on purpose
# Loops through the last three rows of the lines list array.
for line in lines[-3:]:
    # Unpacks the text tokens split across empty spaces.
    item, qty = line.split()
    try:
        # Attempts to convert the quantity string into an integer and multiply it mathematically.
        print(item, int(qty) * 2)
    # Catches the specific error thrown when a string cannot be parsed into a numeric base.
    except ValueError:
        # Prints a warning message for the corrupt entry and skips processing it.
        print(f"Cannot turn '{qty}' into a number - skipped")


print("\n===== 5. Broken JSON =====")
try:
    # Attempts to deserialize an invalid JSON string structure containing a trailing comma.
    json.loads('{"name": "Asha", }')      # extra comma = invalid JSON
# Catches the specific parser exceptions built into the core json data module.
except json.JSONDecodeError as error:
    # Displays the precise location and nature of the formatting error discovered by the engine.
    print("Invalid JSON:", error)


print("\n===== 6. Using a closed file =====")
with open("notes.txt", encoding="utf-8") as f:
    # Opens and immediately leaves the block, which automatically closes the file handle object.
    pass
try:
    # Attempts to execute a read stream on an stream reference that is already closed.
    f.read()
# Catches the internal valuation exception raised by illegal operations on closed references.
except ValueError as error:
    print("ValueError:", error)


print("\n===== 7. Opening a folder as a file =====")
os.makedirs("output", exist_ok=True)
try:
    # Attempts to call the open file constructor pointing directly at a directory path name instead.
    open("output", encoding="utf-8")
# Uses a tuple to intercept either operating system directory errors or permission conflicts across platforms.
except (IsADirectoryError, PermissionError) as error:   # Windows gives PermissionError
    print(type(error).__name__, "- that is a folder, not a file")


print("\n===== 8. Check first with os.path.exists() =====")
# Iterates through a test array tracking both predictable and random filename keys.
for name in ["story.txt", "unknown.txt"]:
    # Proactively checks the file system structure without using try/except blocks.
    if os.path.exists(name):
        print(name, "exists")
    else:
        print(name, "does NOT exist")
