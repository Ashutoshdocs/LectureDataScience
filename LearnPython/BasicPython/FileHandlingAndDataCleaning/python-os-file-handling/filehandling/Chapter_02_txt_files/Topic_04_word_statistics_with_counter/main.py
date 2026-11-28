# Import the module or specific tools needed for this lesson.
import re
# Import the module or specific tools needed for this lesson.
from collections import Counter

# Open/use the resource in a context manager so it is closed automatically.
with open("article.txt", encoding="utf-8") as f:
    # Assign the calculated or created value to text for later use.
    text = f.read()

# Assign the calculated or created value to lines for later use.
lines = text.splitlines()
# Assign the calculated or created value to words for later use.
words = re.findall(r"[a-z']+", text.lower())

# Display this value so we can inspect the program's result.
print("lines     :", len(lines))
# Display this value so we can inspect the program's result.
print("words     :", len(words))
# Display this value so we can inspect the program's result.
print("characters:", len(text))
# Display this value so we can inspect the program's result.
print("unique    :", len(set(words)))

# Assign the calculated or created value to STOP for later use.
STOP = {"the", "a", "and", "is", "of", "to", "in", "it", "for", "are"}
# Assign the calculated or created value to counts for later use.
counts = Counter(w for w in words if w not in STOP)
# Loop through each item so the same operation is applied repeatedly.
for word, n in counts.most_common(5):
    # Display this value so we can inspect the program's result.
    print(f"{word:<10} {n}")
