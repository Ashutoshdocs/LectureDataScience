"""Encode text categories and train a model inside one pipeline."""
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression

df = pd.DataFrame({
    "age":[22,25,31,35,45,52,28,41],
    "salary":[25000,30000,42000,50000,65000,72000,38000,58000],
    "city":["Pune","Mumbai","Pune","Delhi","Mumbai","Delhi","Pune","Mumbai"],
    "purchased":[0,0,1,1,1,1,0,1]
})
X, y = df[["age","salary","city"]], df["purchased"]
numeric = Pipeline([("fill", SimpleImputer(strategy="median")),
                    ("scale", StandardScaler())])
categorical = Pipeline([("fill", SimpleImputer(strategy="most_frequent")),
                        ("encode", OneHotEncoder(handle_unknown="ignore"))])
prep = ColumnTransformer([("numbers", numeric, ["age","salary"]),
                          ("categories", categorical, ["city"])])
model = Pipeline([("prep", prep), ("classifier", LogisticRegression(max_iter=1000))])
model.fit(X, y)
new_customer = pd.DataFrame({"age":[29], "salary":[40000], "city":["Pune"]})
print("Purchase prediction (1=yes, 0=no):", model.predict(new_customer)[0])
