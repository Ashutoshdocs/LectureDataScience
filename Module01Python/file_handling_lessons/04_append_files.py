# =============================================================
# LESSON 04 - APPENDING (mode "a") AND print() TO A FILE
# Creates: output/diary.txt
# =============================================================
# Mode "a" = append. It ADDS to the END of the file.
# Old content is KEPT. If the file is missing, it is created.

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.makedirs("output", exist_ok=True)


# Start with a fresh file
with open("output/diary.txt", "w", encoding="utf-8") as f:
    f.write("Day 1: Learned to read files.\n")

print("===== 1. Append new lines =====")
with open("output/diary.txt", "a", encoding="utf-8") as f:
    f.write("Day 2: Learned to write files.\n")
    f.write("Day 3: Learned to append.\n")

with open("output/diary.txt", encoding="utf-8") as f:
    print(f.read())


print("===== 2. Append in a loop =====")
for day in range(4, 7):
    with open("output/diary.txt", "a", encoding="utf-8") as f:
        f.write(f"Day {day}: Practised more.\n")

with open("output/diary.txt", encoding="utf-8") as f:
    print(f.read())


print("===== 3. print() can write to a file =====")
# print adds '\n' automatically and accepts numbers too.
with open("output/diary.txt", "a", encoding="utf-8") as f:
    print("Day 7:", "Used print with file=", file=f)
    print("Total days:", 7, file=f)
    print("A", "B", "C", sep="-", file=f)    # sep = what goes between items

with open("output/diary.txt", encoding="utf-8") as f:
    print(f.read())


print("===== 4. Copy shopping.txt items to a new file, adding a tick =====")
with open("shopping.txt", encoding="utf-8") as src, \
     open("output/diary.txt", "a", encoding="utf-8") as dst:
    for line in src:
        dst.write("[x] " + line)
print("Done. Open output/diary.txt to see it.")

# SUMMARY:  "w" = erase and write    "a" = keep and add to end
