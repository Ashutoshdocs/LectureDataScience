# Import the module or specific tools needed for this lesson.
import csv
# Import the module or specific tools needed for this lesson.
import json
# Import the module or specific tools needed for this lesson.
import re
# Import the module or specific tools needed for this lesson.
from collections import defaultdict

# Assign the calculated or created value to EMOJI for later use.
EMOJI = re.compile("[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F1E6-\U0001F1FF\uFE0F\u200D]+")

# Define a reusable function; parameters let the caller provide input.
def clean_text(text):
    # Assign the calculated or created value to text for later use.
    text = EMOJI.sub("", text)
    # Assign the calculated or created value to text for later use.
    text = re.sub(r"([!?.])\1+", r"\1", text)
    # Send this result back to the caller and finish the function.
    return " ".join(text.split())

# Define a reusable function; parameters let the caller provide input.
def parse_rating(value):
    # Assign the calculated or created value to m for later use.
    m = re.search(r"\d+", value)
    # Assign the calculated or created value to n for later use.
    n = int(m.group()) if m else None
    # Send this result back to the caller and finish the function.
    return n if n is not None and 1 <= n <= 5 else None

# Define a reusable function; parameters let the caller provide input.
def parse_price(value):
    # Assign the calculated or created value to digits for later use.
    digits = re.sub(r"[^\d.]", "", value)
    # Send this result back to the caller and finish the function.
    return float(digits) if digits else None

# Define a reusable function; parameters let the caller provide input.
def load_raw(path):
    # Open/use the resource in a context manager so it is closed automatically.
    with open(path, newline="", encoding="utf-8") as f:
        # Assign the calculated or created value to reader for later use.
        reader = csv.reader(f)
        # Assign the calculated or created value to header for later use.
        header = [h.strip().lower() for h in next(reader)]
        # Send this result back to the caller and finish the function.
        return [dict(zip(header, r)) for r in reader]

# Define a reusable function; parameters let the caller provide input.
def clean(raw):
    # Perform this operation; the expression or method shown determines the exact action.
    rows, seen, rejected = [], set(), 0
    # Loop through each item so the same operation is applied repeatedly.
    for r in raw:
        # Assign the calculated or created value to row for later use.
        row = {
            # Perform this operation; the expression or method shown determines the exact action.
            "product": clean_text(r["product"]).title(),
            # Perform this operation; the expression or method shown determines the exact action.
            "rating": parse_rating(r["rating"]),
            # Perform this operation; the expression or method shown determines the exact action.
            "price": parse_price(r["price"]),
            # Perform this operation; the expression or method shown determines the exact action.
            "review": clean_text(r["review"]),
        # Perform this operation; the expression or method shown determines the exact action.
        }
        # Check this condition; the indented block runs only when it is true.
        if not row["product"] or row["rating"] is None:
            # Perform this operation; the expression or method shown determines the exact action.
            rejected += 1
            # Skip to the next iteration of the loop.
            continue
        # Assign the calculated or created value to key for later use.
        key = (row["product"], row["review"].lower())
        # Check this condition; the indented block runs only when it is true.
        if key in seen:
            # Perform this operation; the expression or method shown determines the exact action.
            rejected += 1
            # Skip to the next iteration of the loop.
            continue
        # Perform this operation; the expression or method shown determines the exact action.
        seen.add(key)
        # Perform this operation; the expression or method shown determines the exact action.
        rows.append(row)
    # Send this result back to the caller and finish the function.
    return rows, rejected

# Define a reusable function; parameters let the caller provide input.
def tag_topics(rows, topics):
    # Assign the calculated or created value to patterns for later use.
    patterns = {t: re.compile(r"\b(" + "|".join(map(re.escape, words)) + r")\b", re.IGNORECASE)
                # Loop through each item so the same operation is applied repeatedly.
                for t, words in topics.items()}
    # Loop through each item so the same operation is applied repeatedly.
    for row in rows:
        # Assign the calculated or created value to row["topics"] for later use.
        row["topics"] = ";".join(t for t, p in patterns.items() if p.search(row["review"]))

# Define a reusable function; parameters let the caller provide input.
def topic_report(rows, topics):
    # Assign the calculated or created value to groups for later use.
    groups = defaultdict(list)
    # Loop through each item so the same operation is applied repeatedly.
    for row in rows:
        # Loop through each item so the same operation is applied repeatedly.
        for t in filter(None, row["topics"].split(";")):
            # Perform this operation; the expression or method shown determines the exact action.
            groups[t].append(row)
    # Assign the calculated or created value to report for later use.
    report = {}
    # Loop through each item so the same operation is applied repeatedly.
    for t in topics:
        # Assign the calculated or created value to hits for later use.
        hits = groups.get(t, [])
        # Assign the calculated or created value to report[t] for later use.
        report[t] = {
            # Perform this operation; the expression or method shown determines the exact action.
            "mentions": len(hits),
            # Perform this operation; the expression or method shown determines the exact action.
            "avg_rating": round(sum(h["rating"] for h in hits) / len(hits), 2) if hits else None,
            # Perform this operation; the expression or method shown determines the exact action.
            "negative": sum(1 for h in hits if h["rating"] <= 2),
        # Perform this operation; the expression or method shown determines the exact action.
        }
    # Send this result back to the caller and finish the function.
    return report

# Define a reusable function; parameters let the caller provide input.
def main():
    # Open/use the resource in a context manager so it is closed automatically.
    with open("keywords.json", encoding="utf-8") as f:
        # Assign the calculated or created value to topics for later use.
        topics = json.load(f)

    # Assign the calculated or created value to raw for later use.
    raw = load_raw("raw_reviews.csv")
    # Perform this operation; the expression or method shown determines the exact action.
    rows, rejected = clean(raw)
    # Perform this operation; the expression or method shown determines the exact action.
    tag_topics(rows, topics)

    # Open/use the resource in a context manager so it is closed automatically.
    with open("clean_reviews.csv", "w", newline="", encoding="utf-8") as f:
        # Assign the calculated or created value to writer for later use.
        writer = csv.DictWriter(f, fieldnames=["product", "rating", "price", "review", "topics"])
        # Perform this operation; the expression or method shown determines the exact action.
        writer.writeheader()
        # Perform this operation; the expression or method shown determines the exact action.
        writer.writerows(rows)

    # Assign the calculated or created value to report for later use.
    report = topic_report(rows, topics)
    # Open/use the resource in a context manager so it is closed automatically.
    with open("topic_report.json", "w", encoding="utf-8") as f:
        # Call the relevant Python function/method to perform this file or data operation.
        json.dump({"raw_rows": len(raw), "clean_rows": len(rows), "rejected": rejected, "topics": report}, f, indent=2)

    # Display this value so we can inspect the program's result.
    print(f"{len(raw)} raw rows -> {len(rows)} clean rows ({rejected} rejected)\n")
    # Display this value so we can inspect the program's result.
    print(f"{'topic':<10}{'mentions':>9}{'avg':>6}{'negative':>10}")
    # Loop through each item so the same operation is applied repeatedly.
    for t, s in sorted(report.items(), key=lambda kv: -kv[1]["mentions"]):
        # Assign the calculated or created value to avg for later use.
        avg = f"{s['avg_rating']:.2f}" if s["avg_rating"] is not None else "-"
        # Display this value so we can inspect the program's result.
        print(f"{t:<10}{s['mentions']:>9}{avg:>6}{s['negative']:>10}")

# Run this block only when this file is executed directly, not when imported.
if __name__ == "__main__":
    # Perform this operation; the expression or method shown determines the exact action.
    main()
