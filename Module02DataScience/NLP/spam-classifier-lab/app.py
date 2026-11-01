"""
Practical Lab 4: Spam Message Classifier — Web version
------------------------------------------------------
Trains the models when it starts, then serves a page at
http://127.0.0.1:5000 where you can paste messages and classify them.

Run:
  python app.py
"""

from flask import Flask, jsonify, render_template, request

from spam_classifier import MODEL_NAMES, SpamClassifier

app = Flask(__name__)

print("Training models...")
clf = SpamClassifier()
print(f"Trained on {clf.report['total']} messages from {clf.report['source']}.")

MAX_CHARS = 5000
MAX_LINES = 100


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/model")
def api_model():
    return jsonify({"report": clf.report, "names": MODEL_NAMES})


@app.route("/api/classify", methods=["POST"])
def api_classify():
    data = request.get_json(silent=True) or {}
    text = (data.get("text") or "").strip()
    if not text:
        return jsonify({"error": "Please paste a message."}), 400
    if len(text) > MAX_CHARS:
        return jsonify({"error": f"Text is too long (max {MAX_CHARS:,} characters)."}), 400

    if data.get("batch"):
        lines = [ln.strip() for ln in text.splitlines() if ln.strip()][:MAX_LINES]
        results = [clf.classify(ln) for ln in lines]
    else:
        results = [clf.classify(text)]
    return jsonify({"results": results})


if __name__ == "__main__":
    print("\nOpen http://127.0.0.1:5000 in your browser (Ctrl+C to stop)\n")
    app.run(debug=True, use_reloader=False)
