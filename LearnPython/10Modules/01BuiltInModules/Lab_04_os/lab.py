import os

print("Operating system name:", os.name)
print("Current working directory:", os.getcwd())
print("Directory contents:", os.listdir("."))

# Create a practice directory if it does not exist.
os.makedirs("os_practice", exist_ok=True)
print("Directory exists:", os.path.exists("os_practice"))

# Build a path safely for the current operating system.
file_path = os.path.join("os_practice", "hello.txt")
with open(file_path, "w", encoding="utf-8") as file:
    file.write("Created using Python os module")

print("File path:", file_path)
print("File exists:", os.path.isfile(file_path))
