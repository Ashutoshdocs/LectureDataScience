"""
PERCEPTRON DEMO — A beginner-friendly binary classifier

What this demonstrates:
1. A perceptron calculates a weighted sum: z = (x1*w1) + (x2*w2) + bias
2. It applies a step activation function to predict 0 or 1.
3. During training, it adjusts weights when a prediction is wrong.
4. It learns the AND logic gate from examples.

Run:
    python perceptron_demo.py

Optional:
    pip install scikit-learn
    python perceptron_demo.py --sklearn
"""

import argparse


def step(value):
    """Step activation: return 1 when value >= 0, otherwise 0."""
    return 1 if value >= 0 else 0


class SimplePerceptron:
    def __init__(self, learning_rate=0.1, epochs=10):
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.weights = [0.0, 0.0]
        self.bias = 0.0

    def predict_one(self, inputs):
        weighted_sum = sum(x * w for x, w in zip(inputs, self.weights)) + self.bias
        return step(weighted_sum)

    def fit(self, X, y):
        print("\nTRAINING THE PERCEPTRON")
        print("-" * 55)

        for epoch in range(self.epochs):
            total_errors = 0

            for inputs, actual in zip(X, y):
                prediction = self.predict_one(inputs)
                error = actual - prediction

                # Perceptron learning rule
                for i in range(len(self.weights)):
                    self.weights[i] += self.learning_rate * error * inputs[i]
                self.bias += self.learning_rate * error

                if error != 0:
                    total_errors += 1

            print(
                f"Epoch {epoch + 1:02d}: errors={total_errors}, "
                f"weights={self.weights}, bias={self.bias:.2f}"
            )

            if total_errors == 0:
                print("No errors in this epoch. Training can stop.")
                break

    def predict(self, X):
        return [self.predict_one(row) for row in X]


def run_manual_demo():
    # Inputs and expected outputs for the AND gate
    X = [
        [0, 0],
        [0, 1],
        [1, 0],
        [1, 1],
    ]
    y = [0, 0, 0, 1]

    print("=" * 55)
    print("PERCEPTRON: LEARNING THE AND LOGIC GATE")
    print("=" * 55)
    print("The examples are the training data; the model learns weights.")
    print("\nTraining examples:")
    for inputs, target in zip(X, y):
        print(f"Input: {inputs}  Expected output: {target}")

    model = SimplePerceptron(learning_rate=0.1, epochs=20)
    model.fit(X, y)

    print("\nFINAL PREDICTIONS")
    print("-" * 55)
    print(f"{'Input':<15}{'Actual':<12}{'Predicted':<12}")
    for inputs, actual, predicted in zip(X, y, model.predict(X)):
        print(f"{str(inputs):<15}{actual:<12}{predicted:<12}")

    print("\nLEARNED PARAMETERS")
    print(f"Weights: {model.weights}")
    print(f"Bias:    {model.bias:.2f}")
    print("\nInterpretation:")
    print("- Each input is multiplied by its learned weight.")
    print("- The bias shifts the decision boundary.")
    print("- The step function converts the weighted sum to class 0 or 1.")


def run_sklearn_demo():
    try:
        from sklearn.linear_model import Perceptron
    except ImportError:
        print("scikit-learn is not installed. Run: pip install scikit-learn")
        return

    X = [[0, 0], [0, 1], [1, 0], [1, 1]]
    y = [0, 0, 0, 1]

    model = Perceptron(
        max_iter=1000,
        eta0=0.1,
        random_state=42,
        tol=1e-3,
    )
    model.fit(X, y)

    print("\nSCIKIT-LEARN PERCEPTRON")
    print("-" * 55)
    print("Learned coefficients:", model.coef_)
    print("Learned intercept:", model.intercept_)
    print("Predictions:", model.predict(X).tolist())
    print("Expected:    ", y)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Perceptron teaching demo")
    parser.add_argument(
        "--sklearn",
        action="store_true",
        help="Also run the scikit-learn Perceptron implementation",
    )
    args = parser.parse_args()

    run_manual_demo()
    if args.sklearn:
        run_sklearn_demo()
