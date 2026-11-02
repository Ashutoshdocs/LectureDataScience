"""
Practical Lab 3: Basic Question Answering
-----------------------------------------
A retrieval-based QA system, built from classic NLP steps:

  1. Question analysis  - detect the question type (who / when / where /
                          how many / what ...) and extract keywords
  2. Retrieval          - fetch relevant Wikipedia articles from the internet
                          (or use your own text, offline)
  3. Sentence ranking   - TF-IDF + cosine similarity between the question and
                          every sentence
  4. Answer extraction  - pull a short answer (a name, date, place or number)
                          out of the best sentence, based on the question type

Usage:
  python qa.py -q "Who invented the telephone?"           # search Wikipedia
  python qa.py -q "When was it completed?" -c context.txt # use your own text
  python qa.py -i                                         # ask several questions
  python qa.py -i -c context.txt                          # interactive, offline
"""

import argparse
import re
import sys

import requests
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

WIKI_API = "https://en.wikipedia.org/w/api.php"
HEADERS = {"User-Agent": "NLP-QA-Lab/1.0 (educational student project)"}
MAX_ARTICLE_CHARS = 20000

STOP = set(ENGLISH_STOP_WORDS)
QUESTION_WORDS = {"who", "whom", "whose", "what", "when", "where", "which",
                  "why", "how", "many", "much", "long", "old", "tall", "far",
                  "big", "large", "high", "does", "did", "do", "is", "are",
                  "was", "were", "the", "a", "an", "of", "in", "on", "to"}
_stemmer = PorterStemmer()


# =============================================================== 1. question

QTYPES = {
    "PERSON": "a person or organisation",
    "DATE": "a date or year",
    "PLACE": "a place",
    "NUMBER": "a number or quantity",
    "DESCRIPTION": "a description or explanation",
}


def question_type(q):
    ql = q.lower().strip()
    # "Who was Mumtaz Mahal?" asks *about* a named person -> a description
    if re.match(r"\s*(who|what)\s+(is|was|are|were)\s+(?:[A-Z][\w.'-]*\s*)+\??\s*$",
                q.strip()[0].lower() + q.strip()[1:]):
        return "DESCRIPTION"
    if re.match(r"(who|whom|whose)\b", ql) or re.search(r"\b(who|whom|whose)\b", ql[:25]):
        return "PERSON"
    if re.match(r"(when|what year|which year|what date|in what year)\b", ql):
        return "DATE"
    if re.match(r"(where|what country|which country|what city|which city|in which)\b", ql):
        return "PLACE"
    if re.match(r"how (many|much|long|old|tall|far|big|large|high|deep|heavy)\b", ql):
        return "NUMBER"
    return "DESCRIPTION"


def keywords(q):
    """Important words from the question, used as the search query."""
    words = re.findall(r"[A-Za-z0-9][A-Za-z0-9'\-]*", q)
    keep = [w for w in words if w.lower() not in STOP and w.lower() not in QUESTION_WORDS]
    return keep or words


# =============================================================== 2. retrieval

def wiki_search(query, limit=3):
    r = requests.get(WIKI_API, headers=HEADERS, timeout=10, params={
        "action": "query", "list": "search", "srsearch": query,
        "srlimit": limit, "format": "json", "formatversion": 2,
    })
    r.raise_for_status()
    return [hit["title"] for hit in r.json()["query"]["search"]]


def wiki_article(title):
    r = requests.get(WIKI_API, headers=HEADERS, timeout=10, params={
        "action": "query", "prop": "extracts", "explaintext": 1,
        "titles": title, "redirects": 1, "format": "json", "formatversion": 2,
    })
    r.raise_for_status()
    pages = r.json()["query"]["pages"]
    return pages[0].get("extract", "") if pages else ""


def wiki_url(title):
    return "https://en.wikipedia.org/wiki/" + title.replace(" ", "_")


def fetch_documents(question, n_articles=3):
    """Search Wikipedia with the question's keywords; return (query, docs)."""
    query = " ".join(keywords(question))
    titles = wiki_search(query, n_articles)
    if not titles:  # retry with the whole question
        titles = wiki_search(question, n_articles)
    docs = []
    for t in titles:
        text = wiki_article(t)[:MAX_ARTICLE_CHARS]
        if text:
            docs.append({"title": t, "url": wiki_url(t), "text": text})
    return query, docs


# =============================================================== preprocessing

ABBREV = r"(?:Mr|Mrs|Ms|Dr|Prof|Sr|Jr|St|Mt|vs|etc|e\.g|i\.e|c|ca|approx|U\.S|U\.K|No)"


def clean(text):
    text = re.sub(r"^=+.*?=+\s*$", " ", text, flags=re.M)       # == headings ==
    text = re.sub(r"\(\s*[;,]?\s*\)", "", text)                  # empty ( )
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def split_sentences(text):
    text = clean(text)
    # protect abbreviations like "Dr." and "U.S." from being split
    protected = re.sub(rf"\b({ABBREV})\.", lambda m: m.group(1).replace(".", "<D>") + "<D>", text)
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9\"'(])", protected)
    out = [p.replace("<D>", ".").strip() for p in parts]
    return [s for s in out if 4 <= len(s.split()) <= 80]


def stem_tokens(text):
    """Lower-case, drop stop words and possessive 's, then reduce words to
    their stem so that "invented", "inventing" and "inventor" all match."""
    text = re.sub(r"['’]s\b", "", text.lower())
    out = []
    for w in re.findall(r"[a-z0-9]+", text):
        if w in STOP or len(w) < 2:
            continue
        s = _stemmer.stem(w)
        if len(s) > 6 and s.endswith(("or", "er")):  # inventor -> invent
            s = s[:-2]
        out.append(s)
    return out


# =============================================================== 3. ranking

MONTHS = ("January|February|March|April|May|June|July|August|September|"
          "October|November|December")
DATE_RE = re.compile(
    rf"\b(?:\d{{1,2}} (?:{MONTHS}) \d{{3,4}}|(?:{MONTHS}) \d{{1,2}}, \d{{3,4}}|"
    rf"(?:{MONTHS}) \d{{3,4}}|\d{{3,4}}s?(?: (?:BC|BCE|AD|CE))?)\b")
_NUM = r"\d[\d,]*(?:\.\d+)?"
_UNIT = (r"(?:million|billion|trillion|thousand|hundred|percent|per cent|%|km|"
         r"kilometres|kilometers|miles|metres|meters|m|ft|feet|kg|tonnes|tons|"
         r"years|days|hours|people|species)")
NUMBER_RE = re.compile(  # "20,000", "73 metres", "7 and 8 million", "5 to 10 km"
    rf"\b{_NUM}(?:\s?(?:and|to|-|–)\s?{_NUM})?(?:\s?{_UNIT})?(?![\w%])")
NAME_RE = re.compile(
    r"\b(?:[A-Z][a-z]+|[A-Z]\.)(?:\s+(?:[A-Z][a-z]+|[A-Z]\.|de|da|van|von|bin|al|of)){0,4}\b")
LIFESPAN_RE = re.compile(r"\(\s*[^()]*\d{3,4}\s*[–-]\s*[^()]*\d{3,4}\s*\)")
PLACE_RE = re.compile(
    r"\b(?:in|at|from|near|of)\s+((?:the\s+)?[A-Z][a-z]+(?:[\s,]+[A-Z][a-z]+){0,3})")

NOT_NAMES = {"The", "A", "An", "In", "On", "At", "It", "He", "She", "They", "This",
             "That", "These", "Those", "His", "Her", "Their", "However", "After",
             "Before", "During", "When", "While", "Although", "Since", "As", "By",
             "For", "From", "With", "Its", "There", "Some", "Many", "Most", "Today",
             "Also", "Both", "Each", "Other", "Such", "Following", "According"}


def candidates(sentence, qtype, question):
    """Possible short answers of the expected type found in a sentence."""
    qwords = {w.lower() for w in re.findall(r"[A-Za-z]+", question)}
    if qtype == "DATE":
        found = DATE_RE.findall(sentence)
        # "(March 3, 1847 – August 2, 1922)": born = first date, died = last
        if re.search(r"\b(die|died|death|dead)\b", question.lower()):
            found.reverse()
        found.sort(key=lambda d: not re.search(MONTHS, d))  # full dates first
        return found
    if qtype == "NUMBER":
        found = [n.strip() for n in NUMBER_RE.findall(sentence)
                 if not re.fullmatch(r"1[0-9]{3}|20[0-9]{2}", n.strip())]  # skip years
        found.sort(key=lambda n: -bool(re.search(r"[a-z%]", n)))  # prefer numbers with units
        return found
    if qtype == "PLACE":
        found = [p.strip(" ,") for p in PLACE_RE.findall(sentence)]
        return [p for p in found
                if not re.match(MONTHS, p.replace("the ", ""))
                and not {w.lower() for w in p.split()} <= qwords]
    if qtype == "PERSON":
        out = []
        for m in NAME_RE.finditer(sentence):
            words = m.group(0).split()
            while words and words[0] in NOT_NAMES:
                words = words[1:]
            while words and words[-1] in {"of", "de", "da", "van", "von", "bin", "al"}:
                words = words[:-1]
            name = " ".join(words)
            if not name or name.lower() in qwords or re.search(MONTHS, name):
                continue
            if all(w.lower() in qwords for w in words):
                continue
            out.append(name)
        out.sort(key=lambda n: -len(n.split()))  # prefer full names
        return out
    return []


def rank_sentences(question, docs, top_k=5):
    qtype = question_type(question)
    items = []
    for d_i, doc in enumerate(docs):
        for s_i, s in enumerate(split_sentences(doc["text"])):
            items.append({"sentence": s, "doc": d_i, "pos": s_i})
    if not items:
        return qtype, []

    # Dates in brackets after a name, e.g. "(March 3, 1847 – August 2, 1922)",
    # are birth and death dates, so let them match "born" / "died" questions.
    def matching_text(s):
        return s + (" born died" if LIFESPAN_RE.search(s) else "")

    vec = TfidfVectorizer(tokenizer=stem_tokens, token_pattern=None,
                          ngram_range=(1, 2), sublinear_tf=True)
    matrix = vec.fit_transform([question] + [matching_text(it["sentence"]) for it in items])
    sims = cosine_similarity(matrix[0], matrix[1:]).ravel()

    titles = {d["title"].lower() for d in docs}
    q_lower = question.lower()
    for it, sim in zip(items, sims):
        # "Who was X?" -> the opening sentence of X's own article defines X.
        if (qtype == "DESCRIPTION" and it["pos"] == 0 and sim > 0
                and docs[it["doc"]]["title"].lower() in q_lower):
            sim += 0.15
        cands = candidates(it["sentence"], qtype, question)
        # A name with its own article in the search results is a strong answer.
        cands.sort(key=lambda c: c.lower() not in titles)
        type_bonus = 0.12 if (cands and sim > 0) else 0.0
        if cands and cands[0].lower() in titles and sim > 0:
            type_bonus += 0.05
        lead_bonus = 0.04 / (1 + it["pos"] / 3)           # opening sentences matter
        doc_bonus = 0.03 if it["doc"] == 0 else 0.0       # top search result
        it.update(similarity=float(sim), candidates=cands,
                  score=float(sim) + type_bonus + (lead_bonus + doc_bonus) * (sim > 0))
    items.sort(key=lambda it: it["score"], reverse=True)
    return qtype, items[:top_k]


# =============================================================== 4. answer

def answer(question, docs):
    """Run steps 3-4 on already-retrieved documents."""
    qtype, top = rank_sentences(question, docs)
    total = sum(len(split_sentences(d["text"])) for d in docs)
    result = {
        "question": question, "qtype": qtype, "expects": QTYPES[qtype],
        "keywords": keywords(question), "short_answer": None,
        "answer": None, "confidence": "None", "top": [],
        "sentences_searched": total,
        "sources": [{"title": d["title"], "url": d.get("url")} for d in docs],
    }
    if not top or top[0]["similarity"] == 0:
        return result

    best = top[0]
    # For who/when/where/how-many questions, prefer the best sentence that
    # actually contains an answer of that type, as long as it is still
    # reasonably related to the question.
    if qtype != "DESCRIPTION":
        for it in top:
            if it["candidates"] and it["similarity"] >= top[0]["similarity"] * 0.4:
                best = it
                result["short_answer"] = it["candidates"][0]
                break

    s = best["score"]
    result["confidence"] = "High" if s >= 0.4 else "Medium" if s >= 0.22 else "Low"
    result["answer"] = best["sentence"]
    result["answer_source"] = result["sources"][best["doc"]]
    result["top"] = [{
        "sentence": it["sentence"], "score": round(it["score"], 3),
        "similarity": round(it["similarity"], 3),
        "source": result["sources"][it["doc"]],
        "chosen": it is best,
    } for it in top if it["similarity"] > 0]
    return result


def ask(question, context=None):
    """Answer from `context` text if given, otherwise search Wikipedia."""
    if context:
        docs = [{"title": "Your text", "url": None, "text": context}]
        r = answer(question, docs)
        r["mode"] = "context"
        return r
    query, docs = fetch_documents(question)
    r = answer(question, docs)
    r["mode"] = "wikipedia"
    r["search_query"] = query
    return r


# =============================================================== CLI

def print_result(r):
    print(f"\nQuestion : {r['question']}")
    print(f"Type     : {r['qtype']}  (expects {r['expects']})")
    print(f"Keywords : {', '.join(r['keywords'])}")
    if r["mode"] == "wikipedia":
        titles = ", ".join(s["title"] for s in r["sources"]) or "none found"
        print(f"Searched : Wikipedia for '{r['search_query']}' -> {titles}")
    print(f"Checked  : {r['sentences_searched']} sentences")
    print("-" * 70)
    if not r["answer"]:
        print("Sorry, I couldn't find an answer. Try rephrasing the question.")
        return
    if r["short_answer"]:
        print(f"Answer   : {r['short_answer']}")
    print(f"Evidence : {r['answer']}")
    src = r["answer_source"]
    print(f"Source   : {src['title']}" + (f"  ({src['url']})" if src.get("url") else ""))
    print(f"Confidence: {r['confidence']}")
    others = [t for t in r["top"] if not t["chosen"]][:3]
    if others:
        print("\nOther candidate sentences:")
        for t in others:
            print(f"  [{t['score']:.2f}] {t['sentence'][:110]}"
                  + ("…" if len(t["sentence"]) > 110 else ""))


def run(question, context):
    try:
        print_result(ask(question, context))
    except requests.RequestException as e:
        print(f"\nCouldn't reach Wikipedia ({e.__class__.__name__}).\n"
              "Check your internet connection, or answer from your own text with -c file.txt")


def main():
    p = argparse.ArgumentParser(description="Basic Question Answering demo")
    p.add_argument("-q", "--question", help="the question to answer")
    p.add_argument("-c", "--context", help="text file to answer from (offline mode)")
    p.add_argument("-i", "--interactive", action="store_true", help="ask several questions")
    args = p.parse_args()

    context = None
    if args.context:
        try:
            with open(args.context, encoding="utf-8") as fh:
                context = fh.read()
        except FileNotFoundError:
            sys.exit(f"File not found: {args.context}")

    print("\n=== Practical Lab 3: Basic Question Answering ===")
    print("Mode:", "your text (" + args.context + ")" if context else "Wikipedia (internet)")

    if args.interactive or not args.question:
        print("Type a question and press Enter (q to quit).")
        while True:
            try:
                q = input("\n? ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                break
            if q.lower() in {"q", "quit", "exit"}:
                break
            if q:
                run(q, context)
    else:
        run(args.question, context)


if __name__ == "__main__":
    main()
