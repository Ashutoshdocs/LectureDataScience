# =============================================================
# LESSON 03 - WRITING FILES (mode "w")
# Creates: output/my_notes.txt
# =============================================================
# Mode "w" = write.
#   - If the file does NOT exist -> Python creates it
#   - If the file DOES exist     -> Python ERASES it first!

import os

# Changes the working directory to the folder where this specific script is saved.
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Creates a folder named "output" if it doesn't already exist.
# exist_ok=True prevents Python from throwing an error if the directory is already there.
os.makedirs("output", exist_ok=True)   # make an 'output' folder (lesson 13 explains)


print("===== 1. write(): write a string =====")
# Opens a file in "w" (Write) mode. This will create 'my_notes.txt' inside the 'output' folder.
with open("output/my_notes.txt", "w", encoding="utf-8") as f:
    # Writes the string to the file and saves the count of written characters (12) into 'count'.
    count = f.write("Hello file!\n")   # write() returns number of characters
    # Writes a second line of text into the file object.
    f.write("This is my second line.\n")
# Prints the number of characters written in that first f.write() statement.
print("write() returned:", count)

# Reopens the file in default read mode to verify and print the current contents.
with open("output/my_notes.txt", encoding="utf-8") as f:
    print(f.read())
# IMPORTANT: write() does NOT add a new line. You must add '\n' yourself.


print("===== 2. Opening with 'w' again ERASES the old text =====")
# Opening an existing file in "w" mode completely wipes out (truncates) any text inside it.
with open("output/my_notes.txt", "w", encoding="utf-8") as f:
    # Overwrites the file entirely with this new single string.
    f.write("Old lines are gone!\n")

# Reopens the file to display the updated, overwritten contents.
with open("output/my_notes.txt", encoding="utf-8") as f:
    print(f.read())


print("===== 3. writelines(): write a list of strings =====")
# A list of strings, where each element explicitly includes its own newline tag.
fruits = ["apple\n", "mango\n", "banana\n"]
# Opens the file in write mode, resetting it again.
with open("output/my_notes.txt", "w", encoding="utf-8") as f:
    # Takes an iterable (like a list) and writes all its strings sequentially into the file.
    f.writelines(fruits)

# Reopens the file to display the printed list of fruits.
with open("output/my_notes.txt", encoding="utf-8") as f:
    print(f.read())


print("===== 4. Write a list using a loop =====")
# A clean list of strings that do not contain newline tags.
colors = ["red", "green", "blue"]
# Opens the file in write mode, erasing previous data.
with open("output/my_notes.txt", "w", encoding="utf-8") as f:
    # Loops through the colors list item by item.
    for color in colors:
        # Concatenates a newline character to each color string before writing it out.
        f.write(color + "\n")


print("===== 5. Write a list using join() =====")
# Opens the file in write mode, wiping out the text from the previous step.
with open("output/my_notes.txt", "w", encoding="utf-8") as f:
    # Joins the list elements together into a single string separated by '\n', 
    # then appends a final '\n' at the very end to format the last line properly.
    f.write("\n".join(colors) + "\n")

# Reopens the file to verify the resulting structure.
with open("output/my_notes.txt", encoding="utf-8") as f:
    print(f.read())


print("===== 6. Numbers must become strings =====")
# Opens the file in write mode, clearing all text one last time.
with open("output/my_notes.txt", "w", encoding="utf-8") as f:
    # An integer variable.
    age = 15
    # f.write(age)        <- ERROR: write() only accepts strings
    # Converts the integer 15 into the string "15" and adds a newline before saving.
    f.write(str(age) + "\n")          # convert with str()
    # Uses an f-string to evaluate the math (15 + 1) and automatically converts it to text.
    f.write(f"Next year I will be {age + 1}\n")   # or use an f-string

# Reopens the file to print out the final, numerical-based text results.
with open("output/my_notes.txt", encoding="utf-8") as f:
    print(f.read())
