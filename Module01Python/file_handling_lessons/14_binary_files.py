# =============================================================
# LESSON 14 - BINARY FILES AND ENCODING
# Creates: output/secret.bin, output/notes_backup.txt, output/hindi.txt
# =============================================================
# Text mode ("r", "w")   -> you get str (characters)
# Binary mode ("rb","wb") -> you get bytes (numbers 0-255)
# Images, music, PDFs and videos are binary files.

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.makedirs("output", exist_ok=True)


print("===== 1. Read a text file in binary mode =====")
with open("shopping.txt", "rb") as f:
    data = f.read(15)
print(data)                    # b'rice 2\nmilk 4\n...'
print(type(data))              # <class 'bytes'>
print("First byte:", data[0], "= letter", chr(data[0]))


print("\n===== 2. encode() and decode() =====")
word = "Pune"
b = word.encode("utf-8")       # str -> bytes
print(b, "->", b.decode("utf-8"))   # bytes -> str
hindi = "नमस्ते"
print("Hindi letters:", len(hindi), " bytes:", len(hindi.encode("utf-8")))


print("\n===== 3. Write and read bytes =====")
with open("output/secret.bin", "wb") as f:
    f.write(bytes([72, 105, 33]))       # numbers 72,105,33 = H i !
with open("output/secret.bin", "rb") as f:
    content = f.read()
print(content, list(content), content.decode())


print("\n===== 4. Copy ANY file (works for images too) =====")
with open("notes.txt", "rb") as src, open("output/notes_backup.txt", "wb") as dst:
    while True:
        chunk = src.read(100)           # read 100 bytes at a time
        if not chunk:                   # empty -> end of file
            break
        dst.write(chunk)
same = open("notes.txt", "rb").read() == open("output/notes_backup.txt", "rb").read()
print("Copy is identical?", same)


print("\n===== 5. Why encoding='utf-8' matters =====")
with open("output/hindi.txt", "w", encoding="utf-8") as f:
    f.write("नमस्ते Pune\n")
try:
    with open("output/hindi.txt", encoding="ascii") as f:
        f.read()
except UnicodeDecodeError:
    print("Reading with the wrong encoding -> UnicodeDecodeError")
with open("output/hindi.txt", encoding="utf-8") as f:
    print("Correct encoding ->", f.read().strip())
