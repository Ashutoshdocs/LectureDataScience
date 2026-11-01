# =============================================================
# LESSON 07 - DOING THINGS WITH THE TEXT YOU READ
# Files used: notes.txt, story.txt, shopping.txt
# Creates: output/story_upper.txt
# =============================================================

import os

# Changes the working directory to the folder containing this script to avoid path errors.
os.chdir(os.path.dirname(os.path.abspath(__file__)))
# Creates an 'output' directory if it doesn't already exist.
os.makedirs("output", exist_ok=True)

# Opens the file story.txt in default read mode with UTF-8 character matching
with open("story.txt", encoding="utf-8") as f:
    # Reads the entire contents of the file into a single string variable
    text = f.read()
# Splits the huge text string by newlines, creating a clean list of individual lines without '\n'
lines = text.splitlines()


print("===== 1. Count lines, words, characters =====")
# split() without arguments breaks the text down into an array of individual words using whitespace as a divider
words = text.split()                     # split() breaks text at spaces
# Counts the total number of line elements inside the list
print("Lines     :", len(lines))
# Counts the total number of words found after splitting on spaces
print("Words     :", len(words))
# Counts every individual character inside the file including spaces and newlines
print("Characters:", len(text))


print("\n===== 2. Search with 'in' and count() =====")
# Evaluates to True if the exact substring "Pixel" exists inside the text string (case-sensitive)
print("'Pixel' in text?  ", "Pixel" in text)
# Evaluates to True if the exact substring "dragon" exists inside the text string
print("'dragon' in text? ", "dragon" in text)
# Returns the absolute frequency of how many times the substring "Pixel" shows up in the file
print("'Pixel' appears", text.count("Pixel"), "times")
# Returns the lowest integer index position where the word "box" starts; returns -1 if not found
print("'box' first found at position", text.find("box"))


print("\n===== 3. Show lines that contain a word =====")
# Target string we want to search for
word = "book"
# Iterates through the list of lines while generating a line number tracker starting at 1
for number, line in enumerate(lines, start=1):
    # Converts the whole line to lowercase so that search results match regardless of capitalisation
    if word in line.lower():
        # Prints out the matching row number alongside its text
        print(f"line {number}: {line}")


print("\n===== 4. Cleaning text =====")
# A messy test string containing spaces on both sides and a trailing newline
messy = "   Hello World!   \n"
# repr() demonstrates that strip() completely slices off leading and trailing spaces/newlines
print(repr(messy.strip()))          # remove spaces and \n from both ends
# Cleans the text margins and forces all letters into lowercase format
print(messy.strip().lower())        # small letters
# Cleans the text margins and forces all letters into uppercase format
print(messy.strip().upper())        # CAPITAL letters
# Cleans the text margins and swaps out the string target "World" for the replacement "Python"
print(messy.strip().replace("World", "Python"))


print("\n===== 5. Split a line into parts =====")
# Opens the shopping database document in read mode
with open("shopping.txt", encoding="utf-8") as f:
    # Initialises a counter variable to track the mathematical sum
    total = 0
    # Iterates over the raw file handler row by row
    for line in f:
        # Splits the line text at the space, unpacking the first part into 'item' and the second into 'qty'
        item, qty = line.split()    # "eggs 12" -> ["eggs", "12"]
        # Converts the 'qty' text string into an actual integer number and adds it to our running sum
        total += int(qty)           # int() turns "12" into 12
print("Total quantity of all items:", total)


print("\n===== 6. Most common words =====")
# Initialises an empty dictionary to map words to their frequency scores
counts = {}
# Iterates through our list of words generated in Section 1
for w in words:
    # Drops full stops and commas from margins and normalises letters to lowercase format
    w = w.strip(".,").lower()       # remove punctuation, make lowercase
    # Fetches the word's current score (defaults to 0 if new) and increments it by 1
    counts[w] = counts.get(w, 0) + 1
# Converts dictionary to key-value pairs, sorts them by count value (index 1) in descending order, and takes top 5
top = sorted(counts.items(), key=lambda pair: pair[1], reverse=True)[:5]
print(top)


print("\n===== 7. First, last, longest =====")
# Uses a list slice to print out the first three rows of the text file
print("First 3 lines:", lines[:3])
# Uses a negative index (-1) to target and print out the absolute last row of the file
print("Last line    :", lines[-1])
# Uses max() with a key parameter to find and print the string that has the highest character length
print("Longest line :", max(lines, key=len))


print("\n===== 8. Lines that START with something =====")
# Opens notes.txt in standard read mode
with open("notes.txt", encoding="utf-8") as f:
    # Loops over each line inside notes.txt
    for line in f:
        # Checks if the first characters of the row match the prefix "Mode" exactly
        if line.startswith("Mode"):
            # Strips the newline character off the row and prints it out
            print(line.strip())


print("\n===== 9. Read -> change -> save to a new file =====")
# Opens story.txt for reading and output/story_upper.txt for writing simultaneously
with open("story.txt", encoding="utf-8") as src, \
     open("output/story_upper.txt", "w", encoding="utf-8") as dst:
    # Iterates through the source file while counting row numbers starting at 1
    for number, line in enumerate(src, start=1):
        # Writes out the padded two-digit line number, a dot, and the completely capitalised line string
        dst.write(f"{number:02}. {line.upper()}")
print("Saved output/story_upper.txt")
