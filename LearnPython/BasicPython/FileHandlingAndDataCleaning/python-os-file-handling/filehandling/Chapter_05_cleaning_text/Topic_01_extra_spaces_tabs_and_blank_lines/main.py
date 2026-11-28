# Import the module or specific tools needed for this lesson.
import re

# Open/use the resource in a context manager so it is closed automatically.
with open("messy.txt", encoding="utf-8") as f:
    # Assign the calculated or created value to raw_lines for later use.
    raw_lines = f.readlines()

# Display this value so we can inspect the program's result.
print("RAW (repr shows hidden characters):")
# Loop through each item so the same operation is applied repeatedly.
for line in raw_lines:
    # Display this value so we can inspect the program's result.
    print(" ", repr(line))

# Define a reusable function; parameters let the caller provide input.
def tidy(line):
    # Send this result back to the caller and finish the function.
    return " ".join(line.split())

# Assign the calculated or created value to clean for later use.
clean = [tidy(line) for line in raw_lines]
# Assign the calculated or created value to clean for later use.
clean = [line for line in clean if line]

# Display this value so we can inspect the program's result.
print("CLEAN:")
# Loop through each item so the same operation is applied repeatedly.
for line in clean:
    # Display this value so we can inspect the program's result.
    print(" ", repr(line))

# Assign the calculated or created value to same for later use.
same = re.sub(r"\s+", " ", raw_lines[0]).strip()
# Display this value so we can inspect the program's result.
print("regex version:", repr(same))

# Open/use the resource in a context manager so it is closed automatically.
with open("clean.txt", "w", encoding="utf-8") as f:
    # Perform this operation; the expression or method shown determines the exact action.
    f.write("\n".join(clean) + "\n")
