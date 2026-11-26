# Assign the calculated or created value to items for later use.
items = ["apples", "bananas", "cherries"]

# Open/use the resource in a context manager so it is closed automatically.
with open("shopping.txt", "w", encoding="utf-8") as f:
    # Perform this operation; the expression or method shown determines the exact action.
    f.write("Shopping list\n")
    # Perform this operation; the expression or method shown determines the exact action.
    f.write("-------------\n")
    # Perform this operation; the expression or method shown determines the exact action.
    f.writelines(item + "\n" for item in items)
    # Display this value so we can inspect the program's result.
    print("Total items:", len(items), file=f)

# Open/use the resource in a context manager so it is closed automatically.
with open("shopping.txt", encoding="utf-8") as f:
    # Display this value so we can inspect the program's result.
    print(f.read().strip())

# Assign the calculated or created value to count for later use.
count = open("shopping.txt", encoding="utf-8").read().count("\n")
# Display this value so we can inspect the program's result.
print("lines written:", count)
