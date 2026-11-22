"""Lecture 09: OneHotEncoder, OrdinalEncoder, LabelEncoder, unknown & rare categories, TargetEncoder, get_dummies pitfall."""
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, OrdinalEncoder, TargetEncoder

df = pd.DataFrame({
    "city": ["Pune", "Delhi", "Mumbai", "Pune", "Delhi", "Chennai"],
    "size": ["M", "L", "S", "XL", "M", "L"],
    "colour": ["red", "blue", "red", "green", "blue", "red"],
})

print("=== 1. Naive numbering implies a fake order ===")
fake = {c: i for i, c in enumerate(sorted(df["city"].unique()))}
print("  ", fake, "-> the model would think Pune (3) > Mumbai (2) > Delhi (1)")

print("\n=== 2. OneHotEncoder ===")
enc = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
encoded = enc.fit_transform(df[["city", "colour"]])
print("  categories_:", [list(c) for c in enc.categories_])
print("  columns    :", list(enc.get_feature_names_out()))
print(pd.DataFrame(encoded.astype(int), columns=enc.get_feature_names_out()).head(3).to_string(index=False))

print("\n=== 3. Unknown categories at predict time ===")
new = pd.DataFrame({"city": ["Kolkata"], "colour": ["red"]})
print("  handle_unknown='ignore' ->", enc.transform(new).astype(int), "(Kolkata = all zeros)")
strict = OneHotEncoder(sparse_output=False).fit(df[["city", "colour"]])
try:
    strict.transform(new)
except ValueError as e:
    print("  default (error)         ->", str(e).splitlines()[0][:80])

print("\n=== 4. drop='first' and sparse output ===")
d = OneHotEncoder(drop="first", sparse_output=False).fit(df[["colour"]])
print("  drop='first' columns:", list(d.get_feature_names_out()), "(blue is implied by all zeros)")
sp = OneHotEncoder().fit_transform(df[["city"]])
print("  default output type :", type(sp).__name__, "with", sp.nnz, "stored values instead of", sp.shape[0] * sp.shape[1])

print("\n=== 5. Rare categories: min_frequency ===")
cities = pd.DataFrame({"city": ["Pune"] * 5 + ["Delhi"] * 4 + ["Goa", "Agra", "Ooty"]})
rare = OneHotEncoder(min_frequency=2, handle_unknown="infrequent_if_exist", sparse_output=False).fit(cities)
print("  columns:", list(rare.get_feature_names_out()))
print("  infrequent categories grouped:", list(rare.infrequent_categories_[0]))

print("\n=== 6. OrdinalEncoder: give the order explicitly ===")
alphabetical = OrdinalEncoder().fit(df[["size"]])
print("  default (alphabetical) order:", list(alphabetical.categories_[0]), "<- wrong for sizes")
ordered = OrdinalEncoder(categories=[["S", "M", "L", "XL"]], handle_unknown="use_encoded_value", unknown_value=-1)
codes = ordered.fit_transform(df[["size"]]).ravel()
print("  sizes", df["size"].tolist(), "->", codes.astype(int).tolist())
print("  unseen size 'XXL' ->", ordered.transform(pd.DataFrame({"size": ["XXL"]})).ravel())

print("\n=== 7. LabelEncoder is for y ===")
y = ["spam", "ham", "spam", "ham", "ham"]
le = LabelEncoder()
y_enc = le.fit_transform(y)
print("  classes_:", le.classes_.tolist(), "| encoded:", y_enc.tolist(), "| back:", le.inverse_transform([0, 1]).tolist())

print("\n=== 8. TargetEncoder for high-cardinality columns ===")
rng = np.random.default_rng(0)
zips = rng.choice([f"Z{i:03d}" for i in range(50)], size=500)
zip_effect = {z: rng.normal(50, 15) for z in np.unique(zips)}
price = np.array([zip_effect[z] for z in zips]) + rng.normal(0, 5, 500)
te = TargetEncoder()
encoded_zip = te.fit_transform(zips.reshape(-1, 1), price)
print("  50 zip codes -> 1 numeric column; correlation with price:",
      round(np.corrcoef(encoded_zip.ravel(), price)[0, 1], 3))

print("\n=== 9. Why not pd.get_dummies inside a model ===")
train_dummies = pd.get_dummies(df[["colour"]]).columns.tolist()
test_dummies = pd.get_dummies(pd.DataFrame({"colour": ["red", "purple"]})).columns.tolist()
print("  train columns:", train_dummies)
print("  test columns :", test_dummies, "<- different columns: the model would break")
colour_enc = OneHotEncoder(handle_unknown="ignore", sparse_output=False).fit(df[["colour"]])
test_out = colour_enc.transform(pd.DataFrame({"colour": ["red", "purple"]}))
print("  OneHotEncoder on test:", list(colour_enc.get_feature_names_out()), test_out.astype(int).tolist(),
      "<- same columns as training; purple = all zeros")
