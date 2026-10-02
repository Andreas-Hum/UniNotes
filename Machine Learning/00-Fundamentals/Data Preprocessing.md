---
tags: [ml, fundamentals, data]
---
# Data Preprocessing

## Scaling
- **Min–max**: $x' = \frac{x-x_{min}}{x_{max}-x_{min}}$
- **Standardization (z-score)**: $x' = \frac{x-\mu}{\sigma}$
- **Robust**: use median and IQR, resists outliers.

Needed for: [[Gradient Descent]], [[k-Nearest Neighbors]], [[Support Vector Machines]], [[PCA]], regularized models. Not needed for tree models ([[Decision Trees]]).

## Missing data
MCAR / MAR / MNAR. Options: drop, mean/median/mode, kNN or model-based imputation, missing-indicator.

## Outliers
Inspect (box plot, z-score, IQR), winsorize, or use robust losses (Huber). See [[Anomaly Detection]].

## Imbalance
Class weights, resampling (SMOTE), threshold moving, PR-AUC. See [[Model Evaluation and Metrics]].

## Pipeline rule
Compute statistics on **train only**, apply to val/test.

## Learn more
- [scikit-learn – preprocessing](https://scikit-learn.org/stable/modules/preprocessing.html)
- [scikit-learn – imputation](https://scikit-learn.org/stable/modules/impute.html)
