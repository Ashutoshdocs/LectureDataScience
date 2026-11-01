# Practical Lab 3: Basic Question Answering

A question answering (QA) app built from classic NLP steps. Ask a question in plain English and it finds the answer in:

- **Wikipedia** (uses the internet for up-to-date, wide-ranging answers), or
- **your own text** (paste a paragraph or notes; works completely offline)

| Question | What you get |
|----------|--------------|
| Who invented the telephone? | **Alexander Graham Bell** + the sentence it came from + a link to the Wikipedia article |
| How tall is the central dome? *(from your text)* | **73 metres** + "The central dome rises to a height of about 73 metres." |

### How it works (the NLP pipeline)

```
Question ──► 1. Question analysis ──► 2. Retrieval ──► 3. Sentence ranking ──► 4. Answer extraction ──► Answer
             type + keywords           Wikipedia API     TF-IDF + cosine          name / date / place /
                                       or your text      similarity               number from best sentence
```

1. **Question analysis:** detects the question type from its first words and removes stop words to get the keywords.

   | Starts with | Type | Looks for |
   |-------------|------|-----------|
   | Who | PERSON | Capitalised names (e.g. *Shah Jahan*) |
   | When / What year | DATE | Dates and years (e.g. *March 3, 1847*, *1632*) |
   | Where | PLACE | Capitalised words after *in / at / from* (e.g. *Agra*) |
   | How many / How tall / How much… | NUMBER | Numbers with units (e.g. *73 metres*, *7 and 8 million*) |
   | What / Why / How / Who was X | DESCRIPTION | The best sentence (no short answer) |

2. **Retrieval:** searches Wikipedia with the keywords and downloads the top 3 articles as plain text (or uses the text you pasted).
3. **Sentence ranking:** splits the text into sentences, reduces words to their stem (*invented → invent*) with the Porter stemmer, turns every sentence into a **TF-IDF** vector and measures its **cosine similarity** to the question. Small bonuses are added for sentences that contain the expected answer type or appear early in an article.
4. **Answer extraction:** uses regular expressions to pull the short answer of the expected type out of the best sentence.

---

## Project files

```
question-answering-lab/
├── app.py              # web app (Flask) — ask questions in the browser
├── templates/
│   └── index.html      # the web page
├── qa.py               # command-line version + the QA engine
├── requirements.txt    # Python dependencies
├── context.txt         # sample text about the Taj Mahal (offline mode)
└── README.md
```

> **Important:** `index.html` must stay inside a folder named `templates`, next to `app.py`. Flask looks for it there.

---

## Python setup — step by step

### 1. Install Python (3.9 or newer)

- **Windows:** download from <https://www.python.org/downloads/>. During install, tick **"Add Python to PATH"**.
- **macOS:** `brew install python` (or use the python.org installer).
- **Linux (Ubuntu/Debian):** `sudo apt update && sudo apt install python3 python3-venv python3-pip`

Check it worked:

```bash
python --version      # Windows
python3 --version     # macOS / Linux
```

### 2. Create a project folder

Put all the files in one folder (with `index.html` inside a `templates` subfolder), then open a terminal there:

```bash
cd path/to/question-answering-lab
```

### 3. Create a virtual environment

A virtual environment keeps this project's packages separate from the rest of your system.

```bash
# Windows
python -m venv venv

# macOS / Linux
python3 -m venv venv
```

### 4. Activate the virtual environment

```bash
# Windows (Command Prompt)
venv\Scripts\activate

# Windows (PowerShell)
venv\Scripts\Activate.ps1

# macOS / Linux
source venv/bin/activate
```

You should now see `(venv)` at the start of your prompt.

> **PowerShell error "running scripts is disabled"?** Run
> `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once, then activate again.

### 5. Install the dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This installs Flask (web server), Requests (talks to Wikipedia), scikit-learn (TF-IDF) and NLTK (Porter stemmer). Unlike Labs 1 and 2, **no extra NLTK data download is needed**.

### 6. Run the web app (browser)

```bash
python app.py
```

You'll see `Running on http://127.0.0.1:5000`. Open **http://127.0.0.1:5000** in your browser.

- **🌐 Search Wikipedia:** type a question and click **Ask** (or press Enter). Needs internet.
- **📄 My own text:** the Taj Mahal sample loads automatically. Replace it with any text you like (your notes, a textbook paragraph, an article) and ask questions about it. Works offline.
- Click an example under the box to try a ready-made question.
- The page shows:
  - **The answer** in large text, with the source sentence below it (answer highlighted yellow, question keywords underlined) and a confidence label
  - **How it found the answer:** question type, keywords, articles searched and number of sentences checked
  - **Top candidate sentences** with their scores, and which one was used
  - **Recent questions** you can click to ask again

Press **Ctrl + C** in the terminal to stop the server.

> **Running Lab 1 or Lab 2 at the same time?** They all use port 5000. Stop the other one first, or see Troubleshooting to change the port.

### 7. Or run the command-line version

```bash
python qa.py
```

---

## Command-line usage

| Command | What it does |
|---------|--------------|
| `python qa.py -q "Who invented the telephone?"` | Answers one question from Wikipedia |
| `python qa.py -q "How tall is the central dome?" -c context.txt` | Answers from your own text file (offline) |
| `python qa.py` or `python qa.py -i` | Interactive: ask several Wikipedia questions, `q` to quit |
| `python qa.py -i -c context.txt` | Interactive, from your own text |

### Sample output (offline mode)

```
=== Practical Lab 3: Basic Question Answering ===
Mode: your text (context.txt)

Question : How tall is the central dome?
Type     : NUMBER  (expects a number or quantity)
Keywords : central, dome
Checked  : 13 sentences
----------------------------------------------------------------------
Answer   : 73 metres
Evidence : The central dome rises to a height of about 73 metres.
Source   : Your text
Confidence: High
```

In Wikipedia mode you'll also see a `Searched :` line showing the search keywords and the article titles used, plus the article link under `Source`. Wikipedia articles change over time, so your exact answers and scores may differ slightly from a classmate's.

### Questions to try with `context.txt`

| Question | Expected answer |
|----------|-----------------|
| Who commissioned the Taj Mahal? | Shah Jahan |
| When was the Taj Mahal commissioned? | 1632 |
| Where is the Taj Mahal located? | Agra |
| Who was the chief architect? | Ustad Ahmad Lahauri |
| How many artisans worked on it? | 20,000 |
| How many visitors does it get? | 7 and 8 million |
| When did it become a World Heritage Site? | 1983 |
| When did Mumtaz Mahal die? | 1631 |
| Why do the minarets lean outwards? | *(full sentence: so they would fall away from the tomb in an earthquake)* |

---

## Lab exercises

1. Ask the questions in the table above. Then ask **"Where did the marble come from?"** The text says *"The white marble was brought from Makrana"*, but the app answers *Agra*. Why? (Hint: does "come" share a stem with "brought"? What does TF-IDF know about synonyms?)
2. Ask the same fact in two ways, e.g. *"Who built the Taj Mahal?"* and *"Who commissioned the Taj Mahal?"* Do you get the same answer? What does this tell you about keyword matching?
3. Paste a paragraph from one of your textbooks into **My own text** and write five questions about it. How many does the app answer correctly? For the wrong ones, look at the candidate sentences: was the right sentence found but the wrong short answer extracted, or was the right sentence not found at all?
4. In Wikipedia mode, try a question about something very recent (e.g. this year's events). Then try one about a famous historical fact. Which works better and why?
5. In `qa.py`, find `type_bonus = 0.12` and change it to `0` (no bonus for containing the expected answer type). Which questions get worse?
6. **Extension:** use a **transformer** model that finds the exact answer span instead of using rules:
   ```bash
   pip install transformers torch
   ```
   ```python
   from transformers import pipeline
   reader = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")
   context = open("context.txt", encoding="utf-8").read()
   print(reader(question="Where did the marble come from?", context=context))
   ```
   The model downloads about 260 MB the first time. Does it get exercise 1 right? This "retrieve, then read" design (search for text, then run a reader model) is how many modern QA systems work.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `ModuleNotFoundError: No module named 'flask'` (or `requests`, `sklearn`, `nltk`) | The venv isn't active — repeat step 4, then step 5 |
| `'python' is not recognized` (Windows) | Reinstall Python with **Add to PATH** ticked, or use `py` instead of `python` |
| "Couldn't reach Wikipedia" | Check your internet connection. Some college or office networks block Wikipedia's API — use **My own text** mode instead, or try a mobile hotspot |
| "No answer found" | Rephrase with different keywords, e.g. include the full name of the person or place |
| Answer is wrong but the right sentence is in the candidate list | Expected — the rules for extracting names, dates and places are simple. See exercise 3 |
| `TemplateNotFound: index.html` | `index.html` isn't inside a `templates` folder next to `app.py` |
| Browser says "can't reach this page" | `python app.py` isn't running, or you closed that terminal — start it again |
| `Address already in use` / port 5000 busy | Another program (or Lab 1/2) is using port 5000. On macOS this is often AirPlay Receiver. Change the last line of `app.py` to `app.run(debug=True, port=8000)` and open http://127.0.0.1:8000 |

To leave the virtual environment when you're done: `deactivate`
