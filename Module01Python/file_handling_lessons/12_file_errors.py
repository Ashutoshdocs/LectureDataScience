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
os.chdir(os.path.dirname(os.path.abspath(__file__)))


print("===== 1. FileNotFoundError =====")
try:
    with open("missing.txt", encoding="utf-8") as f:
        print(f.read())
except FileNotFoundError:
    print("Sorry, missing.txt was not found.")


print("\n===== 2. Getting the error message with 'as' =====")
try:
    open("missing.txt", encoding="utf-8")
except FileNotFoundError as error:
    print("Error type   :", type(error).__name__)
    print("Error message:", error)


print("\n===== 3. try / except / else / finally =====")
def read_file(name):
    try:
        f = open(name, encoding="utf-8")
    except FileNotFoundError:
        print(f"  except : {name} not found")
    else:
        with f:
            print(f"  else   : {name} has {len(f.readlines())} lines")
    finally:
        print(f"  finally: finished with {name}")

read_file("notes.txt")
read_file("ghost.txt")


print("\n===== 4. Bad data inside a file =====")
with open("shopping.txt", encoding="utf-8") as f:
    lines = f.readlines()
lines.append("chocolate many\n")          # a broken line, on purpose
for line in lines[-3:]:
    item, qty = line.split()
    try:
        print(item, int(qty) * 2)
    except ValueError:
        print(f"Cannot turn '{qty}' into a number - skipped")


print("\n===== 5. Broken JSON =====")
try:
    json.loads('{"name": "Asha", }')      # extra comma = invalid JSON
except json.JSONDecodeError as error:
    print("Invalid JSON:", error)


print("\n===== 6. Using a closed file =====")
with open("notes.txt", encoding="utf-8") as f:
    pass
try:
    f.read()
except ValueError as error:
    print("ValueError:", error)


print("\n===== 7. Opening a folder as a file =====")
os.makedirs("output", exist_ok=True)
try:
    open("output", encoding="utf-8")
except (IsADirectoryError, PermissionError) as error:   # Windows gives PermissionError
    print(type(error).__name__, "- that is a folder, not a file")


print("\n===== 8. Check first with os.path.exists() =====")
for name in ["story.txt", "unknown.txt"]:
    if os.path.exists(name):
        print(name, "exists")
    else:
        print(name, "does NOT exist")
