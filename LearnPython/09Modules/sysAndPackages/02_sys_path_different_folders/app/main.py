# Main application file.
# Add the sibling modules folder to Python's module search path.

import os
import sys

# Get the path of this main.py file.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Build the path to the sibling "modules" folder.
MODULES_DIR = os.path.join(BASE_DIR, "..", "modules")

# Add that folder to Python's import search path.
sys.path.append(os.path.abspath(MODULES_DIR))

import operations
import messages

messages.show_title()
print("Modules folder:", os.path.abspath(MODULES_DIR))
print("Multiplication:", operations.multiply(6, 7))
messages.show_message("Import worked from a different folder!")
