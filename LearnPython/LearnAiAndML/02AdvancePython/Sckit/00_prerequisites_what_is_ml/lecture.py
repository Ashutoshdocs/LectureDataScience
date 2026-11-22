"""Lecture 00: NumPy/pandas refresher, rules vs learning, types of ML."""
import numpy as np
import pandas as pd
import sklearn
from sklearn.tree import DecisionTreeClassifier

print("=== 0. Versions ===")
print(f"  scikit-learn {sklearn.__version__} | numpy {np.__version__} | pandas {pd.__version__}")

print("\n=== 1. NumPy you will need ===")
X = np.array([[25, 50_000], [32, 64_000], [47, 120_000], [51, 90_000]])
print("  X.shape          :", X.shape, "-> (rows=samples, columns=features)")
print("  first column X[:, 0]:", X[:, 0])
print("  column means     :", X.mean(axis=0).tolist())
flat = np.array([1, 2, 3, 4])
print("  reshape(-1, 1)   :", flat.shape, "->", flat.reshape(-1, 1).shape)
pred = np.array([1, 0, 1, 1])
truth = np.array([1, 0, 0, 1])
print("  (pred == truth)  :", pred == truth, "-> accuracy", (pred == truth).mean())
print("  boolean mask     :", X[X[:, 0] > 30][:, 0], "(ages over 30)")

print("\n=== 2. pandas you will need ===")
df = pd.DataFrame({"age": [25, 32, 47, 51], "city": ["Pune", "Delhi", "Pune", "Mumbai"],
                   "salary": [50_000, 64_000, 120_000, None], "bought": [0, 1, 1, 0]})
print(df.to_string(index=False))
print("  dtypes        :", dict(df.dtypes.astype(str)))
print("  missing values:", df.isna().sum().to_dict())
X_df = df.drop(columns="bought")
y = df["bought"]
print("  X columns:", list(X_df.columns), "| y:", y.tolist())

print("\n=== 3. Rules vs learning ===")
emails = ["win free money now!!!", "meeting at 10am", "free offer, click!!!", "lunch tomorrow?",
          "claim your prize!!!", "project report attached"]
labels = [1, 0, 1, 0, 1, 0]                     # 1 = spam


def rule_based(text):                            # hand-written rule
    return int("free" in text or text.count("!") > 2)


def features(text):                              # turn text into numbers for the model
    return [text.count("!"), int("free" in text), int("prize" in text), len(text.split())]


X_emails = [features(e) for e in emails]
model = DecisionTreeClassifier(random_state=0).fit(X_emails, labels)
tests = ["urgent prize waiting!!!", "free coffee in the kitchen", "see you at the meeting"]
for t in tests:
    print(f"  {t!r:<32} rule={rule_based(t)}  learned={model.predict([features(t)])[0]}")
print("  The rule flags 'free coffee' as spam; the model learned that '!!!' matters more.")

print("\n=== 4. Classification vs regression vs clustering ===")
tasks = {"Will this email be spam?": "classification (category)",
         "What price will this flat sell for?": "regression (number)",
         "Which customers behave alike?": "clustering (no labels)",
         "Is this tumour malignant?": "classification (category)",
         "How many units will we sell next week?": "regression (number)"}
for question, kind in tasks.items():
    print(f"  {question:<42} -> {kind}")
