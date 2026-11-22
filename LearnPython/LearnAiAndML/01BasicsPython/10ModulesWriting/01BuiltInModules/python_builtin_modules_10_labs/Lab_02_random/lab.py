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
