"""
=====================================================================
   FILE HANDLING IN PYTHON  -  FROM ZERO TO PRO  (a runnable course)
=====================================================================

HOW TO USE THIS FILE
--------------------
1. Save it anywhere, open a terminal in that folder and run:

       python file_handling_masterclass.py        -> interactive menu
       python file_handling_masterclass.py all    -> run every lesson
       python file_handling_masterclass.py 3      -> run only lesson 3

2. It creates a folder called  demo_files/  next to this script and puts
   every practice file there. Nothing else on your computer is touched.
   (Lesson 0 always runs first so the practice files exist.)

3. READ THE CODE while you watch the output. Every lesson is a normal
   function below. The comments are the "textbook", the output is the
   "lab". Change things, break things, run again - that is how you learn.

Needs Python 3.8+ (3.10+ recommended).

COURSE MAP
----------
 0  What is a file? Paths, folders, creating our practice files
 1  Opening and READING files (open, read, readline, readlines, loops, with)
 2  WRITING and APPENDING (modes w, a, x, r+, w+, a+, print to file)
 3  The file CURSOR (tell, seek, truncate, flush)
 4  The file OBJECT itself (attributes and helper methods)
 5  Working with the TEXT you read (string operations, searching, counting)
 6  Encodings and BINARY files (bytes, encode/decode, struct)
 7  Structured formats: CSV, JSON, INI, Pickle
 8  The FILE SYSTEM: pathlib, os, shutil, tempfile
 9  ERRORS and how to handle them properly
10  PRO techniques: big files, generators, context managers, zip/gzip,
    hashing, mmap, StringIO, atomic writes
11  Cheat-sheet of every function and operator used
12  Practice exercises with solutions
"""

import configparser
import csv
import fileinput
import gzip
import hashlib
import io
import json
import mmap
import os
import pickle
import shutil
import struct
import sys
import tempfile
import zipfile
from collections import Counter
from contextlib import contextmanager
from pathlib import Path

# ---------------------------------------------------------------------
# Small printing helpers (not part of the lesson, they just make the
# output easy to read)
# ---------------------------------------------------------------------
BASE = Path(__file__).resolve().parent / "demo_files"
INTERACTIVE = False


def title(number, text):
    print("\n" + "=" * 70)
    print(f"  LESSON {number}: {text}")
    print("=" * 70)


def step(text):
    print(f"\n--- {text} " + "-" * max(0, 64 - len(text)))


def note(text):
    for line in text.strip().splitlines():
        print("   # " + line.strip())


def pause():
    if INTERACTIVE:
        input("\n[Press Enter to continue]")


# =====================================================================
# LESSON 0  -  WHAT IS A FILE?  PATHS.  CREATE PRACTICE FILES
# =====================================================================
def lesson_0():
    title(0, "What is a file? Paths and our practice files")
    note("""
    A FILE is a named chunk of data stored on disk. Python never touches
    the disk directly - it asks the operating system to 'open' the file
    and gives you back a FILE OBJECT you can read from or write to.

    A PATH is the address of a file:
      absolute path -> full address from the root, e.g. C:\\Users\\me\\a.txt
                       or /home/me/a.txt
      relative path -> address starting from the CURRENT WORKING DIRECTORY
                       e.g. 'demo_files/poem.txt'
    """)

    step("Where am I? (current working directory)")
    print("os.getcwd()        ->", os.getcwd())
    print("Path.cwd()         ->", Path.cwd())
    print("This script lives  ->", Path(__file__).resolve().parent)

    step("Building paths safely with the / operator")
    note("""
    Never glue paths with '+' strings: Windows uses '\\', Mac/Linux use '/'.
    pathlib.Path overloads the '/' operator to join paths correctly.
    """)
    p = BASE / "poem.txt"
    print("BASE / 'poem.txt'  ->", p)
    print("os.path.join(...)  ->", os.path.join(str(BASE), "poem.txt"))

    step("Creating the practice folder and files")
    BASE.mkdir(exist_ok=True)          # exist_ok=True: no error if it exists
    create_sample_files()
    for f in sorted(BASE.iterdir()):
        print(f"   created {f.name:<18} {f.stat().st_size:>6} bytes")
    pause()


def create_sample_files():
    """Writes every file used by the later lessons."""
    poem = (
        "The river keeps no record of the rain,\n"
        "yet every drop is somewhere in its flow.\n"
        "A file is like that river, line by line,\n"
        "it holds the words we gave it long ago.\n"
        "\n"
        "Open it gently, read it as you go,\n"
        "and close it when you finish, so you know.\n"
    )
    (BASE / "poem.txt").write_text(poem, encoding="utf-8")

    students = [
        ["name", "age", "city", "score"],
        ["Asha", "21", "Pune", "88"],
        ["Rahul", "22", "Mumbai", "74"],
        ["Meera", "20", "Delhi", "95"],
        ["John", "23", "Pune", "67"],
        ["Fatima", "21", "Chennai", "81"],
    ]
    with open(BASE / "students.csv", "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(students)

    config = {
        "app": "FileMaster",
        "version": 1.2,
        "debug": True,
        "languages": ["en", "hi", "mr"],
        "owner": {"name": "Asha", "email": "asha@example.com"},
    }
    (BASE / "config.json").write_text(json.dumps(config, indent=2), encoding="utf-8")

    (BASE / "settings.ini").write_text(
        "[database]\nhost = localhost\nport = 5432\nuser = admin\n\n"
        "[ui]\ntheme = dark\nfont_size = 14\n",
        encoding="utf-8",
    )

    (BASE / "unicode.txt").write_text(
        "English: Hello\nHindi: नमस्ते\nMarathi: नमस्कार\nEmoji: 🐍📁✨\n",
        encoding="utf-8",
    )

    # A binary file: 4 integers packed as raw bytes + a short byte header
    (BASE / "data.bin").write_bytes(b"PYDM" + struct.pack("<4i", 10, 20, 30, 40))

    # A "big" log file so we can practise reading in chunks
    levels = ["INFO", "INFO", "WARNING", "INFO", "ERROR"]
    with open(BASE / "server.log", "w", encoding="utf-8") as f:
        for i in range(1, 501):
            f.write(f"2026-11-01 10:{i % 60:02d}:00 {levels[i % 5]} request #{i} handled\n")


# =====================================================================
# LESSON 1  -  OPENING AND READING
# =====================================================================
def lesson_1():
    title(1, "Opening and reading files")
    path = BASE / "poem.txt"

    step("1.1  The 3-step way: open -> read -> close")
    note("""
    open(path, mode, encoding)  returns a file object.
    mode 'r' = read text (the default). Always pass encoding='utf-8'
    so your program behaves the same on every computer.
    """)
    f = open(path, "r", encoding="utf-8")
    content = f.read()             # read EVERYTHING into one string
    f.close()                      # give the file back to the OS
    print(content)
    print("type(content) ->", type(content))
    print("f.closed      ->", f.closed)

    step("1.2  The RIGHT way: the 'with' statement")
    note("""
    'with' closes the file automatically - even if an error happens
    inside the block. Use it every time. This is a CONTEXT MANAGER.
    """)
    with open(path, encoding="utf-8") as f:
        print("inside with, closed? ", f.closed)
        first_line = f.readline()
    print("outside with, closed?", f.closed)
    print("first line was:", repr(first_line))
    note("repr() shows hidden characters - notice the '\\n' newline at the end.")

    step("1.3  read(n) - read only n characters")
    with open(path, encoding="utf-8") as f:
        print(repr(f.read(9)))     # first 9 characters
        print(repr(f.read(6)))     # continues where it stopped!
    note("The file remembers its position (the CURSOR). More in lesson 3.")

    step("1.4  readline() - one line at a time")
    with open(path, encoding="utf-8") as f:
        print("1:", repr(f.readline()))
        print("2:", repr(f.readline()))
        f.readline(); f.readline(); f.readline(); f.readline(); f.readline()
        print("at the end readline() returns:", repr(f.readline()), "(empty string)")

    step("1.5  readlines() - all lines into a LIST")
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()
    print("number of lines:", len(lines))
    print("lines[0] ->", repr(lines[0]))
    print("lines[-1]->", repr(lines[-1]))

    step("1.6  Looping over the file object (best for most cases)")
    note("""
    A file object is an ITERATOR: 'for line in f' gives one line per loop
    and keeps only ONE line in memory. Works for files of any size.
    enumerate() adds a line counter; rstrip('\\n') removes the newline.
    """)
    with open(path, encoding="utf-8") as f:
        for number, line in enumerate(f, start=1):
            print(f"{number:>2} | {line.rstrip(chr(10))}")

    step("1.7  read().splitlines() - lines WITHOUT the '\\n'")
    with open(path, encoding="utf-8") as f:
        clean = f.read().splitlines()
    print(clean[:2])

    step("1.8  Shortcut: Path.read_text()")
    print(repr(path.read_text(encoding="utf-8")[:40]) + " ...")

    step("1.9  All open() modes")
    print("""
    mode | meaning                           | file missing? | file exists?
    -----+-----------------------------------+---------------+---------------
    'r'  | read (default)                    | ERROR         | read from start
    'w'  | write                             | creates it    | ERASES it!
    'a'  | append (add to the end)           | creates it    | writes at end
    'x'  | exclusive create                  | creates it    | ERROR
    'r+' | read AND write                    | ERROR         | cursor at start
    'w+' | write AND read                    | creates it    | ERASES it!
    'a+' | append AND read                   | creates it    | writes at end
    add 'b' for binary (e.g. 'rb', 'wb'), 't' for text (the default)
    """)
    pause()


# =====================================================================
# LESSON 2  -  WRITING AND APPENDING
# =====================================================================
def lesson_2():
    title(2, "Writing and appending")
    out = BASE / "notes.txt"

    step("2.1  'w' mode: create or OVERWRITE")
    with open(out, "w", encoding="utf-8") as f:
        n = f.write("Line one\n")          # write() returns chars written
        f.write("Line two\n")
    print("write() returned:", n)
    print(out.read_text(encoding="utf-8"))
    note("write() does NOT add '\\n' for you. You must add it yourself.")

    step("2.2  writelines() - write a list of strings")
    items = ["apple\n", "banana\n", "cherry\n"]
    with open(out, "w", encoding="utf-8") as f:
        f.writelines(items)
    print(out.read_text(encoding="utf-8"))
    note("'w' erased 'Line one/Line two'! Opening in 'w' wipes the file.")

    step("2.3  Writing a list without newlines using join")
    fruits = ["mango", "guava", "papaya"]
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(fruits) + "\n")
    print(out.read_text(encoding="utf-8"))

    step("2.4  'a' mode: APPEND to the end (keeps old content)")
    with open(out, "a", encoding="utf-8") as f:
        f.write("pineapple\n")
    print(out.read_text(encoding="utf-8"))

    step("2.5  print() can write to a file too")
    with open(out, "a", encoding="utf-8") as f:
        print("orange", "lime", sep=", ", file=f)     # adds '\n' automatically
        print("Total fruits:", 6, file=f)
    print(out.read_text(encoding="utf-8"))

    step("2.6  'x' mode: create ONLY if it does not exist")
    try:
        with open(out, "x", encoding="utf-8") as f:
            f.write("never happens")
    except FileExistsError as e:
        print("FileExistsError:", e.strerror, "-> 'x' protected our file")

    step("2.7  'r+' : read and write the same file")
    with open(out, "r+", encoding="utf-8") as f:
        first = f.readline()
        print("read first line:", repr(first))
        f.seek(0)                          # back to start
        f.write("MANGO")                   # overwrites 5 characters
    print(out.read_text(encoding="utf-8").splitlines()[:2])
    note("r+ OVERWRITES characters in place, it does not insert.")

    step("2.8  'w+' : erase, write, then read back")
    with open(out, "w+", encoding="utf-8") as f:
        f.write("fresh start\n")
        f.seek(0)                          # must rewind before reading
        print("read back:", repr(f.read()))

    step("2.9  'a+' : append and read")
    with open(out, "a+", encoding="utf-8") as f:
        f.write("second line\n")
        f.seek(0)
        print("whole file:", repr(f.read()))
    pause()


# =====================================================================
# LESSON 3  -  THE CURSOR: tell, seek, truncate, flush
# =====================================================================
def lesson_3():
    title(3, "The file cursor: tell, seek, truncate, flush")
    note("""
    Think of an open file like a text editor with a blinking cursor.
    Every read or write MOVES the cursor forward.
      tell()           -> where is the cursor? (a number)
      seek(offset, whence) -> move the cursor
            whence 0 = from start (default), 1 = from current, 2 = from end
    In TEXT mode you may only seek to 0, to the end, or to a value tell()
    gave you. In BINARY mode you can seek anywhere.
    """)
    path = BASE / "poem.txt"

    step("3.1  tell() and seek() in text mode")
    with open(path, encoding="utf-8") as f:
        print("start   tell() ->", f.tell())
        f.readline()
        pos = f.tell()
        print("after 1 line   ->", pos)
        print("line 2:", repr(f.readline()))
        f.seek(pos)                         # jump back to saved position
        print("again :", repr(f.readline()))
        f.seek(0)
        print("seek(0) then read(3) ->", repr(f.read(3)))

    step("3.2  seek with whence in BINARY mode")
    with open(path, "rb") as f:
        f.seek(4)                    # 4 bytes from start
        print("seek(4)       ->", f.read(5))
        f.seek(2, 1)                 # 2 bytes forward from current
        print("seek(2, 1)    ->", f.read(4))
        f.seek(-8, 2)                # 8 bytes before the end
        print("seek(-8, 2)   ->", f.read())
        f.seek(0, 2)
        print("file size via seek(0,2)+tell():", f.tell(), "bytes")

    step("3.3  truncate() - cut the file at the cursor (or at a size)")
    t = BASE / "truncate_me.txt"
    t.write_text("0123456789ABCDEF", encoding="utf-8")
    with open(t, "r+", encoding="utf-8") as f:
        f.truncate(10)
    print("after truncate(10):", t.read_text(encoding="utf-8"))

    step("3.4  flush() - push buffered data to disk NOW")
    note("""
    Python collects writes in a BUFFER (memory) and writes to disk in big
    pieces for speed. flush() forces it to disk without closing.
    Useful for log files that another program reads while you write.
    """)
    fl = BASE / "flush_demo.txt"
    f = open(fl, "w", encoding="utf-8")
    f.write("hello")
    print("before flush, size on disk:", fl.stat().st_size)
    f.flush()
    print("after  flush, size on disk:", fl.stat().st_size)
    f.close()
    pause()


# =====================================================================
# LESSON 4  -  THE FILE OBJECT
# =====================================================================
def lesson_4():
    title(4, "The file object: attributes and helper methods")
    with open(BASE / "poem.txt", "r", encoding="utf-8") as f:
        print("f.name       ->", f.name)
        print("f.mode       ->", f.mode)
        print("f.encoding   ->", f.encoding)
        print("f.closed     ->", f.closed)
        print("f.readable() ->", f.readable())
        print("f.writable() ->", f.writable())
        print("f.seekable() ->", f.seekable())
        print("f.isatty()   ->", f.isatty(), "(True only for a terminal)")
        print("f.fileno()   ->", f.fileno(), "(OS file descriptor number)")
        print("type(f)      ->", type(f).__name__)
    with open(BASE / "poem.txt", "rb") as b:
        print("binary type  ->", type(b).__name__)
    note("""
    TextIOWrapper = text file (gives str).  BufferedReader = binary (gives bytes).
    dir(f) lists every method a file object has - try it!
    """)
    methods = [m for m in dir(f) if not m.startswith("_")]
    print("public methods:", ", ".join(methods))
    pause()


# =====================================================================
# LESSON 5  -  WORKING WITH TEXT YOU READ
# =====================================================================
def lesson_5():
    title(5, "Operations on file content")
    text = (BASE / "poem.txt").read_text(encoding="utf-8")
    lines = text.splitlines()

    step("5.1  Counting: lines, words, characters (like the 'wc' tool)")
    words = text.split()                        # split on any whitespace
    print("lines     :", len(lines))
    print("non-empty :", len([l for l in lines if l.strip()]))
    print("words     :", len(words))
    print("characters:", len(text))
    print("letters   :", sum(ch.isalpha() for ch in text))

    step("5.2  The 'in' and 'not in' operators")
    print("'river' in text      ->", "river" in text)
    print("'ocean' not in text  ->", "ocean" not in text)

    step("5.3  Searching: find(), index(), count(), startswith()")
    print("text.find('file')    ->", text.find("file"), "(position, -1 if missing)")
    print("text.count('it')     ->", text.count("it"))
    print("lines starting with 'A':", [l for l in lines if l.startswith("A")])
    print("lines ending with ',':", sum(l.endswith(",") for l in lines))

    step("5.4  grep: print matching lines with line numbers")
    for no, line in enumerate(lines, 1):
        if "it" in line.lower().split():
            print(f"  {no}: {line}")

    step("5.5  Cleaning: strip, lower, upper, title, replace")
    raw = "   Hello File World!  \n"
    print(repr(raw.strip()), "|", raw.strip().lower(), "|", raw.strip().upper())
    print(raw.strip().replace("World", "Python"), "|", "the river".title())

    step("5.6  Word frequency with Counter")
    cleaned = [w.strip(".,!?;:").lower() for w in words]
    freq = Counter(cleaned)
    print(freq.most_common(5))

    step("5.7  Slicing lines: first, last, reverse, every 2nd")
    print("first 2 :", lines[:2])
    print("last 2  :", lines[-2:])
    print("reversed:", lines[::-1][:2])
    print("every 2nd line count:", len(lines[::2]))

    step("5.8  Sorting, unique values, longest line")
    print("sorted words (first 6):", sorted(set(cleaned))[:6])
    print("unique word count     :", len(set(cleaned)))
    print("longest line          :", max(lines, key=len))
    print("all lines < 50 chars? :", all(len(l) < 50 for l in lines))
    print("any blank line?       :", any(l == "" for l in lines))

    step("5.9  Read -> transform -> write a NEW file")
    src, dst = BASE / "poem.txt", BASE / "poem_numbered_upper.txt"
    with open(src, encoding="utf-8") as fin, open(dst, "w", encoding="utf-8") as fout:
        for no, line in enumerate(fin, 1):
            fout.write(f"{no:02d}: {line.upper()}")
    print(dst.read_text(encoding="utf-8").splitlines()[0])

    step("5.10 Operators you used on strings")
    print("'ab' + 'cd'   ->", "ab" + "cd", "  (+ joins)")
    print("'-' * 10      ->", "-" * 10, "  (* repeats)")
    print("'abc'[1]      ->", "abc"[1], "  ([] index)")
    print("'abcdef'[1:4] ->", "abcdef"[1:4], "  ([:] slice)")
    print("'a' == 'a'    ->", "a" == "a", "  (== compare)")
    pause()


# =====================================================================
# LESSON 6  -  ENCODINGS AND BINARY
# =====================================================================
def lesson_6():
    title(6, "Encodings and binary files")
    note("""
    Computers store BYTES (numbers 0-255). Text is bytes + an ENCODING
    rule that maps them to characters. UTF-8 handles every language.
      str.encode('utf-8') -> bytes      bytes.decode('utf-8') -> str
    """)
    path = BASE / "unicode.txt"

    step("6.1  Reading text in many languages")
    print(path.read_text(encoding="utf-8"))

    step("6.2  Characters vs bytes")
    word = "नमस्ते"
    data = word.encode("utf-8")
    print("characters:", len(word), " bytes:", len(data))
    print("bytes     :", data)
    print("decoded   :", data.decode("utf-8"))

    step("6.3  Wrong encoding -> errors, and the 'errors' parameter")
    try:
        path.read_text(encoding="ascii")
    except UnicodeDecodeError as e:
        print("UnicodeDecodeError:", str(e)[:60], "...")
    with open(path, encoding="ascii", errors="replace") as f:
        print("errors='replace':", f.readline().strip(), "|", f.readline().strip())
    with open(path, encoding="ascii", errors="ignore") as f:
        f.readline()
        print("errors='ignore' :", f.readline().strip())

    step("6.4  Binary mode 'rb' gives bytes, not str")
    with open(BASE / "data.bin", "rb") as f:
        raw = f.read()
    print("raw bytes :", raw)
    print("raw[0]    :", raw[0], "<- indexing bytes gives an INT")
    print("raw[:4]   :", raw[:4], "<- slicing gives bytes")
    print("hex       :", raw.hex(" "))

    step("6.5  struct: turn bytes into numbers and back")
    header, numbers = raw[:4], struct.unpack("<4i", raw[4:])
    print("header:", header.decode(), " numbers:", numbers)
    print("pack(5,6) ->", struct.pack("<2i", 5, 6))
    note("'<4i' = little-endian, 4 integers of 4 bytes each.")

    step("6.6  bytearray: a MUTABLE byte sequence")
    ba = bytearray(b"hello")
    ba[0] = ord("J")
    print(ba, "->", ba.decode())

    step("6.7  Copying any file (image, pdf, ...) in binary chunks")
    src, dst = BASE / "data.bin", BASE / "data_copy.bin"
    with open(src, "rb") as fin, open(dst, "wb") as fout:
        while True:
            chunk = fin.read(4)          # tiny chunk just to demonstrate
            if not chunk:                # empty bytes b'' means end of file
                break
            fout.write(chunk)
    print("identical? ", src.read_bytes() == dst.read_bytes())

    step("6.8  The newline parameter")
    nl = BASE / "newlines.txt"
    with open(nl, "w", encoding="utf-8", newline="\r\n") as f:   # Windows style
        f.write("a\nb\n")
    print("bytes on disk:", nl.read_bytes())
    with open(nl, encoding="utf-8") as f:
        print("read normally:", repr(f.read()), "<- Python converts back to \\n")
    pause()


# =====================================================================
# LESSON 7  -  CSV, JSON, INI, PICKLE
# =====================================================================
def lesson_7():
    title(7, "Structured formats: CSV, JSON, INI, Pickle")

    step("7.1  csv.reader - each row is a LIST of strings")
    with open(BASE / "students.csv", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)            # next() takes the first row
        print("header:", header)
        for row in reader:
            print("  ", row)
    note("Always open CSV files with newline='' (the csv module handles it).")

    step("7.2  csv.DictReader - each row is a DICTIONARY")
    with open(BASE / "students.csv", newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    print(rows[0])
    scores = [int(r["score"]) for r in rows]           # strings -> int!
    print("average score:", round(sum(scores) / len(scores), 2))
    print("from Pune    :", [r["name"] for r in rows if r["city"] == "Pune"])
    print("top student  :", max(rows, key=lambda r: int(r["score"]))["name"])

    step("7.3  csv.writer and csv.DictWriter")
    with open(BASE / "results.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["name", "score", "grade"])
        w.writeheader()
        for r in rows:
            s = int(r["score"])
            grade = "A" if s >= 85 else "B" if s >= 70 else "C"
            w.writerow({"name": r["name"], "score": s, "grade": grade})
    print((BASE / "results.csv").read_text(encoding="utf-8"))

    step("7.4  JSON: load (file -> Python) and dump (Python -> file)")
    with open(BASE / "config.json", encoding="utf-8") as f:
        cfg = json.load(f)
    print("type:", type(cfg).__name__, "| app:", cfg["app"], "| owner:", cfg["owner"]["name"])
    print("languages:", cfg["languages"], "| debug:", cfg["debug"])
    cfg["version"] = 2.0
    cfg["languages"].append("ta")
    with open(BASE / "config_new.json", "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)
    print("saved config_new.json with version", cfg["version"])

    step("7.5  json.loads / json.dumps work with STRINGS ('s' = string)")
    s = json.dumps({"a": 1, "b": [1, 2]})
    print("dumps ->", s, type(s).__name__)
    print("loads ->", json.loads(s), type(json.loads(s)).__name__)
    note("JSON -> Python: object->dict, array->list, true->True, null->None")

    step("7.6  INI config files with configparser")
    cp = configparser.ConfigParser()
    cp.read(BASE / "settings.ini", encoding="utf-8")
    print("sections:", cp.sections())
    print("db host :", cp["database"]["host"])
    print("db port :", cp.getint("database", "port"), "(as int)")
    print("theme   :", cp.get("ui", "theme"))

    step("7.7  Pickle: save ANY Python object (binary)")
    obj = {"scores": scores, "tuple": (1, 2), "set": {3, 4}}
    with open(BASE / "data.pkl", "wb") as f:
        pickle.dump(obj, f)
    with open(BASE / "data.pkl", "rb") as f:
        print("loaded:", pickle.load(f))
    note("""
    WARNING: never unpickle files from people you do not trust -
    loading a pickle can run code. Use JSON for sharing data.
    """)
    pause()


# =====================================================================
# LESSON 8  -  THE FILE SYSTEM
# =====================================================================
def lesson_8():
    title(8, "The file system: pathlib, os, shutil, tempfile")
    p = BASE / "students.csv"

    step("8.1  Pieces of a path")
    print("p.name    ->", p.name)
    print("p.stem    ->", p.stem)
    print("p.suffix  ->", p.suffix)
    print("p.parent  ->", p.parent.name)
    print("p.parts[-2:] ->", p.parts[-2:])
    print("with_suffix('.txt') ->", p.with_suffix(".txt").name)

    step("8.2  Checking things")
    print("exists()  ->", p.exists(), "| is_file() ->", p.is_file(), "| is_dir() ->", p.is_dir())
    st = p.stat()
    print("size      ->", st.st_size, "bytes")
    print("os.path.getsize ->", os.path.getsize(p))
    print("os.path.exists('nope.txt') ->", os.path.exists("nope.txt"))

    step("8.3  Listing files: iterdir, glob, rglob, os.listdir")
    print("txt files :", sorted(f.name for f in BASE.glob("*.txt")))
    print("csv files :", sorted(f.name for f in BASE.glob("*.csv")))
    print("os.listdir count:", len(os.listdir(BASE)))

    step("8.4  Making folders, writing, renaming, deleting")
    sub = BASE / "archive" / "2026"
    sub.mkdir(parents=True, exist_ok=True)       # creates both folders
    tmp = sub / "temp.txt"
    tmp.write_text("temporary", encoding="utf-8")
    renamed = tmp.rename(sub / "renamed.txt")
    print("renamed to:", renamed.name, "| exists:", renamed.exists())
    renamed.unlink()                             # delete a file
    print("after unlink exists:", renamed.exists())

    step("8.5  shutil: copy, move, delete whole folders")
    shutil.copy(p, sub / "students_copy.csv")    # copy content
    shutil.copy2(p, sub / "students_meta.csv")   # copy + timestamps
    shutil.move(str(sub / "students_meta.csv"), str(sub / "moved.csv"))
    print("archive/2026 has:", sorted(f.name for f in sub.iterdir()))
    shutil.rmtree(BASE / "archive")              # delete folder + contents
    print("archive removed:", not (BASE / "archive").exists())
    note("rmtree deletes permanently - no recycle bin. Be careful.")

    step("8.6  os.walk - visit every folder and file")
    for folder, dirs, files in os.walk(BASE):
        print(f"  {Path(folder).name}: {len(files)} files, {len(dirs)} sub-folders")

    step("8.7  tempfile - throw-away files that clean themselves up")
    with tempfile.TemporaryDirectory() as tmpdir:
        tp = Path(tmpdir) / "scratch.txt"
        tp.write_text("gone soon", encoding="utf-8")
        print("temp file exists:", tp.exists())
    print("after with, exists:", tp.exists())
    pause()


# =====================================================================
# LESSON 9  -  ERRORS
# =====================================================================
def lesson_9():
    title(9, "Errors and how to handle them")

    step("9.1  FileNotFoundError")
    try:
        open(BASE / "missing.txt", encoding="utf-8")
    except FileNotFoundError as e:
        print("Caught:", type(e).__name__, "->", e.strerror)

    step("9.2  Opening a folder as a file")
    try:
        open(BASE, encoding="utf-8")
    except (IsADirectoryError, PermissionError) as e:   # Windows says Permission
        print("Caught:", type(e).__name__)

    step("9.3  Using a file after it is closed")
    with open(BASE / "poem.txt", encoding="utf-8") as f:
        pass
    try:
        f.read()
    except ValueError as e:
        print("Caught: ValueError ->", e)

    step("9.4  Reading from a write-only file")
    try:
        with open(BASE / "notes.txt", "a", encoding="utf-8") as f:
            f.read()
    except io.UnsupportedOperation as e:
        print("Caught: UnsupportedOperation ->", e)

    step("9.5  The full try / except / else / finally pattern")
    def safe_read(path):
        try:
            f = open(path, encoding="utf-8")
        except FileNotFoundError:
            print(f"  [except]  {Path(path).name} not found")
            return None
        else:                            # runs only if NO error
            with f:
                data = f.read()
            print(f"  [else]    read {len(data)} chars from {Path(path).name}")
            return data
        finally:                         # runs ALWAYS
            print("  [finally] done trying", Path(path).name)

    safe_read(BASE / "poem.txt")
    safe_read(BASE / "ghost.txt")

    step("9.6  Two styles: LBYL vs EAFP")
    note("""
    LBYL - 'Look Before You Leap':  if path.exists(): open(...)
    EAFP - 'Easier to Ask Forgiveness than Permission': try: open(...) except
    Python prefers EAFP: the file could disappear between the check and
    the open, so try/except is safer.
    """)
    pause()


# =====================================================================
# LESSON 10  -  PRO TECHNIQUES
# =====================================================================
@contextmanager
def opened_with_log(path, mode="r"):
    """A home-made context manager using a generator."""
    print(f"  >> opening {Path(path).name}")
    f = open(path, mode, encoding="utf-8")
    try:
        yield f                          # the value given to 'as'
    finally:
        f.close()
        print(f"  << closed  {Path(path).name}")


class LineCounter:
    """A context manager written as a class with __enter__ / __exit__."""

    def __init__(self, path):
        self.path, self.count = path, 0

    def __enter__(self):
        self.file = open(self.path, encoding="utf-8")
        return self

    def lines(self):
        for line in self.file:
            self.count += 1
            yield line

    def __exit__(self, exc_type, exc, tb):
        self.file.close()
        print(f"  LineCounter: read {self.count} lines, closed file")
        return False                     # False = do not hide errors


def read_matching(path, word):
    """A GENERATOR: yields matching lines lazily, one at a time."""
    with open(path, encoding="utf-8") as f:
        for line in f:
            if word in line:
                yield line.rstrip("\n")


def tail(path, n=3, block=256):
    """Last n lines of a huge file without reading the whole thing."""
    with open(path, "rb") as f:
        f.seek(0, 2)
        end = f.tell()
        data = b""
        while end > 0 and data.count(b"\n") <= n:
            step_size = min(block, end)
            end -= step_size
            f.seek(end)
            data = f.read(step_size) + data
        return [l.decode("utf-8") for l in data.splitlines()[-n:]]


def atomic_write(path, text):
    """Write to a temp file then swap it in: never leaves a half file."""
    path = Path(path)
    fd, tmp = tempfile.mkstemp(dir=path.parent, suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(text)
        f.flush()
        os.fsync(f.fileno())             # force to physical disk
    os.replace(tmp, path)                # atomic on all OSes


def lesson_10():
    title(10, "Pro techniques")
    log = BASE / "server.log"

    step("10.1 Reading a big file in chunks with the walrus operator :=")
    total, chunks = 0, 0
    with open(log, "rb") as f:
        while chunk := f.read(4096):     # assign AND test in one line
            total += len(chunk)
            chunks += 1
    print(f"read {total} bytes in {chunks} chunks of 4 KB")

    step("10.2 Generators: process lines lazily")
    errors = read_matching(log, "ERROR")
    print("generator object:", type(errors).__name__)
    print("first 2 errors  :", next(errors), "|", next(errors))
    print("remaining errors:", sum(1 for _ in errors))

    step("10.3 Counting log levels in one pass")
    with open(log, encoding="utf-8") as f:
        levels = Counter(line.split()[2] for line in f)
    print(dict(levels))

    step("10.4 Last lines of a big file (tail)")
    for line in tail(log, 3):
        print("  ", line)

    step("10.5 Custom context managers")
    with opened_with_log(BASE / "poem.txt") as f:
        print("  first line:", f.readline().strip())
    with LineCounter(BASE / "poem.txt") as lc:
        for _ in lc.lines():
            pass

    step("10.6 fileinput: loop over many files as one stream")
    files = [str(BASE / "poem.txt"), str(BASE / "unicode.txt")]
    if sys.version_info >= (3, 10):
        stream = fileinput.input(files=files, encoding="utf-8")
    else:
        stream = fileinput.input(files=files, openhook=fileinput.hook_encoded("utf-8"))
    with stream as fi:
        for line in fi:
            if fi.isfirstline():
                print(f"  start of {Path(fi.filename()).name} (global line {fi.lineno()})")

    step("10.7 In-memory files: io.StringIO and io.BytesIO")
    fake = io.StringIO("name,score\nAsha,88\nRahul,74\n")
    print("csv from a string:", list(csv.reader(fake)))
    buf = io.BytesIO()
    buf.write(b"binary in RAM")
    print("BytesIO value    :", buf.getvalue())
    note("Great for testing code that expects a file, without touching disk.")

    step("10.8 Compressed files: gzip and zipfile")
    gz = BASE / "server.log.gz"
    with open(log, "rb") as fin, gzip.open(gz, "wb") as fout:
        shutil.copyfileobj(fin, fout)
    print(f"log {log.stat().st_size} B -> gz {gz.stat().st_size} B")
    with gzip.open(gz, "rt", encoding="utf-8") as f:
        print("first gz line:", f.readline().strip())

    zp = BASE / "bundle.zip"
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(BASE / "poem.txt", arcname="poem.txt")
        z.write(BASE / "students.csv", arcname="students.csv")
    with zipfile.ZipFile(zp) as z:
        print("zip contains :", z.namelist())
        print("read inside  :", z.read("poem.txt").decode("utf-8").splitlines()[0])

    step("10.9 Hashing a file (checksum) in chunks")
    h = hashlib.sha256()
    with open(log, "rb") as f:
        for block in iter(lambda: f.read(8192), b""):   # iter(callable, stop)
            h.update(block)
    print("sha256:", h.hexdigest()[:32], "...")
    note("Same hash = same content. Used to check downloads weren't corrupted.")

    step("10.10 mmap: treat a file like a big bytes object")
    with open(log, "rb") as f, mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
        pos = mm.find(b"request #250")
        print("found at byte", pos, "->", mm[pos:pos + 25])

    step("10.11 Atomic writes (safe saving)")
    atomic_write(BASE / "important.txt", "Saved safely!\n")
    print((BASE / "important.txt").read_text(encoding="utf-8").strip())
    pause()


# =====================================================================
# LESSON 11  -  CHEAT SHEET
# =====================================================================
def lesson_11():
    title(11, "Cheat-sheet")
    print("""
 OPENING / CLOSING
   open(path, mode='r', encoding='utf-8', newline=None, errors=None)
   with open(...) as f:           auto-closes          f.close()
 READING
   f.read() f.read(n) f.readline() f.readlines()  for line in f:
   Path.read_text()  Path.read_bytes()  str.splitlines()
 WRITING
   f.write(s) f.writelines(list) print(..., file=f)
   Path.write_text(s)  Path.write_bytes(b)
 CURSOR
   f.tell()  f.seek(offset, whence 0|1|2)  f.truncate(size)  f.flush()
 FILE OBJECT
   f.name f.mode f.closed f.encoding f.readable() f.writable()
   f.seekable() f.fileno() f.isatty()
 TEXT
   strip rstrip lower upper title replace split join find count
   startswith endswith isalpha  len enumerate sorted set max min
   any all sum Counter.most_common
 BYTES
   str.encode() bytes.decode() bytes.hex() bytearray struct.pack/unpack
 FORMATS
   csv.reader csv.writer csv.DictReader csv.DictWriter next()
   json.load json.dump json.loads json.dumps
   configparser.ConfigParser  pickle.load pickle.dump
 FILESYSTEM
   Path / .name .stem .suffix .parent .parts .exists() .is_file()
   .is_dir() .stat() .iterdir() .glob() .rglob() .mkdir() .rename()
   .unlink() .with_suffix()  os.getcwd os.listdir os.walk os.path.*
   os.replace os.fsync  shutil.copy copy2 move rmtree copyfileobj
   tempfile.TemporaryDirectory mkstemp
 PRO
   generators (yield) @contextmanager __enter__/__exit__ fileinput
   io.StringIO io.BytesIO gzip.open zipfile.ZipFile hashlib mmap
   iter(callable, sentinel)
 ERRORS
   FileNotFoundError FileExistsError IsADirectoryError PermissionError
   UnicodeDecodeError ValueError(closed file) io.UnsupportedOperation
   try / except / else / finally
 OPERATORS
   /  join paths           +  join strings        *  repeat string
   in / not in  membership []  index             [a:b:c] slice
   :=  walrus (assign+test) ==  !=  <  >  compare  and or not
   x if cond else y   (conditional expression)
   lambda           (tiny inline function, e.g. key=lambda r: r['score'])
""")
    pause()


# =====================================================================
# LESSON 12  -  EXERCISES
# =====================================================================
EXERCISES = [
    ("Count how many lines in server.log contain WARNING.",
     lambda: sum("WARNING" in l for l in open(BASE / "server.log", encoding="utf-8"))),
    ("Return the names of students scoring above 80 from students.csv.",
     lambda: [r["name"] for r in csv.DictReader(open(BASE / "students.csv", newline="", encoding="utf-8"))
              if int(r["score"]) > 80]),
    ("Return the longest word in poem.txt (ignore punctuation).",
     lambda: max((w.strip(".,") for w in (BASE / "poem.txt").read_text(encoding="utf-8").split()), key=len)),
    ("Read config.json and return the owner's email.",
     lambda: json.loads((BASE / "config.json").read_text(encoding="utf-8"))["owner"]["email"]),
    ("Return the total size in bytes of all .txt files in demo_files.",
     lambda: sum(p.stat().st_size for p in BASE.glob("*.txt"))),
    ("Return the 4 integers stored in data.bin after the 4-byte header.",
     lambda: struct.unpack("<4i", (BASE / "data.bin").read_bytes()[4:])),
]


def lesson_12():
    title(12, "Practice exercises")
    note("""
    Try each one YOURSELF first (write a small function), then compare.
    Note: these one-line solutions leave files to be closed by Python.
    In real code, prefer 'with open(...)' as you learnt in lesson 1.
    """)
    for i, (task, solution) in enumerate(EXERCISES, 1):
        print(f"\n Exercise {i}: {task}")
        if INTERACTIVE:
            input("   (think about it, then press Enter to see the answer)")
        print("   Answer:", solution())
    print("""
 BIGGER CHALLENGES (no solutions - you are ready!):
   1. Write a 'mini grep': ask for a word and a filename, print matches.
   2. Convert students.csv to students.json (a list of dicts).
   3. Split server.log into info.log / warning.log / error.log.
   4. Find duplicate files in a folder by comparing sha256 hashes.
   5. Build a to-do app that saves tasks to a JSON file between runs.
""")
    pause()


# =====================================================================
# MENU
# =====================================================================
LESSONS = [lesson_0, lesson_1, lesson_2, lesson_3, lesson_4, lesson_5, lesson_6,
           lesson_7, lesson_8, lesson_9, lesson_10, lesson_11, lesson_12]


def menu():
    global INTERACTIVE
    INTERACTIVE = True
    lesson_0()
    while True:
        print("\n" + "-" * 70)
        for i, fn in enumerate(LESSONS):
            print(f"  {i:>2}. {fn.__name__.replace('_', ' ').title()} - "
                  f"{(fn.__doc__ or '').strip() or TITLES[i]}")
        choice = input("\nPick a lesson number, 'a' for all, 'q' to quit: ").strip().lower()
        if choice == "q":
            break
        if choice == "a":
            for fn in LESSONS[1:]:
                fn()
        elif choice.isdigit() and int(choice) < len(LESSONS):
            LESSONS[int(choice)]()
        else:
            print("Not a valid choice.")


TITLES = ["Paths & practice files", "Reading", "Writing", "Cursor", "File object",
          "Text operations", "Encodings & binary", "CSV/JSON/INI/Pickle",
          "File system", "Errors", "Pro techniques", "Cheat-sheet", "Exercises"]

if __name__ == "__main__":
    arg = sys.argv[1].lower() if len(sys.argv) > 1 else ""
    if arg == "all":
        for fn in LESSONS:
            fn()
    elif arg.isdigit() and int(arg) < len(LESSONS):
        lesson_0()
        if int(arg) != 0:
            LESSONS[int(arg)]()
    elif sys.stdin.isatty():
        menu()
    else:
        for fn in LESSONS:
            fn()
