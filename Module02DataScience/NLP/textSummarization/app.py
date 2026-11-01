"""
Practical Lab 2: Text Summarization — Web version
-------------------------------------------------
Runs a small Flask server. Open http://127.0.0.1:5000 in your browser,
paste an article, and compare Word Frequency and TextRank summaries.

Run:
  python app.py
"""

from flask import Flask, jsonify, render_template, request

from summarizer import SAMPLE_TEXT, ensure_nltk_data, summarize

app = Flask(__name__)
ensure_nltk_data()

MAX_CHARS = 30000


@app.route("/")
def index():
    return render_template("index.html", sample=SAMPLE_TEXT)


@app.route("/api/summarize", methods=["POST"])
def api_summarize():
    data = request.get_json(silent=True) or {}
    text = (data.get("text") or "").strip()
    try:
        n = int(data.get("sentences", 3))
    except (TypeError, ValueError):
        n = 3

    if not text:
        return jsonify({"error": "Please paste some text to summarise."}), 400
    if len(text) > MAX_CHARS:
        return jsonify({"error": f"Text is too long (max {MAX_CHARS:,} characters)."}), 400

    r = summarize(text, n)
    if len(r["sentences"]) < 2:
        return jsonify({"error": "Please enter at least two sentences."}), 400

    # Round scores and scale each method to 0–1 so the page can draw bars.
    for m in r["methods"].values():
        top = max(m["scores"]) or 1
        m["relative"] = [round(s / top, 3) for s in m["scores"]]
        m["scores"] = [round(s, 4) for s in m["scores"]]
    return jsonify(r)


if __name__ == "__main__":
    print("\nOpen http://127.0.0.1:5000 in your browser (Ctrl+C to stop)\n")
    app.run(debug=True)
