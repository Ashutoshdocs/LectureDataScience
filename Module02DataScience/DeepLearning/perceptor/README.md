# Perceptron Demo — Learning the AND Gate

## 1. What is a Perceptron?

A **perceptron** is one of the simplest neural-network models. It is a supervised
learning algorithm used for binary classification: it predicts one of two classes,
such as `0` or `1`.

Think of it as a tiny decision-making unit:

1. Receive input values.
2. Multiply each input by a weight.
3. Add the results and a bias.
4. Apply an activation function.
5. Produce a prediction.
6. During training, adjust weights when the prediction is incorrect.

## 2. What are we building?

We will train a perceptron to learn the **AND logic gate**.

| Input 1 | Input 2 | Expected output |
|---:|---:|---:|
| 0 | 0 | 0 |
| 0 | 1 | 0 |
| 1 | 0 | 0 |
| 1 | 1 | 1 |

The important teaching point: we provide examples and expected answers. The
algorithm adjusts its weights; we do not write an `if input1 == 1 and input2 == 1`
rule into the model.

## 3. Files

- `perceptron_demo.py` — contains a perceptron implemented from scratch.
- `README.md` — this explanation and the practical steps.

## 4. Setup

Python 3.9 or later is recommended. No third-party package is required for the
main demo.

```bash
python --version
```

## 5. Run the practical

Linux / macOS:

```bash
python3 perceptron_demo.py
```

Windows:

```powershell
python perceptron_demo.py
```

The output shows the training epochs, errors, updated weights and bias, and final
predictions.

## 6. Understand the mathematics

The perceptron first calculates:

```text
z = (x1 * w1) + (x2 * w2) + bias
```

Then it applies a step activation:

```text
if z >= 0: prediction = 1
else:      prediction = 0
```

The learning rule is:

```text
error = actual_output - predicted_output

new_weight = old_weight + learning_rate * error * input
new_bias   = old_bias   + learning_rate * error
```

- **Weight:** how strongly an input influences the result.
- **Bias:** shifts the decision threshold.
- **Learning rate:** controls the size of each update.
- **Epoch:** one pass through all training examples.
- **Activation:** converts the weighted sum into a class prediction.

## 7. Optional: use scikit-learn

Install the library:

```bash
python -m pip install scikit-learn
```

Run both the from-scratch and library implementations:

```bash
python perceptron_demo.py --sklearn
```

The scikit-learn model is a practical example of using an existing ML library.
The from-scratch version makes the learning rule visible.

## 8. Classroom teaching flow

1. Ask learners to predict the AND gate outputs manually.
2. Explain input, weight, bias, weighted sum, and activation.
3. Run the script and observe the epoch-by-epoch weight updates.
4. Compare expected and predicted outputs.
5. Change `learning_rate` from `0.1` to `0.01` and run again.
6. Change the number of `epochs` and observe training.
7. Run the optional scikit-learn version and compare.

## 9. Important limitation: XOR

A single perceptron can learn linearly separable patterns such as AND and OR.
It cannot learn XOR correctly because XOR is not linearly separable.

XOR examples:

| Input 1 | Input 2 | XOR output |
|---:|---:|---:|
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 0 |

This is a useful bridge to the next lesson: **multi-layer neural networks** can learn
patterns that a single perceptron cannot.

## 10. Key takeaway

A perceptron is a simple learning model. It uses examples, adjusts weights based on
prediction errors, and learns a decision boundary for binary classification.
