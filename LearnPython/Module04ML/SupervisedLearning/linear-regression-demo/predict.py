import joblib
import pandas as pd

# Load the model created by train_model.py
model = joblib.load("student_marks_model.pkl")

# Enter new study-hour values here
new_students = pd.DataFrame({
    "hours_studied": [3.5, 5, 7.5, 9, 13]
})

predictions = model.predict(new_students)

results = new_students.copy()
results["predicted_marks"] = predictions.round(2)

print("Predictions for new students:")
print(results.to_string(index=False))
