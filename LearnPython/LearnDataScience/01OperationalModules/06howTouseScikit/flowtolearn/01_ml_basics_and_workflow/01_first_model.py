"""First model: predict exam marks from study hours."""
import numpy as np
from sklearn.linear_model import LinearRegression

# X is a 2D feature table: one row per student, one column for study hours.
X = np.array([1,2,3,4,5,6,7,8]).reshape(-1, 1)
# y is the target: the known exam mark for each student.
y = np.array([35,40,50,55,65,70,80,85])

model = LinearRegression()       # Create an untrained model.
model.fit(X, y)                  # Learn the relationship from examples.
new_student = [[6.5]]            # New input must have one row and one feature.
print("Predicted mark:", round(model.predict(new_student)[0], 2))
print("Learned slope:", model.coef_[0])
print("Learned intercept:", model.intercept_)
