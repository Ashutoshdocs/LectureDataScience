# Import the module or specific tools needed for this lesson.
import re

# Assign the calculated or created value to keyword for later use.
keyword = "python"

# Open/use the resource in a context manager so it is closed automatically.
with open("notes.txt", encoding="utf-8") as f:
    # Assign the calculated or created value to text for later use.
    text = f.read()

# Display this value so we can inspect the program's result.
print("substring matches:", text.lower().count(keyword))

# Assign the calculated or created value to pattern for later use.
pattern = re.compile(rf"\b{re.escape(keyword)}\b", re.IGNORECASE)
# Display this value so we can inspect the program's result.
print("whole-word matches:", len(pattern.findall(text)))

# Display this value so we can inspect the program's result.
print("--- lines containing the word")
# Loop through each item so the same operation is applied repeatedly.
for number, line in enumerate(text.splitlines(), start=1):
    # Check this condition; the indented block runs only when it is true.
    if pattern.search(line):
        # Display this value so we can inspect the program's result.
        print(f"{number:>2}: {line}")
