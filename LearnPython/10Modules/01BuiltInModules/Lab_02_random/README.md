# LAB 2 — Python `random` Module

## Purpose
Generate random values.

## What you will learn
`randint(a, b)` includes both endpoints. `choice()` selects one item, `sample()` selects unique items, and `shuffle()` changes a list in place. Random results vary on each run.

## Code

```python
import random

# Random integer in an inclusive range.
print("Dice roll:", random.randint(1, 6))

# Random decimal between 0.0 and 1.0.
print("Random decimal:", random.random())

colours = ["red", "green", "blue", "yellow"]
print("Random choice:", random.choice(colours))

# Select two unique items.
print("Two sample colours:", random.sample(colours, 2))

# Shuffle a list in place.
cards = [1, 2, 3, 4, 5]
random.shuffle(cards)
print("Shuffled cards:", cards)
```

## Run the lab

From this lab's folder:

```bash
python3 lab.py
```

On Windows, you can use:

```powershell
py lab.py
```

## Expected result
The script prints example values demonstrating the module. Some values are intentionally different on each run or machine (for example, random numbers, current date/time, paths, and platform information).

## Try it yourself
Try changing the dice range or list. For security-sensitive tokens and passwords, use the `secrets` module instead of `random`.

## Key takeaway
This is a Python standard-library module. You can import it directly; no `pip install` is required.
