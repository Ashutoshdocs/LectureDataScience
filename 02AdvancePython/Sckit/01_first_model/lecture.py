"""Lecture 01: create -> fit -> predict; swapping models; regression uses the same pattern."""
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

print("=== 1. The three steps ===")
X = [[1, 4], [2, 5], [3, 6], [6, 7], [8, 6], [9, 8]]   # [hours studied, hours slept]
y = [0, 0, 0, 1, 1, 1]                                  # 0 = fail, 1 = pass

model = DecisionTreeClassifier(random_state=0)          # 1. create
print("  before fit:", model)
model.fit(X, y)                                         # 2. fit
new_students = [[2, 7], [7, 5], [5, 5]]
print("  predictions for", new_students, "->", model.predict(new_students))   # 3. predict
print("  learned attributes: classes_ =", model.classes_, "| n_features_in_ =", model.n_features_in_)

print("\n=== 2. Swap the model: only one line changes ===")
for m in [DecisionTreeClassifier(random_state=0), KNeighborsClassifier(n_neighbors=3),
          LogisticRegression(), RandomForestClassifier(n_estimators=50, random_state=0)]:
    m.fit(X, y)
    print(f"  {type(m).__name__:<24} -> {m.predict(new_students)}")

print("\n=== 3. Regression: same pattern, numeric target ===")
marks = [35, 42, 50, 71, 80, 92]
reg = LinearRegression().fit(X, marks)
for student, mark in zip(new_students, reg.predict(new_students)):
    print(f"  {student} -> predicted mark {mark:.1f}")

print("\n=== 4. Common mistakes ===")
attempts = {
    "predict([2, 7]) single brackets": lambda: model.predict([2, 7]),
    "predict before fit": lambda: DecisionTreeClassifier().predict([[2, 7]]),
    "X and y lengths differ": lambda: DecisionTreeClassifier().fit(X, y[:4]),
}
for label, action in attempts.items():
    try:
        action()
    except Exception as e:
        first_line = str(e).splitlines()[0]
        print(f"  {label:<32} -> {type(e).__name__}: {first_line[:85]}")
