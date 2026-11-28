"""Predict marks from one feature: study hours."""
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

X = np.arange(1, 11).reshape(-1, 1)
y = np.array([30,35,42,48,55,60,68,72,80,88])
model = LinearRegression().fit(X, y)
print("Prediction for 7.5 study hours:", round(model.predict([[7.5]])[0], 2))
print("Training MAE (illustration only):", round(mean_absolute_error(y, model.predict(X)), 2))
