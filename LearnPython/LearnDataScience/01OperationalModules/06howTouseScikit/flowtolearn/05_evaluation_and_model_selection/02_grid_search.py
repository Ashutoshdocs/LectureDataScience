"""Tune a Decision Tree using GridSearchCV; evaluate on held-out test data."""
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

X,y = load_iris(return_X_y=True)
Xtr,Xte,ytr,yte = train_test_split(X,y,test_size=.2,random_state=42,stratify=y)
search = GridSearchCV(DecisionTreeClassifier(random_state=42),
    {"max_depth":[1,2,3,4,None],"criterion":["gini","entropy"]},
    cv=5,scoring="accuracy")
search.fit(Xtr,ytr)
print("Best parameters:", search.best_params_)
print("Best CV score:", round(search.best_score_,3))
print("Held-out test accuracy:", round(accuracy_score(yte,search.best_estimator_.predict(Xte)),3))
