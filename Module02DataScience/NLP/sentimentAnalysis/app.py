"""
Practical Lab 1: Sentiment Analysis — Web version
-------------------------------------------------
Runs a small Flask server. Open http://127.0.0.1:5000 in your browser,
type some text, and see VADER and TextBlob results side by side.

Run:
  python app.py
"""

import re

from flask import Flask, jsonify, render_template, request
from nltk.sentiment import SentimentIntensityAnalyzer

from sentiment_demo import analyse, ensure_vader

app = Flask(__name__)

ensure_vader()
vader = SentimentIntensityAnalyzer()

MAX_CHARS = 5000


def word_scores(text):
    """Split text into tokens and attach each word's VADER lexicon score.

    Used by the page to colour words: green = positive, red = negative.
    """
    tokens = re.findall(r"[A-Za-z']+|[^A-Za-z'\s]+|\s+", text)
    out = []
    for tok in tokens:
        score = vader.lexicon.get(tok.lower())
        out.append({"t": tok, "s": score})
    return out


def analyse_line(text):
    r = analyse(text, vader)
    return {
        "text": text,
        "vader": {
            "label": r["vader_label"],
            "compound": round(r["vader_compound"], 3),
            "pos": r["vader_detail"]["pos"],
            "neu": r["vader_detail"]["neu"],
            "neg": r["vader_detail"]["neg"],
        },
        "textblob": {
            "label": r["tb_label"],
            "polarity": round(r["tb_polarity"], 3),
            "subjectivity": round(r["tb_subjectivity"], 3),
        },
        "agree": r["vader_label"] == r["tb_label"],
        "words": word_scores(text),
    }


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/analyze", methods=["POST"])
def api_analyze():
    data = request.get_json(silent=True) or {}
    text = (data.get("text") or "").strip()
    if not text:
        return jsonify({"error": "Please enter some text."}), 400
    if len(text) > MAX_CHARS:
        return jsonify({"error": f"Text is too long (max {MAX_CHARS} characters)."}), 400

    # "batch" mode analyses each non-empty line separately.
    if data.get("batch"):
        lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
        results = [analyse_line(ln) for ln in lines]
    else:
        results = [analyse_line(text)]

    summary = {"Positive": 0, "Negative": 0, "Neutral": 0}
    for r in results:
        summary[r["vader"]["label"]] += 1

    return jsonify({"results": results, "summary": summary})


if __name__ == "__main__":
    print("\nOpen http://127.0.0.1:5000 in your browser (Ctrl+C to stop)\n")
    app.run(debug=True)
