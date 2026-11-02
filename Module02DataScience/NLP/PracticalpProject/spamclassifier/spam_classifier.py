"""
Practical Lab 4: Spam Message Classifier
----------------------------------------
Supervised machine learning for text. The program:
  1. Loads labelled messages (spam / ham = not spam)
  2. Pre-processes them (lower-case, replace links, phone numbers and money
     amounts with special tokens, flag ALL-CAPS and "!!!")
  3. Turns each message into a TF-IDF vector
  4. Trains two classic classifiers and compares them:
       - Multinomial Naive Bayes
       - Logistic Regression
  5. Evaluates them on messages they have never seen (accuracy, precision,
     recall, F1, confusion matrix), then classifies your messages

Usage:
  python spam_classifier.py                       # train, evaluate, run examples
  python spam_classifier.py -t "You won a prize!" # classify one message
  python spam_classifier.py -f messages.txt       # classify a file (one per line)
  python spam_classifier.py -i                    # interactive mode
  python spam_classifier.py --data SMSSpamCollection   # use a different dataset
"""

import argparse
import csv
import os
import re
import sys

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, precision_recall_fscore_support
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

HERE = os.path.dirname(os.path.abspath(__file__))
BUILTIN_DATA = os.path.join(HERE, "spam_data.csv")
# Optional bigger dataset (5,574 real SMS messages). If either file is in the
# folder it is used automatically instead of the built-in one.
BIG_DATA = [os.path.join(HERE, "SMSSpamCollection"),   # UCI original (tab-separated)
            os.path.join(HERE, "spam.csv")]            # Kaggle version (columns v1, v2)

EXAMPLES = [
    "Congratulations! You have won a Rs 50,000 cash prize. Call 9876543210 to claim now!",
    "Hey, are you coming to the lab tomorrow? Need your help with the code.",
    "URGENT: Your account will be suspended. Verify your KYC at secure-update.example",
    "Mom says dinner is ready, come home soon.",
    "FREE recharge for all users!!! Click the link today only",
    "Your OTP is 551203. Do not share it with anyone.",
]

# ===================================================================== data

def load_data(path=None):
    """Return (messages, labels, source_name). Labels: 1 = spam, 0 = ham."""
    if path is None:
        path = next((p for p in BIG_DATA if os.path.exists(p)), BUILTIN_DATA)
    if not os.path.exists(path):
        sys.exit(f"Dataset not found: {path}")

    texts, labels = [], []
    with open(path, encoding="utf-8", errors="replace", newline="") as fh:
        if path.endswith(".csv"):
            reader = csv.DictReader(fh)
            # built-in file: label,message   Kaggle file: v1,v2
            lab, msg = ("v1", "v2") if "v1" in (reader.fieldnames or []) else ("label", "message")
            for row in reader:
                if row.get(lab) and row.get(msg):
                    texts.append(row[msg])
                    labels.append(1 if row[lab].strip().lower() == "spam" else 0)
        else:  # UCI format: "label<TAB>message" per line
            for line in fh:
                if "\t" in line:
                    label, msg = line.rstrip("\n").split("\t", 1)
                    texts.append(msg)
                    labels.append(1 if label.strip().lower() == "spam" else 0)
    return texts, np.array(labels), os.path.basename(path)


# ===================================================================== preprocessing

URL_RE = re.compile(r"(?:https?://|www\.)\S+|\b(?:[\w-]+\.)+(?:com|in|net|org|ly|co|xyz|info|example|io)\b(?:/\S*)?", re.I)
MONEY_RE = re.compile(r"(?:rs\.?|inr|₹|\$|£|usd|€)\s?\d[\d,]*(?:\.\d+)?|\d[\d,]*\s?(?:rupees|lakh|crore|dollars|pounds)\b", re.I)
PHONE_RE = re.compile(r"\+?\d[\d\s-]{8,}\d")
SHORTCODE_RE = re.compile(r"\b\d{4,6}\b")
NUM_RE = re.compile(r"\d+")


TOKEN_NAMES = {"urltoken": "[link]", "moneytoken": "[money]", "phonetoken": "[phone no.]",
               "shortcodetoken": "[short no.]", "numtoken": "[number]",
               "capstoken": "[ALL CAPS]", "exclaimtoken": "[!!!]"}


def pretty(feature):
    """Readable name for a feature, e.g. 'call phonetoken' -> 'call [phone no.]'."""
    return " ".join(TOKEN_NAMES.get(w, w) for w in feature.split())


def preprocess(text):
    """Normalise a message so the model learns patterns, not exact values.

    "Call 9876543210 to claim Rs 5,000 at prize.example!!!"  ->
    "call phonetoken to claim moneytoken at urltoken exclaimtoken"
    """
    extra = []
    if re.search(r"!{2,}", text):
        extra.append("exclaimtoken")
    if sum(1 for w in re.findall(r"\b[A-Z]{3,}\b", text) if w not in {"OTP", "PNR", "HOD", "ATM", "UPI"}) >= 1:
        extra.append("capstoken")
    t = URL_RE.sub(" urltoken ", text)
    t = MONEY_RE.sub(" moneytoken ", t)
    t = PHONE_RE.sub(" phonetoken ", t)
    t = SHORTCODE_RE.sub(" shortcodetoken ", t)
    t = NUM_RE.sub(" numtoken ", t)
    return t.lower() + " " + " ".join(extra)


# ===================================================================== models

MODEL_NAMES = {"nb": "Naive Bayes", "lr": "Logistic Regression"}


def make_vectorizer():
    return TfidfVectorizer(preprocessor=preprocess, ngram_range=(1, 2),
                           sublinear_tf=True, token_pattern=r"(?u)\b[a-z][a-z']+\b")


def make_models():
    return {
        "nb": make_pipeline(make_vectorizer(), MultinomialNB(alpha=0.3)),
        "lr": make_pipeline(make_vectorizer(), LogisticRegression(C=10, max_iter=2000,
                                                                  class_weight="balanced")),
    }


def evaluate(texts, labels, test_size=0.25, seed=42):
    """Train on 75% of the data, test on the unseen 25%, plus 5-fold CV."""
    X_tr, X_te, y_tr, y_te = train_test_split(texts, labels, test_size=test_size,
                                              stratify=labels, random_state=seed)
    folds = StratifiedKFold(n_splits=5, shuffle=True, random_state=seed)
    report = {"train_size": len(X_tr), "test_size": len(X_te),
              "total": len(texts), "spam": int(labels.sum()),
              "ham": int(len(labels) - labels.sum()), "models": {}}
    for key, model in make_models().items():
        model.fit(X_tr, y_tr)
        pred = model.predict(X_te)
        p, r, f, _ = precision_recall_fscore_support(y_te, pred, average="binary", zero_division=0)
        tn, fp, fn, tp = confusion_matrix(y_te, pred, labels=[0, 1]).ravel()
        cv = cross_val_score(make_models()[key], texts, labels, cv=folds, scoring="accuracy")
        mistakes = [{"message": X_te[i], "actual": "spam" if y_te[i] else "ham",
                     "predicted": "spam" if pred[i] else "ham"}
                    for i in range(len(X_te)) if pred[i] != y_te[i]]
        report["models"][key] = {
            "accuracy": round(accuracy_score(y_te, pred), 3),
            "precision": round(p, 3), "recall": round(r, 3), "f1": round(f, 3),
            "cv_accuracy": round(cv.mean(), 3),
            "confusion": {"tn": int(tn), "fp": int(fp), "fn": int(fn), "tp": int(tp)},
            "mistakes": mistakes,
        }
    return report


class SpamClassifier:
    """Both models trained on the full dataset, ready to classify new text."""

    def __init__(self, data_path=None):
        texts, labels, self.source = load_data(data_path)
        self.report = evaluate(texts, labels)
        self.report["source"] = self.source
        self.models = make_models()
        for m in self.models.values():
            m.fit(texts, labels)

    # ------------------------------------------------------------- explain
    def _contributions(self, key, text):
        """How much each word in `text` pushes the model towards spam (+) or ham (-)."""
        vec, clf = self.models[key].named_steps.values()
        x = vec.transform([text])
        names = vec.get_feature_names_out()
        if key == "lr":
            weights = clf.coef_[0]
        else:  # Naive Bayes: log P(word|spam) - log P(word|ham)
            weights = clf.feature_log_prob_[1] - clf.feature_log_prob_[0]
        idx = x.nonzero()[1]
        return {names[i]: float(weights[i] * x[0, i]) for i in idx}

    def classify(self, text):
        out = {"text": text, "models": {}}
        probs = []
        for key, model in self.models.items():
            p = float(model.predict_proba([text])[0][1])
            probs.append(p)
            out["models"][key] = {"label": "spam" if p >= 0.5 else "ham",
                                  "spam_probability": round(p, 3)}
        avg = sum(probs) / len(probs)
        out["spam_probability"] = round(avg, 3)
        out["label"] = "spam" if avg >= 0.5 else "ham"
        out["agree"] = len({m["label"] for m in out["models"].values()}) == 1

        contrib = self._contributions("lr", text)
        ranked = sorted(contrib.items(), key=lambda kv: kv[1], reverse=True)
        out["spam_words"] = [(pretty(w), round(s, 3)) for w, s in ranked if s > 0][:6]
        out["ham_words"] = [(pretty(w), round(s, 3)) for w, s in reversed(ranked) if s < 0][:6]
        out["segments"] = self._segments(text, contrib)
        return out

    def _segments(self, text, contrib):
        """Split the original message into pieces, each with its word score,
        so the web page can colour spammy words red and safe words green."""
        pattern = re.compile(rf"({URL_RE.pattern})|({MONEY_RE.pattern})|({PHONE_RE.pattern})|"
                             r"([A-Za-z][A-Za-z']+)|(\s+|[^\sA-Za-z]+?)", re.I)
        segs = []
        for m in pattern.finditer(text):
            tok = m.group(0)
            if m.group(1):
                key = "urltoken"
            elif m.group(2):
                key = "moneytoken"
            elif m.group(3):
                key = "phonetoken"
            elif m.group(4):
                key = tok.lower()
            else:
                key = None
            score = contrib.get(key) if key else None
            segs.append({"t": tok, "s": round(score, 3) if score else None})
        return segs


# ===================================================================== CLI

def print_report(rep):
    print(f"Dataset : {rep['source']}  ({rep['total']} messages: {rep['spam']} spam, {rep['ham']} ham)")
    print(f"Split   : trained on {rep['train_size']}, tested on {rep['test_size']} unseen messages\n")
    print(f"{'Model':<22}{'Accuracy':>9}{'Precision':>11}{'Recall':>8}{'F1':>7}{'5-fold CV':>11}")
    print("-" * 68)
    for key, m in rep["models"].items():
        print(f"{MODEL_NAMES[key]:<22}{m['accuracy']:>9.3f}{m['precision']:>11.3f}"
              f"{m['recall']:>8.3f}{m['f1']:>7.3f}{m['cv_accuracy']:>11.3f}")
    for key, m in rep["models"].items():
        c = m["confusion"]
        print(f"\n{MODEL_NAMES[key]} confusion matrix (test set):")
        print("                 predicted ham  predicted spam")
        print(f"  actual ham     {c['tn']:>13}  {c['fp']:>14}")
        print(f"  actual spam    {c['fn']:>13}  {c['tp']:>14}")


def print_result(r):
    icon = "🚫 SPAM" if r["label"] == "spam" else "✅ HAM (not spam)"
    print("-" * 68)
    print(f"Message: {r['text']}")
    print(f"  Verdict: {icon}   spam probability = {r['spam_probability']:.0%}")
    for key, m in r["models"].items():
        print(f"    {MODEL_NAMES[key]:<20} -> {m['label']:<4}  ({m['spam_probability']:.0%} spam)")
    if r["spam_words"]:
        print("  Spammy words:", ", ".join(w for w, _ in r["spam_words"]))
    if r["ham_words"]:
        print("  Safe words  :", ", ".join(w for w, _ in r["ham_words"]))
    if not r["agree"]:
        print("  ⚠ The two models disagree on this one.")


def main():
    ap = argparse.ArgumentParser(description="Spam message classifier")
    ap.add_argument("-t", "--text", help="classify a single message")
    ap.add_argument("-f", "--file", help="file with one message per line")
    ap.add_argument("-i", "--interactive", action="store_true")
    ap.add_argument("--data", help="dataset path (.csv with label,message or UCI SMSSpamCollection)")
    args = ap.parse_args()

    print("\n=== Practical Lab 4: Spam Message Classifier ===\n")
    print("Training models...")
    clf = SpamClassifier(args.data)
    print_report(clf.report)
    print()

    if args.interactive:
        print("Type a message and press Enter (q to quit).")
        while True:
            try:
                msg = input("\n> ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                break
            if msg.lower() in {"q", "quit", "exit"}:
                break
            if msg:
                print_result(clf.classify(msg))
        return

    if args.text:
        messages = [args.text]
    elif args.file:
        try:
            with open(args.file, encoding="utf-8") as fh:
                messages = [ln.strip() for ln in fh if ln.strip()]
        except FileNotFoundError:
            sys.exit(f"File not found: {args.file}")
    else:
        messages = EXAMPLES

    for m in messages:
        print_result(clf.classify(m))
    print("-" * 68)


if __name__ == "__main__":
    main()
