# Import the module or specific tools needed for this lesson.
import re
# Import the module or specific tools needed for this lesson.
import unicodedata

# Assign the calculated or created value to EMOJI for later use.
EMOJI = re.compile(
    # Perform this operation; the expression or method shown determines the exact action.
    "["
    # Perform this operation; the expression or method shown determines the exact action.
    "\U0001F300-\U0001FAFF"   # faces, objects, gestures, food...
    # Perform this operation; the expression or method shown determines the exact action.
    "\U00002600-\U000027BF"   # misc symbols & dingbats: ★ ☀ ✔
    # Perform this operation; the expression or method shown determines the exact action.
    "\U0001F1E6-\U0001F1FF"   # flag letters
    # Perform this operation; the expression or method shown determines the exact action.
    "\uFE0F\u200D"            # invisible emoji modifiers / joiners
    # Perform this operation; the expression or method shown determines the exact action.
    "]+"
# Perform this operation; the expression or method shown determines the exact action.
)

# Define a reusable function; parameters let the caller provide input.
def remove_emojis(text):
    # Send this result back to the caller and finish the function.
    return EMOJI.sub("", text)

# Define a reusable function; parameters let the caller provide input.
def remove_symbols(text):
    # Send this result back to the caller and finish the function.
    return "".join(ch for ch in text if not unicodedata.category(ch).startswith("S"))

# Define a reusable function; parameters let the caller provide input.
def ascii_only(text):
    # Send this result back to the caller and finish the function.
    return text.encode("ascii", "ignore").decode()

# Define a reusable function; parameters let the caller provide input.
def squash(text):
    # Send this result back to the caller and finish the function.
    return " ".join(text.split())

# Open/use the resource in a context manager so it is closed automatically.
with open("reviews.txt", encoding="utf-8") as f:
    # Assign the calculated or created value to lines for later use.
    lines = f.read().splitlines()

# Loop through each item so the same operation is applied repeatedly.
for line in lines:
    # Display this value so we can inspect the program's result.
    print("original :", line)
    # Display this value so we can inspect the program's result.
    print("no emoji :", squash(remove_emojis(line)))
    # Display this value so we can inspect the program's result.
    print("no symbol:", squash(remove_symbols(line)))
    # Display this value so we can inspect the program's result.
    print("ascii    :", squash(ascii_only(line)))
    # Display this value so we can inspect the program's result.
    print()
