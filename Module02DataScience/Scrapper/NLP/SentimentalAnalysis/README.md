# Practical Lab 1: Sentiment Analysis

A small NLP demo that classifies text as **Positive**, **Negative** or **Neutral** using two classic approaches and compares them side by side:

| Model | How it works | Output |
|-------|--------------|--------|
| **VADER** (NLTK) | Lexicon + rules (handles caps, "!!!", negation like "not bad") | `compound` score from -1 to +1 |
| **TextBlob** | Lexicon-based averaging | `polarity` (-1 to +1) and `subjectivity` (0 to 1) |

Labels use the standard thresholds: score ≥ 0.05 → Positive, ≤ -0.05 → Negative, otherwise Neutral.

---

## Project files

```
sentiment-lab/
├── sentiment_demo.py   # the demo script
├── requirements.txt    # Python dependencies
├── reviews.txt         # sample input file
└── README.md
```

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

Put all four files in one folder, then open a terminal there:

```bash
cd path/to/sentiment-lab
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

The script downloads the VADER lexicon automatically on first run. To do it manually:

```bash
python -c "import nltk; nltk.download('vader_lexicon')"
python -m textblob.download_corpora lite
```

### 7. Run the demo

```bash
python sentiment_demo.py
```

---

## Usage

| Command | What it does |
|---------|--------------|
| `python sentiment_demo.py` | Runs the built-in example sentences |
| `python sentiment_demo.py -v` | Same, plus VADER's pos/neu/neg breakdown |
| `python sentiment_demo.py -t "I love this!"` | Analyses one sentence |
| `python sentiment_demo.py -f reviews.txt` | Analyses every line in a file |
| `python sentiment_demo.py -i` | Interactive mode — type sentences, `q` to quit |

### Sample output

```
----------------------------------------------------------------------
Text: I absolutely love this phone, the camera is amazing!
  VADER    -> Positive 😊  compound = +0.862
  TextBlob -> Positive 😊  polarity = +0.625, subjectivity = 0.75
----------------------------------------------------------------------
Text: This is the WORST customer service I have ever experienced!!!
  VADER    -> Negative 😠  compound = -0.772
  TextBlob -> Neutral  😐  polarity = +0.000, subjectivity = 0.95
  ⚠ The two models disagree on this one.
...
======================================================================
Summary (VADER) over 6 text(s):
  Positive   2  ██
  Negative   3  ███
  Neutral    1  █
======================================================================
```

---

## Lab exercises

1. Run the demo and note which sentences the two models **disagree** on. Why does VADER catch "WORST ... !!!" while TextBlob calls it Neutral? (Hint: capitals and punctuation.)
2. Try sarcasm: `-t "Oh great, another Monday."` — what happens, and why do lexicon models struggle?
3. Add 10 of your own product reviews to `reviews.txt` and check the summary.
4. Change the ±0.05 thresholds in `label_from_score()` and see how the Neutral count changes.
5. **Extension:** replace one model with a transformer:
   ```bash
   pip install transformers torch
   ```
   ```python
   from transformers import pipeline
   clf = pipeline("sentiment-analysis")
   print(clf("Not bad at all, I'd actually recommend it."))
   ```

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `ModuleNotFoundError: No module named 'nltk'` | The venv isn't active — repeat step 4, then step 5 |
| `'python' is not recognized` (Windows) | Reinstall Python with **Add to PATH** ticked, or use `py` instead of `python` |
| `LookupError: Resource vader_lexicon not found` | Run the manual download in step 6 |
| `Security Violation ... refusing a proxied fetch` | You're behind a proxy (common on college/office Wi-Fi). Set the variable, then rerun: Windows CMD `set NLTK_ALLOW_PROXIED_URLOPEN=1` · PowerShell `$env:NLTK_ALLOW_PROXIED_URLOPEN=1` · macOS/Linux `export NLTK_ALLOW_PROXIED_URLOPEN=1` |
| Emojis show as `?` on Windows | Use Windows Terminal, or run `chcp 65001` first |

To leave the virtual environment when you're done: `deactivate`
