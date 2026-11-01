PYTHON FILE HANDLING - SMALL LESSONS
====================================

Keep all these files in ONE folder. Run a lesson like this:
    python 01_open_and_read.py

Read the code, run it, compare with the output, then change
something and run again. Lessons save new files in an "output"
folder, so the data files below are never changed.

DATA FILES (20 entries each)
  notes.txt      20 lines of Python facts
  story.txt      20-line short story
  shopping.txt   20 items with quantities ("eggs 12")
  students.csv   20 students with marks
  products.json  20 products with price and stock

LESSONS (do them in order)
  01_open_and_read.py      open(), read(), close(), with
  02_read_methods.py       read(n), readline(), readlines(), for loop
  03_write_files.py        mode "w", write(), writelines()
  04_append_files.py       mode "a", print(file=...)
  05_file_modes.py         all modes: r w a x r+ w+ a+
  06_cursor_seek_tell.py   tell(), seek(), truncate()
  07_text_operations.py    search, count, split, strip, replace
  08_csv_reading.py        csv.reader, csv.DictReader
  09_csv_writing.py        csv.writer, csv.DictWriter
  10_json_reading.py       json.load, json.loads
  11_json_writing.py       json.dump, json.dumps, CSV -> JSON
  12_file_errors.py        try / except / else / finally
  13_files_and_folders.py  os, shutil, pathlib
  14_binary_files.py       "rb"/"wb", bytes, encode/decode
  15_mini_project.py       everything together
