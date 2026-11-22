# Lecture 02: Series, a labelled 1D array

Run: `python lecture.py`

## Definition

A **Series** = **values** (a NumPy-style array) + an **index** (a label for each value) + an optional **name**.

```
index   values
"Mon"    4200
"Tue"    6100
"Wed"    5300
name: steps, dtype: int64
```

## Creating a Series

| From | Code | Index |
|------|------|-------|
| a list | `pd.Series([4200, 6100, 5300])` | `0, 1, 2` (automatic) |
| a list + labels | `pd.Series([...], index=["Mon", "Tue", "Wed"])` | your labels |
| a dict | `pd.Series({"Mon": 4200, "Tue": 6100})` | the keys |
| a scalar | `pd.Series(0, index=["a", "b"])` | repeated value |

## Series vs NumPy array vs dict

| | NumPy array | dict | **Series** |
|---|---|---|---|
| Vectorized maths | ✅ | ❌ | ✅ |
| Labels | ❌ positions only | ✅ keys | ✅ index |
| Ordered, sliceable | ✅ | ❌ | ✅ |
| Missing values | `nan` for floats only | manual | ✅ `NaN` handled |

A Series is like a NumPy array **and** a dict at the same time.

## Accessing values

```python
s["Tue"]          # by label
s.iloc[1]         # by position  (always use .iloc for positions)
s[["Mon", "Wed"]] # several labels
s[s > 5000]       # boolean mask, same as NumPy
```

> ⚠️ `s[1]` on a Series with a text index is ambiguous and deprecated. Use `s.iloc[1]` for positions and `s.loc["Tue"]` or `s["Tue"]` for labels.

## Vectorized maths, aligned by label

Maths works on every element, like NumPy:

```python
s * 2,  s + 100,  s.mean(),  s.max(),  s.idxmax()  # idxmax = label of the max
```

**Alignment:** when two Series are combined, pandas matches them **by label, not by position**:

```python
a = pd.Series({"Mon": 1, "Tue": 2})
b = pd.Series({"Tue": 10, "Wed": 20})
a + b     # Mon NaN, Tue 12, Wed NaN
```

Labels missing from either side produce `NaN`. Use `a.add(b, fill_value=0)` to treat them as 0.

## Useful Series methods

| Method | Does |
|--------|------|
| `.sum() .mean() .median() .min() .max() .std()` | statistics |
| `.idxmax() .idxmin()` | **label** of the max / min (vs NumPy's `argmax` → position) |
| `.value_counts()` | frequency of each value |
| `.unique() .nunique()` | distinct values / how many |
| `.sort_values() .sort_index()` | sorting |
| `.head(n) .tail(n)` | first / last n |
| `.describe()` | summary statistics |
| `.to_list() .to_numpy() .to_dict()` | convert out |

## Exercises

1. Create a Series of 5 city temperatures with city names as the index.
2. Which city is hottest? (`idxmax`)
3. Convert all to Fahrenheit.
4. Add two Series with partly different labels using `fill_value=0`.

<details><summary>Solutions</summary>

```python
t = pd.Series({"Delhi": 39, "Mumbai": 32, "Chennai": 36, "Pune": 30, "Kolkata": 34})
t.idxmax()                  # 'Delhi'
t * 9 / 5 + 32
a.add(b, fill_value=0)      # Mon 1, Tue 12, Wed 20
```
</details>

**Next →** [Lecture 03: DataFrame basics](../03_dataframe_basics/)
