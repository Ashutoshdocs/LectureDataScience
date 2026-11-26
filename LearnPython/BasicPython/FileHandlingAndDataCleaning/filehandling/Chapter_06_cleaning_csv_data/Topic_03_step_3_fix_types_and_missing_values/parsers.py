# Import the module or specific tools needed for this lesson.
import re
# Import the module or specific tools needed for this lesson.
from datetime import datetime

# Assign the calculated or created value to EMOJI for later use.
EMOJI = re.compile("[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F1E6-\U0001F1FF\uFE0F\u200D]+")
# Assign the calculated or created value to EMAIL for later use.
EMAIL = re.compile(r"^[\w.+-]+@[\w-]+\.[\w.]+$")
# Assign the calculated or created value to DATE_FORMATS for later use.
DATE_FORMATS = ["%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d"]

# Define a reusable function; parameters let the caller provide input.
def clean_header(h):
    # Send this result back to the caller and finish the function.
    return "_".join(h.strip().lower().split())

# Define a reusable function; parameters let the caller provide input.
def clean_str(value):
    # Send this result back to the caller and finish the function.
    return " ".join(EMOJI.sub("", value).split())

# Define a reusable function; parameters let the caller provide input.
def to_int(value, low=None, high=None):
    # Start an error-handling block for operations that may fail.
    try:
        # Assign the calculated or created value to n for later use.
        n = int(value.strip())
    # Catch the specified exception so the program can respond safely.
    except ValueError:
        # Send this result back to the caller and finish the function.
        return None
    # Check this condition; the indented block runs only when it is true.
    if (low is not None and n < low) or (high is not None and n > high):
        # Send this result back to the caller and finish the function.
        return None
    # Send this result back to the caller and finish the function.
    return n

# Define a reusable function; parameters let the caller provide input.
def to_money(value):
    # Assign the calculated or created value to digits for later use.
    digits = re.sub(r"[^\d.\-]", "", value)
    # Send this result back to the caller and finish the function.
    return float(digits) if digits else None

# Define a reusable function; parameters let the caller provide input.
def to_date(value):
    # Loop through each item so the same operation is applied repeatedly.
    for fmt in DATE_FORMATS:
        # Start an error-handling block for operations that may fail.
        try:
            # Send this result back to the caller and finish the function.
            return datetime.strptime(value.strip(), fmt).date().isoformat()
        # Catch the specified exception so the program can respond safely.
        except ValueError:
            # Do nothing here; this placeholder keeps the block syntactically valid.
            pass
    # Send this result back to the caller and finish the function.
    return None

# Define a reusable function; parameters let the caller provide input.
def valid_email(value):
    # Send this result back to the caller and finish the function.
    return bool(EMAIL.match(value))
