"""
Beginner-to-intermediate NLP practical:
1. Clean text
2. Tokenize
3. Remove stop words
4. Stem words
5. Convert text to TF-IDF features
6. Train and evaluate a sentiment classifier
"""

import re
import pandas as pd
from nltk.stem import PorterStemmer
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

DATA_FILE = "reviews.csv"
stemmer = PorterStemmer()

# A small teaching stop-word list keeps the example transparent.
# In production, use a fuller language-specific list and review domain terms.
STOP_WORDS = {
    "a", "an", "the", "is", "am", "are", "was", "were", "be", "been",
    "being", "and", "or", "but", "if", "then", "this", "that", "it",
    "its", "i", "we", "you", "he", "she", "they", "them", "my", "our",
    "your", "with", "for", "of", "to", "in", "on", "at", "from", "by",
    "after", "very", "really"
}

def clean_text(text):
    """Lowercase and remove URLs, HTML tags, numbers and punctuation."""
    text = str(text).lower()
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)  # URLs
    text = re.sub(r"<.*?>", " ", text)                  # HTML
    text = re.sub(r"\d+", " ", text)                    # numbers
    text = re.sub(r"[^a-z\s]", " ", text)               # punctuation/symbols
    text = re.sub(r"\s+", " ", text).strip()             # extra spaces
    return text

def tokenize(text):
    """Split cleaned text into word tokens."""
    return text.split()

def remove_stopwords(tokens):
    """Remove frequent words that often add little meaning."""
    return [word for word in tokens if word not in STOP_WORDS]

def stem_tokens(tokens):
    """Reduce related word forms to a common stem."""
    return [stemmer.stem(word) for word in tokens]

def preprocess_text(text, show_steps=False):
    cleaned = clean_text(text)
    tokens = tokenize(cleaned)
    filtered = remove_stopwords(tokens)
    stemmed = stem_tokens(filtered)

    if show_steps:
        print("\nPREPROCESSING WALKTHROUGH")
        print("Original:          ", text)
        print("Cleaned:           ", cleaned)
        print("Tokens:            ", tokens)
        print("After stop words:  ", filtered)
        print("After stemming:    ", stemmed)

    return " ".join(stemmed)

def main():
    print("Loading dataset...")
    df = pd.read_csv(DATA_FILE)
    df = df.dropna(subset=["text", "label"])
    print(f"Rows: {len(df)}")
    print("\nClass distribution:")
    print(df["label"].value_counts())

    # Inspect the full preprocessing flow on one example.
    preprocess_text(df.loc[0, "text"], show_steps=True)

    # Apply preprocessing to every review.
    df["processed_text"] = df["text"].apply(preprocess_text)

    X_train, X_test, y_train, y_test = train_test_split(
        df["processed_text"],
        df["label"],
        test_size=0.25,
        random_state=42,
        stratify=df["label"]
    )

    # TF-IDF converts text into numeric features.
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=1000)
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    # Train a simple supervised sentiment classifier.
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train_vec, y_train)

    predictions = model.predict(X_test_vec)
    print("\nMODEL EVALUATION")
    print("Accuracy:", round(accuracy_score(y_test, predictions), 3))
    print("\nClassification report:")
    print(classification_report(y_test, predictions, zero_division=0))
    print("Confusion matrix (label order:", list(model.classes_), "):")
    print(confusion_matrix(y_test, predictions))

    # Try new sentences. Change these during the practical.
    examples = [
        "The product is excellent and works perfectly!",
        "Very poor service. I am disappointed.",
        "The delivery was quick, but the item is not good."
    ]

    print("\nTRY YOUR OWN TEXT")
    for sentence in examples:
        processed = preprocess_text(sentence)
        features = vectorizer.transform([processed])
        predicted_label = model.predict(features)[0]
        probabilities = model.predict_proba(features)[0]
        confidence = max(probabilities)
        print(f"\nInput: {sentence}")
        print(f"Processed: {processed}")
        print(f"Prediction: {predicted_label} (model score: {confidence:.2f})")

if __name__ == "__main__":
    main()
