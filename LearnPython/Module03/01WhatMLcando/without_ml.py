"""
DEMO 1: Traditional Python programming (NO machine learning)

A programmer writes the rule:
    If study hours >= 5, predict PASS.
    Otherwise, predict FAIL.

The computer does not learn from examples. It only follows our condition.
"""

def predict_result(study_hours):
    if study_hours >= 5:
        return "PASS"
    return "FAIL"


print("TRADITIONAL PYTHON: manually written rule")
print("-" * 48)

for hours in [1, 3, 4, 5, 6, 8]:
    print(f"Study hours: {hours:>2} -> Prediction: {predict_result(hours)}")

print("\\nTry changing the rule in predict_result().")
print("The programmer must decide and update the logic.")
