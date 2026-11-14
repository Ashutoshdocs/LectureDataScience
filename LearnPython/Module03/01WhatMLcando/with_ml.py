
"""
DEMO 2: Machine Learning with Python

Objective:
Predict whether a student will PASS or FAIL based on
the number of hours they study.

In traditional Python, we write conditions ourselves.

In Machine Learning, we provide historical examples
and allow an algorithm to learn patterns from them.
"""

# STEP 1: Import the Machine Learning algorithm
# LogisticRegression is an ML classification algorithm.
# Classification means predicting categories such as PASS or FAIL.

from sklearn.linear_model import LogisticRegression


# STEP 2: Prepare historical training data
# This data represents students whose results are already known.
#
# X_train = Input features (independent variable)
# Here, the input is the number of hours a student studied.
#
# Each inner list represents one student.
# Example: [1] means the student studied for 1 hour.

X_train = [
    [1],
    [2],
    [2.5],
    [3],
    [3.5],
    [4],
    [4.5],
    [5],
    [5.5],
    [6],
    [7],
    [8]
]


# STEP 3: Prepare the actual answers (labels)
#
# y_train = Output labels (dependent variable)
#
# 0 means FAIL
# 1 means PASS
#
# Each answer corresponds to the same-position student
# in X_train.
#
# For example:
# X_train[0] = [1]  -> y_train[0] = 0 (FAIL)
# X_train[6] = [4.5] -> y_train[6] = 1 (PASS)

y_train = [
    0, 0, 0, 0, 0, 0,
    1, 1, 1, 1, 1, 1
]


# STEP 4: Create the Machine Learning model
#
# We are creating an empty Logistic Regression model.
# At this point, it has not learned from our training data.

model = LogisticRegression()


# STEP 5: Train the model
#
# fit() is one of the most important ML operations.
#
# We provide:
# X_train = Historical inputs
# y_train = Historical correct answers
#
# The algorithm studies the relationship between inputs
# and outputs and learns model parameters.
#
# This is where the actual model training happens.

model.fit(X_train, y_train)


# STEP 6: Display training information

print("MACHINE LEARNING: Model learns from examples")
print("-" * 48)

# len() counts how many historical student records we supplied.
print("Training examples:", len(X_train))

# The model has now learned parameters from the examples.
print("Model learned its parameters from the examples.")


# STEP 7: Predict results for NEW students
#
# These students are not part of our training data.
# We want the model to predict their results.

print("\nPredictions for new students:")


# We test the model with different study hours.
# Each value represents a new student's study hours.

for hours in [2, 3.8, 4.2, 4.7, 5.2, 6.5]:

    # predict() returns the predicted class.
    # 0 = FAIL
    # 1 = PASS
    #
    # [[hours]] is used because sklearn expects
    # input in a two-dimensional format.

    prediction = model.predict([[hours]])[0]


    # predict_proba() returns the estimated probabilities
    # for both classes: FAIL and PASS.
    #
    # [0] selects the first student's probability array.
    # [1] selects the probability of class 1 (PASS).

    probability = model.predict_proba([[hours]])[0][1]


    # Convert the numerical prediction into readable text.
    #
    # If prediction is 1, display PASS.
    # Otherwise, display FAIL.

    label = "PASS" if prediction == 1 else "FAIL"


    # Display the study hours, predicted result,
    # and estimated probability of passing.

    print(
        f"Study hours: {hours:>4} -> "
        f"{label:4} "
        f"(estimated pass probability: {probability:.1%})"
    )


# STEP 8: Final explanation
#
# Notice that we never wrote:
#
# if hours >= 5:
#     return "PASS"
#
# Instead, the Logistic Regression algorithm learned
# its decision boundary from historical examples.
#
# This is the fundamental difference between
# traditional programming and Machine Learning.

print("\nThe model's learned boundary was not manually")
print("written as an if-statement.")
print("It was estimated from the training examples.")
