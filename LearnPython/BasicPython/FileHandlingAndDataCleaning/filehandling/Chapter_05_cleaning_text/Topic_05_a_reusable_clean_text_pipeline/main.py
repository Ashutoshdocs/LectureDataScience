# Import the module or specific tools needed for this lesson.
from cleaner import clean_text

# Open/use the resource in a context manager so it is closed automatically.
with open("raw_comments.txt", encoding="utf-8") as f:
    # Assign the calculated or created value to raw for later use.
    raw = f.read().splitlines()

# Assign the calculated or created value to cleaned for later use.
cleaned = []
# Assign the calculated or created value to seen for later use.
seen = set()
# Loop through each item so the same operation is applied repeatedly.
for line in raw:
    # Assign the calculated or created value to text for later use.
    text = clean_text(line)
    # Check this condition; the indented block runs only when it is true.
    if text and text not in seen:
        # Perform this operation; the expression or method shown determines the exact action.
        seen.add(text)
        # Perform this operation; the expression or method shown determines the exact action.
        cleaned.append(text)

# Open/use the resource in a context manager so it is closed automatically.
with open("comments_clean.txt", "w", encoding="utf-8") as f:
    # Perform this operation; the expression or method shown determines the exact action.
    f.write("\n".join(cleaned) + "\n")

# Display this value so we can inspect the program's result.
print(f"{len(raw)} raw lines -> {len(cleaned)} clean lines")
# Loop through each item so the same operation is applied repeatedly.
for text in cleaned:
    # Display this value so we can inspect the program's result.
    print("-", text)
