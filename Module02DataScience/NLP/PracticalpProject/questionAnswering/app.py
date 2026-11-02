"""
Practical Lab 3: Basic Question Answering — Web version
-------------------------------------------------------
Runs a small Flask server. Open http://127.0.0.1:5000 in your browser and
ask a question. Answers come from Wikipedia (needs internet) or from text
you paste in (works offline).

Run:
  python app.py
"""

import os

import requests
from flask import Flask, jsonify, render_template, request

from qa import ask

app = Flask(__name__)

HERE = os.path.dirname(os.path.abspath(__file__))
MAX_CONTEXT = 50000

try:
    with open(os.path.join(HERE, "context.txt"), encoding="utf-8") as fh:
        SAMPLE_CONTEXT = fh.read()
except FileNotFoundError:
    SAMPLE_CONTEXT = ""


@app.route("/")
def index():
    return render_template("index.html", sample_context=SAMPLE_CONTEXT)


@app.route("/api/ask", methods=["POST"])
def api_ask():
    data = request.get_json(silent=True) or {}
    question = (data.get("question") or "").strip()
    mode = data.get("mode", "wikipedia")
    context = (data.get("context") or "").strip()

    if not question:
        return jsonify({"error": "Please type a question."}), 400
    if len(question) > 300:
        return jsonify({"error": "Please keep the question under 300 characters."}), 400

    if mode == "context":
        if not context:
            return jsonify({"error": "Paste some text to answer from, or switch to Wikipedia mode."}), 400
        if len(context) > MAX_CONTEXT:
            return jsonify({"error": f"Text is too long (max {MAX_CONTEXT:,} characters)."}), 400
        return jsonify(ask(question, context))

    try:
        return jsonify(ask(question))
    except requests.RequestException:
        return jsonify({"error": "Couldn't reach Wikipedia. Check your internet connection, "
                                 "or switch to “My own text” to work offline."}), 502


if __name__ == "__main__":
    print("\nOpen http://127.0.0.1:5000 in your browser (Ctrl+C to stop)\n")
    app.run(debug=True)
