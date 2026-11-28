# 02 — Data Preprocessing

Raw data may contain missing values, different numeric scales, and text categories. sklearn provides reusable transformers rather than requiring custom loops for every project.

Topics: `SimpleImputer`, `StandardScaler`, `OneHotEncoder`, `ColumnTransformer`, `Pipeline`.

Run:
```bash
python 02_data_preprocessing/01_missing_values_and_scaling.py
python 02_data_preprocessing/02_encoding_pipeline.py
```
Teaching point: fit preprocessing on training data only. A pipeline helps prevent inconsistent processing and data leakage.
