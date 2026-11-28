# Assign the calculated or created value to f for later use.
f = open("diary.txt", "r", encoding="utf-8")
# Assign the calculated or created value to text for later use.
text = f.read()
# Perform this operation; the expression or method shown determines the exact action.
f.close()

# Display this value so we can inspect the program's result.
print(text)
# Display this value so we can inspect the program's result.
print("closed?", f.closed)
# Display this value so we can inspect the program's result.
print(type(f).__name__)
