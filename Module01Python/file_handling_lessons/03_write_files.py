# =============================================================
# LESSON 03 - WRITING FILES (mode "w")
# Creates: output/my_notes.txt
# =============================================================
# Mode "w" = write.
#   - If the file does NOT exist -> Python creates it
#   - If the file DOES exist     -> Python ERASES it first!

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.makedirs("output", exist_ok=True)   # make an 'output' folder (lesson 13 explains)


print("===== 1. write(): write a string =====")
with open("output/my_notes.txt", "w", encoding="utf-8") as f:
    count = f.write("Hello file!\n")   # write() returns number of characters
    f.write("This is my second line.\n")
print("write() returned:", count)

with open("output/my_notes.txt", encoding="utf-8") as f:
    print(f.read())
# IMPORTANT: write() does NOT add a new line. You must add '\n' yourself.


print("===== 2. Opening with 'w' again ERASES the old text =====")
with open("output/my_notes.txt", "w", encoding="utf-8") as f:
    f.write("Old lines are gone!\n")

with open("output/my_notes.txt", encoding="utf-8") as f:
    print(f.read())


print("===== 3. writelines(): write a list of strings =====")
fruits = ["apple\n", "mango\n", "banana\n"]
with open("output/my_notes.txt", "w", encoding="utf-8") as f:
    f.writelines(fruits)

with open("output/my_notes.txt", encoding="utf-8") as f:
    print(f.read())


print("===== 4. Write a list using a loop =====")
colors = ["red", "green", "blue"]
with open("output/my_notes.txt", "w", encoding="utf-8") as f:
    for color in colors:
        f.write(color + "\n")


print("===== 5. Write a list using join() =====")
with open("output/my_notes.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(colors) + "\n")

with open("output/my_notes.txt", encoding="utf-8") as f:
    print(f.read())


print("===== 6. Numbers must become strings =====")
with open("output/my_notes.txt", "w", encoding="utf-8") as f:
    age = 15
    # f.write(age)        <- ERROR: write() only accepts strings
    f.write(str(age) + "\n")          # convert with str()
    f.write(f"Next year I will be {age + 1}\n")   # or use an f-string

with open("output/my_notes.txt", encoding="utf-8") as f:
    print(f.read())
