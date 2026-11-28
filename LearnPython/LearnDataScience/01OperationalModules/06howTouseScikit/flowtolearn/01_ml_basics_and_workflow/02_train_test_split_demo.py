"""Hold out test data to estimate performance on unseen examples."""
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

data = load_diabetes()
X_train, X_test, y_train, y_test = train_test_split(
    data.data, data.target, test_size=0.2, random_state=42
)
model = LinearRegression()
model.fit(X_train, y_train)
pred = model.predict(X_test)
print("Training rows:", len(X_train), " Test rows:", len(X_test))
print("MAE:", round(mean_absolute_error(y_test, pred), 2))
print("R2:", round(r2_score(y_test, pred), 3))
