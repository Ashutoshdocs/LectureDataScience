import sys

print("Python version:", sys.version)
print("Python executable:", sys.executable)
print("Platform:", sys.platform)
print("Command-line arguments:", sys.argv)
print("Module search paths:")
for location in sys.path:
    print(" -", location)

print("Maximum recursion depth:", sys.getrecursionlimit())
