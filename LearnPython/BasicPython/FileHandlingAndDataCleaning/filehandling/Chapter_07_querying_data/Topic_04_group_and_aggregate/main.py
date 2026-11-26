# Import the module or specific tools needed for this lesson.
import re
# Import the module or specific tools needed for this lesson.
from collections import Counter, defaultdict
# Import the module or specific tools needed for this lesson.
from dataset import load

# Assign the calculated or created value to rows for later use.
rows = load()

# Display this value so we can inspect the program's result.
print("reviews per category:", dict(Counter(r["category"] for r in rows)))

# Assign the calculated or created value to by_product for later use.
by_product = defaultdict(list)
# Loop through each item so the same operation is applied repeatedly.
for r in rows:
    # Perform this operation; the expression or method shown determines the exact action.
    by_product[r["product"]].append(r["rating"])

# Display this value so we can inspect the program's result.
print(f"\n{'product':<14}{'reviews':>8}{'avg':>6}")
# Assign the calculated or created value to summary for later use.
summary = {p: sum(v) / len(v) for p, v in by_product.items()}
# Loop through each item so the same operation is applied repeatedly.
for product, avg in sorted(summary.items(), key=lambda kv: -kv[1]):
    # Display this value so we can inspect the program's result.
    print(f"{product:<14}{len(by_product[product]):>8}{avg:>6.2f}")

# Assign the calculated or created value to city_total for later use.
city_total = defaultdict(float)
# Loop through each item so the same operation is applied repeatedly.
for r in rows:
    # Perform this operation; the expression or method shown determines the exact action.
    city_total[r["city"]] += r["price"]
# Display this value so we can inspect the program's result.
print("\nrevenue by city:", {c: round(t) for c, t in sorted(city_total.items())})

# Assign the calculated or created value to STOP for later use.
STOP = {"the", "and", "is", "a", "was", "of", "for", "after", "but", "from"}
# Perform this operation; the expression or method shown determines the exact action.
negative = [r for r in rows if r["rating"] <= 2]
# Assign the calculated or created value to words for later use.
words = Counter(w for r in negative for w in re.findall(r"[a-z]+", r["review"].lower()) if w not in STOP)
# Display this value so we can inspect the program's result.
print("\ntop words in negative reviews:", words.most_common(4))
