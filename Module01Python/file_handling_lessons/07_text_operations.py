# =============================================================
# LESSON 07 - DOING THINGS WITH THE TEXT YOU READ
# Files used: notes.txt, story.txt, shopping.txt
# Creates: output/story_upper.txt
# =============================================================

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.makedirs("output", exist_ok=True)

with open("story.txt", encoding="utf-8") as f:
    text = f.read()
lines = text.splitlines()


print("===== 1. Count lines, words, characters =====")
words = text.split()                     # split() breaks text at spaces
print("Lines     :", len(lines))
print("Words     :", len(words))
print("Characters:", len(text))


print("\n===== 2. Search with 'in' and count() =====")
print("'Pixel' in text?  ", "Pixel" in text)
print("'dragon' in text? ", "dragon" in text)
print("'Pixel' appears", text.count("Pixel"), "times")
print("'box' first found at position", text.find("box"))


print("\n===== 3. Show lines that contain a word =====")
word = "book"
for number, line in enumerate(lines, start=1):
    if word in line.lower():
        print(f"line {number}: {line}")


print("\n===== 4. Cleaning text =====")
messy = "   Hello World!   \n"
print(repr(messy.strip()))          # remove spaces and \n from both ends
print(messy.strip().lower())        # small letters
print(messy.strip().upper())        # CAPITAL letters
print(messy.strip().replace("World", "Python"))


print("\n===== 5. Split a line into parts =====")
with open("shopping.txt", encoding="utf-8") as f:
    total = 0
    for line in f:
        item, qty = line.split()    # "eggs 12" -> ["eggs", "12"]
        total += int(qty)           # int() turns "12" into 12
print("Total quantity of all items:", total)


print("\n===== 6. Most common words =====")
counts = {}
for w in words:
    w = w.strip(".,").lower()       # remove punctuation, make lowercase
    counts[w] = counts.get(w, 0) + 1
top = sorted(counts.items(), key=lambda pair: pair[1], reverse=True)[:5]
print(top)


print("\n===== 7. First, last, longest =====")
print("First 3 lines:", lines[:3])
print("Last line    :", lines[-1])
print("Longest line :", max(lines, key=len))


print("\n===== 8. Lines that START with something =====")
with open("notes.txt", encoding="utf-8") as f:
    for line in f:
        if line.startswith("Mode"):
            print(line.strip())


print("\n===== 9. Read -> change -> save to a new file =====")
with open("story.txt", encoding="utf-8") as src, \
     open("output/story_upper.txt", "w", encoding="utf-8") as dst:
    for number, line in enumerate(src, start=1):
        dst.write(f"{number:02}. {line.upper()}")
print("Saved output/story_upper.txt")
