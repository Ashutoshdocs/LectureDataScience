"""Predict marks from study hours, attendance, and assignments."""
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

df = pd.DataFrame({
 "study_hours":[1,2,3,4,5,6,7,8,2,5,7,9,3,6,8],
 "attendance":[50,55,60,65,70,75,80,90,58,72,85,95,62,78,88],
 "assignments":[2,3,4,5,6,7,8,10,3,6,9,10,4,7,9],
 "marks":[28,35,42,48,57,65,73,91,37,60,80,96,43,69,86]
})
X, y = df[["study_hours","attendance","assignments"]], df["marks"]
Xtr, Xte, ytr, yte = train_test_split(X,y,test_size=.25,random_state=7)
model = LinearRegression().fit(Xtr,ytr)
pred = model.predict(Xte)
print("MAE:", round(mean_absolute_error(yte,pred),2), "R2:", round(r2_score(yte,pred),3))
print("New student estimate:", round(model.predict(pd.DataFrame({
 "study_hours":[6], "attendance":[82], "assignments":[8]}))[0],2))
