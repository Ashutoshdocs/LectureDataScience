"""Fill missing values, then scale numeric columns."""
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

X = np.array([[22,25000], [25,30000], [np.nan,35000], [32,np.nan], [40,60000]])
print("Raw data:\\n", X)
filled = SimpleImputer(strategy="mean").fit_transform(X)
print("After filling missing values:\\n", filled)
scaled = StandardScaler().fit_transform(filled)
print("After scaling (rounded):\\n", np.round(scaled, 2))
