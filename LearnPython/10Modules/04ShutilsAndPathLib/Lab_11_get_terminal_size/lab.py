import shutil

size = shutil.get_terminal_size()

print("Columns (width):", size.columns)
print("Lines (height):", size.lines)
print("Full result:", size)
