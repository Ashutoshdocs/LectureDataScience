# Import the module or specific tools needed for this lesson.
import json

# Start an error-handling block for operations that may fail.
try:
    # Open/use the resource in a context manager so it is closed automatically.
    with open("broken.json", encoding="utf-8") as f:
        # Call the relevant Python function/method to perform this file or data operation.
        json.load(f)
# Catch the specified exception so the program can respond safely.
except json.JSONDecodeError as e:
    # Display this value so we can inspect the program's result.
    print("Bad JSON:", e.msg, "at line", e.lineno, "column", e.colno)

# Assign the calculated or created value to events for later use.
events = [{"user": "asha", "action": "login"}, {"user": "ravi", "action": "search"}]
# Open/use the resource in a context manager so it is closed automatically.
with open("events.jsonl", "a", encoding="utf-8") as f:
    # Loop through each item so the same operation is applied repeatedly.
    for e in events:
        # Perform this operation; the expression or method shown determines the exact action.
        f.write(json.dumps(e) + "\n")

# Open/use the resource in a context manager so it is closed automatically.
with open("events.jsonl", encoding="utf-8") as f:
    # Assign the calculated or created value to records for later use.
    records = [json.loads(line) for line in f if line.strip()]

# Display this value so we can inspect the program's result.
print(len(records), "events")
# Display this value so we can inspect the program's result.
print([r["action"] for r in records])
