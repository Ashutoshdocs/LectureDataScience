"""
Practical Lab 2: Text Summarization
-----------------------------------
Extractive summarization: pick the most important sentences from the text.
Compares two classic NLP approaches:
  1. Word Frequency  - sentences with many frequent (non-stop) words score high
  2. TextRank        - graph-based; sentences similar to many others score high
                       (the same idea as Google's PageRank, applied to sentences)

Usage:
  python summarizer.py                      # summarise the built-in sample
  python summarizer.py -f article.txt       # summarise a file
  python summarizer.py -f article.txt -n 4  # 4-sentence summary
  python summarizer.py -i                   # paste text interactively
"""

import argparse
import math
import re
import sys
from collections import Counter

import nltk

SAMPLE_TEXT = (
    "Solar energy has become one of the fastest-growing sources of electricity "
    "in the world. The cost of solar panels has fallen by more than eighty percent "
    "over the last decade, making them affordable for homes and businesses. Many "
    "countries now offer subsidies to encourage people to install rooftop solar "
    "systems. However, solar power has one major drawback: it only generates "
    "electricity when the sun is shining. To solve this problem, engineers are "
    "developing better batteries that can store solar energy for use at night. "
    "Battery prices have also dropped sharply, which makes storing solar energy "
    "more practical. Some cities are building large solar farms combined with "
    "battery storage to supply power around the clock. Experts believe that solar "
    "energy, together with storage, could supply a large share of the world's "
    "electricity within a few decades. Critics point out that manufacturing panels "
    "and batteries requires mining, which has its own environmental costs. Even so, "
    "most studies agree that solar energy produces far less pollution over its "
    "lifetime than coal or gas."
)

# Fallback stop-word list, used only if NLTK's list can't be downloaded.
FALLBACK_STOPWORDS = set("""
a about above after again against all am an and any are as at be because been
before being below between both but by can could did do does doing down during
each few for from further had has have having he her here hers herself him
himself his how i if in into is it its itself just me more most my myself no nor
not now of off on once only or other our ours ourselves out over own same she
should so some such than that the their theirs them themselves then there these
they this those through to too under until up very was we were what when where
which while who whom why will with would you your yours yourself yourselves also
one many much may might must us
""".split())

_NLTK_OK = None


def ensure_nltk_data():
    """Download the sentence tokenizer and stop-word list (one time).

    Returns True if NLTK data is available, otherwise False and the script
    falls back to a simple regex splitter and built-in stop words.
    """
    global _NLTK_OK
    if _NLTK_OK is not None:
        return _NLTK_OK
    needed = {"punkt_tab": "tokenizers/punkt_tab", "stopwords": "corpora/stopwords"}
    ok = True
    for pkg, path in needed.items():
        try:
            nltk.data.find(path)
        except LookupError:
            print(f"Downloading NLTK '{pkg}' (one-time)...")
            if not nltk.download(pkg, quiet=True):
                ok = False
    if not ok:
        print(
            "Note: couldn't download NLTK data, using the built-in fallback.\n"
            "      Behind a proxy? Set NLTK_ALLOW_PROXIED_URLOPEN=1 (see README)."
        )
    _NLTK_OK = ok
    return ok


# ---------------------------------------------------------------- preprocessing

def split_sentences(text):
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return []
    if ensure_nltk_data():
        return nltk.sent_tokenize(text)
    return [s for s in re.split(r"(?<=[.!?])\s+(?=[A-Z0-9\"'])", text) if s]


def get_stopwords():
    if ensure_nltk_data():
        from nltk.corpus import stopwords
        return set(stopwords.words("english"))
    return FALLBACK_STOPWORDS


def tokenize(sentence, stop):
    """Lower-case words, with stop words and very short words removed."""
    words = re.findall(r"[a-z][a-z'-]*", sentence.lower())
    return [w for w in words if w not in stop and len(w) > 2]


# ---------------------------------------------------------------- method 1

def frequency_scores(token_lists):
    """Score = sum of normalised word frequencies / number of words."""
    freq = Counter(w for toks in token_lists for w in toks)
    if not freq:
        return [0.0] * len(token_lists)
    top = max(freq.values())
    norm = {w: c / top for w, c in freq.items()}
    return [sum(norm[w] for w in toks) / len(toks) if toks else 0.0
            for toks in token_lists]


# ---------------------------------------------------------------- method 2

def similarity(a, b):
    """TextRank similarity: shared words, normalised by sentence lengths."""
    if len(a) < 2 or len(b) < 2:
        return 0.0
    overlap = len(set(a) & set(b))
    return overlap / (math.log(len(a)) + math.log(len(b)))


def textrank_scores(token_lists, damping=0.85, iterations=50):
    n = len(token_lists)
    if n == 0:
        return []
    # Build the sentence-similarity graph.
    w = [[similarity(token_lists[i], token_lists[j]) if i != j else 0.0
          for j in range(n)] for i in range(n)]
    out_sum = [sum(row) for row in w]
    # Run PageRank by power iteration.
    scores = [1.0 / n] * n
    for _ in range(iterations):
        scores = [
            (1 - damping) / n
            + damping * sum(w[j][i] / out_sum[j] * scores[j]
                            for j in range(n) if out_sum[j])
            for i in range(n)
        ]
    return scores


# ---------------------------------------------------------------- public API

METHODS = {"frequency": frequency_scores, "textrank": textrank_scores}


def keywords(token_lists, k=10):
    freq = Counter(w for toks in token_lists for w in toks)
    return [w for w, _ in freq.most_common(k)]


def summarize(text, n_sentences=3):
    """Return both summaries plus the data needed to explain them."""
    sentences = split_sentences(text)
    stop = get_stopwords()
    tokens = [tokenize(s, stop) for s in sentences]
    n = max(1, min(n_sentences, len(sentences)))

    result = {
        "sentences": sentences,
        "keywords": keywords(tokens),
        "original_words": len(text.split()),
        "methods": {},
    }
    for name, fn in METHODS.items():
        scores = fn(tokens)
        top = sorted(range(len(sentences)), key=lambda i: scores[i], reverse=True)[:n]
        chosen = sorted(top)  # keep the original order so the summary reads well
        summary = " ".join(sentences[i] for i in chosen)
        result["methods"][name] = {
            "scores": scores,
            "chosen": chosen,
            "summary": summary,
            "words": len(summary.split()),
        }
    return result


# ---------------------------------------------------------------- CLI

LABELS = {"frequency": "Word Frequency", "textrank": "TextRank"}


def print_report(r):
    total = len(r["sentences"])
    print(f"Original: {total} sentences, {r['original_words']} words")
    print(f"Keywords: {', '.join(r['keywords'])}\n")
    for name, m in r["methods"].items():
        pct = 100 - round(m["words"] / max(r["original_words"], 1) * 100)
        print("=" * 70)
        print(f"{LABELS[name]} summary  ({m['words']} words, {pct}% shorter)")
        print("-" * 70)
        print(m["summary"])
        print(f"\nPicked sentences: {[i + 1 for i in m['chosen']]}")
    print("=" * 70)
    f, t = (set(r["methods"][k]["chosen"]) for k in ("frequency", "textrank"))
    print(f"Both methods picked: {sorted(i + 1 for i in f & t) or 'none'}")


def main():
    parser = argparse.ArgumentParser(description="Text summarization demo")
    parser.add_argument("-f", "--file", help="text file to summarise")
    parser.add_argument("-n", "--sentences", type=int, default=3,
                        help="number of sentences in the summary (default 3)")
    parser.add_argument("-i", "--interactive", action="store_true",
                        help="paste text, then press Enter on an empty line")
    args = parser.parse_args()

    if args.file:
        try:
            with open(args.file, encoding="utf-8") as fh:
                text = fh.read()
        except FileNotFoundError:
            sys.exit(f"File not found: {args.file}")
    elif args.interactive:
        print("Paste your text, then press Enter on an empty line:")
        lines = []
        while True:
            try:
                line = input()
            except EOFError:
                break
            if not line.strip():
                break
            lines.append(line)
        text = " ".join(lines)
    else:
        text = SAMPLE_TEXT

    if not text.strip():
        sys.exit("No text to summarise.")

    print("\n=== Practical Lab 2: Text Summarization ===\n")
    print_report(summarize(text, args.sentences))


if __name__ == "__main__":
    main()
