---
tags: [ml, unsupervised, anomaly]
---
# Anomaly Detection

Find rare observations that differ from the norm.

- **Statistical**: z-score, IQR, Mahalanobis distance, Gaussian density threshold.
- **Isolation Forest**: anomalies are isolated with few random splits.
- **One-class SVM**: boundary around normal data ([[Support Vector Machines]]).
- **Local Outlier Factor**: density relative to neighbours ([[k-Nearest Neighbors]]).
- **Reconstruction error**: [[PCA]] / autoencoders ([[Generative Models]]).
- **Time series**: residuals of forecasting models, change-point detection.

Evaluate with PR-AUC since classes are extremely imbalanced ([[Model Evaluation and Metrics]]).
