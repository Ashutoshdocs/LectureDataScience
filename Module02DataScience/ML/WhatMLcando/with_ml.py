"""
DEMO 2: Machine learning with Python

Here we provide historical examples (study hours and actual result).
A Logistic Regression model finds a pattern from those examples.

Unlike Demo 1, we do not write 'if hours >= 5'.
The model learns its decision boundary from the training data.
"""

from sklearn.linear_model import LogisticRegression

# Historical examples: study hours and known outcomes.
# 0 = FAIL, 1 = PASS
X_train = [[1], [2], [2.5], [3], [3.5], [4], [4.5], [5], [5.5], [6], [7], [8]]
y_train = [0,    0,   0,     0,   0,     0,   1,     1,   1,     1,   1,   1]

model = LogisticRegression()
model.fit(X_train, y_train)  # Learning happens here.

print("MACHINE LEARNING: model learns from examples")
print("-" * 48)
print("Training examples:", len(X_train))
print("Model learned its parameters from the examples.")

print("\\nPredictions for new students:")
for hours in [2, 3.8, 4.2, 4.7, 5.2, 6.5]:
    prediction = model.predict([[hours]])[0]
    probability = model.predict_proba([[hours]])[0][1]
    label = "PASS" if prediction == 1 else "FAIL"
    print(f"Study hours: {hours:>4} -> {label:4} (estimated pass probability: {probability:.1%})")

print("\\nThe model's learned boundary is not a rule we typed as an if-statement.")
print("It was estimated from the labeled training examples.")
