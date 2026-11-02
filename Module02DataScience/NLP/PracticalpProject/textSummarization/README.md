# Practical Lab 2: Text Summarization

A small NLP demo that shortens a long piece of text into its most important sentences, using two classic **extractive** methods side by side:

| Method | How it works | Good at |
|--------|--------------|---------|
| **Word Frequency** | Removes stop words ("the", "is", "and"…), counts how often each remaining word appears, and scores each sentence by how many frequent words it contains | Simple, fast, easy to explain |
| **TextRank** | Builds a graph where every sentence is a node, links sentences that share words, then ranks them with the PageRank algorithm (the one Google used to rank web pages) | Finding sentences that are "central" to the whole text |

**Extractive** means the summary is made of sentences copied from the original, kept in their original order. (**Abstractive** summarizers write brand-new sentences — see exercise 6.)

### NLP steps used

1. **Sentence tokenization:** split the text into sentences (NLTK `punkt`)
2. **Word tokenization:** split sentences into lower-case words
3. **Stop-word removal:** drop common words that carry little meaning (NLTK `stopwords`)
4. **Scoring:** rank each sentence with Word Frequency or TextRank
5. **Selection:** keep the top N sentences in their original order

---

## Project files

```
textSummarization/
├── app.py              # web app (Flask) — paste text in the browser
├── templates/
│   └── index.html      # the web page
├── summarizer.py       # command-line version + shared NLP code
├── requirements.txt    # Python dependencies
├── article.txt         # sample article to summarise
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
cd path/to/textSummarization
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

### 6. Download the NLP data (one time)

The scripts download this automatically on first run. To do it manually:

```bash
python -c "import nltk; nltk.download('punkt_tab'); nltk.download('stopwords')"
```

If the download fails, the program still works: it falls back to a built-in sentence splitter and stop-word list and prints a short note.

### 7. Run the web app (browser)

```bash
python app.py
```

You'll see `Running on http://127.0.0.1:5000`. Open **http://127.0.0.1:5000** in your browser.

- Paste an article and click **Summarize** (or press **Ctrl + Enter**).
- Use the **Summary length** slider to choose 1–10 sentences. The result updates when you let go.
- Click a sample (Solar energy, Sleep and students, History of the internet) to try a ready-made text.
- The page shows:
  - **Stats and top keywords** for the text
  - **Both summaries** side by side, with word count, % shorter and a **Copy** button
  - **The original text** with picked sentences highlighted (blue = Word Frequency, purple = TextRank, yellow = both)
  - **A score table** showing how each method rated every sentence

Press **Ctrl + C** in the terminal to stop the server.

> **Running Lab 1 at the same time?** Both apps use port 5000. Stop one first, or see Troubleshooting to change the port.

### 8. Or run the command-line version

```bash
python summarizer.py
```

---

## Command-line usage

| Command | What it does |
|---------|--------------|
| `python summarizer.py` | Summarises the built-in sample text |
| `python summarizer.py -f article.txt` | Summarises a text file |
| `python summarizer.py -f article.txt -n 5` | 5-sentence summary (default is 3) |
| `python summarizer.py -i` | Paste text, then press Enter on an empty line |

### Sample output

```
=== Practical Lab 2: Text Summarization ===

Original: 14 sentences, 210 words
Keywords: plastic, microplastics, millions, single-use, items, bags, food, packaging, water, small

======================================================================
Word Frequency summary  (50 words, 76% shorter)
----------------------------------------------------------------------
Much of this plastic comes from single-use items such as bags, bottles and food packaging. Once in the ocean, plastic breaks down into tiny pieces called microplastics. Only a small fraction of all plastic ever made has been recycled, because many types of plastic are difficult or expensive to process.

Picked sentences: [3, 4, 12]
======================================================================
TextRank summary  (43 words, 80% shorter)
----------------------------------------------------------------------
Much of this plastic comes from single-use items such as bags, bottles and food packaging. Once in the ocean, plastic breaks down into tiny pieces called microplastics. Some cities charge customers a small fee for plastic bags, which has sharply reduced their use.

Picked sentences: [3, 4, 9]
======================================================================
Both methods picked: [3, 4]
```

---

## How the two methods score sentences

**Word Frequency**

```
word weight   = count(word) / count(most frequent word)
sentence score = sum of word weights / number of words in the sentence
```

**TextRank**

```
similarity(A, B) = shared words / (log(len A) + log(len B))
score(S) = (1 − d)/N + d × Σ [ similarity(T, S) / Σ similarity(T, ·) ] × score(T)
```

where `d = 0.85` (the damping factor) and the sum runs over every other sentence `T`. The scores are updated 50 times until they settle.

---

## Lab exercises

1. Summarise `article.txt` with `-n 3`. Which sentences do both methods agree on, and which differ? Read the ones that differ: which summary is better?
2. Look at the first sentence of the article ("Plastic pollution has become one of the most serious environmental problems…"). Neither method picks it, yet a human probably would. Why? (Hint: does it share many words with the rest of the text?)
3. Change the summary length from 1 to 10 sentences in the web app. At what length does the summary stop being useful?
4. Paste in a news article of your own. Do the summaries make sense when read on their own, or do they have dangling words like "This" or "However" pointing to sentences that were left out?
5. In `summarizer.py`, change `frequency_scores()` to use the **sum** of word weights instead of dividing by sentence length. What kind of sentences get picked now?
6. **Extension:** try an **abstractive** summarizer that writes new sentences:
   ```bash
   pip install transformers torch
   ```
   ```python
   from transformers import pipeline
   summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
   text = open("article.txt", encoding="utf-8").read()
   print(summarizer(text, max_length=60, min_length=25)[0]["summary_text"])
   ```
   The model downloads about 1.2 GB the first time. Compare its output with the extractive summaries.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `ModuleNotFoundError: No module named 'nltk'` or `'flask'` | The venv isn't active — repeat step 4, then step 5 |
| `'python' is not recognized` (Windows) | Reinstall Python with **Add to PATH** ticked, or use `py` instead of `python` |
| "Note: couldn't download NLTK data, using the built-in fallback" | The program still works. To get the full NLTK data, check your internet connection and run step 6 |
| `Security Violation ... refusing a proxied fetch` | You're behind a proxy (common on college/office Wi-Fi). Set the variable, then rerun: Windows CMD `set NLTK_ALLOW_PROXIED_URLOPEN=1` · PowerShell `$env:NLTK_ALLOW_PROXIED_URLOPEN=1` · macOS/Linux `export NLTK_ALLOW_PROXIED_URLOPEN=1` |
| `TemplateNotFound: index.html` | `index.html` isn't inside a `templates` folder next to `app.py` |
| Browser says "can't reach this page" | `python app.py` isn't running, or you closed that terminal — start it again |
| `Address already in use` / port 5000 busy | Another program (or Lab 1) is using port 5000. On macOS this is often AirPlay Receiver. Change the last line of `app.py` to `app.run(debug=True, port=8000)` and open http://127.0.0.1:8000 |
| "Please enter at least two sentences" | Summarization needs at least two sentences ending in `.`, `!` or `?` |

To leave the virtual environment when you're done: `deactivate`
