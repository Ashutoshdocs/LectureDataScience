# Import the module or specific tools needed for this lesson.
import string
# Import the module or specific tools needed for this lesson.
import unicodedata

# Assign the calculated or created value to samples for later use.
samples = ["Café  CRÈME", "“Smart” quotes ‘here’!", "ＦＵＬＬ　ｗｉｄｔｈ　１２３", "Straße"]

# Define a reusable function; parameters let the caller provide input.
def strip_accents(text):
    # Assign the calculated or created value to decomposed for later use.
    decomposed = unicodedata.normalize("NFKD", text)
    # Send this result back to the caller and finish the function.
    return "".join(ch for ch in decomposed if not unicodedata.combining(ch))

# Assign the calculated or created value to QUOTES for later use.
QUOTES = str.maketrans({"“": '"', "”": '"', "‘": "'", "’": "'"})
# Assign the calculated or created value to NO_PUNCT for later use.
NO_PUNCT = str.maketrans("", "", string.punctuation + "“”‘’")

# Loop through each item so the same operation is applied repeatedly.
for s in samples:
    # Display this value so we can inspect the program's result.
    print(repr(s))
    # Display this value so we can inspect the program's result.
    print("  lower     :", s.lower())
    # Display this value so we can inspect the program's result.
    print("  casefold  :", s.casefold())
    # Display this value so we can inspect the program's result.
    print("  NFKC      :", unicodedata.normalize("NFKC", s))
    # Display this value so we can inspect the program's result.
    print("  no accents:", strip_accents(s))
    # Display this value so we can inspect the program's result.
    print("  quotes    :", s.translate(QUOTES))
    # Display this value so we can inspect the program's result.
    print("  no punct  :", s.translate(NO_PUNCT))
