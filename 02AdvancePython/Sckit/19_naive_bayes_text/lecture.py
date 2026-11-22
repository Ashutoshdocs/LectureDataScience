"""Lecture 19: Naive Bayes (Gaussian/Multinomial), CountVectorizer, TF-IDF, n-grams, a spam filter, sentiment, top words."""
import numpy as np
from sklearn.datasets import load_iris
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.naive_bayes import GaussianNB, MultinomialNB
from sklearn.pipeline import make_pipeline

np.set_printoptions(suppress=True)

print("=== 1. GaussianNB on numeric data ===")
X, y = load_iris(return_X_y=True)
print(f"  iris GaussianNB CV accuracy {cross_val_score(GaussianNB(), X, y, cv=5).mean():.3f} (no tuning, trains in microseconds)")

print("\n=== 2. Bag of words with CountVectorizer ===")
docs = ["Free money now", "Meeting at noon", "free free FREE prize"]
vec = CountVectorizer()
counts = vec.fit_transform(docs)
print("  vocabulary:", vec.get_feature_names_out().tolist())
print("  counts:\n", counts.toarray())
print("  stored as", type(counts).__name__, f"({counts.nnz} non-zeros out of {counts.shape[0] * counts.shape[1]})")
print("  unseen word 'lottery' is ignored:", vec.transform(["free lottery"]).toarray())

print("\n=== 3. TF-IDF down-weights common words ===")
docs2 = ["the cat sat", "the dog sat", "the cat ran fast"]
tf = TfidfVectorizer()
w = tf.fit_transform(docs2).toarray()
for word, col in sorted(tf.vocabulary_.items()):
    print(f"  {word:<5} weight in doc 1: {w[0, col]:.2f}   idf {tf.idf_[col]:.2f}")
print("  'the' appears everywhere -> lowest idf")

print("\n=== 4. A spam filter ===")
spam = ["WIN a FREE prize now", "free money waiting claim now", "cheap loans, act fast!!", "you won a lottery, claim cash",
        "limited offer: free gift card", "urgent! your account prize", "earn money fast from home", "click now free bonus cash",
        "congratulations you are selected winner", "exclusive deal, buy now cheap"]
ham = ["meeting moved to 3pm", "can you review my report", "lunch tomorrow at the cafe?", "project deadline is friday",
       "thanks for the notes from class", "call me when you are free", "the train is late again", "see you at the gym tonight",
       "please send the invoice", "happy birthday, have a great day"]
texts = spam + ham
labels = np.array([1] * len(spam) + [0] * len(ham))
for name, model in [("Count + MultinomialNB", make_pipeline(CountVectorizer(), MultinomialNB())),
                    ("TF-IDF + MultinomialNB", make_pipeline(TfidfVectorizer(), MultinomialNB())),
                    ("TF-IDF + Logistic", make_pipeline(TfidfVectorizer(), LogisticRegression()))]:
    print(f"  {name:<23} CV accuracy {cross_val_score(model, texts, labels, cv=5).mean():.3f}")
spam_filter = make_pipeline(TfidfVectorizer(), MultinomialNB()).fit(texts, labels)
for msg in ["claim your free cash prize", "are we still meeting for lunch?", "are you free for a call about the report"]:
    p = spam_filter.predict_proba([msg])[0, 1]
    print(f"  {msg!r:<45} spam probability {p:.2f} -> {'SPAM' if p >= 0.5 else 'ham'}")

print("\n=== 5. Most 'spammy' words ===")
cv_nb = make_pipeline(CountVectorizer(), MultinomialNB()).fit(texts, labels)
vocab = cv_nb[0].get_feature_names_out()
log_ratio = cv_nb[-1].feature_log_prob_[1] - cv_nb[-1].feature_log_prob_[0]
print("  spam:", vocab[np.argsort(log_ratio)[::-1][:8]].tolist())
print("  ham :", vocab[np.argsort(log_ratio)[:8]].tolist())

print("\n=== 6. n-grams capture 'not good' ===")
reviews = ["good movie", "very good acting", "great fun", "loved it, good story",
           "not good", "not good at all", "boring and bad", "bad acting, not fun"]
sentiment = [1, 1, 1, 1, 0, 0, 0, 0]
for ngrams in [(1, 1), (1, 2)]:
    model = make_pipeline(CountVectorizer(ngram_range=ngrams), MultinomialNB()).fit(reviews, sentiment)
    print(f"  ngram_range={ngrams}: 'not good' -> {model.predict(['not good'])[0]}, "
          f"P(positive) {model.predict_proba(['not good'])[0, 1]:.2f}, features {len(model[0].vocabulary_)}")

print("\n=== 7. Smoothing (alpha) and stop words ===")
for alpha in [0.01, 1.0, 10.0]:
    m = make_pipeline(CountVectorizer(), MultinomialNB(alpha=alpha))
    print(f"  alpha={alpha:<5} CV accuracy {cross_val_score(m, texts, labels, cv=5).mean():.3f}")
sw = CountVectorizer(stop_words="english").fit(["the cat is on the mat"])
print("  stop_words='english' keeps:", sw.get_feature_names_out().tolist())
