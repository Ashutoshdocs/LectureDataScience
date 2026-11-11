import shutil

# Create a sample source file for this exercise.
with open("source.txt", "w", encoding="utf-8") as file:
    file.write("Hello Python")

# Copy the file to a new name.
shutil.copy("source.txt", "backup.txt")

with open("backup.txt", encoding="utf-8") as file:
    print(file.read())
