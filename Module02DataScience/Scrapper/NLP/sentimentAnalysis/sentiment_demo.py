"""
Practical Lab 1: Sentiment Analysis
-----------------------------------
Compares two classic NLP sentiment approaches:
  1. VADER (NLTK)  - rule/lexicon-based, tuned for social media text
  2. TextBlob      - lexicon-based polarity + subjectivity

Usage:
  python sentiment_demo.py                 # run built-in examples
  python sentiment_demo.py -i              # interactive mode
  python sentiment_demo.py -t "I love it"  # analyse a single sentence
  python sentiment_demo.py -f reviews.txt  # analyse a file (one text per line)
"""

import argparse
import sys

import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from textblob import TextBlob


SAMPLE_TEXTS = [
    "I absolutely love this phone, the camera is amazing!",
    "The delivery was late and the box was damaged. Very disappointed.",
    "The movie was okay, nothing special.",
    "This is the WORST customer service I have ever experienced!!!",
    "Not bad at all, I'd actually recommend it to friends.",
    "The meeting is scheduled for 3 PM tomorrow.",
]


def ensure_vader():
    """Download the VADER lexicon the first time the script runs."""
    try:
        nltk.data.find("sentiment/vader_lexicon.zip")
    except LookupError:
        print("Downloading VADER lexicon (one-time)...")
        if not nltk.download("vader_lexicon", quiet=True):
            sys.exit(
                "\nCould not download the VADER lexicon.\n"
                "  - Check your internet connection.\n"
                "  - Behind a college/office proxy? Set NLTK_ALLOW_PROXIED_URLOPEN=1\n"
                "    and run again (see README > Troubleshooting)."
            )


def label_from_score(score, pos=0.05, neg=-0.05):
    if score >= pos:
        return "Positive"
    if score <= neg:
        return "Negative"
    return "Neutral"


def analyse(text, vader):
    v = vader.polarity_scores(text)
    blob = TextBlob(text)
    return {
        "text": text,
        "vader_compound": v["compound"],
        "vader_label": label_from_score(v["compound"]),
        "vader_detail": v,
        "tb_polarity": blob.sentiment.polarity,
        "tb_subjectivity": blob.sentiment.subjectivity,
        "tb_label": label_from_score(blob.sentiment.polarity),
    }


EMOJI = {"Positive": "😊", "Negative": "😠", "Neutral": "😐"}


def print_result(r, verbose=False):
    print("-" * 70)
    print(f"Text: {r['text']}")
    print(f"  VADER    -> {r['vader_label']:<8} {EMOJI[r['vader_label']]}  "
          f"compound = {r['vader_compound']:+.3f}")
    if verbose:
        d = r["vader_detail"]
        print(f"              pos={d['pos']:.2f}  neu={d['neu']:.2f}  neg={d['neg']:.2f}")
    print(f"  TextBlob -> {r['tb_label']:<8} {EMOJI[r['tb_label']]}  "
          f"polarity = {r['tb_polarity']:+.3f}, "
          f"subjectivity = {r['tb_subjectivity']:.2f}")
    if r["vader_label"] != r["tb_label"]:
        print("  ⚠ The two models disagree on this one.")


def print_summary(results):
    counts = {"Positive": 0, "Negative": 0, "Neutral": 0}
    for r in results:
        counts[r["vader_label"]] += 1
    total = len(results)
    print("=" * 70)
    print(f"Summary (VADER) over {total} text(s):")
    for label, n in counts.items():
        bar = "█" * n
        print(f"  {label:<8} {n:>3}  {bar}")
    print("=" * 70)


def interactive(vader):
    print("Interactive mode — type a sentence and press Enter (q to quit).")
    while True:
        try:
            text = input("\n> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if text.lower() in {"q", "quit", "exit"}:
            break
        if text:
            print_result(analyse(text, vader), verbose=True)


def main():
    parser = argparse.ArgumentParser(description="Sentiment Analysis demo")
    parser.add_argument("-t", "--text", help="analyse a single sentence")
    parser.add_argument("-f", "--file", help="text file, one entry per line")
    parser.add_argument("-i", "--interactive", action="store_true")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="show VADER pos/neu/neg breakdown")
    args = parser.parse_args()

    ensure_vader()
    vader = SentimentIntensityAnalyzer()

    print("\n=== Practical Lab 1: Sentiment Analysis ===\n")

    if args.interactive:
        interactive(vader)
        return

    if args.text:
        texts = [args.text]
    elif args.file:
        try:
            with open(args.file, encoding="utf-8") as fh:
                texts = [line.strip() for line in fh if line.strip()]
        except FileNotFoundError:
            sys.exit(f"File not found: {args.file}")
    else:
        texts = SAMPLE_TEXTS

    results = [analyse(t, vader) for t in texts]
    for r in results:
        print_result(r, verbose=args.verbose)
    print_summary(results)


if __name__ == "__main__":
    main()
