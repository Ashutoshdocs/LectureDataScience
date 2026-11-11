from collections import Counter, defaultdict, deque

# Counter counts repeated values.
fruits = ["apple", "banana", "apple", "orange", "banana", "apple"]
counts = Counter(fruits)
print("Fruit counts:", counts)
print("Most common:", counts.most_common(2))

# defaultdict creates a default value for a missing key.
marks = defaultdict(list)
marks["Asha"].append(90)
marks["Asha"].append(95)
marks["Ravi"].append(88)
print("Student marks:", dict(marks))

# deque supports efficient additions/removals at both ends.
tasks = deque(["task1", "task2"])
tasks.append("task3")
tasks.appendleft("urgent task")
print("Task queue:", list(tasks))
print("Next task:", tasks.popleft())
