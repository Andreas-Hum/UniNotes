---
tags: [ml, fundamentals, evaluation]
---
# Model Evaluation and Metrics

## Classification
Confusion matrix: TP, FP, FN, TN.

| Metric | Formula | Use when |
|---|---|---|
| Accuracy | $\frac{TP+TN}{N}$ | balanced classes |
| Precision | $\frac{TP}{TP+FP}$ | false positives costly |
| Recall (TPR) | $\frac{TP}{TP+FN}$ | false negatives costly |
| F1 | $\frac{2PR}{P+R}$ | imbalance, single number |
| Specificity | $\frac{TN}{TN+FP}$ | |
| ROC-AUC | area under TPR vs FPR | ranking quality, threshold-free |
| PR-AUC | area under precision vs recall | heavy imbalance |
| Log loss | $-\frac1N\sum y\log\hat p+(1-y)\log(1-\hat p)$ | probabilistic quality |
| MCC | balanced correlation | imbalance |

## Regression
MSE, RMSE, MAE, $R^2 = 1-\frac{SS_{res}}{SS_{tot}}$, MAPE.

## Clustering
Silhouette, Davies–Bouldin, adjusted Rand index, normalized mutual information. See [[Clustering]].

## Ranking / retrieval
Precision@k, MAP, NDCG, MRR. For graphs see [[Link Prediction]].

> [!warning]
> Accuracy on a 99%/1% split is meaningless. Always check the baseline (majority class).

Splitting strategy: [[Cross-Validation and Model Selection]].

## Learn more
- [scikit-learn – metrics](https://scikit-learn.org/stable/modules/model_evaluation.html)
- [CS229 cheatsheets](https://stanford.edu/~shervine/teaching/cs-229/)
- [StatQuest videos](https://statquest.org/video_index.html)
