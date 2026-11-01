# =============================================================
# LESSON 14 - BINARY FILES AND ENCODING
# Creates: output/secret.bin, output/notes_backup.txt, output/hindi.txt
# =============================================================
# Text mode ("r", "w")   -> you get str (characters)
# Binary mode ("rb","wb") -> you get bytes (numbers 0-255)
# Images, music, PDFs and videos are binary files.

import os

# Changes the working directory to the folder containing this script to avoid path errors.
os.chdir(os.path.dirname(os.path.abspath(__file__)))
# Creates an 'output' directory if it doesn't already exist.
os.makedirs("output", exist_ok=True)


print("===== 1. Read a text file in binary mode =====")
# Opens shopping.txt in "rb" (Read Binary) mode instead of default text mode. No encoding is specified.
with open("shopping.txt", "rb") as f:
    # Reads the first 15 raw bytes from the file rather than characters.
    data = f.read(15)
# Prints the byte string object, which prefixes text representations with a 'b'.
print(data)                    # b'rice 2\nmilk 4\n...'
# Prints the data type class, which evaluates to <class 'bytes'>.
print(type(data))              # <class 'bytes'>
# Accessing an index of a bytes object returns its raw decimal value (ASCII code); 
# chr() converts it back to the character.
print("First byte:", data[0], "= letter", chr(data[0]))


print("\n===== 2. encode() and decode() =====")
# Defines a classic English string text variable.
word = "Pune"
# .encode("utf-8") converts standard Python text (strings) into raw byte array data.
b = word.encode("utf-8")       # str -> bytes
# .decode("utf-8") translates raw numeric byte data streams back into a human-readable Python string.
print(b, "->", b.decode("utf-8"))   # bytes -> str

# Defines a Devnagari text string containing international characters.
hindi = "नमस्ते"
# len() on raw string text returns character count (6), 
# while len() on encoded bytes returns the actual memory storage requirement (18 bytes).
# This shows that non-English characters often require multiple bytes per letter in UTF-8.
print("Hindi letters:", len(hindi), " bytes:", len(hindi.encode("utf-8")))


print("\n===== 3. Write and read bytes =====")
# Opens a file target in "wb" (Write Binary) mode to accept raw byte configurations.
with open("output/secret.bin", "wb") as f:
    # Takes a Python list of integers (0-255) and writes them out directly onto the storage layout.
    f.write(bytes([72, 105, 33]))       # numbers 72,105,33 = H i !

# Reopens the newly populated file in "rb" mode to pull back the stored properties.
with open("output/secret.bin", "rb") as f:
    content = f.read()
# Displays the byte literal format, the numerical integer array list, and the converted decoded string text.
print(content, list(content), content.decode())


print("\n===== 4. Copy ANY file (works for images too) =====")
# Opens a source file and destination file in binary mode to build a reliable, universal copy loop pipeline.
with open("notes.txt", "rb") as src, open("output/notes_backup.txt", "wb") as dst:
    # Loops infinitely until the end of the file is explicitly detected.
    while True:
        # Streams data down in small, memory-efficient packets of 100 bytes at a time.
        chunk = src.read(100)           # read 100 bytes at a time
        # Evaluates to True if the file pointer hits the end (EOF) and returns an empty bytes block b''.
        if not chunk:                   # empty -> end of file
            # Breaks the infinite loop structure immediately.
            break
        # Commits the active chunk block down to the destination file.
        dst.write(chunk)

# Re-reads both absolute files completely to check if their binary byte streams match exactly.
same = open("notes.txt", "rb").read() == open("output/notes_backup.txt", "rb").read()
print("Copy is identical?", same)


print("\n===== 5. Why encoding='utf-8' matters =====")
# Opens hindi.txt in text write mode, forcing text conversions to match the UTF-8 encoding standard map.
with open("output/hindi.txt", "w", encoding="utf-8") as f:
    f.write("नमस्ते Pune\n")

try:
    # Attempts to read a multi-byte character file using a strict 7-bit ASCII layout configuration.
    with open("output/hindi.txt", encoding="ascii") as f:
        f.read()
# Catches the conversion exception thrown when an invalid byte sequence fails decoder matching rules.
except UnicodeDecodeError:
    # Displays a warning notice showing that the encoding parameter choice was mismatched.
    print("Reading with the wrong encoding -> UnicodeDecodeError")

# Re-reads the document passing the correct tracking codec configuration.
with open("output/hindi.txt", encoding="utf-8") as f:
    # Prints the successfully interpreted string characters cleanly.
    print("Correct encoding ->", f.read().strip())
