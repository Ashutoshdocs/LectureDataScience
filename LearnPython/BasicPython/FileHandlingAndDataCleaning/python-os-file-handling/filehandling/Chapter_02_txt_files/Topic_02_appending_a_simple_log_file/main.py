# Define a reusable function; parameters let the caller provide input.
def log(message, level="INFO"):
    # Open/use the resource in a context manager so it is closed automatically.
    with open("app.log", "a", encoding="utf-8") as f:
        # Perform this operation; the expression or method shown determines the exact action.
        f.write(f"[{level:<5}] {message}\n")

# Perform this operation; the expression or method shown determines the exact action.
log("App started")
# Perform this operation; the expression or method shown determines the exact action.
log("User asha logged in")
# Perform this operation; the expression or method shown determines the exact action.
log("Disk almost full", "WARN")
# Perform this operation; the expression or method shown determines the exact action.
log("App stopped")

# Open/use the resource in a context manager so it is closed automatically.
with open("app.log", encoding="utf-8") as f:
    # Assign the calculated or created value to lines for later use.
    lines = [line.rstrip("\n") for line in f]

# Loop through each item so the same operation is applied repeatedly.
for line in lines:
    # Display this value so we can inspect the program's result.
    print(line)

# Assign the calculated or created value to warnings for later use.
warnings = [l for l in lines if l.startswith("[WARN")]
# Display this value so we can inspect the program's result.
print("warnings:", len(warnings))
