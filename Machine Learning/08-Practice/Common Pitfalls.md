---
tags: [ml, practice]
---
# Common Pitfalls

| Pitfall | Fix |
|---|---|
| **Data leakage** (scaling on all data, target in features, future info) | pipelines, split first, time-aware splits |
| Tuning on the test set | validation set / nested CV ([[Cross-Validation and Model Selection]]) |
| Accuracy on imbalanced data | PR-AUC, F1, baselines ([[Model Evaluation and Metrics]]) |
| Not scaling features for distance/gradient methods | [[Data Preprocessing]] |
| Duplicates/groups across train & test | group k-fold |
| Misreading t-SNE | [[Dimensionality Reduction]] |
| Confusing correlation with causation | experiments, causal inference |
| Ignoring baseline | always compare to dummy and simple model |
| Wrong shape/transposed matrices | assert shapes ([[NumPy Snippets]]) |
| Train/eval mode bugs (dropout, BN) | `model.eval()` ([[PyTorch Recipes]]) |
| Non-reproducible results | seeds, logged configs |
| Log of zero / overflow | log-sum-exp, clip probabilities |

## Learn more
- [Made With ML](https://madewithml.com/)
- [Molnar – Interpretable ML](https://christophm.github.io/interpretable-ml-book/)
