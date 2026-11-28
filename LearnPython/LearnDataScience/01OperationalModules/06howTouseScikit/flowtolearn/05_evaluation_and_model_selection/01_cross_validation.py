"""Compare models with stratified cross-validation."""
from sklearn.datasets import load_iris
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier

X,y = load_iris(return_X_y=True)
cv = StratifiedKFold(n_splits=5,shuffle=True,random_state=42)
models = {
 "Logistic Regression": make_pipeline(StandardScaler(),LogisticRegression(max_iter=1000)),
 "Decision Tree": DecisionTreeClassifier(max_depth=3,random_state=42)
}
for name, model in models.items():
 scores = cross_val_score(model,X,y,cv=cv,scoring="accuracy")
 print(name, "folds:", scores.round(3),
       "mean:", round(scores.mean(),3), "std:", round(scores.std(),3))
