"""Classify Iris flowers into one of three species."""
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

iris = load_iris()
Xtr, Xte, ytr, yte = train_test_split(
    iris.data, iris.target, test_size=.25, random_state=42, stratify=iris.target)
model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))
model.fit(Xtr,ytr)
pred = model.predict(Xte)
print("Species:", iris.target_names)
print("Accuracy:", round(accuracy_score(yte,pred),3))
print("Confusion matrix:\\n", confusion_matrix(yte,pred))
print(classification_report(yte,pred,target_names=iris.target_names))
sample = [[5.1,3.5,1.4,.2]]
print("Sample prediction:", iris.target_names[model.predict(sample)[0]])
