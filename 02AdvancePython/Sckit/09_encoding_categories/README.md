# Lecture 09: Encoding categorical data

Run: `python lecture.py`

Models need **numbers**. Columns like `city = "Pune"` or `size = "M"` must be converted to numbers, and *how* you convert them matters.

## Two kinds of categorical data

| Kind | Order? | Examples | Encoder |
|------|--------|----------|---------|
| **Nominal** | no natural order | city, colour, brand | `OneHotEncoder` |
| **Ordinal** | has an order | size S < M < L, rating poor < good < excellent, education level | `OrdinalEncoder(categories=[[...]])` |

## Why not just number them?

`Delhi=0, Mumbai=1, Pune=2` tells a linear model that Pune is "two Delhis" and that Mumbai lies between them. That's nonsense for nominal data.

## `OneHotEncoder`: one 0/1 column per category

```python
enc = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
enc.fit_transform(df[["city"]])          # note: 2-D input (double brackets)
enc.get_feature_names_out()              # ['city_Delhi', 'city_Mumbai', 'city_Pune']
```

| Parameter | Effect |
|-----------|--------|
| `handle_unknown="ignore"` | a category never seen in training becomes all zeros instead of raising an error. **Use it in production.** |
| `handle_unknown="infrequent_if_exist"` + `min_frequency=5` | groups rare categories into one "infrequent" column |
| `max_categories=10` | keep at most 10 columns per feature |
| `drop="first"` / `drop="if_binary"` | drop one column to avoid redundancy (helps unregularised linear models) |
| `sparse_output=False` | return a normal array (the default is a memory-saving sparse matrix) |
| `categories_` | the learned categories per column |

**Downside:** a column with 5,000 distinct values creates 5,000 columns. For such **high-cardinality** features, consider `min_frequency`/`max_categories`, `TargetEncoder`, or grouping.

## `OrdinalEncoder`: categories → 0, 1, 2… in **your** order

```python
OrdinalEncoder(categories=[["S", "M", "L", "XL"]])
```

Always pass the order explicitly. The default order is **alphabetical** (`L, M, S, XL`), which is wrong for sizes. Use `handle_unknown="use_encoded_value", unknown_value=-1` for unseen values.

Tree models handle ordinal-encoded nominal features reasonably well too, and it's much more compact than one-hot.

## `LabelEncoder` is for **y**, not X

`LabelEncoder` turns target labels like `["spam", "ham"]` into `[1, 0]`. It handles one 1-D array. Use `OneHotEncoder` / `OrdinalEncoder` for features. (Most classifiers accept string labels in `y` directly anyway.)

## `TargetEncoder` (advanced)

`TargetEncoder` replaces each category with the **average target value** for that category, learned with internal cross-fitting to limit leakage. It works well for high-cardinality columns such as zip codes or product IDs.

## pandas `get_dummies` vs `OneHotEncoder`

`pd.get_dummies(df)` is quick for exploration, but it doesn't **remember** the categories. If the test data lacks a category, or has a new one, the columns don't match. `OneHotEncoder` learns the categories at `fit` and applies them consistently, so **use it in models**.

## Exercises

1. One-hot encode `colour` and `city` together in one encoder call.
2. Encode sizes with the correct order and check that `XL > L`.
3. Transform a new, unseen city with and without `handle_unknown="ignore"`.
4. Use `min_frequency=2` and see which categories become "infrequent".

**Next →** [Lecture 10: Missing values](../10_missing_values/)
