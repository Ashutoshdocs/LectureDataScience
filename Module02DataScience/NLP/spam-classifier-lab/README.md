# Practical Lab 4: Spam Message Classifier

A machine-learning demo that decides whether a message is **spam** or **ham** (not spam). Unlike Labs 1–3, which use hand-written rules and word lists, this lab **learns from labelled examples**: you show it messages already marked spam or ham, and it works out the patterns by itself.

Two classic text classifiers are trained and compared side by side:

| Model | How it decides | Strength |
|-------|----------------|----------|
| **Multinomial Naive Bayes** | Uses probability: how often each word appears in spam vs ham during training (Bayes' theorem, assuming words are independent) | Very fast, works well with little data, the traditional choice for spam filters |
| **Logistic Regression** | Learns a weight for every word (positive = spammy, negative = safe), adds them up and turns the total into a probability | Weights are easy to inspect, often slightly more accurate on larger datasets |

### The machine-learning pipeline

```
Labelled messages ──► 1. Pre-processing ──► 2. TF-IDF features ──► 3. Train models ──► 4. Evaluate ──► 5. Classify new messages
(spam / ham)          links → [link]          words + word pairs      Naive Bayes          on unseen      with spam probability
                      numbers → [phone no.]   weighted by importance  Logistic Regression  test data      and the words that
                      "!!!", ALL CAPS flags                                                               decided it
```

1. **Pre-processing:** lower-cases text and replaces things that vary but mean the same: links → `[link]`, phone numbers → `[phone no.]`, money amounts like "Rs 5,000" → `[money]`, short codes like 87121 → `[short no.]`. It also adds a flag for `!!!` and for ALL-CAPS words. This way the model learns "spam often contains a phone number" rather than memorising one specific number.
2. **Feature extraction:** turns each message into a **TF-IDF** vector of single words and word pairs (bigrams, e.g. "claim now").
3. **Training:** fits both models on the labelled messages.
4. **Evaluation:** 75% of the messages are used for training and 25% are kept hidden for testing. Reports **accuracy**, **precision**, **recall**, **F1**, a **confusion matrix**, and **5-fold cross-validation** accuracy.
5. **Classification:** predicts new messages and shows which words pushed the decision towards spam or ham.

---

## Project files

```
spamclassifier/
├── app.py               # web app (Flask) — classify messages in the browser
├── templates/
│   └── index.html       # the web page
├── spam_classifier.py   # command-line version + the ML code
├── spam_data.csv        # built-in training data: 199 labelled messages
├── messages.txt         # sample messages to classify
├── requirements.txt     # Python dependencies
└── README.md
```

> **Important:** `index.html` must stay inside a folder named `templates`, next to `app.py`. Flask looks for it there.

### About the training data

`spam_data.csv` contains **199 messages (81 spam, 118 ham)** written for this lab, including Indian-style messages (KYC and UPI scams, loan offers, Hinglish chats, OTP and delivery messages). Each row is `label,message`. You can open it in Excel or a text editor and add your own rows.

For more realistic results, you can also train on the **SMS Spam Collection** (5,574 real SMS messages) — see step 6.

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
cd path/to/spamclassifier
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

This installs Flask (web server), scikit-learn (TF-IDF and the two models) and NumPy. **No internet is needed after this step**, and no extra data downloads are required.

### 6. (Optional) Use the bigger SMS Spam Collection dataset

The built-in 199 messages are enough to see how everything works. For a more realistic model:

1. Download the **SMS Spam Collection** dataset, either:
   - from the **UCI Machine Learning Repository** (search "UCI SMS Spam Collection") — unzip it and take the file named `SMSSpamCollection`, or
   - from **Kaggle** (search "SMS Spam Collection Dataset") — the file is named `spam.csv`.
2. Put that file in the project folder, next to `app.py`. Don't rename it.

Both programs use it automatically when it's there (the output says which dataset was used). Delete or move it to go back to the built-in data. Training on 5,574 messages takes a few extra seconds when the program starts.

### 7. Run the web app (browser)

```bash
python app.py
```

The models train in a few seconds, then you'll see `Running on http://127.0.0.1:5000`. Open **http://127.0.0.1:5000** in your browser.

- Paste a message and click **Classify** (or press **Ctrl + Enter**).
- Click an example to try it. Red dot = spam example, green = not spam, orange = a tricky one.
- **One per line:** classify many messages at once and see a summary table. Click a row to see why.
- The result shows:
  - **The verdict** (Spam / Not spam) with a spam-probability meter
  - **The message with coloured words:** red words push towards spam, green words towards not spam (darker = stronger)
  - **Each model's own verdict** and probability
  - **The spammy and safe features** that mattered most
- Open **Model performance** at the bottom to see accuracy, precision, recall, F1, the confusion matrices and the test messages each model got wrong.

Press **Ctrl + C** in the terminal to stop the server.

> **Running another lab at the same time?** They all use port 5000. Stop the other one first, or see Troubleshooting to change the port.

### 8. Or run the command-line version

```bash
python spam_classifier.py
```

---

## Command-line usage

| Command | What it does |
|---------|--------------|
| `python spam_classifier.py` | Trains, prints the evaluation, classifies 6 example messages |
| `python spam_classifier.py -t "You won a prize!"` | Classifies one message |
| `python spam_classifier.py -f messages.txt` | Classifies every line in a file |
| `python spam_classifier.py -i` | Interactive: type messages one at a time, `q` to quit |
| `python spam_classifier.py --data my_data.csv` | Trains on a different dataset (`label,message` CSV or UCI format) |

### Sample output

```
=== Practical Lab 4: Spam Message Classifier ===

Training models...
Dataset : spam_data.csv  (199 messages: 81 spam, 118 ham)
Split   : trained on 149, tested on 50 unseen messages

Model                  Accuracy  Precision  Recall     F1  5-fold CV
--------------------------------------------------------------------
Naive Bayes               0.920      0.864   0.950  0.905      0.980
Logistic Regression       0.920      0.864   0.950  0.905      0.970

Naive Bayes confusion matrix (test set):
                 predicted ham  predicted spam
  actual ham                27               3
  actual spam                1              19
...
--------------------------------------------------------------------
Message: Congratulations! You have won a Rs 50,000 cash prize. Call 9876543210 to claim now!
  Verdict: 🚫 SPAM   spam probability = 99%
    Naive Bayes          -> spam  (99% spam)
    Logistic Regression  -> spam  (98% spam)
  Spammy words: [money], now, [phone no.], call [phone no.], claim, to
  Safe words  : you
--------------------------------------------------------------------
Message: Hey, are you coming to the lab tomorrow? Need your help with the code.
  Verdict: ✅ HAM (not spam)   spam probability = 5%
    Naive Bayes          -> ham   (2% spam)
    Logistic Regression  -> ham   (7% spam)
  Spammy words: to, with, your
  Safe words  : the, tomorrow, you, lab, are you, coming
```

### Understanding the metrics

| Metric | Meaning | In spam terms |
|--------|---------|---------------|
| **Accuracy** | Correct predictions ÷ all predictions | How often the filter is right overall |
| **Precision** | True spam ÷ everything flagged as spam | When it says "spam", how often is it really spam? Low precision = real messages lost in the spam folder |
| **Recall** | Spam caught ÷ all real spam | How much of the spam does it catch? Low recall = spam reaching your inbox |
| **F1** | Balance of precision and recall | One number combining both |
| **Confusion matrix** | Table of correct and wrong predictions | **False alarm** = real message marked spam. **Missed spam** = spam marked safe |
| **5-fold CV** | Accuracy averaged over 5 different train/test splits | More reliable than one split when the dataset is small |

---

## Lab exercises

1. Run the program and look at the **Model performance** panel. Which messages did each model get wrong? Why do you think "Your Swiggy order is out for delivery…" looks like spam to the model? (Hint: which words does it share with spam messages?)
2. Classify `"Click the link below to join the meeting: meet.google.com/abc-defg-hij"`. It's a genuine message, but it's marked spam. Which features caused this? Add 5 genuine messages containing links to `spam_data.csv` (label them `ham`), restart, and try again.
3. For a spam filter, which mistake is worse: a **false alarm** (an important message goes to spam) or **missed spam**? Should we prefer high precision or high recall? How could you change the 50% threshold in `classify()` to reflect your choice?
4. Remove the pre-processing: in `make_vectorizer()`, delete `preprocessor=preprocess,`. Restart and compare the metrics. Do phone numbers and links still get recognised as spammy?
5. Write 5 new spam messages in a style the model hasn't seen (for example, a fake college admission or scholarship offer). Does it catch them? Add them to the training data and test again.
6. Download the **SMS Spam Collection** (step 6) and retrain. How do the accuracy, precision and recall change with 28× more data? Do the tricky messages from exercises 1 and 2 improve?
7. **Extension:** try another classifier. In `make_models()` add:
   ```python
   from sklearn.svm import LinearSVC
   from sklearn.calibration import CalibratedClassifierCV
   "svm": make_pipeline(make_vectorizer(), CalibratedClassifierCV(LinearSVC())),
   ```
   and add `"svm": "Linear SVM"` to `MODEL_NAMES`. Is it better than the other two?

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `ModuleNotFoundError: No module named 'flask'` or `'sklearn'` | The venv isn't active — repeat step 4, then step 5 |
| `'python' is not recognized` (Windows) | Reinstall Python with **Add to PATH** ticked, or use `py` instead of `python` |
| `Dataset not found` | `spam_data.csv` must be in the same folder as `spam_classifier.py` |
| `KeyError: 'message'` after editing the CSV | The first line of `spam_data.csv` must be exactly `label,message`. Put messages containing commas in double quotes |
| The big dataset isn't being used | The file must be named exactly `SMSSpamCollection` (no extension) or `spam.csv`, and be in the same folder as `app.py` |
| Server takes a while to start | Normal — the models are trained every time it starts (a few seconds, longer with the big dataset) |
| `TemplateNotFound: index.html` | `index.html` isn't inside a `templates` folder next to `app.py` |
| Browser says "can't reach this page" | `python app.py` isn't running, or you closed that terminal — start it again |
| `Address already in use` / port 5000 busy | Another program (or another lab) is using port 5000. On macOS this is often AirPlay Receiver. Change the last line of `app.py` to `app.run(debug=True, use_reloader=False, port=8000)` and open http://127.0.0.1:8000 |

To leave the virtual environment when you're done: `deactivate`
