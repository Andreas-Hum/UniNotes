---
tags: [ml, supervised, ensemble]
---
# Ensemble Methods

Combine many weak/diverse models for lower error.

| Method | Idea | Reduces |
|---|---|---|
| **Bagging** | train on bootstrap samples, average | variance |
| **Random Forest** | bagged [[Decision Trees]] + random feature subset per split | variance, decorrelates trees |
| **AdaBoost** | reweight misclassified points, weighted vote | bias |
| **Gradient Boosting** | fit each tree to the negative gradient (residuals) of the loss | bias |
| **XGBoost / LightGBM / CatBoost** | fast, regularized gradient boosting | state of the art on tabular data |
| **Stacking** | meta-learner on base model predictions | both |
| **Voting** | hard/soft vote of heterogeneous models | variance |

- Random forests give out-of-bag (OOB) error for free.
- Boosting hyperparameters: learning rate (small + many trees), depth (3–8), subsampling.
- Feature importance: impurity-based (biased) vs. permutation importance (preferred).

See [[Bias-Variance Tradeoff]].

## Learn more
- [ISL / ISLP (free)](https://www.statlearning.com/) ch. 8
- [scikit-learn – ensembles](https://scikit-learn.org/stable/modules/ensemble.html)
- [XGBoost docs](https://xgboost.readthedocs.io/)
