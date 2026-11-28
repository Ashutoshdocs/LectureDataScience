"""Decision Tree classification and feature importance."""
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

d = load_breast_cancer()
Xtr,Xte,ytr,yte = train_test_split(d.data,d.target,test_size=.25,
    random_state=42,stratify=d.target)
model = DecisionTreeClassifier(max_depth=3,random_state=42).fit(Xtr,ytr)
pred = model.predict(Xte)
print("Classes:", d.target_names)
print("Accuracy:", round(accuracy_score(yte,pred),3))
print("Tree depth:", model.get_depth(), "Leaves:", model.get_n_leaves())
print("Top feature importances:")
for name, score in sorted(zip(d.feature_names,model.feature_importances_),
                          key=lambda x:x[1],reverse=True)[:5]:
    print(name, round(score,3))
