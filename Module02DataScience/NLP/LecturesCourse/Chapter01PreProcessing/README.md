# NLP Practical: Text Preprocessing and Sentiment Analysis

A beginner-to-intermediate, hands-on Natural Language Processing (NLP) practical.
You will clean text, split it into tokens, remove stop words, stem words, convert
text into numbers with TF-IDF, and train a sentiment classifier.

## 1. What you will build

A small review classifier that predicts whether a review is **positive** or
**negative**.

Files:
- `reviews.csv` — small practice dataset with text and sentiment labels.
- `preprocess.py` — preprocessing functions, TF-IDF, model training and testing.
- `requirements.txt` — Python dependencies.

## 2. Prerequisites

- Python 3.9 or newer
- Basic Python knowledge: variables, functions, lists and importing modules
- Terminal / command prompt

## 3. Setup

Open a terminal in this folder.

### Create a virtual environment (recommended)

Linux / macOS:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:
```bash
python -m pip install -r requirements.txt
```

No NLTK corpus download is required. The practical uses NLTK's Porter stemmer,
which works locally after the package is installed.

## 4. Run the practical

```bash
python preprocess.py
```

The program prints:
1. Dataset size and label distribution
2. A step-by-step preprocessing walkthrough
3. Model accuracy, precision, recall and F1-score
4. Predictions for three new review sentences

The dataset is intentionally small for teaching. Its score is only a demonstration,
not evidence of production-level model quality.

## 5. NLP flow — teach this sequence

```text
Raw text
   |
   v
Text cleaning
(lowercase, remove URLs, HTML, digits, punctuation)
   |
   v
Tokenization
("The movie was great" -> ["the", "movie", "was", "great"])
   |
   v
Stop-word removal
(remove selected frequent words such as "the", "was")
   |
   v
Stemming
("playing", "played" -> approximate root "play")
   |
   v
TF-IDF vectorization
(convert words / phrases into numeric features)
   |
   v
Train / test split
   |
   v
Logistic Regression
   |
   v
Evaluation and prediction
```

## 6. Understand each preprocessing step

| Step | Meaning | Example |
|---|---|---|
| Cleaning | Standardize and remove noise | `GREAT!!!` -> `great` |
| Tokenization | Split text into units | `good movie` -> `["good", "movie"]` |
| Stop-word removal | Remove selected common words | `the movie is good` -> `movie good` |
| Stemming | Reduce word variants to approximate roots | `connected`, `connecting` -> `connect` |
| TF-IDF | Represent text as weighted numeric features | words become columns in a feature matrix |

**Important teaching distinction:** stemming is not the same as lemmatization.
Stemming may produce a word fragment; lemmatization aims to return a valid
dictionary form and usually needs language-aware linguistic resources.

## 7. Suggested classroom walkthrough

1. Open `reviews.csv` and identify the input (`text`) and target (`label`).
2. Run the script once and inspect the preprocessing walkthrough.
3. In `preprocess.py`, temporarily comment out stop-word removal. Compare output.
4. Temporarily comment out stemming. Discuss how the tokens change.
5. Add 4–6 new positive and negative rows to `reviews.csv`.
6. Run again and compare the evaluation metrics.
7. Change the sentences in `examples` and test predictions.
8. Try changing `ngram_range=(1, 2)` to `(1, 1)`. Explain unigrams vs. bigrams.

## 8. Important concepts to explain

- **Feature:** a measurable input used by a machine-learning model.
- **Label:** the answer the model learns to predict (`positive` / `negative`).
- **TF-IDF:** gives higher weight to terms that are informative in a document
  relative to the collection. It is not a language model.
- **Training data:** examples used to fit the model.
- **Test data:** held-out examples used to estimate performance.
- **Overfitting:** when a model learns training examples too closely and performs
  poorly on unseen data.
- **Precision:** of the items predicted as a class, how many were correct?
- **Recall:** of the actual items in a class, how many did the model find?
- **F1-score:** harmonic mean of precision and recall.

## 9. Beginner-to-intermediate extensions

- Add a third label such as `neutral` and collect more examples.
- Compare Logistic Regression with Multinomial Naive Bayes.
- Compare unigram features `(1, 1)` with unigram + bigram features `(1, 2)`.
- Print the most influential positive and negative words.
- Save the trained model and vectorizer with `joblib`, then load them for
  prediction in a separate script.
- Compare stemming with lemmatization using a suitable NLP library.

## 10. Limitations and good practice

- This is a tiny, educational dataset; metrics can vary and are not meaningful
  as a real-world benchmark.
- A word such as `not` can reverse sentiment. Do not blindly remove negation
  words from a real sentiment-analysis pipeline.
- The stop-word list is intentionally small and editable for learning.
- Always fit TF-IDF on training text only, then transform test text. The script
  follows this rule to avoid test-data leakage.
- Real projects need larger, representative, carefully labelled datasets and
  validation on data from the intended use case.

## 11. Quick troubleshooting

**`ModuleNotFoundError`:** activate your virtual environment and run
`python -m pip install -r requirements.txt`.

**CSV file not found:** run `python preprocess.py` from this project folder.

**PowerShell does not allow activation:** you can run the environment's Python
directly with `.\.venv\Scripts\python.exe preprocess.py`, or use your
organization's approved execution-policy approach.
