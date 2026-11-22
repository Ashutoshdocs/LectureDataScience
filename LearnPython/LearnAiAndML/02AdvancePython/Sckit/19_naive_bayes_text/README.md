# Lecture 19: Naive Bayes & text classification

Run: `python lecture.py`

## Naive Bayes in one idea

Using **Bayes' theorem**, the model asks: "given these features, which class is most probable?"

```
P(class | features) ∝ P(class) × P(feature₁ | class) × P(feature₂ | class) × …
```

It's "**naive**" because it assumes the features are **independent** given the class: that "free" and "money" appear independently in spam. That's rarely true, yet it works surprisingly well, especially for text.

| Variant | Features | Typical use |
|---------|----------|-------------|
| `GaussianNB` | continuous, assumed bell-shaped per class | quick baseline on numeric data |
| **`MultinomialNB`** | **counts** (word counts, TF-IDF) | **text classification** |
| `BernoulliNB` | binary present/absent | short texts, yes/no features |
| `ComplementNB` | counts | imbalanced text classes |

`alpha` (default 1.0) is **Laplace smoothing**: it pretends every word was seen `alpha` extra times, so an unseen word doesn't make a probability exactly 0.

✅ Extremely **fast**, works with **little data** and **many features**, and gives a decent baseline instantly. ❌ Probabilities are often over-confident, and it's beaten by logistic regression or SVM when there's plenty of data.

## Turning text into numbers

Models can't read. **Vectorizers** turn each document into a row of numbers.

### `CountVectorizer`: bag of words

```python
vec = CountVectorizer()
X = vec.fit_transform(["free money now", "meeting at noon"])
vec.get_feature_names_out()   # ['at', 'free', 'meeting', 'money', 'noon', 'now']
```

Each column is a word, and each value is how often the word appears. The result is a **sparse matrix** (mostly zeros), stored efficiently.

### `TfidfVectorizer`: weight by importance

**TF-IDF** = term frequency × inverse document frequency. Words common in **every** document ("the", "is") get low weight; words distinctive to a few documents get high weight. It's usually better than raw counts.

### Useful parameters (both vectorizers)

| Parameter | Effect |
|-----------|--------|
| `lowercase=True` (default) | "Free" = "free" |
| `stop_words="english"` | drop common words like *the, and, is* |
| `ngram_range=(1, 2)` | also use word **pairs**: "not good" becomes one feature (in `lecture.py` the model's P(positive) for "not good" drops from 0.28 to 0.12) |
| `min_df=2` / `max_df=0.9` | ignore words in fewer than 2 documents / in more than 90% of them |
| `max_features=5000` | keep only the most frequent words |
| `analyzer="char_wb", ngram_range=(2, 4)` | character n-grams: robust to typos ("fr33 m0ney") |

> ⚠️ Fit the vectorizer on **training texts only**, which a pipeline does for you. Words that appear only in the test set are ignored at transform time.

## A spam filter in three lines

```python
spam_filter = make_pipeline(TfidfVectorizer(ngram_range=(1, 2)), MultinomialNB())
spam_filter.fit(train_texts, train_labels)
spam_filter.predict(["WIN a FREE prize now"])
```

## Exercises

1. Print the vocabulary and the count matrix for three short sentences.
2. Compare `CountVectorizer` + NB with `TfidfVectorizer` + `LogisticRegression` on the spam data.
3. Add `ngram_range=(1, 2)` and test the phrase "not good" in a sentiment example.
4. Print the 10 words most indicative of spam using `feature_log_prob_`.

**Next →** [Lecture 20: Pipelines & ColumnTransformer](../20_pipelines_columntransformer/)
