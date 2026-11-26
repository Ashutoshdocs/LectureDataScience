# Import the module or specific tools needed for this lesson.
import re
# Import the module or specific tools needed for this lesson.
import unicodedata

# Assign the calculated or created value to EMOJI for later use.
EMOJI = re.compile("[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F1E6-\U0001F1FF\uFE0F\u200D]+")
# Assign the calculated or created value to URL for later use.
URL = re.compile(r"https?://\S+")
# Assign the calculated or created value to REPEAT_PUNCT for later use.
REPEAT_PUNCT = re.compile(r"([!?.])\1+")

# Define a reusable function; parameters let the caller provide input.
def clean_text(text, lower=True, remove_emoji=True, remove_urls=True):
    # Perform this operation; the expression or method shown determines the exact action.
    """Return a tidy version of one line of user text."""
    # Assign the calculated or created value to text for later use.
    text = unicodedata.normalize("NFKC", text)
    # Check this condition; the indented block runs only when it is true.
    if remove_urls:
        # Assign the calculated or created value to text for later use.
        text = URL.sub("", text)
    # Check this condition; the indented block runs only when it is true.
    if remove_emoji:
        # Assign the calculated or created value to text for later use.
        text = EMOJI.sub("", text)
    # Assign the calculated or created value to text for later use.
    text = REPEAT_PUNCT.sub(r"\1", text)
    # Assign the calculated or created value to text for later use.
    text = " ".join(text.split())
    # Check this condition; the indented block runs only when it is true.
    if lower:
        # Assign the calculated or created value to text for later use.
        text = text.lower()
    # Send this result back to the caller and finish the function.
    return text

# Run this block only when this file is executed directly, not when imported.
if __name__ == "__main__":
    # Display this value so we can inspect the program's result.
    print(clean_text("  WOW!!!   😍 see https://x.com  "))
