import pandas as pd
import matplotlib.pyplot as plt
import joblib

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

# 1. Load the dataset
data = pd.read_csv("data/student_marks.csv")
print("First five rows:")
print(data.head())

# 2. Separate input feature (X) and target (y)
X = data[["hours_studied"]]
y = data["marks"]

# 3. Split into training and testing data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)

# 4. Create and train the model
model = LinearRegression()
model.fit(X_train, y_train)

# 5. Predict test-set values
y_pred = model.predict(X_test)

# 6. Display the learned equation
print("\\nModel details")
print("Intercept:", model.intercept_)
print("Slope / Coefficient:", model.coef_[0])
print(
    f"Learned equation: marks = {model.intercept_:.2f} + "
    f"({model.coef_[0]:.2f} * hours_studied)"
)

# 7. Evaluate the model
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = mse ** 0.5
r2 = r2_score(y_test, y_pred)

print("\\nModel evaluation")
print("MAE:", round(mae, 2))
print("MSE:", round(mse, 2))
print("RMSE:", round(rmse, 2))
print("R2 Score:", round(r2, 4))

# 8. Compare actual and predicted values
comparison = pd.DataFrame({
    "Hours Studied": X_test["hours_studied"].values,
    "Actual Marks": y_test.values,
    "Predicted Marks": y_pred.round(2)
})
comparison["Error"] = (
    comparison["Actual Marks"] - comparison["Predicted Marks"]
).round(2)

print("\\nActual vs Predicted")
print(comparison.sort_values("Hours Studied").to_string(index=False))

# 9. Plot observations and fitted regression line
plt.scatter(X["hours_studied"], y, label="Actual data")
plt.plot(X["hours_studied"], model.predict(X), label="Regression line")
plt.xlabel("Hours Studied")
plt.ylabel("Marks")
plt.title("Student Marks Prediction — Linear Regression")
plt.legend()
plt.grid(True)
plt.show()

# 10. Save the trained model for predict.py
joblib.dump(model, "student_marks_model.pkl")
print("\\nModel saved as student_marks_model.pkl")
